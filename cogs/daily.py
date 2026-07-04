import discord
from discord import app_commands
from discord.ext import commands
import database as db
from utils.embeds import success_embed, error_embed, info_embed, format_money
from utils.helpers import check_level_up, xp_for_next_level, clamp, pet_bonus
from utils.narrative import get_action_text
from config import ACHIEVEMENTS
from datetime import datetime, timezone


class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="daily", description="Claim your daily reward! Build up streaks for bigger rewards.")
    async def daily(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        now = datetime.now(timezone.utc)

        cd = await db.check_cooldown(interaction.user.id, "daily")
        if cd > 0:
            hours = int(cd // 3600)
            mins = int((cd % 3600) // 60)
            await interaction.response.send_message(embed=error_embed("Already Claimed", f"Come back in {hours}h {mins}m for your next daily reward."), ephemeral=True)
            return

        last_daily = data.get("last_daily")
        streak = data.get("daily_streak", 0)

        if last_daily:
            last_dt = datetime.fromisoformat(last_daily)
            diff = (now - last_dt).total_seconds()
            if diff > 172800:
                streak = 0

        streak += 1
        base_reward = 50
        streak_bonus = min(streak * 10, 200)
        level_bonus = data["level"] * 5
        total = base_reward + streak_bonus + level_bonus

        xp_gain = pet_bonus(data.get("pet_id"), "xp", 20 + streak * 2)
        new_xp = data["xp"] + xp_gain
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))

        await db.update_user(interaction.user.id,
            wallet=data["wallet"] + total,
            daily_streak=streak,
            last_daily=now.isoformat(),
            xp=new_xp,
            level=new_level,
            total_earned=data["total_earned"] + total,
            daily_claims=data.get("daily_claims", 0) + 1,
        )
        await db.add_transaction(interaction.user.id, "daily", total, f"Daily reward (streak {streak})")
        await db.set_cooldown(interaction.user.id, "daily", 86400)
        await db.update_quest_progress(interaction.user.id, "earn", total)

        embed = success_embed("🎁 Daily Reward Claimed!", get_action_text("misc", "daily", amount=format_money(total)))
        embed.add_field(name="Base Reward", value=format_money(base_reward), inline=True)
        embed.add_field(name="Streak Bonus", value=format_money(streak_bonus), inline=True)
        embed.add_field(name="Level Bonus", value=format_money(level_bonus), inline=True)
        embed.add_field(name="🔥 Streak", value=f"{streak} days", inline=True)
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)

        extra = 0
        if streak % 7 == 0:
            bonus = 200 + streak * 20
            extra += bonus
            embed.add_field(name="🎉 Weekly Streak Bonus!", value=f"+{format_money(bonus)}", inline=False)

        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)

        new_achievements = await db.check_achievements(interaction.user.id)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        if new_achievements:
            ach_reward = sum(ACHIEVEMENTS[a]["reward"] for a in new_achievements)
            extra += ach_reward

        if extra > 0:
            await db.update_user(interaction.user.id, wallet=data["wallet"] + total + extra, total_earned=data["total_earned"] + total + extra)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="weekly", description="Claim your weekly reward!")
    async def weekly(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        cd = await db.check_cooldown(interaction.user.id, "weekly")
        if cd > 0:
            days = int(cd // 86400)
            hours = int((cd % 86400) // 3600)
            await interaction.response.send_message(embed=error_embed("Already Claimed", f"Come back in {days}d {hours}h for your next weekly reward."), ephemeral=True)
            return

        reward = 500 + data["level"] * 25
        xp_gain = pet_bonus(data.get("pet_id"), "xp", 100)
        new_xp = data["xp"] + xp_gain
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))

        await db.update_user(interaction.user.id,
            wallet=data["wallet"] + reward,
            xp=new_xp,
            level=new_level,
            total_earned=data["total_earned"] + reward,
        )
        await db.add_transaction(interaction.user.id, "weekly", reward, "Weekly reward")
        await db.set_cooldown(interaction.user.id, "weekly", 604800)
        await db.update_quest_progress(interaction.user.id, "earn", reward)

        embed = success_embed("📦 Weekly Reward Claimed!", get_action_text("misc", "weekly", amount=format_money(reward), xp=xp_gain))
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        new_achievements = await db.check_achievements(interaction.user.id)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        if new_achievements:
            ach_reward = sum(ACHIEVEMENTS[a]["reward"] for a in new_achievements)
            await db.update_user(interaction.user.id, wallet=data["wallet"] + reward + ach_reward, total_earned=data["total_earned"] + reward + ach_reward)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Daily(bot))
