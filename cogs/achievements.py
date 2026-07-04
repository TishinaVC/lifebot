import discord
from discord import app_commands
from discord.ext import commands
import database as db
from utils.embeds import success_embed, error_embed, info_embed, format_money
from config import ACHIEVEMENTS


class Achievements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="achievements", description="View your achievements")
    async def achievements(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        unlocked = await db.get_achievement_ids(interaction.user.id)

        embed = info_embed("🏆 Achievements", f"Unlocked: {len(unlocked)} / {len(ACHIEVEMENTS)}")
        for ach_id, ach in ACHIEVEMENTS.items():
            status = "✅" if ach_id in unlocked else "🔒"
            embed.add_field(
                name=f"{status} {ach['emoji']} {ach['name']}",
                value=f"{ach['description']}\nReward: {format_money(ach['reward'])}",
                inline=False,
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="mystats", description="View your overall statistics")
    async def stats(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        embed = info_embed(f"📊 {interaction.user.display_name}'s Statistics")
        embed.set_thumbnail(url=interaction.user.display_avatar.url)

        embed.add_field(name="Level", value=str(data["level"]), inline=True)
        embed.add_field(name="XP", value=str(data["xp"]), inline=True)
        embed.add_field(name="Total Earned", value=format_money(data["total_earned"]), inline=True)
        embed.add_field(name="Total Lost", value=format_money(data["total_lost"]), inline=True)
        embed.add_field(name="Net Profit", value=format_money(data["total_earned"] - data["total_lost"]), inline=True)
        embed.add_field(name="Times Worked", value=str(data["work_count"]), inline=True)
        embed.add_field(name="Crimes Committed", value=str(data["crimes_committed"]), inline=True)
        embed.add_field(name="Crimes Successful", value=str(data["crimes_successful"]), inline=True)
        embed.add_field(name="Hospital Visits", value=str(data["hospital_visits"]), inline=True)
        embed.add_field(name="Items Used", value=str(data["items_used"]), inline=True)
        embed.add_field(name="Daily Streak", value=f"{data['daily_streak']} days", inline=True)
        embed.add_field(name="Daily Claims", value=str(data.get("daily_claims", 0)), inline=True)
        embed.add_field(name="Married", value="Yes" if data.get("married_to") else "No", inline=True)
        embed.add_field(name="Games Played", value=str(data["games_played"]), inline=True)
        embed.add_field(name="Games Won", value=str(data["games_won"]), inline=True)
        embed.add_field(name="Total Gambled", value=format_money(data["total_gambled"]), inline=True)
        embed.add_field(name="Pet Battles Won", value=str(data.get("battles_won", 0)), inline=True)
        embed.add_field(name="Gifts Given", value=str(data.get("gifts_given", 0)), inline=True)
        embed.add_field(name="Quests Completed", value=str(data.get("quests_completed", 0)), inline=True)
        embed.add_field(name="⚡ Energy", value=f"{data.get('energy', 100)}/100", inline=True)
        embed.add_field(name="🧼 Hygiene", value=f"{data.get('hygiene', 100)}/100", inline=True)

        collectible_count = await db.count_collectibles(interaction.user.id)
        embed.add_field(name="Collectibles", value=str(collectible_count), inline=True)

        if data.get("pet_id"):
            embed.add_field(name="Pet", value=data.get("pet_name", "Unknown"), inline=True)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Achievements(bot))
