"""Activities cog — fishing, mining, exploring, foraging, crafting, and random encounters.
All activities use the procedural narrative engine for dynamic text generation,
the quality system for item rolls, and weather for gameplay modifiers."""

import discord
from discord import app_commands
from discord.ext import commands
import random
from datetime import datetime, timezone
import database as db
import world
import police as _police
from utils.embeds import success_embed, error_embed, info_embed, format_money, warning_embed
from utils.helpers import clamp, stat_modifier, get_housing_bonus
from utils.quality import roll_quality, quality_multiplier, quality_name, quality_emoji
from utils.narrative import (
    generate_explore_intro, generate_explore_find, generate_explore_nothing,
    generate_npc_encounter, generate_danger, generate_reward,
    generate_fish_cast, generate_fish_catch, generate_fish_nothing,
    generate_mine_swing, generate_mine_find, generate_mine_cave_in,
    roll_random_event, generate_item_description, maybe_random_event,
    get_action_text,
)
from config import (
    TOOLS, CLOTHING, POSSESSIONS, STORE_ITEMS, RAW_MATERIALS,
    CRAFTING_RECIPES, WEATHER_STATES, ITEM_QUALITIES,
    HEALTH_MAX, HUNGER_MAX, THIRST_MAX, ENERGY_MAX, HYGIENE_MAX,
    ACHIEVEMENTS,
)


class Activities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ─── Helper: get weather modifier ───
    async def _weather_mod(self, key: str, default=1.0) -> float:
        current = await db.get_weather()
        wdata = WEATHER_STATES.get(current, {})
        return wdata.get("effects", {}).get(key, default)

    # ─── Helper: check weather protection from clothing ───
    async def _has_weather_protection(self, user_id: int) -> bool:
        equipped = await db.get_equipped(user_id)
        current = await db.get_weather()
        for item in equipped:
            if item["item_type"] == "clothing":
                clothing = CLOTHING.get(item["item_id"], {})
                if current in clothing.get("weather_prot", []):
                    return True
        return False

    # ─── Helper: get equipped stat bonuses ───
    async def _get_equipment_bonuses(self, user_id: int) -> dict:
        equipped = await db.get_equipped(user_id)
        bonuses = {"luck": 0, "energy": 0, "health": 0, "hygiene": 0}
        for item in equipped:
            qmult = quality_multiplier(item["quality"])
            if item["item_type"] == "clothing":
                stats = CLOTHING.get(item["item_id"], {}).get("stats", {})
            elif item["item_type"] == "possession":
                stats = POSSESSIONS.get(item["item_id"], {}).get("stats", {})
            else:
                continue
            for stat, val in stats.items():
                bonuses[stat] = bonuses.get(stat, 0) + int(val * qmult)
        return bonuses

    # ─── Helper: apply random event ───
    async def _apply_random_event(self, user_id: int, data: dict) -> dict | None:
        event = maybe_random_event(0.12)
        if not event:
            return None
        new_wallet = data["wallet"]
        if event["coins"] > 0:
            new_wallet += event["coins"]
        elif event["coins"] < 0:
            new_wallet = max(0, new_wallet + event["coins"])
        new_health = clamp(data["health"] - event["hp"], 0, HEALTH_MAX)
        new_energy = clamp(data.get("energy", 100) - event["energy"], 0, ENERGY_MAX)
        new_hygiene = clamp(data.get("hygiene", 100) - event["hygiene"], 0, HYGIENE_MAX)
        new_hunger = clamp(data["hunger"] - event["hunger"], 0, HUNGER_MAX)
        await db.update_user(
            user_id,
            wallet=new_wallet,
            health=new_health,
            energy=new_energy,
            hygiene=new_hygiene,
            hunger=new_hunger,
        )
        if event["coins"] != 0:
            await db.add_transaction(user_id, "event", abs(event["coins"]), event["text"])
        return event

    async def _police_check(self, interaction: discord.Interaction, location_id: str, embed: discord.Embed) -> discord.Embed | None:
        """Check for police tailing after an activity. Modifies embed for hints, sends separate arrest message if needed.
        Returns the embed (possibly modified) or None if already sent (arrest scenario)."""
        result = await _police.check_tailing(interaction.user.id, location_id)
        if result is None:
            return embed

        if result["type"] == "hint":
            if result["stage"] == 0:
                embed.add_field(name="👁️ You Shook Them", value=result["text"], inline=False)
            else:
                embed.add_field(name="👁️ Something's Not Right...", value=result["text"], inline=False)
            return embed

        elif result["type"] == "arrest":
            await interaction.followup.send(embed=embed)
            from cogs.chase import ArrestView
            heat = await _police.get_heat(interaction.user.id)
            arrest_embed = warning_embed("🚨 ARREST ATTEMPT!", result["text"])
            view = ArrestView(interaction.user.id, location_id, heat)
            msg = await interaction.followup.send(embed=arrest_embed, view=view)
            view.message = msg
            return None

    # ─── /activity (merged fish/mine/explore/forage/chop/dig) ───
    @app_commands.command(name="activity", description="Gather resources: fish, mine, explore, forage, chop, or dig")
    @app_commands.choices(activity=[
        app_commands.Choice(name="\U0001F3A3 Fish", value="fish"),
        app_commands.Choice(name="\u26CF\uFE0F Mine", value="mine"),
        app_commands.Choice(name="\U0001F9ED Explore", value="explore"),
        app_commands.Choice(name="\U0001F33F Forage", value="forage"),
        app_commands.Choice(name="\U0001FA93 Chop", value="chop"),
        app_commands.Choice(name="\U0001FA7A Dig", value="dig"),
    ])
    async def activity(self, interaction: discord.Interaction, activity: str):
        if activity == "fish":
            await self._fish(interaction)
        elif activity == "mine":
            await self._mine(interaction)
        elif activity == "explore":
            await self._explore(interaction)
        elif activity == "forage":
            await self._forage(interaction)
        elif activity == "chop":
            await self._chop(interaction)
        elif activity == "dig":
            await self._dig(interaction)
        else:
            await interaction.response.send_message(embed=error_embed("Error", "Invalid activity."), ephemeral=True)

    # ─── /fish ───
    async def _fish(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        tool = await db.has_tool(interaction.user.id, "fishing_rod")
        if not tool:
            await interaction.response.send_message(
                embed=error_embed("No Fishing Rod", "You need a fishing rod! Buy one from the shop with `/shop tools`."),
                ephemeral=True,
            )
            return

        cd = await db.check_cooldown(interaction.user.id, "fish")
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"Try again in {mins}m {secs}s."), ephemeral=True)
            return

        await interaction.response.defer()

        cast_text = generate_fish_cast()
        mods = stat_modifier(data, "work")
        eq_bonuses = await self._get_equipment_bonuses(interaction.user.id)
        weather_pay_mult = await self._weather_mod("work_pay_mult", 1.0)
        protected = await self._has_weather_protection(interaction.user.id)
        if not protected:
            weather_pay_mult = 1.0 + (weather_pay_mult - 1.0) * 0.5

        luck = 1.0 + mods["luck_bonus"] + (eq_bonuses.get("luck", 0) * 0.01)

        # Time-of-day fish luck
        time_effects = await db.get_time_effects()
        time_fish_mult = time_effects.get("fish_luck", 1.0)
        luck *= time_fish_mult

        # Faction benefit
        fish_benefit = await db.get_faction_benefit(interaction.user.id, "fishers")
        fish_luck_mult = fish_benefit.get("fish_luck", 1.0)
        luck *= fish_luck_mult

        from config import NARRATIVE_TEMPLATES
        fish_types = NARRATIVE_TEMPLATES["fish"]["fish_types"]

        if random.random() < 0.25 * luck:
            nothing = generate_fish_nothing()
            await db.set_cooldown(interaction.user.id, "fish", 60)
            await db.damage_equipment(interaction.user.id, "fishing_rod", tool["quality"], 1)
            await interaction.followup.send(embed=info_embed("🎣 Fishing", f"{cast_text}\n\n{nothing}"))
            return

        fish_name, base_value = random.choice(fish_types)
        quality = roll_quality()
        qmult = quality_multiplier(quality)
        value = int(base_value * qmult * weather_pay_mult * mods["pay_mult"])
        xp_gain = int(random.randint(5, 15) * mods["xp_mult"])

        catch_text = generate_fish_catch(fish_name)

        new_xp = data["xp"] + xp_gain
        from utils.helpers import check_level_up, xp_for_next_level
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))

        new_wallet = data["wallet"] + value
        new_energy = clamp(data.get("energy", 100) - 5, 0, ENERGY_MAX)
        new_hunger = clamp(data["hunger"] - 2, 0, HUNGER_MAX)

        await db.update_user(interaction.user.id, wallet=new_wallet, xp=new_xp, level=new_level, energy=new_energy, hunger=new_hunger, total_earned=data["total_earned"] + value)
        await db.add_transaction(interaction.user.id, "fish", value, f"Fished up {quality_name(quality)} catch")
        await db.update_quest_progress(interaction.user.id, "fish", 1)
        await db.add_reputation(interaction.user.id, "fishers", 2)
        await db.set_cooldown(interaction.user.id, "fish", 120)
        await db.damage_equipment(interaction.user.id, "fishing_rod", tool["quality"], 1)

        # World perturbation: fishing depletes docks resources, bumps population
        await world.perturb_location(interaction.user.id, "docks", resources_delta=-0.03, population_delta=0.02)

        embed = success_embed("🎣 Fishing Success!", f"{cast_text}\n\n{catch_text}")
        embed.add_field(name="💰 Earned", value=format_money(value), inline=True)
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        embed.add_field(name="📊 Quality", value=f"{quality_emoji(quality)} {quality_name(quality)}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"You are now level {new_level}!", inline=False)

        event = await self._apply_random_event(interaction.user.id, {**data, "wallet": new_wallet, "energy": new_energy, "hunger": new_hunger})
        if event:
            embed.add_field(name="🎲 Random Event", value=event["text"], inline=False)

        embed = await self._police_check(interaction, "docks", embed)
        if embed:
            await interaction.followup.send(embed=embed)

    # ─── /mine ───
    async def _mine(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        tool = await db.has_tool(interaction.user.id, "pickaxe")
        if not tool:
            await interaction.response.send_message(
                embed=error_embed("No Pickaxe", "You need a pickaxe! Buy one from the shop with `/shop tools`."),
                ephemeral=True,
            )
            return

        cd = await db.check_cooldown(interaction.user.id, "mine")
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"Try again in {mins}m {secs}s."), ephemeral=True)
            return

        await interaction.response.defer()

        swing_text = generate_mine_swing()
        mods = stat_modifier(data, "work")
        weather_pay_mult = await self._weather_mod("work_pay_mult", 1.0)
        protected = await self._has_weather_protection(interaction.user.id)
        if not protected:
            weather_pay_mult = 1.0 + (weather_pay_mult - 1.0) * 0.5

        # Faction benefit
        mine_benefit = await db.get_faction_benefit(interaction.user.id, "miners")
        mine_luck_mult = mine_benefit.get("mine_luck", 1.0)

        from config import NARRATIVE_TEMPLATES
        ore_types = NARRATIVE_TEMPLATES["mine"]["ore_types"]

        if random.random() < 0.20:
            nothing_text = generate_explore_nothing()
            await db.set_cooldown(interaction.user.id, "mine", 90)
            await db.damage_equipment(interaction.user.id, "pickaxe", tool["quality"], 1)
            await interaction.followup.send(embed=info_embed("⛏️ Mining", f"{swing_text}\n\n{nothing_text}"))
            return

        ore_name, base_value = random.choice(ore_types)
        quality = roll_quality()
        qmult = quality_multiplier(quality)
        value = int(base_value * qmult * weather_pay_mult * mods["pay_mult"] * mine_luck_mult)
        xp_gain = int(random.randint(8, 20) * mods["xp_mult"])

        find_text = generate_mine_find(ore_name)

        new_xp = data["xp"] + xp_gain
        from utils.helpers import check_level_up, xp_for_next_level
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))

        new_wallet = data["wallet"] + value
        new_energy = clamp(data.get("energy", 100) - 8, 0, ENERGY_MAX)
        new_health = data["health"]

        if random.random() < 0.08:
            hp_loss = random.randint(3, 10)
            new_health = clamp(new_health - hp_loss, 0, HEALTH_MAX)
            danger_text = generate_danger(hp_loss)
            find_text += f"\n⚠️ {danger_text}"

        await db.update_user(interaction.user.id, wallet=new_wallet, xp=new_xp, level=new_level, energy=new_energy, health=new_health, total_earned=data["total_earned"] + value)
        await db.add_transaction(interaction.user.id, "mine", value, f"Mined {quality_name(quality)} ore")
        await db.update_quest_progress(interaction.user.id, "mine", 1)
        await db.add_reputation(interaction.user.id, "miners", 2)
        await db.set_cooldown(interaction.user.id, "mine", 180)
        await db.damage_equipment(interaction.user.id, "pickaxe", tool["quality"], 1)

        # World perturbation: mining depletes mines resources, increases danger
        await world.perturb_location(interaction.user.id, "mines", resources_delta=-0.04, danger_delta=0.02)

        embed = success_embed("⛏️ Mining Success!", f"{swing_text}\n\n{find_text}")
        embed.add_field(name="💰 Earned", value=format_money(value), inline=True)
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        embed.add_field(name="📊 Quality", value=f"{quality_emoji(quality)} {quality_name(quality)}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"You are now level {new_level}!", inline=False)

        event = await self._apply_random_event(interaction.user.id, {**data, "wallet": new_wallet, "energy": new_energy, "health": new_health})
        if event:
            embed.add_field(name="🎲 Random Event", value=event["text"], inline=False)

        embed = await self._police_check(interaction, "mines", embed)
        if embed:
            await interaction.followup.send(embed=embed)

    # ─── /explore ───
    async def _explore(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        cd = await db.check_cooldown(interaction.user.id, "explore")
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"Try again in {mins}m {secs}s."), ephemeral=True)
            return

        await interaction.response.defer()

        intro = generate_explore_intro()
        mods = stat_modifier(data, "work")
        eq_bonuses = await self._get_equipment_bonuses(interaction.user.id)
        weather_pay_mult = await self._weather_mod("work_pay_mult", 1.0)
        protected = await self._has_weather_protection(interaction.user.id)
        if not protected:
            weather_pay_mult = 1.0 + (weather_pay_mult - 1.0) * 0.5

        luck = 1.0 + mods["luck_bonus"] + (eq_bonuses.get("luck", 0) * 0.01)
        roll = random.random()

        result_text = ""
        embed = None
        xp_gain = int(random.randint(10, 30) * mods["xp_mult"])
        coins_gain = 0
        hp_loss = 0

        if roll < 0.15:
            result_text = generate_explore_nothing()
            xp_gain = int(xp_gain * 0.3)
        elif roll < 0.45:
            encounter, npc, outcome = generate_npc_encounter()
            result_text = f"{encounter}\nThe {npc} {outcome}."
            coins_gain = int(random.randint(10, 80) * mods["pay_mult"] * weather_pay_mult)
            xp_gain = int(random.randint(15, 40) * mods["xp_mult"])
        elif roll < 0.75:
            possible_items = list(RAW_MATERIALS.keys()) + list(STORE_ITEMS.keys())
            found_item_id = random.choice(possible_items)
            item_data = RAW_MATERIALS.get(found_item_id, STORE_ITEMS.get(found_item_id, {}))
            item_name = item_data.get("name", found_item_id)
            quality = roll_quality()
            result_text = generate_explore_find(f"{quality_emoji(quality)} {quality_name(quality)} {item_name}")
            coins_gain = int(random.randint(20, 100) * quality_multiplier(quality) * mods["pay_mult"] * weather_pay_mult)
            await db.add_to_inventory(interaction.user.id, found_item_id, 1)
            await db.record_discovery(interaction.user.id, found_item_id, quality, "explore")
        elif roll < 0.90:
            hp_loss = random.randint(3, 15)
            result_text = generate_danger(hp_loss)
            xp_gain = int(xp_gain * 0.5)
        else:
            quality = roll_quality()
            qmult = quality_multiplier(quality)
            coins_gain = int(random.randint(50, 200) * qmult * mods["pay_mult"] * weather_pay_mult)
            result_text = generate_reward(xp_gain)
            if random.random() < 0.3:
                rare_items = ["gold_watch", "diamond", "ruby", "trophy"]
                rare_id = random.choice(rare_items)
                await db.add_to_inventory(interaction.user.id, rare_id, 1)
                rare_name = STORE_ITEMS.get(rare_id, {}).get("name", rare_id)
                result_text += f"\n✨ You also found a {quality_emoji(quality)} {quality_name(quality)} {rare_name}!"
                await db.record_discovery(interaction.user.id, rare_id, quality, "explore")

        new_xp = data["xp"] + xp_gain
        from utils.helpers import check_level_up, xp_for_next_level
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))

        new_wallet = data["wallet"] + coins_gain
        new_health = clamp(data["health"] - hp_loss, 0, HEALTH_MAX)
        new_energy = clamp(data.get("energy", 100) - 10, 0, ENERGY_MAX)
        new_hygiene = clamp(data.get("hygiene", 100) - 5, 0, HYGIENE_MAX)

        await db.update_user(
            interaction.user.id,
            wallet=new_wallet,
            xp=new_xp,
            level=new_level,
            health=new_health,
            energy=new_energy,
            hygiene=new_hygiene,
            total_earned=data["total_earned"] + coins_gain,
        )
        await db.add_transaction(interaction.user.id, "explore", coins_gain, f"Exploration: {quality_name(quality) if 'quality' in dir() else 'standard'} find")
        await db.update_quest_progress(interaction.user.id, "explore", 1)
        await db.add_reputation(interaction.user.id, "explorers", 2)
        await db.set_cooldown(interaction.user.id, "explore", 300)

        # World perturbation: exploring depletes forest resources, shifts atmosphere
        await world.perturb_location(interaction.user.id, "forest", resources_delta=-0.02, atmosphere_delta=0.03)

        embed = info_embed("🧭 Exploration", f"{intro}\n\n{result_text}")
        if coins_gain > 0:
            embed.add_field(name="💰 Coins", value=format_money(coins_gain), inline=True)
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if hp_loss > 0:
            embed.add_field(name="💔 HP", value=f"-{hp_loss}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"You are now level {new_level}!", inline=False)

        event = await self._apply_random_event(interaction.user.id, {**data, "wallet": new_wallet, "health": new_health, "energy": new_energy, "hygiene": new_hygiene})
        if event:
            embed.add_field(name="🎲 Random Event", value=event["text"], inline=False)

        embed = await self._police_check(interaction, "forest", embed)
        if embed:
            await interaction.followup.send(embed=embed)

    # ─── /forage ───
    async def _forage(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        cd = await db.check_cooldown(interaction.user.id, "forage")
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"Try again in {mins}m {secs}s."), ephemeral=True)
            return

        await interaction.response.defer()

        mods = stat_modifier(data, "work")
        eq_bonuses = await self._get_equipment_bonuses(interaction.user.id)
        luck = 1.0 + mods["luck_bonus"] + (eq_bonuses.get("luck", 0) * 0.01)

        forage_items = [
            ("herbs", "🌿 Herbs", 25),
            ("wood", "🪵 Wood", 10),
            ("cloth", "🧵 Cloth", 15),
            ("stone", "🪨 Stone", 5),
            ("clay", "🟫 Clay", 12),
            ("bread", "🍞 Wild Berries", 20),
            ("water", "💧 Fresh Spring Water", 15),
        ]

        if random.random() < 0.3 * luck:
            item_id, item_name, base_value = random.choice(forage_items)
            quality = roll_quality()
            qmult = quality_multiplier(quality)
            value = int(base_value * qmult * mods["pay_mult"])
            xp_gain = int(random.randint(5, 15) * mods["xp_mult"])

            await db.add_to_inventory(interaction.user.id, item_id, 1)
            await db.record_discovery(interaction.user.id, item_id, quality, "forage")

            new_xp = data["xp"] + xp_gain
            from utils.helpers import check_level_up, xp_for_next_level
            new_level, leveled_up = check_level_up(new_xp, data["level"])
            if leveled_up:
                new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))

            new_energy = clamp(data.get("energy", 100) - 3, 0, ENERGY_MAX)
            await db.update_user(interaction.user.id, xp=new_xp, level=new_level, energy=new_energy)
            await db.set_cooldown(interaction.user.id, "forage", 90)

            embed = success_embed("🌿 Foraging Success!", get_action_text("activities", "forage_success", quality_emoji=quality_emoji(quality), quality_name=quality_name(quality), item_name=item_name))
            embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
            if leveled_up:
                embed.add_field(name="🎉 Level Up!", value=f"You are now level {new_level}!", inline=False)
            embed = await self._police_check(interaction, "forest", embed)
            if embed:
                await interaction.followup.send(embed=embed)
        else:
            new_energy = clamp(data.get("energy", 100) - 3, 0, ENERGY_MAX)
            await db.update_user(interaction.user.id, energy=new_energy)
            await db.set_cooldown(interaction.user.id, "forage", 90)
            nothing_embed = info_embed("🌿 Foraging", get_action_text("activities", "forage_nothing"))
            nothing_embed = await self._police_check(interaction, "forest", nothing_embed)
            if nothing_embed:
                await interaction.followup.send(embed=nothing_embed)

    # ─── /chop ───
    async def _chop(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        tool = await db.has_tool(interaction.user.id, "axe")
        if not tool:
            await interaction.response.send_message(
                embed=error_embed("No Axe", "You need an axe! Buy one from the shop with `/shop tools`."),
                ephemeral=True,
            )
            return

        cd = await db.check_cooldown(interaction.user.id, "chop")
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"Try again in {mins}m {secs}s."), ephemeral=True)
            return

        await interaction.response.defer()

        mods = stat_modifier(data, "work")
        quality = roll_quality()
        qmult = quality_multiplier(quality)
        wood_amount = max(1, int(random.randint(1, 4) * qmult))
        coins_gain = int(random.randint(5, 25) * qmult * mods["pay_mult"])
        xp_gain = int(random.randint(5, 15) * mods["xp_mult"])

        await db.add_to_inventory(interaction.user.id, "wood", wood_amount)

        new_xp = data["xp"] + xp_gain
        from utils.helpers import check_level_up, xp_for_next_level
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))

        new_wallet = data["wallet"] + coins_gain
        new_energy = clamp(data.get("energy", 100) - 6, 0, ENERGY_MAX)
        await db.update_user(interaction.user.id, wallet=new_wallet, xp=new_xp, level=new_level, energy=new_energy, total_earned=data["total_earned"] + coins_gain)
        await db.set_cooldown(interaction.user.id, "chop", 120)
        await db.damage_equipment(interaction.user.id, "axe", tool["quality"], 1)

        embed = success_embed("🪓 Chopping Wood", get_action_text("activities", "chop_success", qty=wood_amount, quality_emoji=quality_emoji(quality), quality_name=quality_name(quality)))
        embed.add_field(name="💰 Coins", value=format_money(coins_gain), inline=True)
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"You are now level {new_level}!", inline=False)
        embed = await self._police_check(interaction, "forest", embed)
        if embed:
            await interaction.followup.send(embed=embed)

    # ─── /dig ───
    async def _dig(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        tool = await db.has_tool(interaction.user.id, "shovel")
        if not tool:
            await interaction.response.send_message(
                embed=error_embed("No Shovel", "You need a shovel! Buy one from the shop with `/shop tools`."),
                ephemeral=True,
            )
            return

        cd = await db.check_cooldown(interaction.user.id, "dig")
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"Try again in {mins}m {secs}s."), ephemeral=True)
            return

        await interaction.response.defer()

        mods = stat_modifier(data, "work")
        eq_bonuses = await self._get_equipment_bonuses(interaction.user.id)
        luck = 1.0 + mods["luck_bonus"] + (eq_bonuses.get("luck", 0) * 0.01)

        roll = random.random()
        if roll < 0.4:
            await db.set_cooldown(interaction.user.id, "dig", 90)
            await db.damage_equipment(interaction.user.id, "shovel", tool["quality"], 1)
            nothing_embed = info_embed("🪏 Digging", get_action_text("activities", "dig_nothing"))
            nothing_embed = await self._police_check(interaction, "ruins", nothing_embed)
            if nothing_embed:
                await interaction.followup.send(embed=nothing_embed)
            return

        quality = roll_quality()
        qmult = quality_multiplier(quality)
        coins_gain = int(random.randint(10, 150) * qmult * mods["pay_mult"] * luck)
        xp_gain = int(random.randint(5, 20) * mods["xp_mult"])

        found_items = [("stone", 0.3), ("clay", 0.2), ("metal_scrap", 0.15), ("gems", 0.05)]
        for item_id, chance in found_items:
            if random.random() < chance * luck:
                await db.add_to_inventory(interaction.user.id, item_id, 1)

        new_xp = data["xp"] + xp_gain
        from utils.helpers import check_level_up, xp_for_next_level
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))

        new_wallet = data["wallet"] + coins_gain
        new_energy = clamp(data.get("energy", 100) - 5, 0, ENERGY_MAX)
        await db.update_user(interaction.user.id, wallet=new_wallet, xp=new_xp, level=new_level, energy=new_energy, total_earned=data["total_earned"] + coins_gain)
        await db.set_cooldown(interaction.user.id, "dig", 120)
        await db.damage_equipment(interaction.user.id, "shovel", tool["quality"], 1)

        embed = success_embed("🪏 Digging Success!", get_action_text("activities", "dig_success", amount=format_money(coins_gain), quality_emoji=quality_emoji(quality), quality_name=quality_name(quality)))
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"You are now level {new_level}!", inline=False)
        embed = await self._police_check(interaction, "ruins", embed)
        if embed:
            await interaction.followup.send(embed=embed)

    # ─── /craft ───
    @app_commands.command(name="craft", description="Craft items from raw materials")
    @app_commands.choices(recipe=[
        app_commands.Choice(name=f"{r['name']} — {r['description']}", value=rid)
        for rid, r in CRAFTING_RECIPES.items()
    ])
    async def craft(self, interaction: discord.Interaction, recipe: app_commands.Choice[str]):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        recipe_id = recipe.value
        recipe_data = CRAFTING_RECIPES.get(recipe_id)
        if not recipe_data:
            await interaction.response.send_message(embed=error_embed("Error", "Invalid recipe."), ephemeral=True)
            return

        inv = await db.get_inventory(interaction.user.id)
        for ingredient, amount in recipe_data["ingredients"].items():
            if inv.get(ingredient, 0) < amount:
                ing_name = RAW_MATERIALS.get(ingredient, STORE_ITEMS.get(ingredient, {})).get("name", ingredient)
                await interaction.response.send_message(
                    embed=error_embed("Missing Ingredients", f"You need {amount}x {ing_name}. You have {inv.get(ingredient, 0)}."),
                    ephemeral=True,
                )
                return

        for ingredient, amount in recipe_data["ingredients"].items():
            await db.remove_from_inventory(interaction.user.id, ingredient, amount)

        result_id = recipe_data["result"]
        quality = roll_quality()
        await db.add_to_inventory(interaction.user.id, result_id, 1)
        await db.record_discovery(interaction.user.id, result_id, quality, "craft")

        xp_gain = random.randint(10, 25)
        new_xp = data["xp"] + xp_gain
        from utils.helpers import check_level_up, xp_for_next_level
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))

        await db.update_user(interaction.user.id, xp=new_xp, level=new_level)
        await db.add_transaction(interaction.user.id, "craft", 0, f"Crafted {quality_name(quality)} {recipe_data['name']}")
        await db.update_quest_progress(interaction.user.id, "craft", 1)

        embed = success_embed(
            "🔨 Crafting Success!",
            get_action_text("activities", "craft", quality_emoji=quality_emoji(quality), quality_name=quality_name(quality), item_name=recipe_data['name'], description=recipe_data['description']),
        )
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"You are now level {new_level}!", inline=False)
        await interaction.response.send_message(embed=embed)

    # ─── /craft_list ───
    @app_commands.command(name="craft_list", description="View all crafting recipes")
    async def craft_list(self, interaction: discord.Interaction):
        embed = info_embed("🔨 Crafting Recipes", "Combine materials to create useful items!")
        for rid, r in CRAFTING_RECIPES.items():
            ingredients_text = ", ".join(f"{amt}x {RAW_MATERIALS.get(ing, STORE_ITEMS.get(ing, {})).get('name', ing)}" for ing, amt in r["ingredients"].items())
            embed.add_field(name=f"{r['name']}", value=f"Ingredients: {ingredients_text}\n{r['description']}", inline=False)
        await interaction.response.send_message(embed=embed)

    # ─── /equipment ───
    @app_commands.command(name="equipment", description="View your tools, clothing, and possessions")
    async def equipment(self, interaction: discord.Interaction):
        equip = await db.get_equipment(interaction.user.id)
        if not equip:
            await interaction.response.send_message(embed=info_embed("🎒 Equipment", "You have no equipment. Buy tools, clothing, or possessions from the shop!"), ephemeral=True)
            return

        embed = info_embed("🎒 Your Equipment", f"Total items: {len(equip)}")

        current_type = None
        for item in equip:
            if item["item_type"] != current_type:
                current_type = item["item_type"]
                type_names = {"tool": "🔧 Tools", "clothing": "👕 Clothing", "possession": "📦 Possessions"}
                embed.add_field(name="\u200b", value=f"**{type_names.get(current_type, current_type.title())}**", inline=False)

            item_data = TOOLS.get(item["item_id"], CLOTHING.get(item["item_id"], POSSESSIONS.get(item["item_id"], {})))
            name = item_data.get("name", item["item_id"])
            q = ITEM_QUALITIES.get(item["quality"], ITEM_QUALITIES["common"])
            eq_mark = " ✅" if item["equipped"] else ""
            dur_text = f" [{item['durability']}/{item['max_durability']}]" if item["item_type"] == "tool" else ""
            embed.add_field(
                name=f"{q['emoji']} {name}{eq_mark}",
                value=f"Quality: {q['name']}{dur_text}\n`/equip item:{item['item_id']} quality:{item['quality']}`",
                inline=True,
            )

        await interaction.response.send_message(embed=embed)

    # ─── /equip ───
    @app_commands.command(name="equip", description="Equip a tool, clothing, or possession")
    async def equip(self, interaction: discord.Interaction, item_id: str, quality: str = "common"):
        success = await db.equip_item(interaction.user.id, item_id, quality)
        if not success:
            await interaction.response.send_message(embed=error_embed("Not Found", "You don't have that item."), ephemeral=True)
            return
        item_data = TOOLS.get(item_id, CLOTHING.get(item_id, POSSESSIONS.get(item_id, {})))
        name = item_data.get("name", item_id)
        q = ITEM_QUALITIES.get(quality, ITEM_QUALITIES["common"])
        await interaction.response.send_message(embed=success_embed("✅ Equipped", get_action_text("activities", "equip", quality_emoji=q['emoji'], quality_name=q['name'], item_name=name)))

    # ─── /unequip ───
    @app_commands.command(name="unequip", description="Unequip an item")
    async def unequip(self, interaction: discord.Interaction, item_id: str, quality: str = "common"):
        await db.unequip_item(interaction.user.id, item_id, quality)
        item_data = TOOLS.get(item_id, CLOTHING.get(item_id, POSSESSIONS.get(item_id, {})))
        name = item_data.get("name", item_id)
        await interaction.response.send_message(embed=info_embed("📤 Unequipped", get_action_text("activities", "unequip", item_name=name)))

    # ─── /discoveries ───
    @app_commands.command(name="discoveries", description="View items you've discovered with qualities")
    async def discoveries(self, interaction: discord.Interaction):
        discoveries = await db.get_discoveries(interaction.user.id)
        if not discoveries:
            await interaction.response.send_message(embed=info_embed("🔍 Discoveries", "You haven't discovered any items yet. Go explore, fish, mine, or forage!"), ephemeral=True)
            return

        embed = info_embed("🔍 Your Discoveries", f"Total: {len(discoveries)} items found")
        for d in discoveries[:25]:
            item_data = RAW_MATERIALS.get(d["item_id"], STORE_ITEMS.get(d["item_id"], TOOLS.get(d["item_id"], CLOTHING.get(d["item_id"], POSSESSIONS.get(d["item_id"], {})))))
            name = item_data.get("name", d["item_id"])
            q = ITEM_QUALITIES.get(d["quality"], ITEM_QUALITIES["common"])
            embed.add_field(name=f"{q['emoji']} {name}", value=f"Quality: {q['name']}\nSource: {d['source']}", inline=True)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Activities(bot))
