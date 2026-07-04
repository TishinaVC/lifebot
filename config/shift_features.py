"""
Phase 5 Deep Features configuration:
- Quality grades (S/A/B/C/D/F)
- Streak combo multipliers
- Random shift events
- Boss shift configuration
- Progressive difficulty scaling
"""

# ═══════════════════════════════════════════════════════════════
# Quality Grades — mapped from performance score (0.0–1.0)
# ═══════════════════════════════════════════════════════════════

GRADE_THRESHOLDS = [
    (0.95, "S", "🌟", "Flawless! Legendary performance!"),
    (0.85, "A", "🥇", "Excellent work! Outstanding effort!"),
    (0.70, "B", "🥈", "Good job! Solid performance."),
    (0.55, "C", "🥉", "Decent shift. Room for improvement."),
    (0.35, "D", "⚠️", "Below average. Try harder next time."),
    (0.00, "F", "❌", "Failed shift. Better luck next time."),
]

GRADE_ORDER = {"S": 5, "A": 4, "B": 3, "C": 2, "D": 1, "F": 0}


def get_grade(performance: float) -> tuple:
    """Convert performance score to (letter, emoji, comment)."""
    for threshold, letter, emoji, comment in GRADE_THRESHOLDS:
        if performance >= threshold:
            return letter, emoji, comment
    return "F", "❌", "Failed shift."


def is_grade_better(new_grade: str, old_grade: str) -> bool:
    """Check if new_grade is better than old_grade."""
    return GRADE_ORDER.get(new_grade, 0) > GRADE_ORDER.get(old_grade, 0)


# ═══════════════════════════════════════════════════════════════
# Streak Combos — consecutive shifts with B or better
# ═══════════════════════════════════════════════════════════════

STREAK_GRADE_THRESHOLD = "B"  # B or better maintains streak

STREAK_MULTIPLIERS = [
    (1, 1.00, "No streak bonus"),
    (3, 1.10, "🔥 3-shift streak! +10% pay"),
    (5, 1.20, "🔥🔥 5-shift streak! +20% pay"),
    (10, 1.35, "🔥🔥🔥 10-shift streak! +35% pay"),
    (15, 1.50, "⚡ 15-shift streak! +50% pay"),
    (20, 1.75, "⚡⚡ 20-shift streak! +75% pay"),
    (30, 2.00, "💫 30-shift streak! DOUBLE PAY!"),
]


def get_streak_multiplier(streak: int) -> tuple:
    """Get (multiplier, description) for current streak."""
    result = (1.0, "No streak bonus")
    for threshold, mult, desc in STREAK_MULTIPLIERS:
        if streak >= threshold:
            result = (mult, desc)
    return result


# ═══════════════════════════════════════════════════════════════
# Random Shift Events — 15% chance per shift
# ═══════════════════════════════════════════════════════════════

SHIFT_EVENT_CHANCE = 0.15

SHIFT_EVENTS = [
    {
        "id": "overtime",
        "name": "📋 Overtime",
        "emoji": "📋",
        "description": "Your boss asked you to work overtime — extra pay if you do well!",
        "pay_mult": 1.50,
        "xp_mult": 1.20,
        "stat_cost_mult": 1.30,
        "min_performance": 0.0,
    },
    {
        "id": "inspector",
        "name": "👁️ Surprise Inspection",
        "emoji": "👁️",
        "description": "A surprise inspection is happening — perform well for a big bonus!",
        "pay_mult": 1.30,
        "xp_mult": 1.50,
        "stat_cost_mult": 1.0,
        "min_performance": 0.5,
    },
    {
        "id": "rush",
        "name": "⚡ Rush Hour",
        "emoji": "⚡",
        "description": "It's rush hour — harder work but double pay!",
        "pay_mult": 2.00,
        "xp_mult": 1.0,
        "stat_cost_mult": 1.50,
        "min_performance": 0.0,
    },
    {
        "id": "mentor",
        "name": "🎓 Mentor Duty",
        "emoji": "🎓",
        "description": "You're training a new hire — extra XP for good performance!",
        "pay_mult": 1.0,
        "xp_mult": 2.00,
        "stat_cost_mult": 0.80,
        "min_performance": 0.0,
    },
    {
        "id": "short_staffed",
        "name": "😷 Short-Staffed",
        "emoji": "😷",
        "description": "Half the team called in sick — more work but bigger payout!",
        "pay_mult": 1.40,
        "xp_mult": 1.30,
        "stat_cost_mult": 1.40,
        "min_performance": 0.0,
    },
    {
        "id": "vip",
        "name": "⭐ VIP Client",
        "emoji": "⭐",
        "description": "A VIP is visiting — nail this for triple XP!",
        "pay_mult": 1.20,
        "xp_mult": 3.00,
        "stat_cost_mult": 1.10,
        "min_performance": 0.6,
    },
    {
        "id": "equipment_fail",
        "name": "🔧 Equipment Failure",
        "emoji": "🔧",
        "description": "Your equipment is acting up — tougher shift, but hazard pay!",
        "pay_mult": 1.60,
        "xp_mult": 1.10,
        "stat_cost_mult": 1.20,
        "min_performance": 0.0,
    },
    {
        "id": "good_mood",
        "name": "😊 Great Day",
        "emoji": "😊",
        "description": "Everything's going your way — reduced fatigue, normal pay!",
        "pay_mult": 1.10,
        "xp_mult": 1.10,
        "stat_cost_mult": 0.60,
        "min_performance": 0.0,
    },
]


def roll_shift_event() -> dict | None:
    """Roll for a random shift event. Returns event dict or None."""
    import random
    if random.random() < SHIFT_EVENT_CHANCE:
        return random.choice(SHIFT_EVENTS)
    return None


# ═══════════════════════════════════════════════════════════════
# Progressive Difficulty — scales with job level
# ═══════════════════════════════════════════════════════════════

def get_difficulty_multiplier(job_level: int) -> float:
    """Get difficulty multiplier based on job level.
    Level 1 = 1.0 (normal), scales up to 1.5 at level 10+.
    This reduces performance score slightly for higher-level jobs."""
    if job_level <= 1:
        return 1.0
    return min(1.5, 1.0 + (job_level - 1) * 0.05)


def apply_difficulty(performance: float, job_level: int) -> float:
    """Apply difficulty scaling to performance score."""
    diff = get_difficulty_multiplier(job_level)
    if diff <= 1.0:
        return performance
    # Reduce performance by difficulty factor (so level 10 is ~5% harder)
    penalty = (diff - 1.0) * 0.3  # 30% of difficulty factor as penalty
    return max(0.0, performance * (1.0 - penalty))


# ═══════════════════════════════════════════════════════════════
# Boss Shifts — rare special shifts with big rewards
# ═══════════════════════════════════════════════════════════════

BOSS_SHIFT_CHANCE = 0.05  # 5% chance per shift

BOSS_SHIFT_CONFIG = {
    "pay_mult": 3.00,
    "xp_mult": 2.50,
    "stat_cost_mult": 1.50,
    "min_performance": 0.5,  # Must score at least 50% to win
    "name": "👹 Boss Shift",
    "emoji": "👹",
    "description": "Your boss is personally evaluating you — nail this for a massive bonus!",
    "fail_description": "Your boss wasn't impressed. No bonus, but you still get base pay.",
    "win_description": "Your boss is impressed! Massive bonus earned!",
}


def roll_boss_shift() -> bool:
    """Roll for a boss shift. Returns True if boss shift triggers."""
    import random
    return random.random() < BOSS_SHIFT_CHANCE
