"""
Job reputation system — per-category standing that grows with work.
Higher reputation in a category gives pay/XP bonuses for jobs in that category.

Reputation is earned by working jobs in a category:
- Grade S: +5 rep, Grade A: +3, Grade B: +2, Grade C: +1, D/F: +0
- Boss shift win: +3 bonus rep
- Streak milestone (5, 10, 20): +2 bonus rep

Reputation tiers and benefits:
- Novice (0-9): no bonus
- Apprentice (10-24): +5% pay
- Journeyman (25-49): +10% pay, +5% XP
- Expert (50-99): +15% pay, +10% XP
- Master (100-199): +20% pay, +15% XP, -5% stat cost
- Legend (200+): +25% pay, +20% XP, -10% stat cost
"""

JOB_REP_TIERS = [
    (200, "Legend", "👑", {"pay_mult": 1.25, "xp_mult": 1.20, "stat_cost_mult": 0.90}),
    (100, "Master", "🏆", {"pay_mult": 1.20, "xp_mult": 1.15, "stat_cost_mult": 0.95}),
    (50, "Expert", "⭐", {"pay_mult": 1.15, "xp_mult": 1.10, "stat_cost_mult": 1.0}),
    (25, "Journeyman", "🔧", {"pay_mult": 1.10, "xp_mult": 1.05, "stat_cost_mult": 1.0}),
    (10, "Apprentice", "📚", {"pay_mult": 1.05, "xp_mult": 1.0, "stat_cost_mult": 1.0}),
    (0, "Novice", "🌱", {"pay_mult": 1.0, "xp_mult": 1.0, "stat_cost_mult": 1.0}),
]

GRADE_REP_GAIN = {"S": 5, "A": 3, "B": 2, "C": 1, "D": 0, "F": 0}
BOSS_REP_BONUS = 3
STREAK_MILESTONE_REP = {5: 2, 10: 2, 20: 2, 30: 3}


def get_rep_tier(rep: int) -> tuple:
    """Get (threshold, name, emoji, benefits) for a reputation value."""
    for threshold, name, emoji, benefits in JOB_REP_TIERS:
        if rep >= threshold:
            return threshold, name, emoji, benefits
    return 0, "Novice", "🌱", {"pay_mult": 1.0, "xp_mult": 1.0, "stat_cost_mult": 1.0}


def get_rep_gain(grade: str, boss_win: bool = False, new_streak: int = 0) -> int:
    """Calculate reputation gain from a shift."""
    gain = GRADE_REP_GAIN.get(grade, 0)
    if boss_win:
        gain += BOSS_REP_BONUS
    if new_streak in STREAK_MILESTONE_REP:
        gain += STREAK_MILESTONE_REP[new_streak]
    return gain
