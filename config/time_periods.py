DAY_NIGHT_INTERVAL = 1800  # 30 min real = 1 game hour shift (synced with weather)

TIME_PERIODS = {
    "dawn": {
        "name": "🌅 Dawn", "emoji": "🌅",
        "description": "The first light of day. A time of new beginnings.",
        "effects": {"energy_regen": 2, "fish_luck": 1.3, "crime_success": 0.8, "encounter_chance": 1.1},
        "game_hours": (5, 8),
    },
    "morning": {
        "name": "☀️ Morning", "emoji": "☀️",
        "description": "Bright and fresh. The world is awake and busy.",
        "effects": {"energy_regen": 1, "fish_luck": 1.0, "crime_success": 0.9, "encounter_chance": 1.0, "work_pay": 1.1},
        "game_hours": (8, 12),
    },
    "noon": {
        "name": "🌞 Midday", "emoji": "🌞",
        "description": "The sun is high. Energy is at its peak.",
        "effects": {"energy_regen": 0, "fish_luck": 0.8, "crime_success": 0.7, "encounter_chance": 0.9, "work_pay": 1.15},
        "game_hours": (12, 14),
    },
    "afternoon": {
        "name": "🌤️ Afternoon", "emoji": "🌤️",
        "description": "The day winds down. A good time for exploration.",
        "effects": {"energy_regen": 0, "fish_luck": 1.1, "crime_success": 0.9, "encounter_chance": 1.1, "work_pay": 1.0},
        "game_hours": (14, 18),
    },
    "evening": {
        "name": "🌆 Evening", "emoji": "🌆",
        "description": "The golden hour. Shadows lengthen across the land.",
        "effects": {"energy_regen": 1, "fish_luck": 1.2, "crime_success": 1.1, "encounter_chance": 1.2, "work_pay": 0.95},
        "game_hours": (18, 21),
    },
    "night": {
        "name": "🌙 Night", "emoji": "🌙",
        "description": "Darkness falls. The streets belong to the bold.",
        "effects": {"energy_regen": 3, "fish_luck": 0.6, "crime_success": 1.3, "encounter_chance": 1.4, "work_pay": 0.8},
        "game_hours": (21, 24),
    },
    "midnight": {
        "name": "🌑 Midnight", "emoji": "🌑",
        "description": "The witching hour. Strange things happen now.",
        "effects": {"energy_regen": 4, "fish_luck": 0.4, "crime_success": 1.5, "encounter_chance": 1.6, "work_pay": 0.6, "rare_find_chance": 1.5},
        "game_hours": (0, 5),
    },
}
