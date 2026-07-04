"""
Co-op job shift configuration.
Players can invite others to join a co-op shift for bonus rewards.
"""

COOP_MAX_PLAYERS = 4
COOP_JOIN_TIMEOUT = 60  # seconds to wait for players to join
COOP_MIN_PLAYERS = 2   # need at least 2 to start

# Team bonus: combined performance gets multiplied by this factor
# More players = higher bonus potential
COOP_TEAM_BONUS = {
    2: 1.15,  # 2 players = +15% each
    3: 1.25,  # 3 players = +25% each
    4: 1.40,  # 4 players = +40% each
}

# Co-op shift event chance (higher than solo)
COOP_EVENT_CHANCE = 0.25

COOP_EVENTS = [
    {"name": "🎯 Team Target", "description": "Your team has a shared target — work together for a big bonus!", "pay_mult": 1.30, "xp_mult": 1.30},
    {"name": "🔄 Shift Swap", "description": "Roles are rotating — adaptability is key!", "pay_mult": 1.20, "xp_mult": 1.50},
    {"name": "📊 Group Review", "description": "Your team is being evaluated together — don't let anyone down!", "pay_mult": 1.50, "xp_mult": 1.20},
    {"name": "⚡ Crunch Time", "description": "Deadline moved up — everyone needs to perform!", "pay_mult": 1.40, "xp_mult": 1.40},
]

# Bonus for all players getting B or better
COOP_ALL_GOOD_BONUS = 1.10  # +10% if everyone gets B+

# Penalty if anyone fails (performance = 0)
COOP_FAIL_PENALTY = 0.85  # -15% for everyone if anyone fails
