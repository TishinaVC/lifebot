import discord
from discord.ext import commands
import database as db
from config import ACHIEVEMENTS
from utils.helpers import check_level_up, xp_for_next_level
from utils.embeds import error_embed, format_money


class BaseCog(commands.Cog):
    """Base cog with common helper methods for all Lifebot cogs."""

    def __init__(self, bot):
        self.bot = bot

    async def get_user(self, interaction: discord.Interaction) -> dict:
        return await db.get_or_create_user(
            interaction.user.id,
            interaction.guild.id if interaction.guild else 0,
        )

    async def check_cooldown(self, interaction: discord.Interaction, command: str, ephemeral: bool = True) -> bool:
        """Check cooldown. Sends error embed and returns True if on cooldown. Returns False if OK."""
        cd = await db.check_cooldown(interaction.user.id, command)
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            time_str = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"
            await interaction.response.send_message(
                embed=error_embed("On Cooldown", f"Try again in {time_str}."),
                ephemeral=ephemeral,
            )
            return True
        return False

    async def grant_xp(self, user_id: int, xp_gain: int, current_xp: int, current_level: int) -> tuple:
        """Grant XP and handle level ups. Returns (new_xp, new_level, leveled_up)."""
        new_xp = current_xp + xp_gain
        new_level, leveled_up = check_level_up(new_xp, current_level)
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(current_level, new_level))
            await db.update_user(user_id, xp=new_xp, level=new_level)
        else:
            await db.update_user(user_id, xp=new_xp)
        return new_xp, new_level, leveled_up

    async def check_and_reward_achievements(
        self, user_id: int, embed: discord.Embed, base_wallet: int, base_earned: int
    ) -> int:
        """Check for new achievements, add embed fields, update wallet with rewards.
        Returns total achievement reward amount."""
        new_achievements = await db.check_achievements(user_id)
        total_reward = 0
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(
                name="🏆 Achievement Unlocked!",
                value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!",
                inline=False,
            )
            total_reward += ach["reward"]
        if total_reward > 0:
            await db.update_user(
                user_id,
                wallet=base_wallet + total_reward,
                total_earned=base_earned + total_reward,
            )
        return total_reward

    @staticmethod
    def add_level_up_field(embed: discord.Embed, new_level: int):
        embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
