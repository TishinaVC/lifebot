import discord
from discord import app_commands
from discord.ext import commands
import random
import asyncio
import database as db
from utils.embeds import success_embed, error_embed, info_embed, format_money, themed_embed
from utils.helpers import job_pay, check_level_up, xp_for_next_level, clamp, pet_bonus, stat_modifier, get_housing_bonus
from config import JOBS, JOB_CATEGORIES, ACHIEVEMENTS, QUALIFICATIONS, STATS, STAT_KEYS
from config.jobs import JOB_SUBCATEGORIES, get_jobs_by_category, get_subcategories
from config.job_requirements import JOB_REQUIREMENTS
from utils.narrative import get_action_text
from cogs.minigames import run_minigame, get_minigame_type
from config.shift_features import (
    get_grade, is_grade_better, GRADE_ORDER,
    get_streak_multiplier, STREAK_GRADE_THRESHOLD,
    roll_shift_event, apply_difficulty, roll_boss_shift, BOSS_SHIFT_CONFIG,
)
from config.job_reputation import get_rep_tier, get_rep_gain


def _format_stat_reqs(stat_reqs: dict) -> str:
    if not stat_reqs:
        return "None"
    return ", ".join(f"{STATS.get(s, {}).get('short', s)} >= {v}" for s, v in stat_reqs.items())


def _format_qual_reqs(qual_reqs: list) -> str:
    if not qual_reqs:
        return "None"
    return ", ".join(QUALIFICATIONS.get(q, {}).get("name", q) for q in qual_reqs)


_SLOT_CHOICES = [
    app_commands.Choice(name="Slot 1", value="1"),
    app_commands.Choice(name="Slot 2", value="2"),
    app_commands.Choice(name="Slot 3", value="3"),
]


# ═══════════════════════════════════════════════════════════════
# Interactive Views — category → subcategory → job navigation
# Uses discord.ui.Select menus (25 options each) chained together,
# bypassing Discord's 25-choice slash command limit entirely.
# ═══════════════════════════════════════════════════════════════

class JobNavView(discord.ui.View):
    """Interactive navigation view for browsing and setting jobs.

    Flow: category select → subcategory select → job list (embed)
          In 'set' mode: → job select → slot buttons → _do_set_job
    """

    def __init__(self, cog, user_id: int, guild_id: int, mode: str = "browse"):
        super().__init__(timeout=180)
        self.cog = cog
        self.user_id = user_id
        self.guild_id = guild_id
        self.mode = mode
        self.category = None
        self.subcategory = None
        self._add_category_select()

    def _add_category_select(self):
        self.clear_items()
        cat_select = discord.ui.Select(
            placeholder="Choose a job category...",
            min_values=1, max_values=1,
            options=[
                discord.SelectOption(
                    label=v["name"], value=k,
                    description=v.get("description", "")[:100],
                )
                for k, v in JOB_CATEGORIES.items()
            ]
        )
        cat_select.callback = self._on_category
        self.add_item(cat_select)

    def _add_subcategory_select(self):
        self.clear_items()
        subs = get_subcategories(self.category)
        sub_select = discord.ui.Select(
            placeholder=f"Choose a subcategory in {JOB_CATEGORIES[self.category]['name']}...",
            min_values=1, max_values=1,
            options=[
                discord.SelectOption(
                    label=v["name"], value=k,
                    description=v.get("description", "")[:100],
                )
                for k, v in subs.items()
            ]
        )
        sub_select.callback = self._on_subcategory
        self.add_item(sub_select)
        back_btn = discord.ui.Button(label="← Back", style=discord.ButtonStyle.secondary)
        back_btn.callback = self._back_to_categories
        self.add_item(back_btn)

    async def _on_category(self, interaction: discord.Interaction):
        self.category = interaction.data["values"][0]
        self._add_subcategory_select()
        await interaction.response.edit_message(
            content=f"**{JOB_CATEGORIES[self.category]['name']}** — Choose a subcategory:",
            embed=None, view=self,
        )

    async def _on_subcategory(self, interaction: discord.Interaction):
        self.subcategory = interaction.data["values"][0]
        await self._show_jobs(interaction)

    async def _show_jobs(self, interaction: discord.Interaction):
        jobs = get_jobs_by_category(self.category, self.subcategory)
        if not jobs:
            await interaction.response.edit_message(content="No jobs in this subcategory.", embed=None, view=None)
            return

        cat_info = JOB_CATEGORIES.get(self.category, {})
        sub_info = get_subcategories(self.category).get(self.subcategory, {})
        embed = info_embed(
            f"{cat_info.get('name', '')} → {sub_info.get('name', '')}",
            sub_info.get("description", ""),
        )

        player_jobs = await db.get_player_jobs(self.user_id)
        current_ids = {j["job_id"] for j in player_jobs.values() if j}
        data = await db.get_or_create_user(self.user_id, self.guild_id)

        for jid, job in jobs.items():
            reqs = JOB_REQUIREMENTS.get(jid, {})
            stat_reqs = reqs.get("stat_reqs", {})
            qual_reqs = reqs.get("qual_reqs", [])
            games = reqs.get("minigames", [reqs.get("minigame", "quick_pick")])
            mg_display = " / ".join(games)
            locked = "\U0001F512" if data["level"] < job["min_level"] else "\u2705"
            equipped = " \U0001F4CC" if jid in current_ids else ""
            embed.add_field(
                name=f"{locked}{equipped} {job['name']}",
                value=(
                    f"Pay: {format_money(job['base_pay'])} | Min Lv: {job['min_level']} | "
                    f"CD: {job['cooldown']//60}min | Games: {mg_display}\n"
                    f"Stats: {_format_stat_reqs(stat_reqs)} | Quals: {_format_qual_reqs(qual_reqs)}\n"
                    f"{job['description']}"
                ),
                inline=False,
            )

        self.clear_items()

        if self.mode == "set":
            job_select = discord.ui.Select(
                placeholder="Choose a job to set...",
                min_values=1, max_values=1,
                options=[
                    discord.SelectOption(
                        label=job["name"], value=jid,
                        description=f"{format_money(job['base_pay'])}/shift - Min Lv {job['min_level']}"[:100],
                    )
                    for jid, job in list(jobs.items())[:25]
                ],
            )
            job_select.callback = self._on_job_select
            self.add_item(job_select)

        back_btn = discord.ui.Button(label="← Back to Subcategories", style=discord.ButtonStyle.secondary)
        back_btn.callback = self._back_to_subcategories
        self.add_item(back_btn)

        await interaction.response.edit_message(embed=embed, content=None, view=self)

    async def _on_job_select(self, interaction: discord.Interaction):
        job_id = interaction.data["values"][0]
        job = JOBS.get(job_id, {})

        self.clear_items()
        slot1_btn = discord.ui.Button(label="Slot 1", style=discord.ButtonStyle.primary)
        slot1_btn.callback = lambda i, jid=job_id: self._on_slot(i, jid, 1)
        self.add_item(slot1_btn)

        slot2_btn = discord.ui.Button(label="Slot 2", style=discord.ButtonStyle.primary)
        slot2_btn.callback = lambda i, jid=job_id: self._on_slot(i, jid, 2)
        self.add_item(slot2_btn)

        slot3_btn = discord.ui.Button(label="Slot 3", style=discord.ButtonStyle.primary)
        slot3_btn.callback = lambda i, jid=job_id: self._on_slot(i, jid, 3)
        self.add_item(slot3_btn)

        cancel_btn = discord.ui.Button(label="Cancel", style=discord.ButtonStyle.danger)
        cancel_btn.callback = self._cancel
        self.add_item(cancel_btn)

        await interaction.response.edit_message(
            content=f"Set **{job.get('name', job_id)}** to which slot?",
            embed=None, view=self,
        )

    async def _on_slot(self, interaction: discord.Interaction, job_id: str, slot: int):
        self.stop()
        await self.cog._do_set_job_response(interaction, job_id, slot)

    async def _back_to_categories(self, interaction: discord.Interaction):
        self.category = None
        self.subcategory = None
        self._add_category_select()
        await interaction.response.edit_message(
            content="**Browse Jobs** — Choose a category to explore:",
            embed=None, view=self,
        )

    async def _back_to_subcategories(self, interaction: discord.Interaction):
        self.subcategory = None
        self._add_subcategory_select()
        await interaction.response.edit_message(
            content=f"**{JOB_CATEGORIES[self.category]['name']}** — Choose a subcategory:",
            embed=None, view=self,
        )

    async def _cancel(self, interaction: discord.Interaction):
        self.stop()
        await interaction.response.edit_message(content="Cancelled.", embed=None, view=None)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your menu!", ephemeral=True)
            return False
        return True


class Jobs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="jobs", description="Browse all available jobs — interactive category navigation")
    async def jobs_list(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id if interaction.guild else 0
        view = JobNavView(self, interaction.user.id, guild_id, mode="browse")
        await interaction.response.send_message(
            content="**Browse Jobs** — Choose a category to explore:",
            view=view,
        )

    job_group = app_commands.Group(name="job", description="View, set, or quit your jobs (3-slot system)")

    @job_group.command(name="view", description="View your current jobs (all slots)")
    async def job_view(self, interaction: discord.Interaction):
        player_jobs = await db.get_player_jobs(interaction.user.id)
        embed = info_embed("Your Jobs", "You can hold up to 3 jobs simultaneously. Each shift randomly picks one of 3 minigames!")
        for slot in [1, 2, 3]:
            pj = player_jobs.get(slot)
            if pj:
                job = JOBS.get(pj["job_id"], {})
                reqs = JOB_REQUIREMENTS.get(pj["job_id"], {})
                games = reqs.get("minigames", [reqs.get("minigame", "quick_pick")])
                mg_display = " / ".join(games)
                xp_needed = 500 * pj["job_level"]
                embed.add_field(
                    name=f"Slot {slot}: {job.get('name', pj['job_id'])} (Lv {pj['job_level']})",
                    value=f"Pay: {format_money(job.get('base_pay', 0))} | XP: {pj['job_xp']}/{xp_needed} | Games: {mg_display}\n{job.get('description', '')}",
                    inline=False,
                )
            else:
                embed.add_field(name=f"Slot {slot}: Empty", value="Use `/job set` to choose a job.", inline=False)
        await interaction.response.send_message(embed=embed)

    @job_group.command(name="set", description="Set a job — interactive category → subcategory → job selection")
    async def job_set(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id if interaction.guild else 0
        view = JobNavView(self, interaction.user.id, guild_id, mode="set")
        await interaction.response.send_message(
            content="**Set a Job** — Choose a category to find a job:",
            view=view,
        )

    @job_group.command(name="quit", description="Quit a job from a specific slot")
    @app_commands.choices(slot=_SLOT_CHOICES)
    async def job_quit(self, interaction: discord.Interaction, slot: app_commands.Choice[str]):
        slot_num = int(slot.value)
        player_jobs = await db.get_player_jobs(interaction.user.id)
        pj = player_jobs.get(slot_num)
        if not pj:
            await interaction.response.send_message(embed=error_embed("Empty Slot", f"Slot {slot_num} is already empty."), ephemeral=True)
            return
        job = JOBS.get(pj["job_id"], {})
        await db.quit_player_job(interaction.user.id, slot_num)
        await interaction.response.send_message(embed=success_embed("Job Quit", f"You quit **{job.get('name', pj['job_id'])}** from slot {slot_num}.\n{get_action_text('misc', 'job_quit')}"))

    async def _do_set_job_response(self, interaction: discord.Interaction, job_id: str, slot: int):
        """Handle job assignment from the interactive JobNavView."""
        guild_id = interaction.guild.id if interaction.guild else 0
        data = await db.get_or_create_user(interaction.user.id, guild_id)
        if job_id not in JOBS:
            await interaction.response.send_message(embed=error_embed("Invalid Job", "That job doesn't exist."), ephemeral=True)
            return
        job = JOBS[job_id]
        if data["level"] < job["min_level"]:
            await interaction.response.send_message(embed=error_embed("Level Too Low", f"You need **level {job['min_level']}** to work as a {job['name']}."), ephemeral=True)
            return

        reqs = JOB_REQUIREMENTS.get(job_id, {})
        stat_reqs = reqs.get("stat_reqs", {})
        qual_reqs = reqs.get("qual_reqs", [])
        if stat_reqs or qual_reqs:
            meets, missing_stats, missing_quals = await db.check_job_requirements(interaction.user.id, stat_reqs, qual_reqs)
            if not meets:
                lines = []
                for stat, info in missing_stats.items():
                    lines.append(f"  {STATS.get(stat, {}).get('name', stat)}: {info['have']}/{info['need']}")
                for q in missing_quals:
                    lines.append(f"  Missing: {QUALIFICATIONS.get(q, {}).get('name', q)}")
                await interaction.response.send_message(embed=error_embed("Requirements Not Met", f"You don't meet the requirements for **{job['name']}**:\n" + "\n".join(lines)), ephemeral=True)
                return

        player_jobs = await db.get_player_jobs(interaction.user.id)
        existing = player_jobs.get(slot)
        if existing and existing["job_id"] == job_id:
            await interaction.response.send_message(embed=error_embed("Already Set", f"You already have this job in slot {slot}."), ephemeral=True)
            return
        other_slots = [s for s in [1, 2, 3] if s != slot]
        for other_slot in other_slots:
            other = player_jobs.get(other_slot)
            if other and other["job_id"] == job_id:
                await interaction.response.send_message(embed=error_embed("Duplicate Job", f"You already have this job in slot {other_slot}."), ephemeral=True)
                return

        await db.set_player_job(interaction.user.id, slot, job_id)
        await interaction.response.send_message(embed=success_embed("Job Set", f"You are now a **{job['name']}** in slot {slot}!\n{get_action_text('misc', 'job_set', job_name=job['name'])}"))

    @app_commands.command(name="work", description="Work at your job — complete a minigame to earn money!")
    @app_commands.choices(slot=_SLOT_CHOICES)
    async def work(self, interaction: discord.Interaction, slot: app_commands.Choice[str] = None):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        player_jobs = await db.get_player_jobs(interaction.user.id)
        filled = {s: pj for s, pj in player_jobs.items() if pj}
        if not filled:
            await interaction.response.send_message(embed=error_embed("No Job", "You need a job first! Use `/jobs` to browse and `/job set` to choose one."), ephemeral=True)
            return

        if slot is not None:
            slot_num = int(slot.value)
        elif len(filled) == 1:
            slot_num = list(filled.keys())[0]
        else:
            await interaction.response.send_message(embed=error_embed("Choose a Slot", "You have multiple jobs! Use `/work slot:` to pick which one to work."), ephemeral=True)
            return

        pj = player_jobs.get(slot_num)
        if not pj:
            await interaction.response.send_message(embed=error_embed("Empty Slot", f"Slot {slot_num} is empty."), ephemeral=True)
            return

        job_id = pj["job_id"]
        if job_id not in JOBS:
            await db.quit_player_job(interaction.user.id, slot_num)
            await interaction.response.send_message(embed=error_embed("Job Error", "Your job was invalid and has been removed."), ephemeral=True)
            return

        job = JOBS[job_id]
        cd = await db.check_cooldown(interaction.user.id, f"work_{slot_num}")
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"Still tired from your last **{job['name']}** shift. Try again in {mins}m {secs}s."), ephemeral=True)
            return
        if data["health"] <= 10:
            await interaction.response.send_message(embed=error_embed("Too Weak", "Your health is too low to work!"), ephemeral=True)
            return
        if data["hunger"] <= 5:
            await interaction.response.send_message(embed=error_embed("Too Hungry", "You're too hungry to work!"), ephemeral=True)
            return
        if data["thirst"] <= 5:
            await interaction.response.send_message(embed=error_embed("Too Thirsty", "You're too thirsty to work!"), ephemeral=True)
            return

        mg_type = get_minigame_type(job_id)

        # ── Phase 5: Roll for special shift types ──
        is_boss_shift = roll_boss_shift()
        shift_event = roll_shift_event()

        # Build shift intro message
        shift_intro = f"Starting a **{mg_type}** minigame for your {job['name']} job..."
        if is_boss_shift:
            shift_intro = f"{BOSS_SHIFT_CONFIG['emoji']} **{BOSS_SHIFT_CONFIG['name']}** for {job['name']}!\n{BOSS_SHIFT_CONFIG['description']}"
        elif shift_event:
            shift_intro = f"{shift_event['emoji']} **{shift_event['name']}** for {job['name']}!\n{shift_event['description']}"

        await interaction.response.send_message(embed=themed_embed("Work Minigame", shift_intro, category=job.get("category")))
        performance = await run_minigame(interaction, job_id, interaction.user.id)

        if performance <= 0:
            await interaction.followup.send(embed=error_embed("Failed", "You failed the minigame and earned nothing. Try again next shift!"))
            await db.set_cooldown(interaction.user.id, f"work_{slot_num}", job["cooldown"] // 2)
            # Reset streak on failure
            if data.get("work_streak", 0) > 0:
                await db.update_user(interaction.user.id, work_streak=0)
            return

        # ── Phase 5: Progressive difficulty ──
        performance = apply_difficulty(performance, pj["job_level"])

        # ── Phase 5: Quality grade ──
        grade_letter, grade_emoji, grade_comment = get_grade(performance)

        # ── Phase 5: Streak combo ──
        current_streak = data.get("work_streak", 0)
        grade_rank = GRADE_ORDER.get(grade_letter, 0)
        streak_threshold_rank = GRADE_ORDER.get(STREAK_GRADE_THRESHOLD, 0)
        if grade_rank >= streak_threshold_rank:
            new_streak = current_streak + 1
        else:
            new_streak = 0
        streak_mult, streak_desc = get_streak_multiplier(new_streak)

        # ── Phase 5: Shift event / boss shift modifiers ──
        event_pay_mult = 1.0
        event_xp_mult = 1.0
        event_stat_cost_mult = 1.0
        event_label = ""
        boss_win = False

        if is_boss_shift:
            event_pay_mult = BOSS_SHIFT_CONFIG["pay_mult"]
            event_xp_mult = BOSS_SHIFT_CONFIG["xp_mult"]
            event_stat_cost_mult = BOSS_SHIFT_CONFIG["stat_cost_mult"]
            event_label = BOSS_SHIFT_CONFIG["name"]
            if performance >= BOSS_SHIFT_CONFIG["min_performance"]:
                boss_win = True
            else:
                event_pay_mult = 1.0  # No bonus on failed boss shift
                event_xp_mult = 1.0
        elif shift_event:
            event_pay_mult = shift_event["pay_mult"]
            event_xp_mult = shift_event["xp_mult"]
            event_stat_cost_mult = shift_event["stat_cost_mult"]
            event_label = shift_event["name"]
            if performance < shift_event.get("min_performance", 0.0):
                event_pay_mult = 1.0
                event_xp_mult = 1.0

        # ── Job reputation benefits ──
        job_category = job.get("category", "entry")
        rep_benefits = await db.get_job_rep_benefits(interaction.user.id, job_category)
        rep_pay_mult = rep_benefits.get("pay_mult", 1.0)
        rep_xp_mult = rep_benefits.get("xp_mult", 1.0)
        rep_stat_cost_mult = rep_benefits.get("stat_cost_mult", 1.0)

        # ── Calculate pay with all multipliers ──
        pay = pet_bonus(data.get("pet_id"), "pay", job_pay(job["base_pay"], pj["job_level"], performance))
        mods = stat_modifier(data, "work")
        housing = await get_housing_bonus(interaction.user.id)
        from config import WEATHER_STATES
        current_weather = await db.get_weather()
        weather_pay_mult = WEATHER_STATES.get(current_weather, {}).get("effects", {}).get("work_pay_mult", 1.0)
        time_effects = await db.get_time_effects()
        time_pay_mult = time_effects.get("work_pay", 1.0)
        buff_pay_mult = await db.get_buff_mult(interaction.user.id, "work_pay")
        pay = int(pay * mods["pay_mult"] * housing["pay_mult"] * weather_pay_mult * time_pay_mult * buff_pay_mult * streak_mult * event_pay_mult * rep_pay_mult)
        xp_gain = pet_bonus(data.get("pet_id"), "xp", int(25 * performance))
        xp_gain = int(xp_gain * mods["xp_mult"] * housing["xp_mult"] * event_xp_mult * rep_xp_mult)
        job_xp_gain = int(15 * performance * mods["xp_mult"] * housing["xp_mult"] * event_xp_mult * rep_xp_mult)
        stat_cost = mods["stat_cost_mult"] * event_stat_cost_mult * rep_stat_cost_mult

        new_xp = data["xp"] + xp_gain
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp = new_xp - sum(xp_for_next_level(l) for l in range(data["level"], new_level))

        new_job_xp = pj["job_xp"] + job_xp_gain
        new_job_level = pj["job_level"]
        while new_job_xp >= 500 * new_job_level:
            new_job_xp -= 500 * new_job_level
            new_job_level += 1

        # ── Update best grade ──
        best_grade = data.get("best_grade", "")
        update_fields = {
            "wallet": data["wallet"] + pay,
            "xp": new_xp,
            "level": new_level,
            "work_count": data["work_count"] + 1,
            "total_earned": data["total_earned"] + pay,
            "hunger": clamp(data["hunger"] - int(5 * stat_cost)),
            "thirst": clamp(data["thirst"] - int(5 * stat_cost)),
            "energy": clamp(data.get("energy", 100) - int(10 * stat_cost)),
            "health": clamp(data["health"] - int(2 * stat_cost)),
            "work_streak": new_streak,
        }
        if is_grade_better(grade_letter, best_grade):
            update_fields["best_grade"] = grade_letter
        if boss_win:
            update_fields["boss_shifts_won"] = data.get("boss_shifts_won", 0) + 1

        await db.update_user(interaction.user.id, **update_fields)
        await db.update_job_xp(interaction.user.id, slot_num, new_job_xp, new_job_level)
        await db.add_transaction(interaction.user.id, "work", pay, f"Worked as {job['name']}")
        await db.set_cooldown(interaction.user.id, f"work_{slot_num}", job["cooldown"])
        await db.update_quest_progress(interaction.user.id, "work", 1)
        await db.update_quest_progress(interaction.user.id, "earn", pay)

        # ── Job reputation gain ──
        rep_gain = get_rep_gain(grade_letter, boss_win, new_streak)
        if rep_gain > 0:
            await db.add_job_reputation(interaction.user.id, job_category, rep_gain)
        current_rep = await db.get_job_reputation(interaction.user.id, job_category)
        rep_tier_name, rep_tier_emoji, _, _ = get_rep_tier(current_rep)

        # ── Build result embed ──
        title = f"{grade_emoji} Grade {grade_letter} — Work Complete!"
        if is_boss_shift:
            title = f"{BOSS_SHIFT_CONFIG['emoji']} {'🏆' if boss_win else '💀'} Boss Shift — Grade {grade_letter}!"
        embed = themed_embed(title, get_action_text("misc", "work_success", amount=format_money(pay), job_name=job['name']), category=job.get("category"), grade=grade_letter)
        embed.add_field(name="Grade", value=f"{grade_emoji} **{grade_letter}** — {grade_comment}", inline=False)
        embed.add_field(name="Performance", value=f"{int(performance*100)}%", inline=True)
        embed.add_field(name="Pay", value=format_money(pay), inline=True)
        embed.add_field(name="XP Gained", value=f"+{xp_gain}", inline=True)
        embed.add_field(name="Job XP", value=f"+{job_xp_gain}", inline=True)

        # Streak field
        streak_text = f"🔥 **{new_streak}** shifts" if new_streak > 0 else "No streak"
        if streak_mult > 1.0:
            streak_text += f" ({streak_desc})"
        embed.add_field(name="Work Streak", value=streak_text, inline=True)

        # Job reputation field
        rep_text = f"{rep_tier_emoji} {rep_tier_name} ({current_rep} rep)"
        if rep_gain > 0:
            rep_text += f" | +{rep_gain}"
        embed.add_field(name="Job Rep", value=rep_text, inline=True)

        # Shift event / boss field
        if is_boss_shift:
            if boss_win:
                embed.add_field(name="Boss Shift", value=f"🏆 {BOSS_SHIFT_CONFIG['win_description']}", inline=False)
            else:
                embed.add_field(name="Boss Shift", value=f"💀 {BOSS_SHIFT_CONFIG['fail_description']}", inline=False)
        elif shift_event:
            event_text = f"{shift_event['emoji']} {shift_event['name']}"
            if event_pay_mult > 1.0:
                event_text += f" — {int((event_pay_mult - 1) * 100)}% bonus pay!"
            if event_xp_mult > 1.0:
                event_text += f" {int((event_xp_mult - 1) * 100)}% bonus XP!"
            embed.add_field(name="Shift Event", value=event_text, inline=False)

        embed.add_field(name="Slot", value=f"Slot {slot_num}", inline=True)
        cond_text = "Great condition!" if mods["combined"] >= 0.9 else ("Good condition" if mods["combined"] >= 0.75 else "Poor condition — low stats hurt performance")
        embed.add_field(name="Condition", value=cond_text, inline=True)

        if leveled_up:
            embed.add_field(name="Level Up!", value=f"You are now level {new_level}!", inline=False)
        if new_job_level > pj["job_level"]:
            embed.add_field(name="Job Level Up!", value=f"Your {job['name']} is now level {new_job_level}!", inline=False)

        new_achievements = await db.check_achievements(interaction.user.id)
        if new_achievements:
            total_ach_reward = 0
            for ach_id in new_achievements:
                ach = ACHIEVEMENTS[ach_id]
                total_ach_reward += ach["reward"]
                embed.add_field(name="Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — {format_money(ach['reward'])} reward!", inline=False)
            await db.update_user(interaction.user.id,
                wallet=data["wallet"] + pay + total_ach_reward,
                total_earned=data["total_earned"] + pay + total_ach_reward,
            )

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="jobrep", description="View your job reputation standings across all categories")
    async def jobrep(self, interaction: discord.Interaction):
        from utils.embeds import info_embed
        all_rep = await db.get_all_job_reputation(interaction.user.id)
        embed = info_embed("💼 Job Reputation", "Your standing in each job category:")
        for cat_id, cat_data in JOB_CATEGORIES.items():
            rep = all_rep.get(cat_id, 0)
            tier_threshold, tier_name, tier_emoji, benefits = get_rep_tier(rep)
            benefit_text = ""
            if benefits.get("pay_mult", 1.0) > 1.0:
                benefit_text += f" +{int((benefits['pay_mult'] - 1) * 100)}% pay"
            if benefits.get("xp_mult", 1.0) > 1.0:
                benefit_text += f" +{int((benefits['xp_mult'] - 1) * 100)}% XP"
            if benefits.get("stat_cost_mult", 1.0) < 1.0:
                benefit_text += f" -{int((1 - benefits['stat_cost_mult']) * 100)}% fatigue"
            embed.add_field(
                name=f"{cat_data['emoji']} {cat_data['name']}",
                value=f"{tier_emoji} **{tier_name}** — {rep} rep{benefit_text}",
                inline=True,
            )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Jobs(bot))
