import discord
from discord import app_commands
from discord.ext import commands
import os
import aiohttp
import database as db
from utils.embeds import stats_bar, format_money, info_embed, success_embed, error_embed
from config import (
    HOUSING_TIERS, TOOLS, CLOTHING, POSSESSIONS, BUFF_TYPES,
    FACTIONS, TIME_PERIODS, WEATHER_STATES, JOBS,
)
from config.jobs import JOB_CATEGORIES

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "TishinaVC/lifebot")


class Core(commands.Cog):
    """Core commands: help, ping, profile, reset."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="View all available commands")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🤖 Lifebot Commands",
            description="A full-featured Discord economy & survival bot!",
            color=discord.Color.blurple(),
        )
        categories = {
            "💰 Economy": "`/balance` `/deposit` `/withdraw` `/pay` `/leaderboard` `/upgrade_bank`",
            "💼 Jobs (3 slots)": "`/jobs` `/job set` `/job view` `/job quit` `/work` `/coop` `/jobrep` — Browse categories → subcategories → jobs interactively! Co-op shifts, grades, streaks, boss shifts, and per-category reputation!",
            "🎰 Gambling": "`/coinflip` `/dice` `/slots` `/blackjack` `/higherlower` `/crash` `/horse_race` `/roulette` `/keno` `/lucky_wheel` `/plinko` `/overunder` `/mystery_box` `/poker`",
            "🛒 Store": "`/shop` `/buy` `/inventory` `/use` `/sell` `/collectibles` `/buy_equipment` `/sell_equipment` — Autocomplete for items!",
            "⛏️ Activities": "`/activity` (fish/mine/explore/forage/chop/dig) `/craft` `/craft_list`",
            "🎒 Equipment": "`/equipment` `/equip` `/unequip` `/discoveries`",
            "❤️ Survival": "`/status` `/hospital` `/heal` `/sleep` `/shower`",
            "🏠 Housing": "`/house` `/housing_list` `/buy_house` `/rent_house` `/pay_rent` `/sell_house` `/stop_renting` `/rest` `/upgrade_house` `/decorate` `/housing_market` `/buy_from_market` `/cancel_listing` `/store_item` `/retrieve_item` `/home_storage`",
            "🏆 Leveling": "`/rank` `/level_rewards`",
            "🎁 Daily": "`/daily` `/weekly`",
            "🦹 Crime": "`/crime` `/rob_user`",
            "💕 Social": "`/marry` `/divorce` `/relationship` `/gift`",
            "🐾 Pets": "`/pet` (shop/adopt/info/feed/play/battle/abandon)",
            "🏆 Achievements": "`/achievements`",
            "📊 RPG Stats": "`/stats view` `/stats train` `/school list` `/school enroll` `/qualifications`",
            "📋 Quests": "`/quests` `/quest_refresh` `/quest_claim`",
            "🌤️ Weather & Time": "`/weather` `/time`",
            "🗺️ World": "`/locations` `/travel` `/npc` (talk/trade/quest/complete) `/world` (overview/npc/location)",
            "🍳 Cooking & Buffs": "`/cook` `/cookbook` `/buffs`",
            "⚖️ Reputation": "`/reputation`",
            "👤 Profile": "`/profile` `/ping` `/reset` `/feedback`",
        }
        for category, commands_list in categories.items():
            embed.add_field(name=category, value=commands_list, inline=False)
        embed.set_footer(text="All commands are slash commands. Start typing / to see them!")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! Latency: {latency_ms}ms")

    @app_commands.command(name="profile", description="View your full profile")
    async def profile(self, interaction: discord.Interaction, user: discord.Member = None):
        target = user or interaction.user
        data = await db.get_or_create_user(target.id, interaction.guild.id if interaction.guild else 0)

        embed = discord.Embed(
            title=f"👤 {target.display_name}'s Profile",
            color=discord.Color.blurple(),
        )
        embed.set_thumbnail(url=target.display_avatar.url)

        embed.add_field(name="Level", value=str(data["level"]), inline=True)
        embed.add_field(name="XP", value=f"{data['xp']}", inline=True)
        player_jobs = await db.get_player_jobs(target.id)
        job_names = []
        for slot in [1, 2, 3]:
            pj = player_jobs.get(slot)
            if pj:
                j = JOBS.get(pj["job_id"], {})
                job_names.append(f"{j.get('name', pj['job_id'])} (Lv {pj['job_level']})")
        embed.add_field(name="💼 Jobs", value="\n".join(job_names) if job_names else "Unemployed", inline=True)
        embed.add_field(name="💰 Wallet", value=f"🪙 {data['wallet']:,}", inline=True)
        embed.add_field(name="🏦 Bank", value=f"🪙 {data['bank']:,}/{data['bank_capacity']:,}", inline=True)
        embed.add_field(name="🔥 Daily Streak", value=f"{data['daily_streak']} days", inline=True)

        work_streak = data.get("work_streak", 0)
        best_grade = data.get("best_grade", "")
        grade_display = f"🔥 {work_streak} shifts"
        if best_grade:
            grade_display += f" | Best: {best_grade}"
        embed.add_field(name="💼 Work Streak", value=grade_display, inline=True)

        boss_wins = data.get("boss_shifts_won", 0)
        if boss_wins > 0:
            embed.add_field(name="👹 Boss Shifts Won", value=str(boss_wins), inline=True)

        # Job reputation (show top categories)
        from config.job_reputation import get_rep_tier
        all_job_rep = await db.get_all_job_reputation(target.id)
        if all_job_rep:
            rep_lines = []
            for cat_id, rep_val in sorted(all_job_rep.items(), key=lambda x: x[1], reverse=True)[:3]:
                _, tier_name, tier_emoji, _ = get_rep_tier(rep_val)
                cat_data = JOB_CATEGORIES.get(cat_id, {})
                cat_emoji = cat_data.get("emoji", "")
                rep_lines.append(f"{cat_emoji} {tier_emoji} {tier_name} ({rep_val})")
            embed.add_field(name="💼 Job Rep", value="\n".join(rep_lines), inline=True)

        embed.add_field(name=f"❤️ Health {stats_bar(data['health'], 100)}", value=f"{data['health']}/100", inline=True)
        embed.add_field(name=f"🍖 Hunger {stats_bar(data['hunger'], 100)}", value=f"{data['hunger']}/100", inline=True)
        embed.add_field(name=f"💧 Thirst {stats_bar(data['thirst'], 100)}", value=f"{data['thirst']}/100", inline=True)
        embed.add_field(name=f"⚡ Energy {stats_bar(data.get('energy', 100), 100)}", value=f"{data.get('energy', 100)}/100", inline=True)
        embed.add_field(name=f"🧼 Hygiene {stats_bar(data.get('hygiene', 100), 100)}", value=f"{data.get('hygiene', 100)}/100", inline=True)

        home = await db.get_home(target.id)
        if home:
            tier = HOUSING_TIERS.get(home["tier_id"], {})
            ownership_icon = "🏠" if home["ownership"] == "owned" else "🔑"
            embed.add_field(name="🏠 Home", value=f"{ownership_icon} {tier.get('name', home['tier_id'])}", inline=True)

        equipped = await db.get_equipped(target.id)
        if equipped:
            equip_names = []
            for item in equipped:
                item_data = TOOLS.get(item["item_id"], CLOTHING.get(item["item_id"], POSSESSIONS.get(item["item_id"], {})))
                name = item_data.get("name", item["item_id"])
                equip_names.append(f"{name}")
            embed.add_field(name="🎒 Equipped", value=", ".join(equip_names[:5]), inline=False)

        buffs = await db.get_buffs(target.id)
        if buffs:
            buff_names = []
            for b in buffs:
                btype = BUFF_TYPES.get(b["buff_stat"], {})
                buff_names.append(f"{btype.get('name', b['buff_name'])} ({b['buff_value']:+.2f})")
            embed.add_field(name="✨ Active Buffs", value=", ".join(buff_names[:5]), inline=False)

        rep_data = await db.get_all_reputation(target.id)
        if rep_data:
            rep_str = ", ".join(f"{FACTIONS.get(f, {}).get('emoji', '')} {r}" for f, r in rep_data.items())
            embed.add_field(name="⚖️ Reputation", value=rep_str, inline=False)

        if data.get("married_to"):
            embed.add_field(name="💍 Married", value=f"<@{data['married_to']}>", inline=True)
        if data.get("pet_id"):
            embed.add_field(name="🐾 Pet", value=data.get("pet_name", "Unknown"), inline=True)

        gt = await db.get_game_time()
        weather = await db.get_weather()
        period = TIME_PERIODS.get(gt["time_period"], {})
        wdata = WEATHER_STATES.get(weather, {})
        embed.add_field(name="🕐 Time", value=f"{period.get('name', '?')} (Hr {gt['game_hour']})", inline=True)
        embed.add_field(name="🌤️ Weather", value=wdata.get("name", weather), inline=True)

        import world as world_engine
        market = await world_engine.get_market_state()
        if market:
            demand = market.get("demand", 0.5)
            _, demand_lbl = world_engine.demand_label(demand)
            embed.add_field(name="🌍 World", value=f"Market: {demand_lbl}", inline=True)

        embed.set_footer(text=f"Total Earned: 🪙{data['total_earned']:,} | Total Lost: 🪙{data['total_lost']:,}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="reset", description="Reset your account (WARNING: irreversible!)")
    async def reset_account(self, interaction: discord.Interaction):
        view = discord.ui.View(timeout=30)

        async def confirm_callback(interaction2: discord.Interaction):
            if interaction2.user.id != interaction.user.id:
                await interaction2.response.send_message("This isn't your confirmation button!", ephemeral=True)
                return
            await db.reset_user(interaction.user.id)
            await interaction2.response.edit_message(
                content="✅ Your account has been reset. Use commands to start fresh!",
                view=None,
            )

        async def cancel_callback(interaction2: discord.Interaction):
            if interaction2.user.id != interaction.user.id:
                await interaction2.response.send_message("This isn't your cancel button!", ephemeral=True)
                return
            await interaction2.response.edit_message(content="❌ Reset cancelled.", view=None)

        confirm_btn = discord.ui.Button(label="Confirm Reset", style=discord.ButtonStyle.danger)
        cancel_btn = discord.ui.Button(label="Cancel", style=discord.ButtonStyle.secondary)
        confirm_btn.callback = confirm_callback
        cancel_btn.callback = cancel_callback
        view.add_item(confirm_btn)
        view.add_item(cancel_btn)

        await interaction.response.send_message(
            content=f"⚠️ **WARNING**: This will permanently delete all your progress including money, level, items, pets, and stats. Are you sure?",
            view=view,
        )

    # ─── /feedback — Submit anonymous feedback as a GitHub issue ───
    @app_commands.command(name="feedback", description="Submit anonymous feedback or a feature request")
    @app_commands.describe(feedback="Your feedback or feature request (no personal info needed)")
    async def feedback(self, interaction: discord.Interaction, feedback: str):
        if len(feedback) < 5:
            await interaction.response.send_message(
                embed=error_embed("Too Short", "Please provide at least a few words of feedback."),
                ephemeral=True,
            )
            return
        if len(feedback) > 1000:
            await interaction.response.send_message(
                embed=error_embed("Too Long", "Please keep feedback under 1000 characters."),
                ephemeral=True,
            )
            return

        await interaction.response.defer(ephemeral=True)

        if not GITHUB_TOKEN:
            await interaction.followup.send(
                embed=error_embed("Not Configured", "Feedback is not set up yet. Contact the bot owner."),
                ephemeral=True,
            )
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://api.github.com/repos/{GITHUB_REPO}/issues",
                    headers={
                        "Authorization": f"token {GITHUB_TOKEN}",
                        "Accept": "application/vnd.github.v3+json",
                    },
                    json={
                        "title": f"User Feedback: {feedback[:80]}{'...' if len(feedback) > 80 else ''}",
                        "body": f"**Feedback submitted via `/feedback` command**\n\n> {feedback}\n\n---\n_Submitted anonymously from Discord_",
                        "labels": ["user-feedback"],
                    },
                ) as resp:
                    if resp.status == 201:
                        data = await resp.json()
                        issue_url = data.get("html_url", "")
                        await interaction.followup.send(
                            embed=success_embed(
                                "✅ Feedback Submitted",
                                f"Thank you! Your feedback has been recorded. The developers will review it.\n\n[View on GitHub]({issue_url})",
                            ),
                            ephemeral=True,
                        )
                    else:
                        await interaction.followup.send(
                            embed=error_embed("Error", "Could not submit feedback. Please try again later."),
                            ephemeral=True,
                        )
        except Exception as e:
            await interaction.followup.send(
                embed=error_embed("Error", f"Something went wrong: {e}"),
                ephemeral=True,
            )


async def setup(bot):
    await bot.add_cog(Core(bot))
