import discord
from discord import app_commands
from discord.ext import commands
import database as db
from utils.base import BaseCog
from utils.embeds import success_embed, error_embed, info_embed, money_embed, stats_bar, format_money
from utils.helpers import xp_for_next_level
from utils.narrative import get_action_text
from config import HEALTH_MAX, HUNGER_MAX, THIRST_MAX, ENERGY_MAX, HYGIENE_MAX, JOBS


class Economy(BaseCog):

    @app_commands.command(name="balance", description="Check your balance and stats")
    async def balance(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        data = await db.get_or_create_user(target.id, interaction.guild.id if interaction.guild else 0)

        embed = info_embed(f"📊 {target.display_name}'s Profile")
        embed.set_thumbnail(url=target.display_avatar.url)

        embed.add_field(name="💰 Wallet", value=format_money(data["wallet"]), inline=True)
        embed.add_field(name="🏦 Bank", value=f"{format_money(data['bank'])} / {format_money(data['bank_capacity'])}", inline=True)
        embed.add_field(name="📈 Level", value=f"Level {data['level']}", inline=True)

        xp_next = xp_for_next_level(data["level"])
        embed.add_field(name="⭐ XP", value=f"{data['xp']} / {xp_next}", inline=True)

        health_bar = stats_bar(data["health"], HEALTH_MAX)
        hunger_bar = stats_bar(data["hunger"], HUNGER_MAX)
        thirst_bar = stats_bar(data["thirst"], THIRST_MAX)
        energy_bar = stats_bar(data.get("energy", 100), ENERGY_MAX)
        hygiene_bar = stats_bar(data.get("hygiene", 100), HYGIENE_MAX)
        embed.add_field(name=f"❤️ Health ({data['health']}/{HEALTH_MAX})", value=health_bar, inline=False)
        embed.add_field(name=f"🍖 Hunger ({data['hunger']}/{HUNGER_MAX})", value=hunger_bar, inline=False)
        embed.add_field(name=f"💧 Thirst ({data['thirst']}/{THIRST_MAX})", value=thirst_bar, inline=False)
        embed.add_field(name=f"⚡ Energy ({data.get('energy', 100)}/{ENERGY_MAX})", value=energy_bar, inline=False)
        embed.add_field(name=f"🧼 Hygiene ({data.get('hygiene', 100)}/{HYGIENE_MAX})", value=hygiene_bar, inline=False)

        player_jobs = await db.get_player_jobs(target.id)
        job_names = []
        for slot in [1, 2, 3]:
            pj = player_jobs.get(slot)
            if pj:
                j = JOBS.get(pj["job_id"], {})
                job_names.append(f"{j.get('name', pj['job_id'])} (Lv {pj['job_level']})")
        if job_names:
            embed.add_field(name="💼 Jobs", value="\n".join(job_names), inline=True)

        work_streak = data.get("work_streak", 0)
        best_grade = data.get("best_grade", "")
        if work_streak > 0 or best_grade:
            streak_text = f"🔥 {work_streak} shifts"
            if best_grade:
                streak_text += f" | Best: {best_grade}"
            embed.add_field(name="📊 Work Stats", value=streak_text, inline=True)

        boss_wins = data.get("boss_shifts_won", 0)
        if boss_wins > 0:
            embed.add_field(name="👹 Boss Wins", value=str(boss_wins), inline=True)

        # Job reputation summary
        from config.job_reputation import get_rep_tier
        all_job_rep = await db.get_all_job_reputation(target.id)
        if all_job_rep:
            top_rep = sorted(all_job_rep.items(), key=lambda x: x[1], reverse=True)[:2]
            rep_lines = []
            for cat_id, rep_val in top_rep:
                _, tier_name, tier_emoji, _ = get_rep_tier(rep_val)
                rep_lines.append(f"{tier_emoji} {tier_name} ({rep_val})")
            embed.add_field(name="💼 Job Rep", value="\n".join(rep_lines), inline=True)

        if data["pet_id"]:
            embed.add_field(name="🐾 Pet", value=f"{data['pet_id'].title()} ({data.get('pet_name', 'Unnamed')})", inline=True)
        if data["married_to"]:
            embed.add_field(name="💍 Married", value=f"<@{data['married_to']}>", inline=True)

        home = await db.get_home(target.id)
        if home:
            from config import HOUSING_TIERS
            tier = HOUSING_TIERS.get(home["tier_id"], {})
            ownership = "🏠 Owned" if home["ownership"] == "owned" else "🔑 Rented"
            embed.add_field(name="🏡 Home", value=f"{tier.get('name', 'Unknown')} ({ownership})", inline=True)

        embed.set_footer(text=f"Total Earned: {data['total_earned']:,} | Total Lost: {data['total_lost']:,}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="deposit", description="Deposit money into your bank")
    async def deposit(self, interaction: discord.Interaction, amount: str):
        data = await self.get_user(interaction)
        if amount.lower() == "all":
            amount = data["wallet"]
        else:
            try:
                amount = int(amount)
            except ValueError:
                await interaction.response.send_message(embed=error_embed("Invalid Amount", "Enter a valid number or 'all'."), ephemeral=True)
                return

        if amount <= 0:
            await interaction.response.send_message(embed=error_embed("Invalid Amount", "You must deposit a positive amount."), ephemeral=True)
            return

        if amount > data["wallet"]:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You only have {format_money(data['wallet'])} in your wallet."), ephemeral=True)
            return

        space = data["bank_capacity"] - data["bank"]
        if amount > space:
            await interaction.response.send_message(embed=error_embed("Bank Full", f"Your bank can only hold {format_money(space)} more."), ephemeral=True)
            return

        await db.update_user(interaction.user.id,
            wallet=data["wallet"] - amount,
            bank=data["bank"] + amount,
            total_deposited=data["total_deposited"] + amount,
        )
        await db.add_transaction(interaction.user.id, "deposit", amount, "Deposited to bank")
        await interaction.response.send_message(embed=success_embed("🏦 Deposit Successful", get_action_text("economy", "deposit", amount=format_money(amount), wallet=format_money(data['wallet'] - amount), bank=format_money(data['bank'] + amount))))

    @app_commands.command(name="withdraw", description="Withdraw money from your bank")
    async def withdraw(self, interaction: discord.Interaction, amount: str):
        data = await self.get_user(interaction)
        if amount.lower() == "all":
            amount = data["bank"]
        else:
            try:
                amount = int(amount)
            except ValueError:
                await interaction.response.send_message(embed=error_embed("Invalid Amount", "Enter a valid number or 'all'."), ephemeral=True)
                return

        if amount <= 0:
            await interaction.response.send_message(embed=error_embed("Invalid Amount", "You must withdraw a positive amount."), ephemeral=True)
            return

        if amount > data["bank"]:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You only have {format_money(data['bank'])} in your bank."), ephemeral=True)
            return

        await db.update_user(interaction.user.id,
            wallet=data["wallet"] + amount,
            bank=data["bank"] - amount,
        )
        await db.add_transaction(interaction.user.id, "withdraw", amount, "Withdrew from bank")
        await interaction.response.send_message(embed=success_embed("💸 Withdrawal Successful", get_action_text("economy", "withdraw", amount=format_money(amount), wallet=format_money(data['wallet'] + amount), bank=format_money(data['bank'] - amount))))

    @app_commands.command(name="pay", description="Pay another user from your wallet")
    async def pay(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if user.id == interaction.user.id:
            await interaction.response.send_message(embed=error_embed("Error", "You can't pay yourself."), ephemeral=True)
            return
        if user.bot:
            await interaction.response.send_message(embed=error_embed("Error", "You can't pay a bot."), ephemeral=True)
            return
        if amount <= 0:
            await interaction.response.send_message(embed=error_embed("Error", "Amount must be positive."), ephemeral=True)
            return

        data = await self.get_user(interaction)

        if await self.check_cooldown(interaction, "pay"):
            return

        if amount > data["wallet"]:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You only have {format_money(data['wallet'])} in your wallet."), ephemeral=True)
            return

        target_data = await db.get_or_create_user(user.id, interaction.guild.id if interaction.guild else 0)
        await db.update_user(interaction.user.id, wallet=data["wallet"] - amount, total_lost=data["total_lost"] + amount)
        await db.update_user(user.id, wallet=target_data["wallet"] + amount, total_earned=target_data["total_earned"] + amount)
        await db.add_transaction(interaction.user.id, "pay", amount, f"Paid to {user.name}")
        await db.add_transaction(user.id, "receive", amount, f"Received from {interaction.user.name}")
        await db.set_cooldown(interaction.user.id, "pay", 60)

        embed = success_embed("💸 Payment Successful", get_action_text("economy", "pay", payer=interaction.user.mention, recipient=user.mention, amount=format_money(amount)))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="leaderboard", description="View the top players")
    @app_commands.choices(category=[
        app_commands.Choice(name="💰 Wealth (Wallet)", value="wallet"),
        app_commands.Choice(name="🏦 Bank Balance", value="bank"),
        app_commands.Choice(name="📈 Level", value="level"),
        app_commands.Choice(name="🏆 Total Earned", value="total_earned"),
        app_commands.Choice(name="🎮 Games Won", value="games_won"),
        app_commands.Choice(name="💼 Work Count", value="work_count"),
        app_commands.Choice(name="⚔️ Pet Battles Won", value="battles_won"),
        app_commands.Choice(name="🎁 Gifts Given", value="gifts_given"),
        app_commands.Choice(name="📆 Daily Claims", value="daily_claims"),
        app_commands.Choice(name="📋 Quests Completed", value="quests_completed"),
        app_commands.Choice(name="🦹 Crimes Successful", value="crimes_successful"),
        app_commands.Choice(name="🔥 Daily Streak", value="daily_streak"),
    ])
    async def leaderboard(self, interaction: discord.Interaction, category: app_commands.Choice[str] = None):
        sort_by = category.value if category else "wallet"
        entries = await db.get_leaderboard(sort_by, 10)

        if not entries:
            await interaction.response.send_message(embed=error_embed("No Data", "No players found yet."))
            return

        medals = ["🥇", "🥈", "🥉"]
        lines = []
        for i, (uid, score) in enumerate(entries):
            medal = medals[i] if i < 3 else f"`#{i+1}`"
            label = format_money(score) if sort_by in ("wallet", "bank", "total_earned") else str(score)
            lines.append(f"{medal} <@{uid}> — **{label}**")

        title = f"🏆 Leaderboard — {category.name}" if category else "🏆 Leaderboard — Wealth"
        embed = info_embed(title, "\n".join(lines))
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="upgrade_bank", description="Upgrade your bank capacity (costs 1000 coins per 1000 capacity)")
    async def upgrade_bank(self, interaction: discord.Interaction):
        data = await self.get_user(interaction)

        if await self.check_cooldown(interaction, "upgrade_bank"):
            return

        cost = 1000
        if data["wallet"] < cost:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You need {format_money(cost)} to upgrade your bank."), ephemeral=True)
            return

        await db.update_user(interaction.user.id,
            wallet=data["wallet"] - cost,
            bank_capacity=data["bank_capacity"] + 1000,
            total_spent=data["total_spent"] + cost,
        )
        await db.add_transaction(interaction.user.id, "upgrade", cost, "Bank capacity upgrade")
        await db.set_cooldown(interaction.user.id, "upgrade_bank", 3600)
        await interaction.response.send_message(embed=success_embed("🏦 Bank Upgraded", get_action_text("economy", "upgrade_bank", capacity=format_money(data['bank_capacity'] + 1000))))


async def setup(bot):
    await bot.add_cog(Economy(bot))
