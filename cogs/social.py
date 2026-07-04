import discord
from discord import app_commands
from discord.ext import commands
import database as db
from utils.embeds import success_embed, error_embed, info_embed, format_money
from utils.helpers import check_level_up, xp_for_next_level, clamp, stat_modifier
from utils.narrative import get_action_text
from datetime import datetime, timezone


class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="marry", description="Propose to another user!")
    async def marry(self, interaction: discord.Interaction, user: discord.Member):
        if user.id == interaction.user.id:
            await interaction.response.send_message(embed=error_embed("Error", "You can't marry yourself."), ephemeral=True)
            return
        if user.bot:
            await interaction.response.send_message(embed=error_embed("Error", "You can't marry a bot."), ephemeral=True)
            return

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        cd = await db.check_cooldown(interaction.user.id, "marry")
        if cd > 0:
            mins = int(cd // 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"You need to wait before proposing again. Try again in {mins}m."), ephemeral=True)
            return

        if data.get("married_to"):
            await interaction.response.send_message(embed=error_embed("Already Married", f"You're already married to <@{data['married_to']}>. Use `/divorce` first."), ephemeral=True)
            return

        target_data = await db.get_or_create_user(user.id, interaction.guild.id if interaction.guild else 0)
        if target_data.get("married_to"):
            await interaction.response.send_message(embed=error_embed("Already Taken", f"{user.display_name} is already married."), ephemeral=True)
            return

        view = MarriageView(interaction.user.id, user.id, timeout=60)
        await interaction.response.send_message(
            content=f"💍 {interaction.user.mention} is proposing to {user.mention}! Do you accept?",
            view=view,
        )
        await view.wait()

        if view.accepted:
            now = datetime.now(timezone.utc).isoformat()
            await db.update_user(interaction.user.id, married_to=user.id, marriage_date=now)
            await db.update_user(user.id, married_to=interaction.user.id, marriage_date=now)
            await db.unlock_achievement(interaction.user.id, "married")
            await db.unlock_achievement(user.id, "married")
            xp_gain = 50
            await db.update_user(interaction.user.id, xp=data["xp"] + xp_gain)
            await db.update_user(user.id, xp=target_data["xp"] + xp_gain)
            await db.set_cooldown(interaction.user.id, "marry", 300)
            await interaction.followup.send(embed=success_embed("💍 Married!", get_action_text("social", "marry_accept", proposer=interaction.user.mention, recipient=user.mention, xp=xp_gain)))
        else:
            await db.set_cooldown(interaction.user.id, "marry", 300)
            await interaction.followup.send(embed=error_embed("💔 Rejected", get_action_text("social", "marry_reject", recipient=user.display_name)))

    @app_commands.command(name="divorce", description="Divorce your partner")
    async def divorce(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if not data.get("married_to"):
            await interaction.response.send_message(embed=error_embed("Not Married", "You're not married to anyone."), ephemeral=True)
            return

        partner_id = data["married_to"]
        await db.update_user(interaction.user.id, married_to=None, marriage_date=None)
        await db.update_user(partner_id, married_to=None, marriage_date=None)
        await interaction.response.send_message(embed=success_embed("💔 Divorced", get_action_text("social", "divorce", partner=f"<@{partner_id}>")))

    @app_commands.command(name="relationship", description="View your relationship status")
    async def relationship(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if not data.get("married_to"):
            await interaction.response.send_message(embed=info_embed("💔 Single", "You are not married. Use `/marry` to propose to someone!"))
            return
        embed = info_embed("💍 Relationship Status")
        embed.add_field(name="Partner", value=f"<@{data['married_to']}>", inline=True)
        if data.get("marriage_date"):
            dt = datetime.fromisoformat(data["marriage_date"])
            days = (datetime.now(timezone.utc) - dt).days
            embed.add_field(name="Married For", value=f"{days} days", inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="gift", description="Gift coins to another user")
    async def gift(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if user.id == interaction.user.id:
            await interaction.response.send_message(embed=error_embed("Error", "You can't gift yourself."), ephemeral=True)
            return
        if user.bot:
            await interaction.response.send_message(embed=error_embed("Error", "You can't gift a bot."), ephemeral=True)
            return
        if amount <= 0:
            await interaction.response.send_message(embed=error_embed("Error", "Amount must be positive."), ephemeral=True)
            return

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        cd = await db.check_cooldown(interaction.user.id, "gift")
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"You need to wait before gifting again. Try again in {mins}m {secs}s."), ephemeral=True)
            return

        if amount > data["wallet"]:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You only have {format_money(data['wallet'])}."), ephemeral=True)
            return

        target_data = await db.get_or_create_user(user.id, interaction.guild.id if interaction.guild else 0)
        mods = stat_modifier(data, "social")
        await db.update_user(interaction.user.id, wallet=data["wallet"] - amount, gifts_given=data.get("gifts_given", 0) + 1)
        await db.update_user(user.id, wallet=target_data["wallet"] + amount, total_earned=target_data["total_earned"] + amount)
        await db.add_transaction(interaction.user.id, "gift", amount, f"Gifted to {user.name}")
        await db.add_transaction(user.id, "gift_received", amount, f"Gift from {interaction.user.name}")

        xp_gain = int(10 * mods["xp_mult"])
        new_xp = data["xp"] + xp_gain
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))
        await db.update_user(interaction.user.id, xp=new_xp, level=new_level)

        await db.set_cooldown(interaction.user.id, "gift", 300)
        embed = success_embed("🎁 Gift Sent!", get_action_text("social", "gift_sent", amount=format_money(amount), recipient=user.mention, xp=xp_gain))
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        await interaction.response.send_message(embed=embed)


class MarriageView(discord.ui.View):
    def __init__(self, proposer_id, target_id, timeout=60):
        super().__init__(timeout=timeout)
        self.proposer_id = proposer_id
        self.target_id = target_id
        self.accepted = False

    @discord.ui.button(label="Accept 💍", style=discord.ButtonStyle.success)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target_id:
            await interaction.response.send_message("Only the proposed person can respond!", ephemeral=True)
            return
        self.accepted = True
        self.stop()
        await interaction.response.edit_message(content="💍 Proposal accepted!", view=None)

    @discord.ui.button(label="Decline 💔", style=discord.ButtonStyle.danger)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.target_id:
            await interaction.response.send_message("Only the proposed person can respond!", ephemeral=True)
            return
        self.accepted = False
        self.stop()
        await interaction.response.edit_message(content="💔 Proposal declined.", view=None)

    async def on_timeout(self):
        self.accepted = False
        self.stop()


async def setup(bot):
    await bot.add_cog(Social(bot))
