"""
Co-op job shifts — multiplayer work minigames with team bonuses.
/coop start — start a co-op shift (others can join)
/coop join — join an open co-op shift
"""
import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random
import time
import database as db
from utils.embeds import success_embed, error_embed, info_embed, format_money, themed_embed
from utils.helpers import job_pay, check_level_up, xp_for_next_level, clamp, pet_bonus, stat_modifier, get_housing_bonus
from config import JOBS, JOB_CATEGORIES, ACHIEVEMENTS
from config.shift_features import get_grade, is_grade_better, GRADE_ORDER, get_streak_multiplier, STREAK_GRADE_THRESHOLD, apply_difficulty
from config.job_reputation import get_rep_tier, get_rep_gain
from config.coop import COOP_MAX_PLAYERS, COOP_JOIN_TIMEOUT, COOP_MIN_PLAYERS, COOP_TEAM_BONUS, COOP_EVENTS, COOP_EVENT_CHANCE, COOP_ALL_GOOD_BONUS, COOP_FAIL_PENALTY
from cogs.minigames import run_minigame, get_minigame_type
from utils.narrative import get_action_text


class CoopShift:
    """Tracks an open co-op shift session."""
    def __init__(self, host_id: int, host_name: str, job_id: str, slot_num: int, channel_id: int):
        self.host_id = host_id
        self.host_name = host_name
        self.job_id = job_id
        self.slot_num = slot_num
        self.channel_id = channel_id
        self.players = [(host_id, host_name, slot_num)]  # list of (user_id, display_name, slot_num)
        self.created_at = time.time()
        self.started = False

    @property
    def is_full(self) -> bool:
        return len(self.players) >= COOP_MAX_PLAYERS

    @property
    def is_expired(self) -> bool:
        return time.time() - self.created_at > COOP_JOIN_TIMEOUT


# Active co-op sessions keyed by channel_id
_active_coop: dict[int, CoopShift] = {}


class CoopJobs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="coop", description="Start or join a co-op job shift for team bonuses!")
    @app_commands.choices(action=[
        app_commands.Choice(name="Start a co-op shift", value="start"),
        app_commands.Choice(name="Join a co-op shift", value="join"),
    ])
    async def coop(self, interaction: discord.Interaction, action: app_commands.Choice[str]):
        if action.value == "start":
            await self._start_coop(interaction)
        else:
            await self._join_coop(interaction)

    async def _start_coop(self, interaction: discord.Interaction):
        channel_id = interaction.channel_id
        if channel_id in _active_coop and not _active_coop[channel_id].is_expired:
            await interaction.response.send_message(
                embed=error_embed("Co-op Active", f"There's already a co-op shift open in this channel! Use `/coop join` to join {_active_coop[channel_id].host_name}'s shift."),
                ephemeral=True,
            )
            return

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        player_jobs = await db.get_player_jobs(interaction.user.id)
        filled = {s: pj for s, pj in player_jobs.items() if pj}
        if not filled:
            await interaction.response.send_message(
                embed=error_embed("No Job", "You need a job first! Use `/jobs` to browse and `/job set` to choose one."),
                ephemeral=True,
            )
            return

        # If multiple jobs, ask which slot; if 1, use it
        if len(filled) > 1:
            slot_num = list(filled.keys())[0]  # default to first filled slot for co-op
        else:
            slot_num = list(filled.keys())[0]

        pj = player_jobs[slot_num]
        job_id = pj["job_id"]
        if job_id not in JOBS:
            await interaction.response.send_message(embed=error_embed("Job Error", "Your job was invalid."), ephemeral=True)
            return

        job = JOBS[job_id]
        cd = await db.check_cooldown(interaction.user.id, f"work_{slot_num}")
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            await interaction.response.send_message(
                embed=error_embed("On Cooldown", f"Still tired from your last shift. Try again in {mins}m {secs}s."),
                ephemeral=True,
            )
            return

        if data["health"] <= 10 or data["hunger"] <= 5 or data["thirst"] <= 5:
            await interaction.response.send_message(
                embed=error_embed("Not Ready", "Your stats are too low to work! Eat, drink, and heal first."),
                ephemeral=True,
            )
            return

        # Set cooldown immediately to prevent double-work during join window
        await db.set_cooldown(interaction.user.id, f"work_{slot_num}", job["cooldown"])

        shift = CoopShift(interaction.user.id, interaction.user.display_name, job_id, slot_num, channel_id)
        _active_coop[channel_id] = shift

        embed = themed_embed(
            "🤝 Co-op Shift Started!",
            f"**{interaction.user.display_name}** is hosting a co-op **{job['name']}** shift!\n\nUse `/coop join` to join the team!\n\n⏱️ Join window: {COOP_JOIN_TIMEOUT}s\n👥 Max players: {COOP_MAX_PLAYERS}\n💰 Team bonus applies to everyone!",
            category=job.get("category"),
        )
        embed.add_field(name="Host", value=interaction.user.display_name, inline=True)
        embed.add_field(name="Job", value=job["name"], inline=True)
        embed.add_field(name="Players", value=f"1/{COOP_MAX_PLAYERS}", inline=True)
        await interaction.response.send_message(embed=embed)

        # Wait for join window
        await asyncio.sleep(COOP_JOIN_TIMEOUT)

        if shift.started:
            return  # already started

        # Time's up — start the shift
        if len(shift.players) < COOP_MIN_PLAYERS:
            del _active_coop[channel_id]
            await interaction.followup.send(
                embed=error_embed("Co-op Cancelled", f"Not enough players joined (need {COOP_MIN_PLAYERS}). The co-op shift was cancelled."),
            )
            return

        await self._run_coop_shift(interaction, shift)

    async def _join_coop(self, interaction: discord.Interaction):
        channel_id = interaction.channel_id
        if channel_id not in _active_coop or _active_coop[channel_id].is_expired:
            await interaction.response.send_message(
                embed=error_embed("No Co-op Shift", "There's no active co-op shift in this channel. Use `/coop start` to begin one!"),
                ephemeral=True,
            )
            return

        shift = _active_coop[channel_id]
        if shift.started:
            await interaction.response.send_message(
                embed=error_embed("Already Started", "This co-op shift has already begun!"),
                ephemeral=True,
            )
            return

        if shift.host_id == interaction.user.id:
            await interaction.response.send_message(
                embed=error_embed("Already In", "You're already the host of this co-op shift!"),
                ephemeral=True,
            )
            return

        if any(p[0] == interaction.user.id for p in shift.players):
            await interaction.response.send_message(
                embed=error_embed("Already Joined", "You've already joined this co-op shift!"),
                ephemeral=True,
            )
            return

        if shift.is_full:
            await interaction.response.send_message(
                embed=error_embed("Full", "This co-op shift is already full!"),
                ephemeral=True,
            )
            return

        # Check the joining player has the same job and stats
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        player_jobs = await db.get_player_jobs(interaction.user.id)
        filled = {s: pj for s, pj in player_jobs.items() if pj}
        if not filled:
            await interaction.response.send_message(
                embed=error_embed("No Job", "You need a job to join a co-op shift! Use `/job set` first."),
                ephemeral=True,
            )
            return

        # Find the slot that has the same job as the host
        joiner_slot = None
        for s, pj in filled.items():
            if pj["job_id"] == shift.job_id:
                joiner_slot = s
                break
        if joiner_slot is None:
            job_name = JOBS.get(shift.job_id, {}).get("name", shift.job_id)
            await interaction.response.send_message(
                embed=error_embed("Wrong Job", f"You need to have the same job (**{job_name}**) to join this co-op shift!"),
                ephemeral=True,
            )
            return

        # Check work cooldown for the joiner's slot
        cd = await db.check_cooldown(interaction.user.id, f"work_{joiner_slot}")
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            await interaction.response.send_message(
                embed=error_embed("On Cooldown", f"Still tired from your last shift. Try again in {mins}m {secs}s."),
                ephemeral=True,
            )
            return

        if data["health"] <= 10 or data["hunger"] <= 5 or data["thirst"] <= 5:
            await interaction.response.send_message(
                embed=error_embed("Not Ready", "Your stats are too low to work!"),
                ephemeral=True,
            )
            return

        # Set cooldown immediately to prevent double-work during join window
        await db.set_cooldown(interaction.user.id, f"work_{joiner_slot}", JOBS[shift.job_id]["cooldown"])

        shift.players.append((interaction.user.id, interaction.user.display_name, joiner_slot))

        embed = success_embed(
            "Joined Co-op Shift!",
            f"**{interaction.user.display_name}** joined the co-op **{JOBS[shift.job_id]['name']}** shift!\nPlayers: {len(shift.players)}/{COOP_MAX_PLAYERS}",
        )
        await interaction.response.send_message(embed=embed)

        if shift.is_full:
            # Start immediately if full
            shift.started = True
            await self._run_coop_shift(interaction, shift)

    async def _run_coop_shift(self, interaction: discord.Interaction, shift: CoopShift):
        shift.started = True
        job = JOBS[shift.job_id]
        mg_type = get_minigame_type(shift.job_id)

        # Roll co-op event
        coop_event = None
        if random.random() < COOP_EVENT_CHANCE:
            coop_event = random.choice(COOP_EVENTS)

        intro = f"🤝 **Co-op Shift Starting!**\n**{job['name']}** — {mg_type}\nPlayers: {', '.join(p[1] for p in shift.players)}"
        if coop_event:
            intro += f"\n\n{coop_event['name']} — {coop_event['description']}"

        await interaction.followup.send(embed=themed_embed("🤝 Co-op Shift", intro, category=job.get("category")))

        # Each player plays the minigame
        results = []
        for user_id, user_name, _slot in shift.players:
            await interaction.followup.send(embed=info_embed("Co-op Shift", f"**{user_name}**'s turn!"))
            perf = await run_minigame(interaction, shift.job_id, user_id)
            results.append((user_id, user_name, perf))

        # Clean up active session
        if shift.channel_id in _active_coop:
            del _active_coop[shift.channel_id]

        # Calculate team results
        valid_perfs = [p for _, _, p in results if p > 0]
        any_failed = len(valid_perfs) < len(results)
        all_good = all(get_grade(apply_difficulty(p, 1))[0] in ("S", "A", "B") for _, _, p in results if p > 0) and not any_failed

        team_bonus = COOP_TEAM_BONUS.get(len(results), 1.0)
        if all_good:
            team_bonus *= COOP_ALL_GOOD_BONUS
        if any_failed:
            team_bonus *= COOP_FAIL_PENALTY

        event_pay_mult = coop_event["pay_mult"] if coop_event else 1.0
        event_xp_mult = coop_event["xp_mult"] if coop_event else 1.0

        # Build result embed
        embed = themed_embed("🤝 Co-op Results!", "All players have completed the shift!", category=job.get("category"))
        embed.add_field(name="Team Size", value=str(len(results)), inline=True)
        embed.add_field(name="Team Bonus", value=f"+{int((team_bonus - 1) * 100)}%", inline=True)
        if coop_event:
            embed.add_field(name="Event", value=coop_event["name"], inline=True)

        # Process each player's rewards
        # Map user_id → slot_num for cooldown setting
        player_slots = {p[0]: p[2] for p in shift.players}

        for user_id, user_name, perf in results:
            if perf <= 0:
                embed.add_field(name=f"{user_name}", value="❌ Failed — no rewards", inline=False)
                continue

            # Get player data
            pdata = await db.get_or_create_user(user_id, 0)
            pplayer_jobs = await db.get_player_jobs(user_id)
            pslot = player_slots.get(user_id, shift.slot_num)
            ppj = pplayer_jobs.get(pslot)
            if not ppj:
                embed.add_field(name=f"{user_name}", value="❌ No job found", inline=False)
                continue

            pjob_level = ppj["job_level"]
            perf = apply_difficulty(perf, pjob_level)
            grade_letter, grade_emoji, grade_comment = get_grade(perf)

            # Streak
            current_streak = pdata.get("work_streak", 0)
            grade_rank = GRADE_ORDER.get(grade_letter, 0)
            streak_threshold_rank = GRADE_ORDER.get(STREAK_GRADE_THRESHOLD, 0)
            new_streak = current_streak + 1 if grade_rank >= streak_threshold_rank else 0
            streak_mult, streak_desc = get_streak_multiplier(new_streak)

            # Pay calculation
            base_pay = pet_bonus(pdata.get("pet_id"), "pay", job_pay(job["base_pay"], pjob_level, perf))
            mods = stat_modifier(pdata, "work")
            housing = await get_housing_bonus(user_id)
            from config import WEATHER_STATES
            current_weather = await db.get_weather()
            weather_pay_mult = WEATHER_STATES.get(current_weather, {}).get("effects", {}).get("work_pay_mult", 1.0)
            time_effects = await db.get_time_effects()
            time_pay_mult = time_effects.get("work_pay", 1.0)
            buff_pay_mult = await db.get_buff_mult(user_id, "work_pay")
            job_category = job.get("category", "entry")
            rep_benefits = await db.get_job_rep_benefits(user_id, job_category)

            pay = int(base_pay * mods["pay_mult"] * housing["pay_mult"] * weather_pay_mult * time_pay_mult * buff_pay_mult * streak_mult * team_bonus * event_pay_mult * rep_benefits.get("pay_mult", 1.0))
            xp_gain = int(pet_bonus(pdata.get("pet_id"), "xp", int(25 * perf)) * mods["xp_mult"] * housing["xp_mult"] * event_xp_mult * team_bonus * rep_benefits.get("xp_mult", 1.0))
            job_xp_gain = int(15 * perf * mods["xp_mult"] * housing["xp_mult"] * event_xp_mult * rep_benefits.get("xp_mult", 1.0))
            stat_cost = mods["stat_cost_mult"] * rep_benefits.get("stat_cost_mult", 1.0)

            new_xp = pdata["xp"] + xp_gain
            new_level, leveled_up = check_level_up(new_xp, pdata["level"])
            if leveled_up:
                new_xp = new_xp - sum(xp_for_next_level(l) for l in range(pdata["level"], new_level))

            new_job_xp = ppj["job_xp"] + job_xp_gain
            new_job_level = ppj["job_level"]
            while new_job_xp >= 500 * new_job_level:
                new_job_xp -= 500 * new_job_level
                new_job_level += 1

            update_fields = {
                "wallet": pdata["wallet"] + pay,
                "xp": new_xp,
                "level": new_level,
                "work_count": pdata["work_count"] + 1,
                "total_earned": pdata["total_earned"] + pay,
                "hunger": clamp(pdata["hunger"] - int(5 * stat_cost)),
                "thirst": clamp(pdata["thirst"] - int(5 * stat_cost)),
                "energy": clamp(pdata.get("energy", 100) - int(10 * stat_cost)),
                "health": clamp(pdata["health"] - int(2 * stat_cost)),
                "work_streak": new_streak,
            }
            best_grade = pdata.get("best_grade", "")
            if is_grade_better(grade_letter, best_grade):
                update_fields["best_grade"] = grade_letter

            await db.update_user(user_id, **update_fields)
            await db.update_job_xp(user_id, pslot, new_job_xp, new_job_level)
            await db.add_transaction(user_id, "work", pay, f"Co-op work as {job['name']}")
            await db.update_quest_progress(user_id, "work", 1)
            await db.update_quest_progress(user_id, "earn", pay)
            await db.update_quest_progress(user_id, "coop", 1)

            # Job reputation
            rep_gain = get_rep_gain(grade_letter, False, new_streak)
            if rep_gain > 0:
                await db.add_job_reputation(user_id, job_category, rep_gain)

            result_text = f"{grade_emoji} **{grade_letter}** — {int(perf*100)}% | {format_money(pay)} | +{xp_gain} XP"
            if streak_mult > 1.0:
                result_text += f" | 🔥{new_streak}"
            embed.add_field(name=user_name, value=result_text, inline=False)

        # Check achievements for all participants and credit rewards
        for user_id, _, _ in results:
            new_achs = await db.check_achievements(user_id)
            if new_achs:
                ach_reward = sum(ACHIEVEMENTS.get(a, {}).get("reward", 0) for a in new_achs)
                if ach_reward > 0:
                    adata = await db.get_or_create_user(user_id, 0)
                    await db.update_user(user_id, wallet=adata["wallet"] + ach_reward, total_earned=adata["total_earned"] + ach_reward)
                for ach_id in new_achs:
                    ach = ACHIEVEMENTS.get(ach_id, {})
                    embed.add_field(name="Achievement Unlocked!", value=f"{ach.get('emoji', '🏆')} **{ach.get('name', ach_id)}** — {format_money(ach.get('reward', 0))} reward!", inline=False)

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CoopJobs(bot))
