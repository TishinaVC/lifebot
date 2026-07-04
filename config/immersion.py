COOKING_RECIPES = {
    "grilled_fish": {
        "name": "🐟 Grilled Fish", "emoji": "🐟",
        "ingredients": {"fish": 1, "firewood": 1},
        "effects": {"hunger": 35, "energy": 10},
        "buff": {"name": "Well Fed", "stat": "energy_regen", "value": 2, "duration": 1800},
        "description": "A perfectly grilled fish. Restores energy over time.",
    },
    "herbal_soup": {
        "name": "🍲 Herbal Soup", "emoji": "🍲",
        "ingredients": {"herbs": 2, "water": 1, "firewood": 1},
        "effects": {"hunger": 25, "health": 15},
        "buff": {"name": "Healing Touch", "stat": "health_regen", "value": 1, "duration": 1200},
        "description": "A warming soup that slowly restores health.",
    },
    "trail_mix": {
        "name": "🥜 Trail Mix", "emoji": "🥜",
        "ingredients": {"herbs": 1, "stone": 0},
        "effects": {"hunger": 15, "energy": 5},
        "buff": {"name": "Trail Energy", "stat": "energy", "value": 5, "duration": 600},
        "description": "A quick snack for explorers on the go.",
    },
    "feast": {
        "name": "🍖 Grand Feast", "emoji": "🍖",
        "ingredients": {"fish": 2, "herbs": 3, "firewood": 2, "water": 1},
        "effects": {"hunger": 60, "health": 20, "energy": 25, "hygiene": 5},
        "buff": {"name": "Feast of Kings", "stat": "all_regen", "value": 3, "duration": 3600},
        "description": "A magnificent meal that restores everything and grants powerful regeneration.",
    },
    "energy_bar": {
        "name": "🍫 Energy Bar", "emoji": "🍫",
        "ingredients": {"herbs": 1, "cloth": 0},
        "effects": {"energy": 20},
        "buff": {"name": "Sugar Rush", "stat": "work_pay", "value": 1.15, "duration": 900},
        "description": "A quick energy boost that also improves work performance temporarily.",
    },
    "stone_soup": {
        "name": "🪨 Stone Soup", "emoji": "🪨",
        "ingredients": {"stone": 1, "water": 1, "firewood": 1},
        "effects": {"hunger": 10, "health": 5},
        "buff": {"name": "Humble Meal", "stat": "hygiene_regen", "value": 1, "duration": 600},
        "description": "A humble soup. Not much, but it warms the soul.",
    },
    "spicy_stew": {
        "name": "🌶️ Spicy Stew", "emoji": "🌶️",
        "ingredients": {"fish": 1, "herbs": 2, "firewood": 1},
        "effects": {"hunger": 40, "energy": 15, "health": 5},
        "buff": {"name": "Spicy Fire", "stat": "crime_success", "value": 1.1, "duration": 1200},
        "description": "A fiery stew that makes you feel bold and daring.",
    },
    "medley": {
        "name": "🍱 Wild Medley", "emoji": "🍱",
        "ingredients": {"herbs": 2, "fish": 1, "clay": 0},
        "effects": {"hunger": 30, "health": 10, "hygiene": 5},
        "buff": {"name": "Forager's Luck", "stat": "luck", "value": 5, "duration": 1800},
        "description": "A mix of wild ingredients. Improves your luck while it lasts.",
    },
}

BUFF_TYPES = {
    "energy_regen": {"name": "⚡ Energy Regeneration", "description": "Restores energy over time"},
    "health_regen": {"name": "❤️ Health Regeneration", "description": "Restores health over time"},
    "hygiene_regen": {"name": "🧼 Hygiene Regeneration", "description": "Restores hygiene over time"},
    "all_regen": {"name": "✨ Total Regeneration", "description": "Restores all stats over time"},
    "energy": {"name": "⚡ Energy Boost", "description": "Extra energy from activities"},
    "work_pay": {"name": "💼 Work Bonus", "description": "Increased work pay"},
    "crime_success": {"name": "🦹 Criminal Confidence", "description": "Increased crime success rate"},
    "luck": {"name": "🍀 Lucky", "description": "Increased luck for all activities"},
    "rare_find": {"name": "💎 Treasure Sense", "description": "Increased chance of rare finds"},
    "energy_drain": {"name": "🥶 Energy Drain", "description": "Loses extra energy over time"},
    "health_drain": {"name": "🤒 Health Drain", "description": "Loses health over time"},
    "hygiene_drain": {"name": "🤢 Hygiene Drain", "description": "Loses extra hygiene over time"},
}

WEATHER_BUFFS = {
    "rainy": {
        "buff_name": "Soaked",
        "stat": "hygiene_drain",
        "value": 3,
        "duration": 600,
        "chance": 0.15,
        "message": "🌧️ You're soaked from the rain! Extra hygiene drain for 10 min.",
    },
    "stormy": {
        "buff_name": "Drenched",
        "stat": "hygiene_drain",
        "value": 5,
        "duration": 900,
        "chance": 0.25,
        "message": "⛈️ The storm has left you drenched! Severe hygiene drain for 15 min.",
    },
    "snowy": {
        "buff_name": "Frostbite",
        "stat": "energy_drain",
        "value": 3,
        "duration": 900,
        "chance": 0.20,
        "message": "🌨️ The biting cold gives you frostbite! Extra energy drain for 15 min.",
    },
    "windy": {
        "buff_name": "Windchill",
        "stat": "energy_drain",
        "value": 2,
        "duration": 600,
        "chance": 0.12,
        "message": "💨 The wind chills you to the bone! Mild energy drain for 10 min.",
    },
    "heatwave": {
        "buff_name": "Heatstroke",
        "stat": "health_drain",
        "value": 2,
        "duration": 900,
        "chance": 0.25,
        "message": "🥵 The heat is overwhelming! You're suffering from heatstroke — health drain for 15 min.",
    },
    "foggy": {
        "buff_name": "Chilled",
        "stat": "energy_drain",
        "value": 1,
        "duration": 600,
        "chance": 0.10,
        "message": "🌫️ The damp fog chills you slightly. Mild energy drain for 10 min.",
    },
}

FACTIONS = {
    "merchants": {
        "name": "🏪 Merchant Guild", "emoji": "🏪",
        "description": "Traders and shopkeepers. High standing means better prices.",
        "benefits": {
            10: {"pay_mult": 1.05, "desc": "5% better sell prices"},
            25: {"pay_mult": 1.10, "desc": "10% better sell prices"},
            50: {"pay_mult": 1.20, "desc": "20% better sell prices + access to rare goods"},
        },
        "activities": {"trade": 2, "buy": 1, "sell": 1},
    },
    "fishers": {
        "name": "🎣 Angler's Club", "emoji": "🎣",
        "description": "The fishing community. High standing improves your catches.",
        "benefits": {
            10: {"fish_luck": 1.1, "desc": "10% better fish catches"},
            25: {"fish_luck": 1.25, "desc": "25% better fish catches"},
            50: {"fish_luck": 1.5, "desc": "50% better fish catches + rare fish chance"},
        },
        "activities": {"fish": 2},
    },
    "miners": {
        "name": "⛏️ Miners Union", "emoji": "⛏️",
        "description": "The mining brotherhood. High standing means richer yields.",
        "benefits": {
            10: {"mine_luck": 1.1, "desc": "10% better mining yields"},
            25: {"mine_luck": 1.25, "desc": "25% better mining yields"},
            50: {"mine_luck": 1.5, "desc": "50% better mining yields + rare ore chance"},
        },
        "activities": {"mine": 2},
    },
    "explorers": {
        "name": "🧭 Explorer Society", "emoji": "🧭",
        "description": "Adventurers and pathfinders. High standing reveals hidden locations.",
        "benefits": {
            10: {"encounter_chance": 1.1, "desc": "10% more encounters"},
            25: {"encounter_chance": 1.25, "desc": "25% more encounters + better loot"},
            50: {"encounter_chance": 1.5, "desc": "50% more encounters + rare finds"},
        },
        "activities": {"explore": 2, "forage": 1},
    },
    "underworld": {
        "name": "🦹 The Underworld", "emoji": "🦹",
        "description": "Criminals and rogues. High standing improves crime success.",
        "benefits": {
            10: {"crime_success": 1.05, "desc": "5% better crime success"},
            25: {"crime_success": 1.10, "desc": "10% better crime success"},
            50: {"crime_success": 1.20, "desc": "20% better crime success + access to black market"},
        },
        "activities": {"crime": 2},
    },
    "chefs": {
        "name": "👨‍🍳 Culinary Circle", "emoji": "👨‍🍳",
        "description": "Food enthusiasts and cooks. High standing improves cooking results.",
        "benefits": {
            10: {"cook_quality": 1.1, "desc": "10% better cooking quality rolls"},
            25: {"cook_quality": 1.25, "desc": "25% better cooking quality rolls"},
            50: {"cook_quality": 1.5, "desc": "50% better cooking quality + unlock secret recipes"},
        },
        "activities": {"cook": 2, "craft": 1},
    },
}
