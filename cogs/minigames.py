"""
Minigame engine for Lifebot job system.
Each minigame type is a Discord UI View that returns a performance score (0.0–1.0).
Anti-automation: randomization in content, order, timing, and button positions.
"""
import discord
import random
import asyncio
import time
import logging
from config.minigame_content import JOB_CONTENT, GENERIC
from config.job_requirements import JOB_REQUIREMENTS
from utils.proc_gen import generate_content as proc_generate

log = logging.getLogger(__name__)


def get_minigame_type(job_id: str) -> str:
    """Get the minigame type assigned to a job. Randomly picks from 3 options."""
    req = JOB_REQUIREMENTS.get(job_id, {})
    games = req.get("minigames")
    if games and len(games) > 1:
        return random.choice(games)
    return req.get("minigame", "quick_pick")


def get_minigame_content(job_id: str, mg_type: str = None) -> dict:
    """Get themed content for a job's minigame. If mg_type is provided, use it
    instead of randomly picking (ensures content matches the chosen minigame)."""
    if mg_type is None:
        mg_type = get_minigame_type(job_id)
    content = JOB_CONTENT.get(job_id, {})
    raw = content.get(mg_type, GENERIC.get(mg_type, {}))
    return _procedural_variant(raw, job_id, mg_type)


import random as _rnd

# Procedural prompt variation prefixes — adds flavor so prompts never look identical
_PROMPT_PREFIXES = [
    "", "Quick! ", "Hurry up — ", "Your shift depends on this: ", "Don't mess this up: ",
    "The clock is ticking: ", "Your boss is watching: ", "Customer waiting: ",
    "Critical task: ", "Priority one: ", "Urgent: ", "Listen carefully: ",
    "You've got this: ", "Stay focused: ", "No pressure, but: ",
]

_PROMPT_SUFFIXES = [
    "", " Choose wisely!", " Think fast!", " Don't second-guess yourself.",
    " Time is money!", " Get it right!", " No mistakes!", " You know this!",
    " Trust your instincts.", " Show them what you've got!",
]


def _procedural_variant(raw: dict, job_id: str, mg_type: str) -> dict:
    """Transform static content into a procedurally varied version.
    
    Supports:
    - 'variants': list of content dicts — picks one randomly each playthrough
    - 'prompts': list of prompt strings — picks one randomly
    - 'options_pool': list larger than 4 — picks 4 random options (including correct)
    - Procedural prompt wrapping with random prefixes/suffixes
    - 'items_pool': list larger than needed — picks a random subset
    - 'pairs_pool': list of pairs — picks a random subset
    - 'tasks_pool': list of tasks — picks a random subset
    """
    # If variants exist, pick one randomly and recurse
    if "variants" in raw:
        chosen = _rnd.choice(raw["variants"])
        return _procedural_variant(chosen, job_id, mg_type)
    
    c = dict(raw)  # shallow copy so we don't mutate the original
    
    # Random prompt selection from a list
    if "prompts" in c and isinstance(c["prompts"], list):
        c["prompt"] = _rnd.choice(c["prompts"])
    
    # Procedural prompt wrapping (adds prefix/suffix for variety)
    prompt = c.get("prompt", "")
    if prompt and _rnd.random() < 0.7:
        prefix = _rnd.choice(_PROMPT_PREFIXES)
        suffix = _rnd.choice(_PROMPT_SUFFIXES)
        c["prompt"] = f"{prefix}{prompt}{suffix}"
    
    # Quick pick: if options_pool exists, build a random question from it
    if mg_type == "quick_pick" and "options_pool" in c:
        pool = c["options_pool"]
        correct = c.get("correct", "")
        # Pick 3 random distractors + the correct answer
        distractors = [o for o in pool if o != correct]
        chosen_distractors = _rnd.sample(distractors, min(3, len(distractors)))
        c["options"] = chosen_distractors + [correct]
        _rnd.shuffle(c["options"])
    
    # Sequence/sort: if items_pool exists, pick a random subset
    if mg_type in ("sequence", "sort") and "items_pool" in c:
        pool = c["items_pool"]
        count = _rnd.randint(4, min(6, len(pool)))
        chosen = _rnd.sample(pool, count)
        c["items"] = chosen
        # For sequence, the order is the sorted version of chosen items
        if "order_pool" in c:
            c["order"] = [o for o in c["order_pool"] if o in chosen]
        else:
            c["order"] = chosen  # same as items if no explicit order
    
    # Match pairs: if pairs_pool exists, pick a random subset
    if mg_type == "match_pairs" and "pairs_pool" in c:
        pool = c["pairs_pool"]
        count = _rnd.randint(3, min(4, len(pool)))
        c["pairs"] = _rnd.sample(pool, count)
    
    # Speed run: if tasks_pool exists, pick a random subset
    if mg_type == "speed_run" and "tasks_pool" in c:
        pool = c["tasks_pool"]
        count = _rnd.randint(3, min(5, len(pool)))
        c["tasks"] = _rnd.sample(pool, count)
    
    # Memory: if items_pool exists, pick a random subset
    if mg_type == "memory" and "items_pool" in c:
        pool = c["items_pool"]
        count = _rnd.randint(4, min(6, len(pool)))
        c["sequence"] = _rnd.sample(pool, count)
    
    # Spot error: if sequences_pool exists, pick a random pair
    if mg_type == "spot_error" and "sequences_pool" in c:
        pair = _rnd.choice(c["sequences_pool"])
        c["correct_sequence"] = pair["correct_sequence"]
        c["presented_sequence"] = pair["presented_sequence"]
    
    # Pattern: if patterns_pool exists, pick a random one
    if mg_type == "pattern" and "patterns_pool" in c:
        pat = _rnd.choice(c["patterns_pool"])
        c["sequence"] = pat["sequence"]
        c["answer"] = pat["answer"]
    
    # Precision: randomize target within range
    if mg_type == "precision" and "target_range" in c:
        lo, hi = c["target_range"]
        c["target"] = _rnd.randint(lo, hi)
    
    # Timing: randomize number of beats
    if mg_type == "timing" and "beats_range" in c:
        lo, hi = c["beats_range"]
        c["beats"] = _rnd.randint(lo, hi)
    
    # Budget: if budget_range exists, randomize the total
    if mg_type == "budget" and "budget_range" in c:
        lo, hi = c["budget_range"]
        c["budget"] = _rnd.randint(lo, hi)
    
    # Fill blank: if blanks_pool exists, pick a random one
    if mg_type == "fill_blank" and "blanks_pool" in c:
        item = _rnd.choice(c["blanks_pool"])
        c["prompt"] = item.get("prompt", c.get("prompt", ""))
        c["answer"] = item.get("answer", c.get("answer", ""))
        c["context"] = item.get("context", c.get("context", ""))
    
    # Math: if math_pool exists, pick a random problem
    if mg_type == "math" and "math_pool" in c:
        prob = _rnd.choice(c["math_pool"])
        c["prompt"] = prob.get("prompt", c.get("prompt", ""))
        c["formula"] = prob.get("formula", c.get("formula", ""))
        c["answer"] = prob.get("answer", c.get("answer", 0))
    
    # Typing race: if phrases_pool exists, pick a random phrase
    if mg_type == "typing_race" and "phrases_pool" in c:
        c["phrase"] = _rnd.choice(c["phrases_pool"])
    
    # Route plan: if routes_pool exists, pick a random route
    if mg_type == "route_plan" and "routes_pool" in c:
        route = _rnd.choice(c["routes_pool"])
        c["stops"] = route.get("stops", c.get("stops", []))
        c["optimal"] = route.get("optimal", c.get("optimal", c["stops"]))
    
    # Diagnosis: if cases_pool exists, pick a random case
    if mg_type == "diagnosis" and "cases_pool" in c:
        case = _rnd.choice(c["cases_pool"])
        c["prompt"] = case.get("prompt", c.get("prompt", ""))
        c["options"] = case.get("options", c.get("options", []))
        c["correct"] = case.get("correct", c.get("correct", ""))
        c["reasoning"] = case.get("reasoning", c.get("reasoning", ""))
    
    # Multi-stage: if stages_pool exists, pick random stages
    if mg_type == "multi_stage" and "stages_pool" in c:
        pool = c["stages_pool"]
        count = min(3, len(pool))
        c["stages"] = _rnd.sample(pool, count)
    
    # Shift sim: if situations_pool exists, pick a random subset
    if mg_type == "shift_sim" and "situations_pool" in c:
        pool = c["situations_pool"]
        count = _rnd.randint(3, min(5, len(pool)))
        c["situations"] = _rnd.sample(pool, count)
    
    # Triage: if patients_pool exists, pick a random subset
    if mg_type == "triage" and "patients_pool" in c:
        pool = c["patients_pool"]
        count = _rnd.randint(3, min(5, len(pool)))
        c["patients"] = _rnd.sample(pool, count)
    
    return c


# ═══════════════════════════════════════════════════════════════
# UI Views for each minigame type
# ═══════════════════════════════════════════════════════════════

class SequenceView(discord.ui.View):
    """Reorder shuffled items into the correct sequence by clicking them in order."""
    def __init__(self, items: list, correct_order: list, timeout: int = 60):
        super().__init__(timeout=timeout)
        self.correct_order = correct_order
        self.selected = []
        self.result = None
        self.start_time = None
        self.user_id = None

        shuffled = items.copy()
        while shuffled == correct_order:
            random.shuffle(shuffled)

        for i, item in enumerate(shuffled):
            btn = discord.ui.Button(label=item[:80], style=discord.ButtonStyle.secondary, custom_id=f"seq_{i}")
            btn.callback = self._make_callback(item, btn)
            self.add_item(btn)

    def _make_callback(self, item: str, btn: discord.ui.Button):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            if self.result is not None:
                return
            self.selected.append(item)
            btn.disabled = True
            btn.style = discord.ButtonStyle.success
            await interaction.response.edit_message(view=self)

            if len(self.selected) == len(self.correct_order):
                elapsed = time.time() - self.start_time
                correct = sum(1 for i, s in enumerate(self.selected) if i < len(self.correct_order) and s == self.correct_order[i])
                accuracy = correct / len(self.correct_order)
                speed_bonus = max(0, 1.0 - elapsed / 45.0) * 0.3
                self.result = min(1.0, accuracy * 0.7 + speed_bonus)
                self.stop()
        return callback

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class SortView(discord.ui.View):
    """Sort items into categories using dropdowns."""
    def __init__(self, items: list, categories: list, timeout: int = 60):
        super().__init__(timeout=timeout)
        self.items = items
        self.categories = categories
        self.user_answers = {}
        self.result = None
        self.user_id = None
        self.start_time = None
        self._build_dropdowns()

    def _build_dropdowns(self):
        unique_cats = list(set(self.categories))
        for i, item in enumerate(self.items):
            select = discord.ui.Select(
                placeholder=f"Sort: {item[:50]}",
                options=[discord.SelectOption(label=c[:100], value=c) for c in unique_cats],
                custom_id=f"sort_{i}",
            )
            select.callback = self._make_callback(item, i)
            self.add_item(select)

    def _make_callback(self, item: str, idx: int):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            select = self.children[idx]
            self.user_answers[item] = select.values[0]
            await interaction.response.edit_message(view=self)
            if len(self.user_answers) == len(self.items):
                elapsed = time.time() - self.start_time
                correct = sum(1 for i, item in enumerate(self.items) if self.user_answers.get(item) == self.categories[i])
                accuracy = correct / len(self.items)
                speed_bonus = max(0, 1.0 - elapsed / 50.0) * 0.2
                self.result = min(1.0, accuracy * 0.8 + speed_bonus)
                self.stop()
        return callback

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class QuickPickView(discord.ui.View):
    """Pick the correct answer from multiple choice buttons (shuffled positions)."""
    def __init__(self, prompt: str, options: list, correct: str, timeout: int = 20):
        super().__init__(timeout=timeout)
        self.correct = correct
        self.result = None
        self.start_time = None
        self.user_id = None

        shuffled = options.copy()
        random.shuffle(shuffled)

        for i, opt in enumerate(shuffled):
            btn = discord.ui.Button(label=opt[:80], style=discord.ButtonStyle.primary, custom_id=f"qp_{i}")
            btn.callback = self._make_callback(opt)
            self.add_item(btn)

    def _make_callback(self, option: str):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            if self.result is not None:
                return
            elapsed = time.time() - self.start_time
            if option == self.correct:
                speed_bonus = max(0, 1.0 - elapsed / 10.0) * 0.3
                self.result = min(1.0, 0.7 + speed_bonus)
            else:
                self.result = 0.2
            for child in self.children:
                child.disabled = True
                if child.label == self.correct[:80]:
                    child.style = discord.ButtonStyle.success
                elif child.label == option[:80]:
                    child.style = discord.ButtonStyle.danger
            await interaction.response.edit_message(view=self)
            self.stop()
        return callback

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class MemoryView(discord.ui.View):
    """Memorize a sequence, then reproduce it by clicking buttons in order."""
    def __init__(self, sequence: list, timeout: int = 45):
        super().__init__(timeout=timeout)
        self.sequence = sequence
        self.show_phase = True
        self.input_phase = False
        self.user_input = []
        self.result = None
        self.start_time = None
        self.user_id = None
        self._message = None

    async def start(self, interaction: discord.Interaction, content: str):
        self._message = await interaction.followup.send(content=content, view=self)
        await asyncio.sleep(min(3 + len(self.sequence), 8))
        self.show_phase = False
        self.input_phase = True
        unique_items = list(dict.fromkeys(self.sequence))
        self.clear_items()
        random.shuffle(unique_items)
        for i, item in enumerate(unique_items):
            btn = discord.ui.Button(label=item[:80], style=discord.ButtonStyle.primary, custom_id=f"mem_{i}")
            btn.callback = self._make_callback(item)
            self.add_item(btn)
        await self._message.edit(content="🔁 **Now reproduce the sequence!** Click buttons in the correct order.", view=self)

    def _make_callback(self, item: str):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            if self.result is not None:
                return
            self.user_input.append(item)
            idx = len(self.user_input) - 1
            if idx < len(self.sequence) and item == self.sequence[idx]:
                if len(self.user_input) == len(self.sequence):
                    elapsed = time.time() - self.start_time
                    speed_bonus = max(0, 1.0 - elapsed / 30.0) * 0.3
                    self.result = min(1.0, 0.7 + speed_bonus)
                    for child in self.children:
                        child.disabled = True
                    await interaction.response.edit_message(content="✅ **Perfect memory!**", view=self)
                    self.stop()
                else:
                    await interaction.response.edit_message(view=self)
            else:
                self.result = 0.2
                for child in self.children:
                    child.disabled = True
                await interaction.response.edit_message(content="❌ **Wrong sequence!**", view=self)
                self.stop()
        return callback

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class TimingView(discord.ui.View):
    """Click the button when the progress bar hits the target zone."""
    def __init__(self, beats: int = 4, timeout: int = 30):
        super().__init__(timeout=timeout)
        self.beats = beats
        self.current_beat = 0
        self.scores = []
        self.result = None
        self.start_time = None
        self.user_id = None
        self._bar_pos = 0.0
        self._bar_task = None
        self._target_start = 0.4
        self._target_end = 0.6

        btn = discord.ui.Button(label="🎯 CLICK!", style=discord.ButtonStyle.danger, custom_id="timing_btn")
        btn.callback = self._on_click
        self.add_item(btn)

    async def _bar_loop(self):
        direction = 1
        while self.current_beat < self.beats and self.result is None:
            self._bar_pos += direction * 0.05
            if self._bar_pos >= 1.0:
                self._bar_pos = 1.0
                direction = -1
            elif self._bar_pos <= 0.0:
                self._bar_pos = 0.0
                direction = 1
            await asyncio.sleep(0.08)

    async def _on_click(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
            return
        if self.result is not None:
            return
        if self._target_start <= self._bar_pos <= self._target_end:
            self.scores.append(1.0)
        else:
            dist = min(abs(self._bar_pos - self._target_start), abs(self._bar_pos - self._target_end))
            self.scores.append(max(0, 1.0 - dist * 3))

        self.current_beat += 1
        self._target_start = random.uniform(0.3, 0.5)
        self._target_end = self._target_start + random.uniform(0.1, 0.2)

        if self.current_beat >= self.beats:
            self.result = sum(self.scores) / len(self.scores) if self.scores else 0.0
            for child in self.children:
                child.disabled = True
            await interaction.response.edit_message(content=f"⏱️ **Timing complete!** Score: {int(self.result * 100)}%", view=self)
            self.stop()
        else:
            bar = self._render_bar()
            await interaction.response.edit_message(content=f"🎯 **Beat {self.current_beat + 1}/{self.beats}**\n{bar}\nClick when the █ hits the target zone!", view=self)

    def _render_bar(self) -> str:
        length = 20
        pos = int(self._bar_pos * length)
        target_s = int(self._target_start * length)
        target_e = int(self._target_end * length)
        bar = ""
        for i in range(length):
            if i == pos:
                bar += "█"
            elif target_s <= i <= target_e:
                bar += "▓"
            else:
                bar += "░"
        return bar

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class MatchPairsView(discord.ui.View):
    """Match items from left column to right column using dropdowns."""
    def __init__(self, pairs: list, timeout: int = 45):
        super().__init__(timeout=timeout)
        self.pairs = pairs
        self.left_items = [p[0] for p in pairs]
        self.right_items = [p[1] for p in pairs]
        self.answers = {}
        self.result = None
        self.start_time = None
        self.user_id = None

        shuffled_right = self.right_items.copy()
        random.shuffle(shuffled_right)
        self._shuffled_right = shuffled_right

        for i, left in enumerate(self.left_items):
            select = discord.ui.Select(
                placeholder=f"Match: {left[:50]}",
                options=[discord.SelectOption(label=r[:100], value=r) for r in shuffled_right],
                custom_id=f"match_{i}",
            )
            select.callback = self._make_callback(left)
            self.add_item(select)

    def _make_callback(self, left: str):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            if self.result is not None:
                return
            for child in self.children:
                if isinstance(child, discord.ui.Select) and child.placeholder == f"Match: {left[:50]}":
                    self.answers[left] = child.values[0]
                    break
            await interaction.response.edit_message(view=self)
            if len(self.answers) == len(self.left_items):
                elapsed = time.time() - self.start_time
                correct = sum(1 for l, r in self.pairs if self.answers.get(l) == r)
                accuracy = correct / len(self.pairs)
                speed_bonus = max(0, 1.0 - elapsed / 35.0) * 0.2
                self.result = min(1.0, accuracy * 0.8 + speed_bonus)
                self.stop()
        return callback

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class SpotErrorView(discord.ui.View):
    """Find the difference between two sequences/code snippets."""
    def __init__(self, correct_seq: list, presented_seq: list, timeout: int = 30):
        super().__init__(timeout=timeout)
        self.correct_seq = correct_seq
        self.presented_seq = presented_seq
        self.result = None
        self.start_time = None
        self.user_id = None

        diff_indices = [i for i in range(len(presented_seq)) if i >= len(correct_seq) or presented_seq[i] != correct_seq[i]]
        self._diff_indices = diff_indices

        for i, item in enumerate(presented_seq):
            btn = discord.ui.Button(label=str(item)[:80], style=discord.ButtonStyle.secondary, custom_id=f"se_{i}")
            btn.callback = self._make_callback(i)
            self.add_item(btn)

    def _make_callback(self, idx: int):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            if self.result is not None:
                return
            elapsed = time.time() - self.start_time
            if idx in self._diff_indices:
                speed_bonus = max(0, 1.0 - elapsed / 15.0) * 0.3
                self.result = min(1.0, 0.7 + speed_bonus)
            else:
                self.result = 0.3
            for child in self.children:
                child.disabled = True
                if int(child.custom_id.split("_")[1]) in self._diff_indices:
                    child.style = discord.ButtonStyle.success
                elif child.custom_id == f"se_{idx}":
                    child.style = discord.ButtonStyle.danger
            await interaction.response.edit_message(view=self)
            self.stop()
        return callback

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class PatternView(discord.ui.View):
    """Complete the pattern — type the next item in the sequence."""
    def __init__(self, sequence: list, answer: str, timeout: int = 25):
        super().__init__(timeout=timeout)
        self.answer = answer
        self.result = None
        self.start_time = None
        self.user_id = None

    async def run(self, interaction: discord.Interaction, prompt: str):
        modal = discord.ui.Modal(title="Complete the Pattern")
        text_input = discord.ui.TextInput(label="What comes next?", placeholder="Type your answer...", required=True, max_length=50)
        modal.add_item(text_input)

        async def on_submit(modal_interaction: discord.Interaction):
            if modal_interaction.user.id != self.user_id:
                await modal_interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            elapsed = time.time() - self.start_time
            user_answer = text_input.value.strip().lower()
            if user_answer == str(self.answer).strip().lower():
                speed_bonus = max(0, 1.0 - elapsed / 12.0) * 0.3
                self.result = min(1.0, 0.7 + speed_bonus)
            else:
                self.result = 0.2
            await modal_interaction.response.edit_message(view=self)
            self.stop()

        modal.on_submit = on_submit
        await interaction.response.send_modal(modal)

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class PrecisionView(discord.ui.View):
    """Stop the counter at the exact target value."""
    def __init__(self, target: float, tolerance: float, timeout: int = 20):
        super().__init__(timeout=timeout)
        self.target = target
        self.tolerance = tolerance
        self.current = 0.0
        self.result = None
        self.start_time = None
        self.user_id = None
        self._running = True

        btn = discord.ui.Button(label="🎯 STOP!", style=discord.ButtonStyle.danger, custom_id="prec_btn")
        btn.callback = self._on_click
        self.add_item(btn)

    async def _counter_loop(self):
        while self._running and self.result is None:
            self.current += 0.5
            if self.current > self.target * 2 + 10:
                self.current = 0.0
            await asyncio.sleep(0.1)

    async def _on_click(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
            return
        if self.result is not None:
            return
        self._running = False
        diff = abs(self.current - self.target)
        if diff <= self.tolerance:
            self.result = 1.0
        elif diff <= self.tolerance * 2:
            self.result = 0.7
        elif diff <= self.tolerance * 3:
            self.result = 0.4
        else:
            self.result = 0.1
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(
            content=f"🎯 Target: {self.target} | You hit: {self.current:.1f} | Score: {int(self.result * 100)}%",
            view=self,
        )
        self.stop()

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class ComboLockView(discord.ui.View):
    """Pick a combination lock — find the correct pin values using +/- buttons."""
    def __init__(self, pins: list, max_val: int = 9, timeout: int = 60):
        super().__init__(timeout=timeout)
        self.pins = pins
        self.max_val = max_val
        self.current = [0] * len(pins)
        self.result = None
        self.start_time = None
        self.user_id = None

        submit_btn = discord.ui.Button(label="🔓 Unlock!", style=discord.ButtonStyle.success, custom_id="combo_submit")
        submit_btn.callback = self._on_submit
        self.add_item(submit_btn)

    async def _on_submit(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
            return
        if self.result is not None:
            return
        elapsed = time.time() - self.start_time
        correct = sum(1 for i, p in enumerate(self.pins) if self.current[i] == p)
        accuracy = correct / len(self.pins)
        if accuracy == 1.0:
            speed_bonus = max(0, 1.0 - elapsed / 40.0) * 0.3
            self.result = min(1.0, 0.7 + speed_bonus)
        else:
            self.result = accuracy * 0.5
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(
            content=f"🔓 Correct: {self.pins} | You entered: {self.current} | Score: {int(self.result * 100)}%",
            view=self,
        )
        self.stop()

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class SpeedRunView(discord.ui.View):
    """Click all buttons as fast as possible — buttons appear one at a time."""
    def __init__(self, tasks: list, timeout: int = 30):
        super().__init__(timeout=timeout)
        self.tasks = tasks
        self.completed = 0
        self.result = None
        self.start_time = None
        self.user_id = None
        self._show_next()

    def _show_next(self):
        self.clear_items()
        if self.completed >= len(self.tasks):
            return
        task = self.tasks[self.completed]
        positions = list(range(5))
        random.shuffle(positions)
        row = positions[0] % 5
        btn = discord.ui.Button(label=f"▶️ {task[:70]}", style=discord.ButtonStyle.primary, row=row, custom_id="speed_task")
        btn.callback = self._on_click
        self.add_item(btn)

    async def _on_click(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
            return
        if self.result is not None:
            return
        self.completed += 1
        if self.completed >= len(self.tasks):
            elapsed = time.time() - self.start_time
            speed_bonus = max(0, 1.0 - elapsed / (len(self.tasks) * 3.0)) * 0.4
            self.result = min(1.0, 0.6 + speed_bonus)
            await interaction.response.edit_message(content=f"⚡ **All tasks done!** Score: {int(self.result * 100)}%", view=None)
            self.stop()
        else:
            self._show_next()
            await interaction.response.edit_message(
                content=f"⚡ **Task {self.completed}/{len(self.tasks)} complete!** Next task:",
                view=self,
            )

    async def on_timeout(self):
        if self.result is None:
            self.result = max(0, self.completed / len(self.tasks) * 0.5) if self.tasks else 0.0


class AssemblyView(discord.ui.View):
    """Assemble parts in the correct dependency order using dropdowns."""
    def __init__(self, parts: list, timeout: int = 45):
        super().__init__(timeout=timeout)
        self.parts = parts
        self.assembled = []
        self.result = None
        self.start_time = None
        self.user_id = None
        self._build_select()

    def _build_select(self):
        self.clear_items()
        available = []
        for part, depends_on in self.parts:
            part_name = part if isinstance(part, str) else part[0]
            dep = depends_on if isinstance(depends_on, str) else depends_on[0]
            if dep in self.assembled or dep == "Base" or dep == "Ground" or dep == "Foundation":
                available.append((part_name, dep))

        if not available:
            return

        select = discord.ui.Select(
            placeholder="Select the next part to assemble...",
            options=[discord.SelectOption(label=p[:100], value=p) for p, _ in available],
            custom_id="assembly_select",
        )
        select.callback = self._on_select
        self.add_item(select)

    async def _on_select(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
            return
        if self.result is not None:
            return
        selected = self.children[0].values[0]
        correct_next = None
        for part, depends_on in self.parts:
            part_name = part if isinstance(part, str) else part[0]
            dep = depends_on if isinstance(depends_on, str) else depends_on[0]
            if part_name == selected and part_name not in self.assembled:
                correct_next = part_name
                break

        if correct_next:
            self.assembled.append(correct_next)
            if len(self.assembled) == len(self.parts):
                elapsed = time.time() - self.start_time
                speed_bonus = max(0, 1.0 - elapsed / 35.0) * 0.2
                self.result = min(1.0, 0.8 + speed_bonus)
                await interaction.response.edit_message(content=f"🔧 **Assembly complete!** Score: {int(self.result * 100)}%", view=None)
                self.stop()
            else:
                self._build_select()
                await interaction.response.edit_message(
                    content=f"🔧 **Assembled: {correct_next}** ({len(self.assembled)}/{len(self.parts)})",
                    view=self,
                )
        else:
            self.result = 0.3
            await interaction.response.edit_message(content="❌ Wrong part order!", view=None)
            self.stop()

    async def on_timeout(self):
        if self.result is None:
            self.result = max(0, len(self.assembled) / len(self.parts) * 0.4) if self.parts else 0.0


class TypingRaceView(discord.ui.View):
    """Type a phrase as fast and accurately as possible using a modal."""
    def __init__(self, phrase: str, timeout: int = 30):
        super().__init__(timeout=timeout)
        self.phrase = phrase
        self.result = None
        self.start_time = None
        self.user_id = None

        btn = discord.ui.Button(label="⌨️ Type Now!", style=discord.ButtonStyle.primary, custom_id="typing_btn")
        btn.callback = self._on_click
        self.add_item(btn)

    async def _on_click(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
            return
        if self.result is not None:
            return
        modal = discord.ui.Modal(title="Typing Race")
        text_input = discord.ui.TextInput(
            label="Type the phrase exactly:",
            default=self.phrase,
            required=True,
            max_length=500,
            style=discord.TextStyle.paragraph,
        )
        modal.add_item(text_input)

        async def on_submit(modal_interaction: discord.Interaction):
            if modal_interaction.user.id != self.user_id:
                await modal_interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            elapsed = time.time() - self.start_time
            typed = text_input.value.strip()
            correct_chars = sum(1 for a, b in zip(typed, self.phrase) if a == b)
            accuracy = correct_chars / max(len(self.phrase), 1)
            speed_bonus = max(0, 1.0 - elapsed / 20.0) * 0.3
            self.result = min(1.0, accuracy * 0.7 + speed_bonus)
            for child in self.children:
                child.disabled = True
            await modal_interaction.response.edit_message(
                content=f"⌨️ **Accuracy: {int(accuracy * 100)}%** | Score: {int(self.result * 100)}%",
                view=self,
            )
            self.stop()

        modal.on_submit = on_submit
        await interaction.response.send_modal(modal)

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class MathView(discord.ui.View):
    """Solve a math problem using a modal input."""
    def __init__(self, answer, formula: str = "", timeout: int = 25):
        super().__init__(timeout=timeout)
        self.answer = answer
        self.formula = formula
        self.result = None
        self.start_time = None
        self.user_id = None

        btn = discord.ui.Button(label="🧮 Solve It!", style=discord.ButtonStyle.primary, custom_id="math_btn")
        btn.callback = self._on_click
        self.add_item(btn)

    async def _on_click(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
            return
        if self.result is not None:
            return
        modal = discord.ui.Modal(title="Math Problem")
        text_input = discord.ui.TextInput(label="Your answer:", placeholder="Enter the number...", required=True, max_length=20)
        modal.add_item(text_input)

        async def on_submit(modal_interaction: discord.Interaction):
            if modal_interaction.user.id != self.user_id:
                await modal_interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            elapsed = time.time() - self.start_time
            try:
                user_ans = float(text_input.value.strip())
            except ValueError:
                user_ans = None
            if user_ans is not None and abs(user_ans - float(self.answer)) < 0.01:
                speed_bonus = max(0, 1.0 - elapsed / 15.0) * 0.3
                self.result = min(1.0, 0.7 + speed_bonus)
            else:
                self.result = 0.2
            for child in self.children:
                child.disabled = True
            await modal_interaction.response.edit_message(
                content=f"🧮 Answer: {self.answer} | You: {text_input.value} | Score: {int(self.result * 100)}%",
                view=self,
            )
            self.stop()

        modal.on_submit = on_submit
        await interaction.response.send_modal(modal)

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class FillBlankView(discord.ui.View):
    """Fill in the blank using a modal input."""
    def __init__(self, answer: str, context: str = "", timeout: int = 25):
        super().__init__(timeout=timeout)
        self.answer = answer.lower().strip()
        self.context = context
        self.result = None
        self.start_time = None
        self.user_id = None

        btn = discord.ui.Button(label="✍️ Fill the Blank!", style=discord.ButtonStyle.primary, custom_id="fill_btn")
        btn.callback = self._on_click
        self.add_item(btn)

    async def _on_click(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
            return
        if self.result is not None:
            return
        modal = discord.ui.Modal(title="Fill in the Blank")
        text_input = discord.ui.TextInput(label="Type the missing word(s):", placeholder="Your answer...", required=True, max_length=100)
        modal.add_item(text_input)

        async def on_submit(modal_interaction: discord.Interaction):
            if modal_interaction.user.id != self.user_id:
                await modal_interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            elapsed = time.time() - self.start_time
            user_ans = text_input.value.strip().lower()
            if user_ans == self.answer:
                speed_bonus = max(0, 1.0 - elapsed / 15.0) * 0.3
                self.result = min(1.0, 0.7 + speed_bonus)
            elif self.answer in user_ans or user_ans in self.answer:
                self.result = 0.5
            else:
                self.result = 0.2
            for child in self.children:
                child.disabled = True
            await modal_interaction.response.edit_message(
                content=f"✍️ Answer: '{self.answer}' | You: '{text_input.value}' | Score: {int(self.result * 100)}%",
                view=self,
            )
            self.stop()

        modal.on_submit = on_submit
        await interaction.response.send_modal(modal)

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class BudgetView(discord.ui.View):
    """Allocate a budget across categories using dropdowns."""
    def __init__(self, categories: list, budget: int, optimal: dict, timeout: int = 45):
        super().__init__(timeout=timeout)
        self.categories = categories
        self.budget = budget
        self.optimal = optimal
        self.allocations = {}
        self.result = None
        self.start_time = None
        self.user_id = None
        self._build_dropdowns()

    def _build_dropdowns(self):
        amounts = [0, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 350000, 500000]
        amounts = [a for a in amounts if a <= self.budget]
        for i, cat in enumerate(self.categories):
            select = discord.ui.Select(
                placeholder=f"Allocate for: {cat}",
                options=[discord.SelectOption(label=f"${a:,}", value=str(a)) for a in amounts],
                custom_id=f"budget_{i}",
            )
            select.callback = self._make_callback(cat)
            self.add_item(select)

    def _make_callback(self, cat: str):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            if self.result is not None:
                return
            for child in self.children:
                if isinstance(child, discord.ui.Select) and child.placeholder == f"Allocate for: {cat}":
                    self.allocations[cat] = int(child.values[0])
                    break
            await interaction.response.edit_message(view=self)
            if len(self.allocations) == len(self.categories):
                total = sum(self.allocations.values())
                if total > self.budget:
                    self.result = 0.2
                else:
                    score = 0
                    for cat in self.categories:
                        opt = self.optimal.get(cat, 0)
                        actual = self.allocations.get(cat, 0)
                        if opt > 0:
                            ratio = min(actual, opt) / max(actual, opt, 1)
                            score += ratio
                    self.result = min(1.0, score / len(self.categories))
                self.stop()
        return callback

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class RoutePlanView(discord.ui.View):
    """Plan a route by clicking stops in the optimal order."""
    def __init__(self, stops: list, optimal: list, timeout: int = 40):
        super().__init__(timeout=timeout)
        self.optimal = optimal
        self.selected = []
        self.result = None
        self.start_time = None
        self.user_id = None

        shuffled = stops.copy()
        while shuffled == optimal:
            random.shuffle(shuffled)

        for i, stop in enumerate(shuffled):
            btn = discord.ui.Button(label=stop[:80], style=discord.ButtonStyle.secondary, custom_id=f"route_{i}")
            btn.callback = self._make_callback(stop, btn)
            self.add_item(btn)

    def _make_callback(self, stop: str, btn: discord.ui.Button):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            if self.result is not None:
                return
            self.selected.append(stop)
            btn.disabled = True
            btn.style = discord.ButtonStyle.success
            await interaction.response.edit_message(view=self)
            if len(self.selected) == len(self.optimal):
                elapsed = time.time() - self.start_time
                correct = sum(1 for i, s in enumerate(self.selected) if i < len(self.optimal) and s == self.optimal[i])
                accuracy = correct / len(self.optimal)
                speed_bonus = max(0, 1.0 - elapsed / 30.0) * 0.2
                self.result = min(1.0, accuracy * 0.8 + speed_bonus)
                self.stop()
        return callback

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class RecipeBuildView(discord.ui.View):
    """Build a recipe by selecting ingredients in the correct order."""
    def __init__(self, ingredients: list, order: list, timeout: int = 40):
        super().__init__(timeout=timeout)
        self.order = order
        self.selected = []
        self.result = None
        self.start_time = None
        self.user_id = None

        shuffled = ingredients.copy()
        while shuffled == order:
            random.shuffle(shuffled)

        for i, ing in enumerate(shuffled):
            btn = discord.ui.Button(label=ing[:80], style=discord.ButtonStyle.secondary, custom_id=f"recipe_{i}")
            btn.callback = self._make_callback(ing, btn)
            self.add_item(btn)

    def _make_callback(self, ing: str, btn: discord.ui.Button):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            if self.result is not None:
                return
            self.selected.append(ing)
            btn.disabled = True
            btn.style = discord.ButtonStyle.success
            await interaction.response.edit_message(view=self)
            if len(self.selected) == len(self.order):
                elapsed = time.time() - self.start_time
                correct = sum(1 for i, s in enumerate(self.selected) if i < len(self.order) and s == self.order[i])
                accuracy = correct / len(self.order)
                speed_bonus = max(0, 1.0 - elapsed / 30.0) * 0.2
                self.result = min(1.0, accuracy * 0.8 + speed_bonus)
                self.stop()
        return callback

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class ShiftSimView(discord.ui.View):
    """Handle situations in priority order by clicking them sequentially."""
    def __init__(self, situations: list, optimal: list, timeout: int = 45):
        super().__init__(timeout=timeout)
        self.optimal = optimal
        self.selected = []
        self.result = None
        self.start_time = None
        self.user_id = None

        shuffled = situations.copy()
        while shuffled == optimal:
            random.shuffle(shuffled)

        for i, sit in enumerate(shuffled):
            btn = discord.ui.Button(label=sit[:80], style=discord.ButtonStyle.secondary, custom_id=f"shift_{i}")
            btn.callback = self._make_callback(sit, btn)
            self.add_item(btn)

    def _make_callback(self, sit: str, btn: discord.ui.Button):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            if self.result is not None:
                return
            self.selected.append(sit)
            btn.disabled = True
            btn.style = discord.ButtonStyle.success
            await interaction.response.edit_message(view=self)
            if len(self.selected) == len(self.optimal):
                elapsed = time.time() - self.start_time
                correct = sum(1 for i, s in enumerate(self.selected) if i < len(self.optimal) and s == self.optimal[i])
                accuracy = correct / len(self.optimal)
                speed_bonus = max(0, 1.0 - elapsed / 35.0) * 0.2
                self.result = min(1.0, accuracy * 0.8 + speed_bonus)
                self.stop()
        return callback

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class TriageView(discord.ui.View):
    """Triage patients by clicking them in priority order."""
    def __init__(self, patients: list, optimal: list, timeout: int = 40):
        super().__init__(timeout=timeout)
        self.optimal = optimal
        self.selected = []
        self.result = None
        self.start_time = None
        self.user_id = None

        shuffled = patients.copy()
        while shuffled == optimal:
            random.shuffle(shuffled)

        for i, patient in enumerate(shuffled):
            btn = discord.ui.Button(label=patient[:80], style=discord.ButtonStyle.secondary, custom_id=f"triage_{i}")
            btn.callback = self._make_callback(patient, btn)
            self.add_item(btn)

    def _make_callback(self, patient: str, btn: discord.ui.Button):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            if self.result is not None:
                return
            self.selected.append(patient)
            btn.disabled = True
            btn.style = discord.ButtonStyle.success
            await interaction.response.edit_message(view=self)
            if len(self.selected) == len(self.optimal):
                elapsed = time.time() - self.start_time
                correct = sum(1 for i, s in enumerate(self.selected) if i < len(self.optimal) and s == self.optimal[i])
                accuracy = correct / len(self.optimal)
                speed_bonus = max(0, 1.0 - elapsed / 30.0) * 0.2
                self.result = min(1.0, accuracy * 0.8 + speed_bonus)
                self.stop()
        return callback

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class DiagnosisView(discord.ui.View):
    """Diagnose a patient — pick the correct diagnosis from options."""
    def __init__(self, prompt: str, options: list, correct: str, reasoning: str = "", timeout: int = 25):
        super().__init__(timeout=timeout)
        self.correct = correct
        self.reasoning = reasoning
        self.result = None
        self.start_time = None
        self.user_id = None

        shuffled = options.copy()
        random.shuffle(shuffled)

        for i, opt in enumerate(shuffled):
            btn = discord.ui.Button(label=opt[:80], style=discord.ButtonStyle.primary, custom_id=f"diag_{i}")
            btn.callback = self._make_callback(opt)
            self.add_item(btn)

    def _make_callback(self, option: str):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            if self.result is not None:
                return
            elapsed = time.time() - self.start_time
            if option == self.correct:
                speed_bonus = max(0, 1.0 - elapsed / 15.0) * 0.3
                self.result = min(1.0, 0.7 + speed_bonus)
            else:
                self.result = 0.2
            for child in self.children:
                child.disabled = True
                if child.label == self.correct[:80]:
                    child.style = discord.ButtonStyle.success
                elif child.label == option[:80]:
                    child.style = discord.ButtonStyle.danger
            await interaction.response.edit_message(view=self)
            self.stop()
        return callback

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class NegotiationView(discord.ui.View):
    """Negotiate — pick the best response from options."""
    def __init__(self, prompt: str, options: list, correct: str, explanation: str = "", timeout: int = 25):
        super().__init__(timeout=timeout)
        self.correct = correct
        self.explanation = explanation
        self.result = None
        self.start_time = None
        self.user_id = None

        shuffled = options.copy()
        random.shuffle(shuffled)

        for i, opt in enumerate(shuffled):
            btn = discord.ui.Button(label=opt[:80], style=discord.ButtonStyle.primary, custom_id=f"neg_{i}")
            btn.callback = self._make_callback(opt)
            self.add_item(btn)

    def _make_callback(self, option: str):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            if self.result is not None:
                return
            elapsed = time.time() - self.start_time
            if option == self.correct:
                speed_bonus = max(0, 1.0 - elapsed / 15.0) * 0.3
                self.result = min(1.0, 0.7 + speed_bonus)
            else:
                self.result = 0.3
            for child in self.children:
                child.disabled = True
                if child.label == self.correct[:80]:
                    child.style = discord.ButtonStyle.success
                elif child.label == option[:80]:
                    child.style = discord.ButtonStyle.danger
            await interaction.response.edit_message(view=self)
            self.stop()
        return callback

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class CategorizeView(discord.ui.View):
    """Categorize items using dropdowns (like SortView but with named categories)."""
    def __init__(self, items: list, categories: list, timeout: int = 50):
        super().__init__(timeout=timeout)
        self.items = items
        self.categories = categories
        self.answers = {}
        self.result = None
        self.start_time = None
        self.user_id = None
        self._build()

    def _build(self):
        unique_cats = list(set(self.categories))
        for i, item in enumerate(self.items):
            select = discord.ui.Select(
                placeholder=f"Classify: {item[:50]}",
                options=[discord.SelectOption(label=c[:100], value=c) for c in unique_cats],
                custom_id=f"cat_{i}",
            )
            select.callback = self._make_callback(item)
            self.add_item(select)

    def _make_callback(self, item: str):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your minigame!", ephemeral=True)
                return
            if self.result is not None:
                return
            for child in self.children:
                if isinstance(child, discord.ui.Select) and child.placeholder == f"Classify: {item[:50]}":
                    self.answers[item] = child.values[0]
                    break
            await interaction.response.edit_message(view=self)
            if len(self.answers) == len(self.items):
                elapsed = time.time() - self.start_time
                correct = sum(1 for i, item in enumerate(self.items) if self.answers.get(item) == self.categories[i])
                accuracy = correct / len(self.items)
                speed_bonus = max(0, 1.0 - elapsed / 40.0) * 0.2
                self.result = min(1.0, accuracy * 0.8 + speed_bonus)
                self.stop()
        return callback

    async def on_timeout(self):
        if self.result is None:
            self.result = 0.0


class MultiStageView(discord.ui.View):
    """Run multiple sub-minigames in sequence, averaging scores."""
    def __init__(self, stages: list, timeout: int = 90):
        super().__init__(timeout=timeout)
        self.stages = stages
        self.current_stage = 0
        self.scores = []
        self.result = None
        self.start_time = None
        self.user_id = None

    async def run_stage(self, interaction: discord.Interaction):
        if self.current_stage >= len(self.stages):
            self.result = sum(self.scores) / len(self.scores) if self.scores else 0.0
            self.stop()
            return

        stage = self.stages[self.current_stage]
        stage_type = stage.get("type", "quick_pick")
        stage_score = await run_minigame_sub(interaction, stage_type, stage, self.user_id, self.start_time)
        self.scores.append(stage_score)
        self.current_stage += 1
        await self.run_stage(interaction)


# ═══════════════════════════════════════════════════════════════
# Main dispatcher — runs the appropriate minigame for a job
# ═══════════════════════════════════════════════════════════════

async def run_minigame(interaction: discord.Interaction, job_id: str, user_id: int) -> float:
    """Run the minigame for a specific job. Returns performance score 0.0–1.0."""
    mg_type = get_minigame_type(job_id)
    start_time = time.time()

    # Try procedural generation first for unique scenarios each playthrough
    content = proc_generate(job_id, mg_type)
    
    # Fall back to static content if generator doesn't support this type
    if content is None:
        content = get_minigame_content(job_id, mg_type)

    return await _dispatch_minigame(interaction, mg_type, content, user_id, start_time)


async def run_minigame_sub(interaction: discord.Interaction, mg_type: str, content: dict, user_id: int, start_time: float) -> float:
    """Run a sub-minigame (used by MultiStageView)."""
    return await _dispatch_minigame(interaction, mg_type, content, user_id, start_time)


async def _dispatch_minigame(interaction: discord.Interaction, mg_type: str, content: dict, user_id: int, start_time: float) -> float:
    """Dispatch to the correct minigame view based on type."""

    if mg_type == "sequence":
        items = content.get("items", content.get("sequence", GENERIC["sequence"]))
        order = content.get("order", items)
        view = SequenceView(items, order)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"📋 **{content.get('prompt', 'Arrange in the correct order:')}**\nClick items in the correct sequence:", view=view)
        await view.wait()
        return view.result or 0.0

    elif mg_type == "sort":
        items = content.get("items", GENERIC["sort"])
        categories = content.get("categories", content.get("order", []))
        if not categories:
            order = content.get("order", items)
            view = SequenceView(items, order)
        else:
            view = SortView(items, categories)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"📂 **{content.get('prompt', 'Sort the items:')}**", view=view)
        await view.wait()
        return view.result or 0.0

    elif mg_type == "quick_pick":
        options = content.get("options", GENERIC["quick_pick"])
        correct = content.get("correct", options[0] if options else "")
        view = QuickPickView(content.get("prompt", "Pick the correct answer:"), options, correct)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"❓ **{content.get('prompt', 'Pick the correct answer:')}**", view=view)
        await view.wait()
        return view.result or 0.0

    elif mg_type == "memory":
        sequence = content.get("sequence", GENERIC["memory"])
        view = MemoryView(sequence)
        view.user_id = user_id
        view.start_time = start_time
        await view.start(interaction, f"🧠 **{content.get('prompt', 'Memorize this sequence:')}**\n\n" + " → ".join(sequence))
        await view.wait()
        return view.result or 0.0

    elif mg_type == "timing":
        beats = content.get("beats", 4)
        view = TimingView(beats)
        view.user_id = user_id
        view.start_time = start_time
        bar = view._render_bar()
        await interaction.followup.send(content=f"⏱️ **{content.get('prompt', 'Click when the █ hits the ▓ target zone!')}**\n{bar}", view=view)
        asyncio.create_task(view._bar_loop())
        await view.wait()
        return view.result or 0.0

    elif mg_type == "match_pairs":
        pairs = content.get("pairs", GENERIC["match_pairs"])
        view = MatchPairsView(pairs)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"🔗 **{content.get('prompt', 'Match each pair:')}**", view=view)
        await view.wait()
        return view.result or 0.0

    elif mg_type == "spot_error":
        correct_seq = content.get("correct_sequence", content.get("correct_code", content.get("expected", "").split("\n")))
        presented_seq = content.get("presented_sequence", content.get("buggy_code", content.get("actual", "").split("\n")))
        view = SpotErrorView(correct_seq, presented_seq)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(
            content=f"🔍 **{content.get('prompt', 'Find the error!')}**\nClick the item that's wrong:",
            view=view,
        )
        await view.wait()
        return view.result or 0.0

    elif mg_type == "pattern":
        seq = content.get("sequence", GENERIC["pattern"])
        answer = content.get("answer", "")
        view = PatternView(seq, str(answer))
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"🔢 **{content.get('prompt', 'Complete the pattern:')}**\n" + " → ".join(str(s) for s in seq))
        await view.run(interaction, content.get("prompt", "Complete the pattern:"))
        await view.wait()
        return view.result or 0.0

    elif mg_type == "precision":
        target = content.get("target", 50)
        tolerance = content.get("tolerance", 2)
        view = PrecisionView(target, tolerance)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"🎯 **{content.get('prompt', 'Stop at the target!')}**\nTarget: {target} (±{tolerance})")
        asyncio.create_task(view._counter_loop())
        await view.wait()
        return view.result or 0.0

    elif mg_type == "combo_lock":
        pins = content.get("pins", GENERIC["combo_lock"])
        max_val = content.get("max_val", 9)
        view = ComboLockView(pins, max_val)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(
            content=f"🔓 **{content.get('prompt', 'Crack the combination lock!')}**\nUse the buttons to set each pin, then click Unlock.\nPins: {len(pins)} | Range: 0-{max_val}",
            view=view,
        )
        await view.wait()
        return view.result or 0.0

    elif mg_type == "speed_run":
        tasks = content.get("tasks", GENERIC["speed_run"])
        view = SpeedRunView(tasks)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"⚡ **{content.get('prompt', 'Complete all tasks fast!')}**\nClick each task button as it appears!", view=view)
        await view.wait()
        return view.result or 0.0

    elif mg_type == "assembly":
        parts = content.get("parts", GENERIC["assembly"])
        view = AssemblyView(parts)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"🔧 **{content.get('prompt', 'Assemble in the correct order!')}**\nSelect parts in dependency order:", view=view)
        await view.wait()
        return view.result or 0.0

    elif mg_type == "typing_race":
        phrase = content.get("phrase", GENERIC["typing_race"][0])
        view = TypingRaceView(phrase)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(
            content=f"⌨️ **{content.get('prompt', 'Type the phrase fast and accurately!')}**\n```\n{phrase}\n```",
            view=view,
        )
        await view.wait()
        return view.result or 0.0

    elif mg_type == "math":
        answer = content.get("answer", 0)
        formula = content.get("formula", "")
        view = MathView(answer, formula)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"🧮 **{content.get('prompt', 'Solve the math problem:')}**")
        await view.wait()
        return view.result or 0.0

    elif mg_type == "fill_blank":
        answer = content.get("answer", "")
        context = content.get("context", "")
        view = FillBlankView(answer, context)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"✍️ **{content.get('prompt', 'Fill in the blank:')}**")
        await view.wait()
        return view.result or 0.0

    elif mg_type == "budget":
        categories = content.get("categories", [])
        budget = content.get("budget", 10000)
        optimal = content.get("optimal", {})
        view = BudgetView(categories, budget, optimal)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"💰 **{content.get('prompt', 'Allocate the budget:')}**\nTotal budget: ${budget:,}")
        await view.wait()
        return view.result or 0.0

    elif mg_type == "route_plan":
        stops = content.get("stops", content.get("optimal", []))
        optimal = content.get("optimal", stops)
        view = RoutePlanView(stops, optimal)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"🗺️ **{content.get('prompt', 'Plan the best route!')}**\nClick stops in the most efficient order:", view=view)
        await view.wait()
        return view.result or 0.0

    elif mg_type == "recipe_build":
        ingredients = content.get("ingredients", content.get("order", []))
        order = content.get("order", ingredients)
        view = RecipeBuildView(ingredients, order)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"👨‍🍳 **{content.get('prompt', 'Build the recipe in order!')}**\nClick ingredients in the correct sequence:", view=view)
        await view.wait()
        return view.result or 0.0

    elif mg_type == "shift_sim":
        situations = content.get("situations", [])
        optimal = content.get("optimal", situations)
        view = ShiftSimView(situations, optimal)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"📋 **{content.get('prompt', 'Handle situations in priority order!')}**\nClick by priority:", view=view)
        await view.wait()
        return view.result or 0.0

    elif mg_type == "triage":
        patients = content.get("patients", content.get("optimal", []))
        optimal = content.get("optimal", patients)
        view = TriageView(patients, optimal)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"🏥 **{content.get('prompt', 'Triage patients by priority!')}**\nClick patients in treatment order:", view=view)
        await view.wait()
        return view.result or 0.0

    elif mg_type == "diagnosis":
        options = content.get("options", [])
        correct = content.get("correct", options[0] if options else "")
        view = DiagnosisView(content.get("prompt", "Diagnose the patient:"), options, correct, content.get("reasoning", ""))
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"🩺 **{content.get('prompt', 'Diagnose the patient:')}**")
        await view.wait()
        return view.result or 0.0

    elif mg_type == "negotiation":
        options = content.get("options", [])
        correct = content.get("correct", options[0] if options else "")
        view = NegotiationView(content.get("prompt", "Negotiate:"), options, correct, content.get("explanation", ""))
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"🤝 **{content.get('prompt', 'Negotiate the best outcome:')}**")
        await view.wait()
        return view.result or 0.0

    elif mg_type == "categorize":
        items = content.get("items", [])
        categories = content.get("categories", [])
        view = CategorizeView(items, categories)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"🏷️ **{content.get('prompt', 'Classify each item:')}**", view=view)
        await view.wait()
        return view.result or 0.0

    elif mg_type == "multi_stage":
        stages = content.get("stages", [])
        view = MultiStageView(stages)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"🎭 **{content.get('prompt', 'Multi-stage challenge!')}**\nComplete each stage in sequence...")
        await view.run_stage(interaction)
        await view.wait()
        return view.result or 0.0

    else:
        # Fallback to quick_pick
        options = content.get("options", GENERIC["quick_pick"])
        correct = content.get("correct", options[0] if options else "")
        view = QuickPickView(content.get("prompt", "Pick the correct answer:"), options, correct)
        view.user_id = user_id
        view.start_time = start_time
        await interaction.followup.send(content=f"❓ **{content.get('prompt', 'Pick the correct answer:')}**", view=view)
        await view.wait()
        return view.result or 0.0
