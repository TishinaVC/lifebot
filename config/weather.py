WEATHER_INTERVAL = 1800  # 30 minutes

WEATHER_STATES = {
    "sunny": {
        "name": "☀️ Sunny", "emoji": "☀️",
        "effects": {"energy_decay_mult": 0.8, "hygiene_decay_mult": 1.2, "work_pay_mult": 1.1, "crime_success_mult": 1.0, "fish_luck_mult": 1.1, "rare_find_chance": 1.0},
        "description": "Clear skies and warm sunshine.",
        "weight": 25,
    },
    "cloudy": {
        "name": "☁️ Cloudy", "emoji": "☁️",
        "effects": {"energy_decay_mult": 1.0, "hygiene_decay_mult": 1.0, "work_pay_mult": 1.0, "crime_success_mult": 1.05, "fish_luck_mult": 1.0, "rare_find_chance": 1.0},
        "description": "Overcast skies, mild weather.",
        "weight": 20,
    },
    "rainy": {
        "name": "🌧️ Rainy", "emoji": "🌧️",
        "effects": {"energy_decay_mult": 1.1, "hygiene_decay_mult": 1.5, "work_pay_mult": 0.9, "crime_success_mult": 1.1, "fish_luck_mult": 1.3, "rare_find_chance": 1.0},
        "description": "Rain pours down, soaking everything.",
        "weight": 15,
    },
    "stormy": {
        "name": "⛈️ Stormy", "emoji": "⛈️",
        "effects": {"energy_decay_mult": 1.3, "hygiene_decay_mult": 2.0, "work_pay_mult": 0.7, "crime_success_mult": 1.2, "fish_luck_mult": 1.5, "rare_find_chance": 1.2},
        "description": "Thunder and lightning crack across the sky!",
        "weight": 8,
    },
    "snowy": {
        "name": "🌨️ Snowy", "emoji": "🌨️",
        "effects": {"energy_decay_mult": 1.4, "hygiene_decay_mult": 1.0, "work_pay_mult": 0.8, "crime_success_mult": 0.9, "fish_luck_mult": 0.7, "rare_find_chance": 1.1},
        "description": "Snow blankets the ground, biting cold.",
        "weight": 8,
    },
    "foggy": {
        "name": "🌫️ Foggy", "emoji": "🌫️",
        "effects": {"energy_decay_mult": 1.1, "hygiene_decay_mult": 1.0, "work_pay_mult": 0.95, "crime_success_mult": 1.15, "fish_luck_mult": 0.8, "rare_find_chance": 1.3},
        "description": "Thick fog obscures vision.",
        "weight": 10,
    },
    "windy": {
        "name": "💨 Windy", "emoji": "💨",
        "effects": {"energy_decay_mult": 1.15, "hygiene_decay_mult": 1.3, "work_pay_mult": 0.95, "crime_success_mult": 1.05, "fish_luck_mult": 0.9, "rare_find_chance": 1.0},
        "description": "Strong winds whip through the streets.",
        "weight": 10,
    },
    "heatwave": {
        "name": "🥵 Heatwave", "emoji": "🥵",
        "effects": {"energy_decay_mult": 1.6, "hygiene_decay_mult": 1.8, "work_pay_mult": 0.8, "crime_success_mult": 1.0, "fish_luck_mult": 0.6, "rare_find_chance": 0.8},
        "description": "Blistering heat bakes the city!",
        "weight": 4,
    },
}
