HOUSING_TIERS = {
    "tent": {
        "name": "⛺ Tent", "tier": 1, "buy_price": 50, "rent": 5,
        "storage": 2,
        "stats_bonus": {"energy": 15, "hygiene": -2, "health": 0},
        "advantage": "Fresh air: +5 energy on rest",
        "disadvantage": "Exposed: 10% chance to lose 10 coins to weather",
    },
    "sleeping_bag": {
        "name": "🛏️ Sleeping Bag (under bridge)", "tier": 2, "buy_price": 100, "rent": 10,
        "storage": 3,
        "stats_bonus": {"energy": 20, "hygiene": -5, "health": 0},
        "advantage": "Street smart: +3% crime success",
        "disadvantage": "Rough night: 15% chance to lose 5 HP",
    },
    "shack": {
        "name": "🏚️ Shack", "tier": 3, "buy_price": 300, "rent": 25,
        "storage": 5,
        "stats_bonus": {"energy": 25, "hygiene": 0, "health": 2},
        "advantage": "DIY repairs: +3 HP on rest",
        "disadvantage": "Drafty: 10% chance to lose 3 energy",
    },
    "van": {
        "name": "🚐 Van", "tier": 4, "buy_price": 600, "rent": 40,
        "storage": 8,
        "stats_bonus": {"energy": 30, "hygiene": 5, "health": 2},
        "advantage": "Mobile: +5% crime escape chance",
        "disadvantage": "Cramped: -2 hygiene on rest",
    },
    "studio": {
        "name": "🏢 Studio Apartment", "tier": 5, "buy_price": 1200, "rent": 75,
        "storage": 10,
        "stats_bonus": {"energy": 35, "hygiene": 10, "health": 3},
        "advantage": "Cozy: +5 energy on rest",
        "disadvantage": "Thin walls: 5% chance to lose 2 energy from noise",
    },
    "apartment_1br": {
        "name": "🏠 1-Bedroom Apartment", "tier": 6, "buy_price": 2500, "rent": 120,
        "storage": 15,
        "stats_bonus": {"energy": 40, "hygiene": 15, "health": 5},
        "advantage": "Comfortable: +5 HP on rest",
        "disadvantage": "Landlord visits: 5% chance to pay 50 coins extra",
    },
    "apartment_2br": {
        "name": "🏘️ 2-Bedroom Apartment", "tier": 7, "buy_price": 4000, "rent": 180,
        "storage": 20,
        "stats_bonus": {"energy": 45, "hygiene": 20, "health": 5},
        "advantage": "Extra room: +10% XP from resting",
        "disadvantage": "Higher utilities: 8% chance to pay 75 coins",
    },
    "townhouse": {
        "name": "🏡 Townhouse", "tier": 8, "buy_price": 7000, "rent": 250,
        "storage": 25,
        "stats_bonus": {"energy": 50, "hygiene": 25, "health": 8},
        "advantage": "Private entrance: +3 hygiene on rest",
        "disadvantage": "Maintenance: 5% chance to pay 100 coins",
    },
    "loft": {
        "name": "🏗️ Loft", "tier": 9, "buy_price": 10000, "rent": 350,
        "storage": 30,
        "stats_bonus": {"energy": 55, "hygiene": 25, "health": 8},
        "advantage": "Open space: +8 energy on rest",
        "disadvantage": "Echoey: 3% chance to lose 2 energy",
    },
    "condo": {
        "name": "🏬 Condo", "tier": 10, "buy_price": 15000, "rent": 450,
        "storage": 35,
        "stats_bonus": {"energy": 60, "hygiene": 30, "health": 10},
        "advantage": "Amenities: +10 hygiene on rest",
        "disadvantage": "HOA fees: 10% chance to pay 150 coins",
    },
    "suburban_house": {
        "name": "🏡 Suburban House", "tier": 11, "buy_price": 22000, "rent": 550,
        "storage": 40,
        "stats_bonus": {"energy": 65, "hygiene": 35, "health": 12},
        "advantage": "Yard: +5 hygiene, +5 energy on rest",
        "disadvantage": "Lawn care: 7% chance to pay 120 coins",
    },
    "duplex": {
        "name": "🏠 Duplex", "tier": 12, "buy_price": 30000, "rent": 650,
        "storage": 45,
        "stats_bonus": {"energy": 70, "hygiene": 35, "health": 12},
        "advantage": "Rental income potential: +5% pay from work",
        "disadvantage": "Shared wall: 5% chance to lose 3 energy",
    },
    "farmhouse": {
        "name": "🚜 Farmhouse", "tier": 13, "buy_price": 40000, "rent": 700,
        "storage": 60,
        "stats_bonus": {"energy": 75, "hygiene": 30, "health": 15},
        "advantage": "Self-sufficient: +10 HP, +5 hunger on rest",
        "disadvantage": "Chores: 10% chance to lose 5 energy",
    },
    "cabin": {
        "name": "🛖 Mountain Cabin", "tier": 14, "buy_price": 55000, "rent": 800,
        "storage": 50,
        "stats_bonus": {"energy": 80, "hygiene": 35, "health": 18},
        "advantage": "Fresh mountain air: +15 energy on rest",
        "disadvantage": "Isolation: 5% chance to lose 50 coins on supplies",
    },
    "beach_house": {
        "name": "🏖️ Beach House", "tier": 15, "buy_price": 75000, "rent": 1000,
        "storage": 55,
        "stats_bonus": {"energy": 85, "hygiene": 40, "health": 18},
        "advantage": "Ocean breeze: +15 hygiene on rest",
        "disadvantage": "Storm risk: 5% chance to pay 200 coins repairs",
    },
    "villa": {
        "name": "🏛️ Villa", "tier": 16, "buy_price": 120000, "rent": 1500,
        "storage": 70,
        "stats_bonus": {"energy": 90, "hygiene": 50, "health": 20},
        "advantage": "Luxury: +20 energy, +10 hygiene on rest",
        "disadvantage": "Staff costs: 8% chance to pay 300 coins",
    },
    "mansion": {
        "name": "🏰 Mansion", "tier": 17, "buy_price": 200000, "rent": 2500,
        "storage": 100,
        "stats_bonus": {"energy": 95, "hygiene": 55, "health": 25},
        "advantage": "Grand: +25 energy, +15 hygiene, +10 HP on rest",
        "disadvantage": "Upkeep: 10% chance to pay 500 coins",
    },
    "estate": {
        "name": "🌳 Private Estate", "tier": 18, "buy_price": 350000, "rent": 3500,
        "storage": 120,
        "stats_bonus": {"energy": 100, "hygiene": 60, "health": 30},
        "advantage": "Self-contained: full energy restore on rest",
        "disadvantage": "Groundskeeping: 8% chance to pay 700 coins",
    },
    "penthouse": {
        "name": "🌆 Penthouse", "tier": 19, "buy_price": 500000, "rent": 5000,
        "storage": 150,
        "stats_bonus": {"energy": 100, "hygiene": 70, "health": 35},
        "advantage": "Top of the world: full energy + 20 hygiene on rest",
        "disadvantage": "Premium HOA: 10% chance to pay 1000 coins",
    },
    "sky_mansion": {
        "name": "✨ Sky Mansion", "tier": 20, "buy_price": 1000000, "rent": 0,
        "storage": 200,
        "stats_bonus": {"energy": 100, "hygiene": 80, "health": 40},
        "advantage": "Ultimate luxury: full stat restore on rest, +10% all XP",
        "disadvantage": "None — you've made it",
    },
}

HOME_UPGRADES = {
    "extra_room": {
        "name": "🚪 Extra Room", "description": "+10 storage slots per level",
        "price": 2000, "price_mult": 1.5, "max_level": 5, "effect": "storage",
    },
    "kitchen": {
        "name": "🍳 Kitchen Upgrade", "description": "+5 hunger restore on rest per level",
        "price": 1500, "price_mult": 1.4, "max_level": 5, "effect": "hunger",
    },
    "bathroom": {
        "name": "🛁 Bathroom Upgrade", "description": "+10 hygiene restore on rest per level",
        "price": 1800, "price_mult": 1.4, "max_level": 5, "effect": "hygiene",
    },
    "bedroom": {
        "name": "🛏️ Bedroom Upgrade", "description": "+10 energy restore on rest per level",
        "price": 2000, "price_mult": 1.5, "max_level": 5, "effect": "energy",
    },
    "garden": {
        "name": "🌱 Garden", "description": "+5 HP on rest, +3 hygiene per level",
        "price": 3000, "price_mult": 1.6, "max_level": 3, "effect": "health",
    },
    "security": {
        "name": "🔒 Security System", "description": "-10% crime success against you per level",
        "price": 2500, "price_mult": 1.5, "max_level": 3, "effect": "security",
    },
    "solar_panels": {
        "name": "☀️ Solar Panels", "description": "-20% rent per level",
        "price": 4000, "price_mult": 1.6, "max_level": 3, "effect": "rent_reduction",
    },
    "gym": {
        "name": "🏋️ Home Gym", "description": "+5 max energy per level, +3 HP on rest",
        "price": 5000, "price_mult": 1.7, "max_level": 3, "effect": "max_energy",
    },
}

HOME_DECORATIONS = {
    "rug":         {"name": "Area Rug",        "emoji": "🟫", "price": 200,   "description": "A cozy area rug"},
    "painting":    {"name": "Oil Painting",    "emoji": "🖼️", "price": 500,   "description": "A fine oil painting"},
    "plant":       {"name": "Potted Plant",    "emoji": "🪴", "price": 150,   "description": "A small potted plant"},
    "bookshelf":   {"name": "Bookshelf",       "emoji": "📚", "price": 800,   "description": "Filled with classic literature"},
    "fireplace":   {"name": "Fireplace",       "emoji": "🔥", "price": 1500,  "description": "A warm stone fireplace"},
    "aquarium":    {"name": "Aquarium",        "emoji": "🐠", "price": 2000,  "description": "A beautiful aquarium"},
    "chandelier":  {"name": "Chandelier",      "emoji": "💡", "price": 3000,  "description": "A crystal chandelier"},
    "statue":      {"name": "Marble Statue",   "emoji": "🗿", "price": 5000,  "description": "An elegant marble statue"},
    "piano":       {"name": "Grand Piano",     "emoji": "🎹", "price": 8000,  "description": "A Steinway grand piano"},
    "hot_tub":     {"name": "Hot Tub",         "emoji": "♨️", "price": 10000, "description": "A luxury hot tub"},
    "home_theater":{"name": "Home Theater",    "emoji": "🎬", "price": 15000, "description": "A full home theater system"},
    "art_gallery": {"name": "Art Gallery",     "emoji": "🎨", "price": 25000, "description": "A private art collection"},
}

RENT_INTERVAL = 604800
