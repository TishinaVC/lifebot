import discord
from discord import app_commands
from discord.ext import commands
import database as db
from utils.embeds import success_embed, error_embed, info_embed, stats_bar, format_money
from utils.helpers import xp_for_next_level, check_level_up
from config import XP_PER_LEVEL


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rank", description="View your rank card with level and XP")
    async def rank(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        data = await db.get_or_create_user(target.id, interaction.guild.id if interaction.guild else 0)

        xp_next = xp_for_next_level(data["level"])
        xp_current = data["xp"]
        progress = (xp_current / xp_next) * 100 if xp_next > 0 else 0

        embed = info_embed(f"🏆 {target.display_name}'s Rank")
        embed.set_thumbnail(url=target.display_avatar.url)
        embed.add_field(name="Level", value=str(data["level"]), inline=True)
        embed.add_field(name="XP", value=f"{xp_current} / {xp_next}", inline=True)
        embed.add_field(name="Progress", value=f"{progress:.1f}%", inline=True)

        bar = stats_bar(xp_current, xp_next, length=15)
        embed.add_field(name="XP Bar", value=bar, inline=False)

        total_xp = sum(xp_for_next_level(l) for l in range(1, data["level"])) + xp_current
        embed.set_footer(text=f"Total XP: {total_xp:,}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="level_rewards", description="View level rewards")
    async def level_rewards(self, interaction: discord.Interaction):
        embed = info_embed("🎁 Level Rewards", "Unlock perks as you level up!")
        rewards = [
            ("Level 3", "Unlock Delivery Driver job"),
            ("Level 5", "Unlock Chef job + 500 bonus coins"),
            ("Level 8", "Unlock Mechanic job + 1000 bonus coins"),
            ("Level 10", "Bank capacity +5000"),
            ("Level 12", "Unlock Doctor job + 2000 bonus coins"),
            ("Level 15", "Unlock Programmer job + 3000 bonus coins"),
            ("Level 20", "Unlock Pilot job + 5000 bonus coins"),
            ("Level 25", "Bank capacity +10000 + 5000 bonus coins"),
            ("Level 30", "Unlock CEO job + 10000 bonus coins"),
            ("Level 50", "Legend status + 25000 bonus coins + bank capacity +50000"),
        ]
        for level, reward in rewards:
            embed.add_field(name=level, value=reward, inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Leveling(bot))
