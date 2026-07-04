import discord
from discord import app_commands
from discord.ext import commands, tasks
import random
import database as db
from utils.embeds import success_embed, error_embed, info_embed, warning_embed, stats_bar, format_money
from utils.helpers import clamp, get_housing_bonus
from utils.narrative import get_action_text
from config import (
    HEALTH_MAX, HUNGER_MAX, THIRST_MAX, ENERGY_MAX, HYGIENE_MAX,
    DECAY_INTERVAL, DECAY_AMOUNT, ENERGY_DECAY, HYGIENE_DECAY,
    HEALTH_DAMAGE_FROM_STARVATION, ENERGY_DAMAGE_FROM_EXHAUSTION, HYGIENE_DAMAGE_FROM_FILTH,
    HOSPITAL_FEE_PERCENT, WEATHER_STATES, WEATHER_BUFFS, CLOTHING,
)
from datetime import datetime, timezone


class Survival(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.decay_loop.start()

    def cog_unload(self):
        self.decay_loop.cancel()

    @tasks.loop(seconds=DECAY_INTERVAL)
    async def decay_loop(self):
        dbobj = await db.get_db()
        now = datetime.now(timezone.utc).isoformat()
        current_weather = await db.get_weather()
        w_effects = WEATHER_STATES.get(current_weather, {}).get("effects", {})
        energy_mult = w_effects.get("energy_decay_mult", 1.0)
        hygiene_mult = w_effects.get("hygiene_decay_mult", 1.0)

        # Time-of-day effects
        time_effects = await db.get_time_effects()
        energy_regen = time_effects.get("energy_regen", 0)

        # Weather debuff application
        weather_buff = WEATHER_BUFFS.get(current_weather)
        weather_buff_chance = weather_buff["chance"] if weather_buff else 0

        async with dbobj.execute("SELECT user_id, health, hunger, thirst, energy, hygiene, wallet, hospital_visits FROM users") as cur:
            rows = await cur.fetchall()
        for row in rows:
            uid = row["user_id"]
            new_hunger = clamp(row["hunger"] - DECAY_AMOUNT, 0, HUNGER_MAX)
            new_thirst = clamp(row["thirst"] - DECAY_AMOUNT, 0, THIRST_MAX)
            # Apply buff regen
            buff_energy_regen = await db.get_buff_add(uid, "energy_regen")
            buff_health_regen = await db.get_buff_add(uid, "health_regen")
            buff_hygiene_regen = await db.get_buff_add(uid, "hygiene_regen")
            buff_all_regen = await db.get_buff_add(uid, "all_regen")
            # Apply weather drain buffs
            buff_energy_drain = await db.get_buff_add(uid, "energy_drain")
            buff_health_drain = await db.get_buff_add(uid, "health_drain")
            buff_hygiene_drain = await db.get_buff_add(uid, "hygiene_drain")

            total_energy_regen = energy_regen + buff_energy_regen + buff_all_regen - buff_energy_drain
            total_health_regen = buff_health_regen + buff_all_regen - buff_health_drain
            total_hygiene_regen = buff_hygiene_regen + buff_all_regen - buff_hygiene_drain

            new_energy = clamp(row["energy"] - int(ENERGY_DECAY * energy_mult) + int(total_energy_regen), 0, ENERGY_MAX)
            new_hygiene = clamp(row["hygiene"] - int(HYGIENE_DECAY * hygiene_mult) + int(total_hygiene_regen), 0, HYGIENE_MAX)
            new_health = clamp(row["health"] + int(total_health_regen), 0, HEALTH_MAX)

            # Roll weather debuff for this user
            if weather_buff and random.random() < weather_buff_chance:
                # Check if player's clothing protects against this weather
                equipped = await db.get_equipped(uid)
                protected = False
                for item in equipped:
                    if item["item_type"] == "clothing":
                        prot = CLOTHING.get(item["item_id"], {}).get("weather_prot", [])
                        if current_weather in prot:
                            protected = True
                            break
                if not protected:
                    await db.add_buff(uid, weather_buff["buff_name"], weather_buff["stat"], weather_buff["value"], weather_buff["duration"])

            if new_hunger <= 0 or new_thirst <= 0:
                new_health = clamp(new_health - HEALTH_DAMAGE_FROM_STARVATION, 0, HEALTH_MAX)
            if new_energy <= 0:
                new_health = clamp(new_health - ENERGY_DAMAGE_FROM_EXHAUSTION, 0, HEALTH_MAX)
            if new_hygiene <= 0:
                new_health = clamp(new_health - HYGIENE_DAMAGE_FROM_FILTH, 0, HEALTH_MAX)

            if new_health <= 0:
                lost = int(row["wallet"] * HOSPITAL_FEE_PERCENT)
                new_wallet = row["wallet"] - lost
                await dbobj.execute(
                    "UPDATE users SET health = ?, hunger = ?, thirst = ?, energy = ?, hygiene = ?, wallet = ?, hospital_visits = ?, total_lost = ?, last_decay = ? WHERE user_id = ?",
                    (HEALTH_MAX, 50, 50, 50, 50, new_wallet, row["hospital_visits"] + 1, row["total_lost"] + lost, now, uid),
                )
                await db.add_transaction(uid, "hospital", lost, "Hospital wakeup fee")
            else:
                await dbobj.execute(
                    "UPDATE users SET health = ?, hunger = ?, thirst = ?, energy = ?, hygiene = ?, last_decay = ? WHERE user_id = ?",
                    (new_health, new_hunger, new_thirst, new_energy, new_hygiene, now, uid),
                )
        await dbobj.commit()

    @decay_loop.before_loop
    async def before_decay(self):
        await self.bot.wait_until_ready()

    @app_commands.command(name="status", description="Check your survival stats")
    async def status(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        embed = info_embed(f"📊 {interaction.user.display_name}'s Survival Status")

        health_bar = stats_bar(data["health"], HEALTH_MAX)
        hunger_bar = stats_bar(data["hunger"], HUNGER_MAX)
        thirst_bar = stats_bar(data["thirst"], THIRST_MAX)
        energy_bar = stats_bar(data.get("energy", 100), ENERGY_MAX)
        hygiene_bar = stats_bar(data.get("hygiene", 100), HYGIENE_MAX)

        embed.add_field(name=f"❤️ Health — {data['health']}/{HEALTH_MAX}", value=health_bar, inline=False)
        embed.add_field(name=f"🍖 Hunger — {data['hunger']}/{HUNGER_MAX}", value=hunger_bar, inline=False)
        embed.add_field(name=f"💧 Thirst — {data['thirst']}/{THIRST_MAX}", value=thirst_bar, inline=False)
        embed.add_field(name=f"⚡ Energy — {data.get('energy', 100)}/{ENERGY_MAX}", value=energy_bar, inline=False)
        embed.add_field(name=f"🧼 Hygiene — {data.get('hygiene', 100)}/{HYGIENE_MAX}", value=hygiene_bar, inline=False)

        current_weather = await db.get_weather()
        wdata = WEATHER_STATES.get(current_weather, {})
        embed.add_field(name=f"天气 Weather", value=f"{wdata.get('name', '☀️ Sunny')} — {wdata.get('description', '')}", inline=False)

        equipped = await db.get_equipped(interaction.user.id)
        if equipped:
            from config import TOOLS, CLOTHING, POSSESSIONS
            eq_text = []
            for item in equipped:
                item_data = TOOLS.get(item["item_id"], CLOTHING.get(item["item_id"], POSSESSIONS.get(item["item_id"], {})))
                name = item_data.get("name", item["item_id"])
                eq_text.append(f"{name} ({item['quality']})")
            embed.add_field(name="🎒 Equipped", value=", ".join(eq_text), inline=False)

        # Game time
        from config import TIME_PERIODS
        gt = await db.get_game_time()
        tp = TIME_PERIODS.get(gt["time_period"], {})
        embed.add_field(name=f"{tp.get('emoji', '🕐')} Time", value=f"{tp.get('name', 'Unknown')} ({gt['game_hour']:02d}:00)", inline=True)

        # Active buffs
        buffs = await db.get_buffs(interaction.user.id)
        if buffs:
            buff_text = []
            from config import BUFF_TYPES
            for b in buffs:
                bt = BUFF_TYPES.get(b["buff_stat"], {})
                buff_text.append(f"{b['buff_name']} ({bt.get('name', b['buff_stat'])})")
            embed.add_field(name="✨ Active Buffs", value="\n".join(buff_text), inline=False)

        warnings = []
        if data["health"] <= 20:
            warnings.append(get_action_text("survival", "health_warning"))
        if data["hunger"] <= 20:
            warnings.append(get_action_text("survival", "hunger_warning"))
        if data["thirst"] <= 20:
            warnings.append(get_action_text("survival", "thirst_warning"))
        if data.get("energy", 100) <= 20:
            warnings.append(get_action_text("survival", "energy_warning"))
        if data.get("hygiene", 100) <= 20:
            warnings.append(get_action_text("survival", "hygiene_warning"))

        if warnings:
            embed.add_field(name="⚠️ Warnings", value="\n".join(warnings), inline=False)
        if data["hospital_visits"] > 0:
            embed.set_footer(text=f"Hospital visits: {data['hospital_visits']}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="hospital", description="Check hospital info and your visit history")
    async def hospital(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        embed = info_embed("🏥 Hospital", get_action_text("survival", "hospital_info"))
        embed.add_field(name="Your Hospital Visits", value=str(data["hospital_visits"]), inline=True)
        embed.add_field(name="Current Health", value=f"{data['health']}/{HEALTH_MAX}", inline=True)
        embed.add_field(name="Current Wallet (at risk)", value=format_money(data["wallet"]), inline=True)
        embed.add_field(name="💰 Tip", value="Deposit money in the bank to protect it from hospital fees! Use `/deposit`", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="heal", description="Use a medical item to restore health")
    @app_commands.choices(item=[
        app_commands.Choice(name="🩹 Medkit (+50 HP)", value="medkit"),
        app_commands.Choice(name="💊 Painkiller (+15 HP)", value="painkiller"),
        app_commands.Choice(name="💊 Vitamin Pack (+30 HP)", value="vitamin"),
        app_commands.Choice(name="🩹 Bandage (+20 HP)", value="bandage"),
        app_commands.Choice(name="🧰 First Aid Kit (+75 HP)", value="first_aid"),
        app_commands.Choice(name="🌿 Herbal Remedy (+35 HP)", value="herbal_meds"),
    ])
    async def heal(self, interaction: discord.Interaction, item: app_commands.Choice[str]):
        inv = await db.get_inventory(interaction.user.id)
        item_id = item.value
        if item_id not in inv or inv[item_id] <= 0:
            await interaction.response.send_message(embed=error_embed("Not Owned", f"You don't have a {item.name}. Buy one from `/shop`!"), ephemeral=True)
            return
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        from config import STORE_ITEMS
        item_data = STORE_ITEMS[item_id]
        new_health = clamp(data["health"] + item_data.get("health", 0), 0, HEALTH_MAX)
        await db.update_user(interaction.user.id, health=new_health, items_used=data["items_used"] + 1)
        await db.remove_from_inventory(interaction.user.id, item_id, 1)
        await db.update_quest_progress(interaction.user.id, "use_item", 1)
        restored_hp = new_health - data['health']
        await interaction.response.send_message(embed=success_embed("🩹 Healed!", get_action_text("survival", "heal", item_name=item_data['name'], restored=restored_hp, old=data['health'], new=new_health)))

    @app_commands.command(name="sleep", description="Rest to restore energy (restores 40 energy, 4h cooldown)")
    async def sleep(self, interaction: discord.Interaction):
        cd = await db.check_cooldown(interaction.user.id, "sleep")
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"You're still resting. Try again in {mins}m {secs}s."), ephemeral=True)
            return
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if data.get("energy", 100) >= ENERGY_MAX:
            await interaction.response.send_message(embed=info_embed("😴 Already Rested", get_action_text("survival", "sleep_full")), ephemeral=True)
            return
        # Housing energy bonus
        home = await db.get_home(interaction.user.id)
        housing_bonus = 0
        home_text = ""
        if home:
            from config import HOUSING_TIERS
            tier = HOUSING_TIERS.get(home["tier_id"], {})
            housing_bonus = tier.get("stats_bonus", {}).get("energy", 0) // 5
            if housing_bonus > 0:
                home_text = f"\n🏠 {tier.get('name', 'Home')} bonus: +{housing_bonus} energy"
        base_restore = 40
        new_energy = clamp(data.get("energy", 100) + base_restore + housing_bonus, 0, ENERGY_MAX)
        restored = new_energy - data.get("energy", 100)
        await db.update_user(interaction.user.id, energy=new_energy)
        await db.set_cooldown(interaction.user.id, "sleep", 14400)
        await interaction.response.send_message(embed=success_embed("😴 Rested", get_action_text("survival", "sleep", restored=restored, home_text=home_text, old=data.get('energy', 100), new=new_energy)))

    @app_commands.command(name="shower", description="Take a shower to restore hygiene (restores 50 hygiene, 2h cooldown)")
    async def shower(self, interaction: discord.Interaction):
        cd = await db.check_cooldown(interaction.user.id, "shower")
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"You just showered. Try again in {mins}m {secs}s."), ephemeral=True)
            return
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if data.get("hygiene", 100) >= HYGIENE_MAX:
            await interaction.response.send_message(embed=info_embed("🧼 Already Clean", get_action_text("survival", "shower_full")), ephemeral=True)
            return
        # Housing hygiene bonus
        home = await db.get_home(interaction.user.id)
        housing_bonus = 0
        home_text = ""
        if home:
            from config import HOUSING_TIERS
            tier = HOUSING_TIERS.get(home["tier_id"], {})
            housing_bonus = max(0, tier.get("stats_bonus", {}).get("hygiene", 0)) // 5
            if housing_bonus > 0:
                home_text = f"\n🏠 {tier.get('name', 'Home')} bonus: +{housing_bonus} hygiene"
        base_restore = 50
        new_hygiene = clamp(data.get("hygiene", 100) + base_restore + housing_bonus, 0, HYGIENE_MAX)
        restored = new_hygiene - data.get("hygiene", 100)
        await db.update_user(interaction.user.id, hygiene=new_hygiene)
        await db.set_cooldown(interaction.user.id, "shower", 7200)
        await interaction.response.send_message(embed=success_embed("🚿 Fresh!", get_action_text("survival", "shower", restored=restored, home_text=home_text, old=data.get('hygiene', 100), new=new_hygiene)))


async def setup(bot):
    await bot.add_cog(Survival(bot))
