PETS = {
    "dog":     {"name": "Dog",      "price": 1000,  "emoji": "🐕", "type": "Loyal",     "bonus": "+5% work pay",       "base_power": 15},
    "cat":     {"name": "Cat",      "price": 800,   "emoji": "🐱", "type": "Lucky",     "bonus": "+3% gamble luck",    "base_power": 12},
    "rabbit":  {"name": "Rabbit",   "price": 600,   "emoji": "🐰", "type": "Fast",      "bonus": "+8% XP gain",        "base_power": 8},
    "parrot":  {"name": "Parrot",   "price": 1500,  "emoji": "🦜", "type": "Smart",     "bonus": "+10% quest rewards", "base_power": 18},
    "fish":    {"name": "Fish",     "price": 300,   "emoji": "🐟", "type": "Calm",      "bonus": "+2% XP gain",        "base_power": 5},
    "turtle":  {"name": "Turtle",   "price": 2500,  "emoji": "🐢", "type": "Tank",      "bonus": "+10% work pay",      "base_power": 25},
    "fox":     {"name": "Fox",      "price": 5000,  "emoji": "🦊", "type": "Cunning",   "bonus": "+5% crime rewards",  "base_power": 30},
    "owl":     {"name": "Owl",      "price": 4000,  "emoji": "🦉", "type": "Wise",      "bonus": "+15% XP gain",       "base_power": 22},
    "wolf":    {"name": "Wolf",     "price": 8000,  "emoji": "🐺", "type": "Fierce",    "bonus": "+12% work pay",      "base_power": 40},
    "phoenix": {"name": "Phoenix",  "price": 30000, "emoji": "🔥", "type": "Epic",      "bonus": "+20% all earnings",  "base_power": 60},
    "dragon":  {"name": "Dragon",   "price": 15000, "emoji": "🐉", "type": "Legendary", "bonus": "+15% all earnings",  "base_power": 50},
    "unicorn": {"name": "Unicorn",  "price": 50000, "emoji": "🦄", "type": "Mythic",    "bonus": "+25% all earnings",  "base_power": 80},
}

PET_BONUSES = {
    "dog":     {"pay_mult": 1.05},
    "cat":     {"gamble_luck": 0.03},
    "rabbit":  {"xp_mult": 1.08},
    "parrot":  {"quest_reward_mult": 1.10},
    "dragon":  {"pay_mult": 1.15, "gamble_luck": 0.03, "xp_mult": 1.15},
    "unicorn": {"pay_mult": 1.25, "gamble_luck": 0.05, "xp_mult": 1.25, "quest_reward_mult": 1.25},
}
