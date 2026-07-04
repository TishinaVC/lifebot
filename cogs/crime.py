import discord
from discord import app_commands
from discord.ext import commands
import random
import database as db
import world
import police as _police
from utils.embeds import success_embed, error_embed, info_embed, warning_embed, format_money
from utils.helpers import check_level_up, xp_for_next_level, clamp, stat_modifier, get_housing_bonus
from utils.narrative import get_action_text
from config import HEALTH_MAX, ACHIEVEMENTS
from config.police import HEAT_PER_CRIME, HEAT_TAILING_THRESHOLD, HEAT_WARRANT_THRESHOLD, HEAT_MAX

CRIME_TYPES = {
    "pickpocket": {"name": "🤏 Pickpocket", "min_amount": 50, "max_amount": 200, "cooldown": 300, "success_rate": 0.65, "fine": 100},
    "rob": {"name": "🔫 Rob Store", "min_amount": 200, "max_amount": 800, "cooldown": 600, "success_rate": 0.45, "fine": 300},
    "heist": {"name": "🏦 Bank Heist", "min_amount": 1000, "max_amount": 5000, "cooldown": 3600, "success_rate": 0.25, "fine": 1000},
    "hack": {"name": "💻 Hack ATM", "min_amount": 500, "max_amount": 2000, "cooldown": 1800, "success_rate": 0.35, "fine": 500},
}


class Crime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="crime", description="Commit a crime for quick cash — but risk getting caught!")
    @app_commands.choices(crime_type=[
        app_commands.Choice(name=v["name"], value=k) for k, v in CRIME_TYPES.items()
    ])
    async def crime(self, interaction: discord.Interaction, crime_type: app_commands.Choice[str]):
        ct = CRIME_TYPES[crime_type.value]
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        cd = await db.check_cooldown(interaction.user.id, "crime")
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"You're laying low. Try again in {mins}m {secs}s."), ephemeral=True)
            return

        if data["health"] <= 20:
            await interaction.response.send_message(embed=error_embed("Too Weak", "Your health is too low to commit crimes!"), ephemeral=True)
            return

        mods = stat_modifier(data, "crime")
        from config import WEATHER_STATES
        current_weather = await db.get_weather()
        weather_crime_mult = WEATHER_STATES.get(current_weather, {}).get("effects", {}).get("crime_success_mult", 1.0)
        time_effects = await db.get_time_effects()
        time_crime_mult = time_effects.get("crime_success", 1.0)
        buff_crime_mult = await db.get_buff_mult(interaction.user.id, "crime_success")
        underworld_benefit = await db.get_faction_benefit(interaction.user.id, "underworld")
        faction_crime_mult = underworld_benefit.get("crime_success", 1.0)
        success = random.random() < (ct["success_rate"] * weather_crime_mult * time_crime_mult * buff_crime_mult * faction_crime_mult + mods["success_bonus"])

        wallet_change = 0
        earned = 0

        if success:
            reward = random.randint(ct["min_amount"], ct["max_amount"])
            level_mult = 1.0 + data["level"] * 0.02
            reward = int(reward * level_mult * mods["pay_mult"])
            xp_gain = int(random.randint(15, 40) * mods["xp_mult"])
            stat_cost = mods["stat_cost_mult"]

            new_xp = data["xp"] + xp_gain
            new_level, leveled_up = check_level_up(new_xp, data["level"])
            if leveled_up:
                new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))

            wallet_change = reward
            earned = reward
            await db.update_user(interaction.user.id,
                wallet=data["wallet"] + reward,
                xp=new_xp,
                level=new_level,
                crimes_committed=data["crimes_committed"] + 1,
                crimes_successful=data["crimes_successful"] + 1,
                total_earned=data["total_earned"] + reward,
                health=clamp(data["health"] - int(5 * stat_cost)),
                energy=clamp(data.get("energy", 100) - int(8 * stat_cost)),
            )
            await db.add_transaction(interaction.user.id, "crime", reward, f"Successful {ct['name']}")
            await db.set_cooldown(interaction.user.id, "crime", ct["cooldown"])
            await db.update_quest_progress(interaction.user.id, "crime", 1)
            await db.update_quest_progress(interaction.user.id, "earn", reward)
            await db.add_reputation(interaction.user.id, "underworld", 2)

            # Add police heat for successful crime
            heat_gain = HEAT_PER_CRIME.get(crime_type.value, 10)
            await _police.add_crime_heat(interaction.user.id, crime_type.value)
            current_heat = await _police.get_heat(interaction.user.id)
            warrant_issued = await _police.check_warrant_eligible(interaction.user.id)

            embed = success_embed(f"🦹 {ct['name']} — Success!", get_action_text("crime", "success", reward=format_money(reward)))
            embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
            embed.add_field(name="🦹 +2 Underworld rep", value=" ", inline=True)
            embed.add_field(name="🔥 Police Heat", value=f"+{heat_gain} heat (now {current_heat}/{HEAT_MAX})", inline=True)
            if warrant_issued:
                embed.add_field(name="📋 WARRANT ISSUED", value=get_action_text("crime", "warrant"), inline=False)
            elif current_heat >= HEAT_TAILING_THRESHOLD:
                embed.add_field(name="⚠️ Heat Warning", value=get_action_text("crime", "heat_warning"), inline=False)
            if leveled_up:
                embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        else:
            fine = ct["fine"]
            if data["wallet"] < fine:
                fine = data["wallet"]
            health_loss = random.randint(10, 25)
            xp_gain = 5

            new_xp = data["xp"] + xp_gain
            new_level, leveled_up = check_level_up(new_xp, data["level"])
            if leveled_up:
                new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))

            wallet_change = -fine
            await db.update_user(interaction.user.id,
                wallet=data["wallet"] - fine,
                xp=new_xp,
                level=new_level,
                crimes_committed=data["crimes_committed"] + 1,
                total_lost=data["total_lost"] + fine,
                health=clamp(data["health"] - health_loss),
            )
            await db.add_transaction(interaction.user.id, "crime_fine", fine, f"Caught doing {ct['name']}")
            await db.set_cooldown(interaction.user.id, "crime", ct["cooldown"])

            # Add extra heat for getting caught
            heat_gain = HEAT_PER_CRIME.get(crime_type.value, 10) + 10
            await _police.add_crime_heat(interaction.user.id, crime_type.value)
            await db.add_heat(interaction.user.id, 10)  # extra heat for getting caught
            current_heat = await _police.get_heat(interaction.user.id)
            warrant_issued = await _police.check_warrant_eligible(interaction.user.id)

            embed = error_embed(f"🚨 {ct['name']} — Caught!", get_action_text("crime", "caught", fine=format_money(fine), hp_loss=health_loss))
            embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
            embed.add_field(name="🔥 Police Heat", value=f"+{heat_gain} heat (now {current_heat}/{HEAT_MAX})", inline=True)
            if warrant_issued:
                embed.add_field(name="📋 WARRANT ISSUED", value=get_action_text("crime", "warrant"), inline=False)
            if leveled_up:
                embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)

        new_achievements = await db.check_achievements(interaction.user.id)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        if new_achievements:
            ach_reward = sum(ACHIEVEMENTS[a]["reward"] for a in new_achievements)
            await db.update_user(interaction.user.id, wallet=data["wallet"] + wallet_change + ach_reward, total_earned=data["total_earned"] + earned + ach_reward)

        # World perturbation: crime increases alleys danger, shifts atmosphere darker
        await world.perturb_location(interaction.user.id, "alleys", danger_delta=0.03, atmosphere_delta=-0.02)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="rob_user", description="Rob another user's wallet!")
    async def rob_user(self, interaction: discord.Interaction, user: discord.Member):
        if user.id == interaction.user.id:
            await interaction.response.send_message(embed=error_embed("Error", "You can't rob yourself."), ephemeral=True)
            return
        if user.bot:
            await interaction.response.send_message(embed=error_embed("Error", "You can't rob a bot."), ephemeral=True)
            return

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        target_data = await db.get_or_create_user(user.id, interaction.guild.id if interaction.guild else 0)

        cd = await db.check_cooldown(interaction.user.id, "rob_user")
        if cd > 0:
            mins = int(cd // 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"Try again in {mins}m."), ephemeral=True)
            return

        if target_data["wallet"] < 100:
            await interaction.response.send_message(embed=error_embed("Not Worth It", f"{user.display_name} doesn't have enough money to rob."), ephemeral=True)
            return

        if data["level"] < 3:
            await interaction.response.send_message(embed=error_embed("Too Low Level", "You need level 3 to rob other users."), ephemeral=True)
            return

        mods = stat_modifier(data, "crime")
        target_housing = await get_housing_bonus(user.id)
        success = random.random() < (0.4 + mods["success_bonus"] - target_housing["security_bonus"])

        wallet_change = 0
        earned = 0

        if success:
            stolen = int(target_data["wallet"] * random.uniform(0.1, 0.3) * mods["pay_mult"])
            xp_gain = int(random.randint(10, 25) * mods["xp_mult"])

            new_xp = data["xp"] + xp_gain
            new_level, leveled_up = check_level_up(new_xp, data["level"])
            if leveled_up:
                new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))

            wallet_change = stolen
            earned = stolen
            await db.update_user(interaction.user.id,
                wallet=data["wallet"] + stolen,
                xp=new_xp,
                level=new_level,
                crimes_committed=data["crimes_committed"] + 1,
                crimes_successful=data["crimes_successful"] + 1,
                total_earned=data["total_earned"] + stolen,
            )
            await db.update_user(user.id,
                wallet=target_data["wallet"] - stolen,
                total_lost=target_data["total_lost"] + stolen,
            )
            await db.add_transaction(interaction.user.id, "rob_user", stolen, f"Robbed {user.name}")
            await db.add_transaction(user.id, "robbed", stolen, f"Robbed by {interaction.user.name}")
            await db.set_cooldown(interaction.user.id, "rob_user", 3600)

            # Add police heat for robbing a user
            await _police.add_crime_heat(interaction.user.id, "rob_user")
            current_heat = await _police.get_heat(interaction.user.id)
            warrant_issued = await _police.check_warrant_eligible(interaction.user.id)

            embed = success_embed("🦹 Robbery Successful!", get_action_text("crime", "rob_success", amount=format_money(stolen), victim=user.mention))
            embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
            embed.add_field(name="🔥 Police Heat", value=f"+{HEAT_PER_CRIME.get('rob_user', 20)} heat (now {current_heat}/{HEAT_MAX})", inline=True)
            if warrant_issued:
                embed.add_field(name="📋 WARRANT ISSUED", value=get_action_text("crime", "warrant"), inline=False)
            elif current_heat >= HEAT_TAILING_THRESHOLD:
                embed.add_field(name="⚠️ Heat Warning", value=get_action_text("crime", "heat_warning"), inline=False)
            if leveled_up:
                embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        else:
            fine = 100
            if data["wallet"] < fine:
                fine = data["wallet"]
            health_loss = random.randint(5, 15)

            wallet_change = -fine
            await db.update_user(interaction.user.id,
                wallet=data["wallet"] - fine,
                health=clamp(data["health"] - health_loss),
                crimes_committed=data["crimes_committed"] + 1,
                total_lost=data["total_lost"] + fine,
            )
            await db.set_cooldown(interaction.user.id, "rob_user", 3600)

            embed = error_embed("🚨 Robbery Failed!", get_action_text("crime", "rob_fail", victim=user.mention, fine=format_money(fine), hp_loss=health_loss))

        new_achievements = await db.check_achievements(interaction.user.id)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        if new_achievements:
            ach_reward = sum(ACHIEVEMENTS[a]["reward"] for a in new_achievements)
            await db.update_user(interaction.user.id, wallet=data["wallet"] + wallet_change + ach_reward, total_earned=data["total_earned"] + earned + ach_reward)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Crime(bot))
