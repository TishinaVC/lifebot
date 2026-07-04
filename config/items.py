STORE_ITEMS = {
    "bread":       {"name": "🍞 Bread",        "price": 30,    "type": "food",    "hunger": 15, "thirst": 0,  "health": 0},
    "burger":      {"name": "🍔 Burger",       "price": 80,    "type": "food",    "hunger": 35, "thirst": -5, "health": 0},
    "steak":       {"name": "🥩 Steak",        "price": 200,   "type": "food",    "hunger": 60, "thirst": 0,  "health": 5},
    "salad":       {"name": "🥗 Salad",        "price": 60,    "type": "food",    "hunger": 25, "thirst": 5,  "health": 5},
    "pizza":       {"name": "🍕 Pizza",        "price": 120,   "type": "food",    "hunger": 45, "thirst": -10, "health": 0},
    "water":       {"name": "💧 Water Bottle", "price": 15,    "type": "drink",   "hunger": 0,  "thirst": 25, "health": 0},
    "soda":        {"name": "🥤 Soda",         "price": 40,    "type": "drink",   "hunger": 5,  "thirst": 30, "health": -2},
    "juice":       {"name": "🧃 Juice",        "price": 45,    "type": "drink",   "hunger": 5,  "thirst": 35, "health": 2},
    "beer":        {"name": "🍺 Beer",         "price": 70,    "type": "drink",   "hunger": 10, "thirst": 30, "health": -5},
    "medkit":      {"name": "🩹 Medkit",       "price": 350,   "type": "medical", "hunger": 0,  "thirst": 0,  "health": 50},
    "bandage":     {"name": "🩹 Bandage",     "price": 120,   "type": "medical", "hunger": 0,  "thirst": 0,  "health": 20},
    "painkiller":  {"name": "💊 Painkiller",   "price": 80,    "type": "medical", "hunger": 0,  "thirst": 0,  "health": 15},
    "lucky_charm": {"name": "🍀 Lucky Charm",  "price": 250,   "type": "booster", "hunger": 0,  "thirst": 0,  "health": 0, "effect": "gamble_luck"},
    "vitamin":     {"name": "💊 Vitamin Pack", "price": 160,   "type": "medical", "hunger": 0,  "thirst": 0,  "health": 30},
    "sushi":       {"name": "🍣 Sushi",        "price": 150,   "type": "food",    "hunger": 40, "thirst": 5,  "health": 10},
    "taco":        {"name": "🌮 Taco",         "price": 70,    "type": "food",    "hunger": 30, "thirst": -5, "health": 3},
    "ramen":       {"name": "🍜 Ramen",        "price": 90,    "type": "food",    "hunger": 35, "thirst": 10, "health": 5},
    "ice_cream":   {"name": "🍨 Ice Cream",    "price": 50,    "type": "food",    "hunger": 15, "thirst": 10, "health": 0},
    "smoothie":    {"name": "🥤 Smoothie",     "price": 65,    "type": "drink",   "hunger": 10, "thirst": 30, "health": 5},
    "tea":         {"name": "🍵 Tea",          "price": 35,    "type": "drink",   "hunger": 0,  "thirst": 20, "health": 3},
    "first_aid":   {"name": "🧰 First Aid Kit","price": 500,   "type": "medical", "hunger": 0,  "thirst": 0,  "health": 75},
    "herbal_meds": {"name": "🌿 Herbal Remedy","price": 220,   "type": "medical", "hunger": 5,  "thirst": 5,  "health": 35},
    "xp_potion":   {"name": "🧪 XP Potion",     "price": 300,   "type": "booster", "hunger": 0,  "thirst": 0,  "health": 0, "energy": 0,  "hygiene": 0,  "effect": "xp_boost"},
    "shield":      {"name": "🛡️ Shield Charm",  "price": 400,   "type": "booster", "hunger": 0,  "thirst": 0,  "health": 0, "energy": 0,  "hygiene": 0,  "effect": "crime_protection"},
    "energy_drink":{"name": "⚡ Energy Drink", "price": 100,   "type": "booster", "hunger": 0,  "thirst": 15, "health": 0, "energy": 40, "hygiene": 0,  "effect": "work_cooldown_reduce"},
    "protein_bar": {"name": "🍫 Protein Bar",  "price": 60,    "type": "food",    "hunger": 15, "thirst": 0,  "health": 0, "energy": 25, "hygiene": 0},
    "coffee":      {"name": "☕ Coffee",       "price": 55,    "type": "drink",   "hunger": 0,   "thirst": 20, "health": 0, "energy": 30, "hygiene": 0},
    "soap":        {"name": "🧼 Soap",         "price": 25,    "type": "hygiene", "hunger": 0,  "thirst": 0,  "health": 0, "energy": 0,  "hygiene": 40},
    "shampoo":     {"name": "🧴 Shampoo",      "price": 50,    "type": "hygiene", "hunger": 0,  "thirst": 0,  "health": 0, "energy": 0,  "hygiene": 60},
    "deodorant":   {"name": "🧻 Deodorant",    "price": 20,    "type": "hygiene", "hunger": 0,  "thirst": 0,  "health": 0, "energy": 0,  "hygiene": 25},
    "gold_watch":  {"name": "⌚ Gold Watch",    "price": 5000,  "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "diamond":     {"name": "💎 Diamond",       "price": 15000, "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "crown":       {"name": "👑 Golden Crown",  "price": 50000, "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "trophy":      {"name": "🏆 Champion Trophy","price": 10000, "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "painting":    {"name": "🎨 Rare Painting","price": 8000,  "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "ruby":        {"name": "❤️ Ruby",          "price": 12000, "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "protein_shake":      {"name": "🥤 Protein Shake",       "price": 150,  "type": "stat_booster", "hunger": 0, "thirst": 0, "health": 0, "stat": "strength",     "boost": 10, "duration": 1800},
    "nootropic":          {"name": "🧠 Nootropic",           "price": 300,  "type": "stat_booster", "hunger": 0, "thirst": 0, "health": 0, "stat": "intelligence", "boost": 15, "duration": 3600},
    "caffeine_pill":      {"name": "💊 Caffeine Pill",       "price": 120,  "type": "stat_booster", "hunger": 0, "thirst": 0, "health": 0, "stat": "focus",        "boost": 10, "duration": 2700},
    "lucky_rabbit_foot":  {"name": "🐇 Lucky Rabbit Foot",   "price": 500,  "type": "stat_booster", "hunger": 0, "thirst": 0, "health": 0, "stat": "luck",         "boost": 15, "duration": 3600},
    "confidence_potion":  {"name": "🍸 Confidence Potion",   "price": 250,  "type": "stat_booster", "hunger": 0, "thirst": 0, "health": 0, "stat": "charisma",     "boost": 12, "duration": 1800},
    "eye_drops":          {"name": "👁️ Eye Drops",           "price": 80,   "type": "stat_booster", "hunger": 0, "thirst": 0, "health": 0, "stat": "perception",   "boost": 10, "duration": 1800},
    "hand_warmup_cream":  {"name": "🧴 Hand Warm-up Cream",  "price": 60,   "type": "stat_booster", "hunger": 0, "thirst": 0, "health": 0, "stat": "dexterity",    "boost": 10, "duration": 1200},
    "endurance_shot":     {"name": "💉 Endurance Shot",      "price": 180,  "type": "stat_booster", "hunger": 0, "thirst": 0, "health": 0, "stat": "endurance",    "boost": 12, "duration": 1800},

    # ─── New Food: Snacks ───
    "donut":        {"name": "🍩 Donut",         "price": 40,    "type": "food",    "hunger": 12, "thirst": 5,  "health": 0},
    "cookie":       {"name": "🍪 Cookie",        "price": 25,    "type": "food",    "hunger": 8,  "thirst": 3,  "health": 0},
    "chips":        {"name": "🍟 Chips",         "price": 35,    "type": "food",    "hunger": 10, "thirst": -5, "health": 0},
    "popcorn":      {"name": "🍿 Popcorn",       "price": 30,    "type": "food",    "hunger": 10, "thirst": -3, "health": 0},
    "pretzel":      {"name": "🥨 Pretzel",       "price": 45,    "type": "food",    "hunger": 15, "thirst": -3, "health": 0},

    # ─── New Food: Meals ───
    "pasta":        {"name": "🍝 Pasta",         "price": 110,   "type": "food",    "hunger": 40, "thirst": 0,  "health": 3},
    "curry":        {"name": "🍛 Curry",         "price": 130,   "type": "food",    "hunger": 45, "thirst": -5, "health": 5},
    "fried_chicken":{"name": "🍗 Fried Chicken", "price": 95,    "type": "food",    "hunger": 38, "thirst": -8, "health": 0},
    "kebab":        {"name": "🥙 Kebab",         "price": 85,    "type": "food",    "hunger": 32, "thirst": -3, "health": 2},
    "noodle_bowl":  {"name": "🍜 Noodle Bowl",   "price": 75,    "type": "food",    "hunger": 30, "thirst": 5,  "health": 3},

    # ─── New Food: Desserts ───
    "cake":         {"name": "🍰 Cake",          "price": 100,   "type": "food",    "hunger": 25, "thirst": 10, "health": 0},
    "pie":          {"name": "🥧 Pie",           "price": 90,    "type": "food",    "hunger": 22, "thirst": 5,  "health": 0},
    "pudding":      {"name": "🍮 Pudding",       "price": 55,    "type": "food",    "hunger": 15, "thirst": 10, "health": 0},
    "chocolate_bar":{"name": "🍫 Chocolate Bar", "price": 40,    "type": "food",    "hunger": 10, "thirst": 0,  "health": 0, "energy": 10},
    "cheesecake":   {"name": "🍰 Cheesecake",    "price": 140,   "type": "food",    "hunger": 30, "thirst": 10, "health": 0},
    "brownie":      {"name": "🍫 Brownie",       "price": 60,    "type": "food",    "hunger": 18, "thirst": 5,  "health": 0, "energy": 5},

    # ─── New Food: Breakfast ───
    "eggs":         {"name": "🍳 Fried Eggs",    "price": 35,    "type": "food",    "hunger": 15, "thirst": 0,  "health": 3, "energy": 10},
    "pancakes":     {"name": "🥞 Pancakes",      "price": 55,    "type": "food",    "hunger": 22, "thirst": 5,  "health": 0, "energy": 10},
    "waffles":      {"name": "🧇 Waffles",       "price": 60,    "type": "food",    "hunger": 25, "thirst": 5,  "health": 0, "energy": 12},
    "oatmeal":      {"name": "🥣 Oatmeal",       "price": 30,    "type": "food",    "hunger": 15, "thirst": 10, "health": 5, "energy": 8},
    "bagel":        {"name": "🥯 Bagel",         "price": 40,    "type": "food",    "hunger": 15, "thirst": 0,  "health": 0},
    "croissant":    {"name": "🥐 Croissant",     "price": 50,    "type": "food",    "hunger": 18, "thirst": 0,  "health": 0},
    "muffin":       {"name": "🧁 Muffin",        "price": 45,    "type": "food",    "hunger": 15, "thirst": 5,  "health": 0},

    # ─── New Food: Healthy ───
    "fruit_bowl":   {"name": "🍓 Fruit Bowl",    "price": 70,    "type": "food",    "hunger": 20, "thirst": 15, "health": 8},
    "veggie_platter":{"name": "🥕 Veggie Platter","price": 65,   "type": "food",    "hunger": 22, "thirst": 10, "health": 10},
    "quinoa_salad": {"name": "🥗 Quinoa Salad",  "price": 90,    "type": "food",    "hunger": 30, "thirst": 5,  "health": 12},
    "yogurt":       {"name": "🥛 Yogurt",        "price": 35,    "type": "food",    "hunger": 10, "thirst": 10, "health": 5},
    "granola_bar":  {"name": "🌾 Granola Bar",   "price": 30,    "type": "food",    "hunger": 12, "thirst": 0,  "health": 0, "energy": 8},

    # ─── New Drinks: Water ───
    "sparkling_water":{"name": "✨ Sparkling Water","price": 25, "type": "drink",  "hunger": 0,  "thirst": 28, "health": 0},
    "mineral_water":{"name": "🏔️ Mineral Water",  "price": 40,  "type": "drink",  "hunger": 0,  "thirst": 35, "health": 3},
    "coconut_water":{"name": "🥥 Coconut Water",  "price": 55,  "type": "drink",  "hunger": 5,  "thirst": 30, "health": 5},

    # ─── New Drinks: Soda ───
    "cola":         {"name": "🥤 Cola",          "price": 45,    "type": "drink",   "hunger": 5,  "thirst": 25, "health": -3, "energy": 15},
    "lemonade":     {"name": "🍋 Lemonade",      "price": 50,    "type": "drink",   "hunger": 5,  "thirst": 30, "health": 2},
    "root_beer":    {"name": "🥤 Root Beer",     "price": 55,    "type": "drink",   "hunger": 8,  "thirst": 25, "health": -2},

    # ─── New Drinks: Hot ───
    "hot_chocolate":{"name": "🍫 Hot Chocolate", "price": 60,    "type": "drink",   "hunger": 10, "thirst": 15, "health": 5, "energy": 15},
    "espresso":     {"name": "☕ Espresso",      "price": 70,    "type": "drink",   "hunger": 0,  "thirst": 10, "health": 0, "energy": 40},
    "matcha_latte": {"name": "🍵 Matcha Latte",  "price": 85,    "type": "drink",   "hunger": 5,  "thirst": 15, "health": 5, "energy": 25},

    # ─── New Drinks: Juice ───
    "orange_juice": {"name": "🍊 Orange Juice",  "price": 50,    "type": "drink",   "hunger": 5,  "thirst": 30, "health": 8},
    "berry_smoothie":{"name": "🫐 Berry Smoothie","price": 70,   "type": "drink",   "hunger": 12, "thirst": 28, "health": 8},
    "green_juice":  {"name": "🥬 Green Juice",   "price": 65,    "type": "drink",   "hunger": 8,  "thirst": 25, "health": 12},

    # ─── New Drinks: Alcohol ───
    "wine":         {"name": "🍷 Wine",          "price": 120,   "type": "drink",   "hunger": 15, "thirst": 25, "health": -8},
    "whiskey":      {"name": "🥃 Whiskey",       "price": 150,   "type": "drink",   "hunger": 10, "thirst": 20, "health": -10},
    "cocktail":     {"name": "🍸 Cocktail",      "price": 100,   "type": "drink",   "hunger": 10, "thirst": 25, "health": -5},
    "sake":         {"name": "🍶 Sake",          "price": 90,    "type": "drink",   "hunger": 12, "thirst": 22, "health": -5},

    # ─── New Medical: Basic ───
    "antiseptic":   {"name": "🧴 Antiseptic",    "price": 60,    "type": "medical", "hunger": 0,  "thirst": 0,  "health": 12},
    "cough_syrup":  {"name": "💊 Cough Syrup",   "price": 50,    "type": "medical", "hunger": 0,  "thirst": 0,  "health": 10},

    # ─── New Medical: Advanced ───
    "vitamin_c":    {"name": "🍊 Vitamin C",     "price": 100,   "type": "medical", "hunger": 0,  "thirst": 5,  "health": 20},
    "antibiotics":  {"name": "💊 Antibiotics",   "price": 180,   "type": "medical", "hunger": 0,  "thirst": 0,  "health": 40},

    # ─── New Medical: Emergency ───
    "adrenaline_shot":{"name": "💉 Adrenaline Shot","price": 600,"type": "medical", "hunger": 0,  "thirst": 0,  "health": 60, "energy": 50},
    "surgery_kit":  {"name": "🔪 Surgery Kit",   "price": 800,   "type": "medical", "hunger": 0,  "thirst": 0,  "health": 90},
    "defibrillator":{"name": "⚡ Defibrillator",  "price": 1000,  "type": "medical", "hunger": 0,  "thirst": 0,  "health": 100},
    "trauma_kit":   {"name": "🩹 Trauma Kit",    "price": 450,   "type": "medical", "hunger": 0,  "thirst": 0,  "health": 55},

    # ─── New Boosters ───
    "mega_xp_potion":{"name": "🧪 Mega XP Potion","price": 600,  "type": "booster", "hunger": 0,  "thirst": 0,  "health": 0, "effect": "mega_xp_boost"},
    "hyper_energy": {"name": "⚡ Hyper Energy",   "price": 200,   "type": "booster", "hunger": 0,  "thirst": 10, "health": 0, "energy": 60, "effect": "work_cooldown_reduce"},
    "super_shield": {"name": "🛡️ Super Shield",  "price": 800,   "type": "booster", "hunger": 0,  "thirst": 0,  "health": 0, "effect": "crime_protection"},
    "alarm_system": {"name": "🚨 Alarm System",  "price": 550,   "type": "booster", "hunger": 0,  "thirst": 0,  "health": 0, "effect": "crime_protection"},
    "four_leaf_clover":{"name": "🍀 Four-Leaf Clover","price": 350,"type": "booster","hunger": 0, "thirst": 0,  "health": 0, "effect": "gamble_luck"},
    "fortune_cookie":{"name": "🥠 Fortune Cookie","price": 100,   "type": "booster", "hunger": 5,  "thirst": 0,  "health": 0, "effect": "gamble_luck"},

    # ─── New Stat Boosters ───
    "muscle_relaxant":    {"name": "💊 Muscle Relaxant",     "price": 140,  "type": "stat_booster", "hunger": 0, "thirst": 0, "health": 0, "stat": "strength",     "boost": 15, "duration": 1800},
    "focus_crystal":      {"name": "🔮 Focus Crystal",       "price": 350,  "type": "stat_booster", "hunger": 0, "thirst": 0, "health": 0, "stat": "focus",        "boost": 18, "duration": 3600},
    "charm_bracelet_boost":{"name": "📿 Charm Bracelet",     "price": 280,  "type": "stat_booster", "hunger": 0, "thirst": 0, "health": 0, "stat": "charisma",     "boost": 15, "duration": 2400},
    "lucky_pen":          {"name": "🖊️ Lucky Pen",           "price": 90,   "type": "stat_booster", "hunger": 0, "thirst": 0, "health": 0, "stat": "luck",         "boost": 8,  "duration": 1200},

    # ─── New Hygiene ───
    "hand_sanitizer":{"name": "🧴 Hand Sanitizer","price": 15,  "type": "hygiene", "hunger": 0,  "thirst": 0,  "health": 0, "energy": 0, "hygiene": 20},
    "dental_kit":   {"name": "🦷 Dental Kit",    "price": 70,   "type": "hygiene", "hunger": 0,  "thirst": 0,  "health": 0, "energy": 0, "hygiene": 50},
    "bath_bomb":    {"name": "🛁 Bath Bomb",     "price": 90,   "type": "hygiene", "hunger": 0,  "thirst": 0,  "health": 5, "energy": 5, "hygiene": 80},
    "perfume":      {"name": "🌸 Perfume",       "price": 120,  "type": "hygiene", "hunger": 0,  "thirst": 0,  "health": 0, "energy": 0, "hygiene": 70},
    "luxury_lotion":{"name": "🧴 Luxury Lotion", "price": 80,   "type": "hygiene", "hunger": 0,  "thirst": 0,  "health": 0, "energy": 0, "hygiene": 55},
    "spa_kit":      {"name": "🧖 Spa Kit",       "price": 200,  "type": "hygiene", "hunger": 0,  "thirst": 0,  "health": 10,"energy": 10,"hygiene": 100},

    # ─── New Collectibles: Gems ───
    "emerald":      {"name": "💚 Emerald",        "price": 9000,  "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "sapphire":     {"name": "💙 Sapphire",       "price": 8500,  "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "amethyst":     {"name": "💜 Amethyst",       "price": 6000,  "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "pearl":        {"name": "🦪 Pearl",          "price": 4000,  "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "opal":         {"name": "🌈 Opal",           "price": 7000,  "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "topaz":        {"name": "💛 Topaz",          "price": 5000,  "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},

    # ─── New Collectibles: Trophies ───
    "gold_medal":   {"name": "🥇 Gold Medal",     "price": 8000,  "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "championship_belt":{"name": "🥋 Championship Belt","price": 15000,"type":"collectible","hunger":0,"thirst":0,"health":0},
    "platinum_cup": {"name": "🏆 Platinum Cup",   "price": 20000, "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},

    # ─── New Collectibles: Art ───
    "sculpture":    {"name": "🗿 Sculpture",      "price": 12000, "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "vintage_vase": {"name": "🏺 Vintage Vase",   "price": 9000,  "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "antique_clock":{"name": "🕰️ Antique Clock", "price": 11000, "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "vinyl_record": {"name": "🎵 Vinyl Record",   "price": 3000,  "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "rare_book":    {"name": "📖 Rare First Edition","price": 7000,"type": "collectible", "hunger": 0, "thirst": 0, "health": 0},

    # ─── New Collectibles: Rare Finds ───
    "golden_idol":  {"name": "🗿 Golden Idol",    "price": 30000, "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "meteor_fragment":{"name": "☄️ Meteor Fragment","price": 25000,"type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "ancient_relic":{"name": "📜 Ancient Relic",  "price": 35000, "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "dragon_egg":   {"name": "🥚 Dragon Egg",     "price": 45000, "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "pharaoh_mask": {"name": "⚰️ Pharaoh's Mask", "price": 40000, "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
}
