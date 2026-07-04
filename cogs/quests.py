import discord
from discord import app_commands
from discord.ext import commands
import random
import database as db
from utils.embeds import success_embed, error_embed, info_embed, format_money
from utils.helpers import check_level_up, xp_for_next_level, pet_bonus
from config import QUESTS, ACHIEVEMENTS
from utils.narrative import get_action_text


class Quests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="quests", description="View your active daily quests")
    async def quests(self, interaction: discord.Interaction):
        active = await db.get_active_quests(interaction.user.id)
        if not active:
            await interaction.response.send_message(embed=info_embed("📋 Quests", "You have no active quests. Use `/quest_refresh` to get new daily quests!"))
            return

        embed = info_embed("📋 Daily Quests", "Complete these tasks for rewards!")
        for quest in active:
            qdef = QUESTS.get(quest["quest_id"], {})
            name = qdef.get("name", quest["quest_id"])
            desc = qdef.get("description", "")
            target = qdef.get("target", 1)
            reward = qdef.get("reward", 100)
            progress = min(quest["quest_progress"], target)
            bar_len = 10
            filled = int((progress / target) * bar_len) if target > 0 else 0
            bar = "█" * filled + "░" * (bar_len - filled)
            status = "✅" if quest["completed"] else "⏳"
            embed.add_field(
                name=f"{status} {name}",
                value=f"{desc}\nProgress: {progress}/{target} [{bar}]\nReward: {format_money(reward)} + XP",
                inline=False,
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="quest_refresh", description="Get new daily quests (resets every 24h)")
    async def quest_refresh(self, interaction: discord.Interaction):
        cd = await db.check_cooldown(interaction.user.id, "quest_refresh")
        if cd > 0:
            hours = int(cd // 3600)
            mins = int((cd % 3600) // 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"New quests available in {hours}h {mins}m."), ephemeral=True)
            return

        await db.clear_quests(interaction.user.id)
        available = list(QUESTS.keys())
        selected = random.sample(available, min(3, len(available)))

        for quest_id in selected:
            qdef = QUESTS[quest_id]
            await db.add_quest(
                interaction.user.id,
                quest_id,
                qdef["description"],
                qdef["type"],
                qdef["target"],
                qdef["reward"],
            )

        await db.set_cooldown(interaction.user.id, "quest_refresh", 86400)
        embed = success_embed("📋 New Quests Available!", get_action_text("misc", "quest_refresh"))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="quest_claim", description="Claim rewards for completed quests")
    async def quest_claim(self, interaction: discord.Interaction):
        active = await db.get_active_quests(interaction.user.id)
        claimed = 0
        total_reward = 0
        total_xp = 0

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        for quest in active:
            if quest["completed"] and not quest.get("claimed"):
                qdef = QUESTS.get(quest["quest_id"], {})
                reward = pet_bonus(data.get("pet_id"), "quest_reward", qdef.get("reward", 100))
                xp_gain = qdef.get("xp", 50)
                total_reward += reward
                total_xp += xp_gain
                claimed += 1
                await db.claim_quest(interaction.user.id, quest["quest_id"])

        if claimed == 0:
            await interaction.response.send_message(embed=error_embed("Nothing to Claim", "Complete some quests first! Use `/quests` to check progress."), ephemeral=True)
            return

        new_xp = data["xp"] + total_xp
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))

        await db.update_user(interaction.user.id,
            wallet=data["wallet"] + total_reward,
            xp=new_xp,
            level=new_level,
            total_earned=data["total_earned"] + total_reward,
            quests_completed=data.get("quests_completed", 0) + claimed,
        )
        await db.add_transaction(interaction.user.id, "quest", total_reward, f"Claimed {claimed} quest(s)")

        embed = success_embed("🎁 Quest Rewards Claimed!", get_action_text("misc", "quest_claimed", count=claimed, reward=format_money(total_reward), xp=total_xp))
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        new_achievements = await db.check_achievements(interaction.user.id)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        if new_achievements:
            ach_reward = sum(ACHIEVEMENTS[a]["reward"] for a in new_achievements)
            await db.update_user(interaction.user.id, wallet=data["wallet"] + total_reward + ach_reward, total_earned=data["total_earned"] + total_reward + ach_reward)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Quests(bot))
