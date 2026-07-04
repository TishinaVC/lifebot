ITEM_QUALITIES = {
    "cursed":    {"name": "💀 Cursed",    "emoji": "💀", "multiplier": 0.3,  "value_mult": 0.2,  "weight": 2},
    "broken":    {"name": "🔧 Broken",    "emoji": "🔧", "multiplier": 0.5,  "value_mult": 0.3,  "weight": 5},
    "worn":      {"name": "📦 Worn",      "emoji": "📦", "multiplier": 0.7,  "value_mult": 0.5,  "weight": 15},
    "common":    {"name": "⬜ Common",    "emoji": "⬜", "multiplier": 1.0,  "value_mult": 1.0,  "weight": 40},
    "fine":      {"name": "🟢 Fine",      "emoji": "🟢", "multiplier": 1.2,  "value_mult": 1.5,  "weight": 20},
    "rare":      {"name": "🔵 Rare",      "emoji": "🔵", "multiplier": 1.5,  "value_mult": 2.5,  "weight": 10},
    "epic":      {"name": "🟣 Epic",      "emoji": "🟣", "multiplier": 1.8,  "value_mult": 4.0,  "weight": 5},
    "legendary": {"name": "🟡 Legendary", "emoji": "🟡", "multiplier": 2.5,  "value_mult": 8.0,  "weight": 2},
    "mythic":    {"name": "🔴 Mythic",    "emoji": "🔴", "multiplier": 3.0,  "value_mult": 15.0, "weight": 1},
}

TOOLS = {
    "fishing_rod":  {"name": "🎣 Fishing Rod",   "price": 200,   "durability": 50,  "activity": "fish",    "description": "Cast a line and catch fish"},
    "pickaxe":      {"name": "⛏️ Pickaxe",        "price": 500,   "durability": 40,  "activity": "mine",    "description": "Mine for ores and gems"},
    "shovel":       {"name": "🪏 Shovel",         "price": 150,   "durability": 60,  "activity": "dig",     "description": "Dig for buried treasure"},
    "axe":          {"name": "🪓 Axe",            "price": 350,   "durability": 45,  "activity": "chop",    "description": "Chop wood for crafting"},
    "camera":       {"name": "📷 Camera",         "price": 800,   "durability": 100, "activity": "photo",   "description": "Take photos for money"},
    "bug_net":      {"name": "🦋 Bug Net",        "price": 100,   "durability": 70,  "activity": "catch_bug","description": "Catch bugs and insects"},
    "metal_detector":{"name": "📡 Metal Detector","price": 1200,  "durability": 80,  "activity": "detect",  "description": "Find hidden metal objects"},
    "hunting_rifle":{"name": "🎯 Hunting Rifle",  "price": 2000,  "durability": 30,  "activity": "hunt",    "description": "Hunt wild game"},
    "lockpick":     {"name": "🔓 Lockpick",       "price": 300,   "durability": 20,  "activity": "lockpick","description": "Pick locks for loot"},
    "compass":      {"name": "🧭 Compass",        "price": 600,   "durability": 999, "activity": "explore", "description": "Explore the wilderness"},
    # ─── New Tools ───
    "telescope":    {"name": "🔭 Telescope",      "price": 1500,  "durability": 90,  "activity": "stargaze",  "description": "Stargaze and discover celestial objects"},
    "binoculars":   {"name": "🔭 Binoculars",     "price": 700,   "durability": 100, "activity": "scout",     "description": "Scout distant areas for better finds"},
    "bow":          {"name": "🏹 Bow",             "price": 1200,  "durability": 50,  "activity": "hunt",      "description": "Silent hunting with a recurve bow"},
    "trap":         {"name": "🪤 Trap",            "price": 400,   "durability": 30,  "activity": "trap",      "description": "Set traps to catch prey passively"},
    "tracking_device":{"name":"📡 Tracking Device","price": 1800,  "durability": 60,  "activity": "track",     "description": "Track animals with GPS technology"},
    "flashlight":   {"name": "🔦 Flashlight",     "price": 200,   "durability": 80,  "activity": "search",    "description": "Search dark places for hidden items"},
    "diving_gear":  {"name": "🤿 Diving Gear",    "price": 2500,  "durability": 70,  "activity": "dive",      "description": "Dive underwater for rare finds"},
    "grappling_hook":{"name":"🪝 Grappling Hook", "price": 900,   "durability": 55,  "activity": "climb",     "description": "Climb cliffs and reach high places"},
    "seismograph":  {"name": "📊 Seismograph",    "price": 3000,  "durability": 999, "activity": "survey",    "description": "Survey land for mineral deposits"},
}

CLOTHING = {
    "tshirt":       {"name": "👕 T-Shirt",        "price": 50,    "slot": "top",    "warmth": 1,  "weather_prot": [],                   "stats": {}},
    "jeans":        {"name": "👖 Jeans",          "price": 80,    "slot": "legs",   "warmth": 2,  "weather_prot": [],                   "stats": {}},
    "jacket":       {"name": "🧥 Jacket",         "price": 300,   "slot": "top",    "warmth": 5,  "weather_prot": ["rainy","windy","snowy"], "stats": {"energy": 5}},
    "raincoat":     {"name": "🧥 Raincoat",       "price": 500,   "slot": "top",    "warmth": 3,  "weather_prot": ["rainy","stormy"],   "stats": {"hygiene": 10}},
    "winter_coat":  {"name": "🧥 Winter Coat",    "price": 800,   "slot": "top",    "warmth": 10, "weather_prot": ["snowy","windy","foggy"], "stats": {"health": 5, "energy": 5}},
    "boots":        {"name": "🥾 Boots",          "price": 250,   "slot": "feet",   "warmth": 3,  "weather_prot": ["rainy","snowy","muddy"], "stats": {"energy": 3}},
    "sandals":      {"name": "🩴 Sandals",        "price": 30,    "slot": "feet",   "warmth": 0,  "weather_prot": [],                   "stats": {}},
    "sunglasses":   {"name": "🕶️ Sunglasses",     "price": 150,   "slot": "accessory","warmth": 0,"weather_prot": ["sunny"],            "stats": {"luck": 2}},
    "umbrella":     {"name": "☂️ Umbrella",       "price": 120,   "slot": "accessory","warmth": 0,"weather_prot": ["rainy","stormy"],    "stats": {"hygiene": 5}},
    "hat":          {"name": "🎩 Hat",            "price": 200,   "slot": "accessory","warmth": 1,"weather_prot": ["sunny"],            "stats": {"luck": 1}},
    "scarf":        {"name": "🧣 Scarf",          "price": 180,   "slot": "accessory","warmth": 4,"weather_prot": ["windy","snowy","foggy"], "stats": {"health": 3}},
    "gloves":       {"name": "🧤 Gloves",         "price": 160,   "slot": "accessory","warmth": 3,"weather_prot": ["snowy","windy"],     "stats": {"energy": 2}},
    "dress":        {"name": "👗 Dress",          "price": 400,   "slot": "top",    "warmth": 2,  "weather_prot": [],                   "stats": {"luck": 3}},
    "suit":         {"name": "🤵 Suit",           "price": 1500,  "slot": "top",    "warmth": 3,  "weather_prot": [],                   "stats": {"luck": 5, "energy": 5}},
    "armor":        {"name": "🛡️ Light Armor",    "price": 3000,  "slot": "top",    "warmth": 4,  "weather_prot": [],                   "stats": {"health": 15}},
    "designer_outfit":{"name": "👗 Designer Outfit","price": 5000,"slot": "top",    "warmth": 3,  "weather_prot": ["sunny"],            "stats": {"luck": 8, "hygiene": 5}},
    "rain_boots":   {"name": "🥾 Rain Boots",     "price": 400,   "slot": "feet",   "warmth": 2,  "weather_prot": ["rainy","stormy","muddy"], "stats": {"hygiene": 8}},
    "snow_boots":   {"name": "🥾 Snow Boots",     "price": 600,   "slot": "feet",   "warmth": 5,  "weather_prot": ["snowy","foggy"],    "stats": {"health": 3, "energy": 3}},
    "thermal_suit": {"name": "🧥 Thermal Suit",   "price": 2000,  "slot": "top",    "warmth": 12, "weather_prot": ["snowy","windy","foggy","rainy"], "stats": {"health": 8, "energy": 8}},
    "hazmat_suit":  {"name": "🟨 Hazmat Suit",   "price": 10000, "slot": "top",    "warmth": 8,  "weather_prot": ["rainy","stormy","foggy","snowy","windy","sunny","heatwave","muddy"], "stats": {"health": 20, "hygiene": 20}},
    # ─── New Clothing: Tops ───
    "hoodie":       {"name": "🧥 Hoodie",         "price": 150,   "slot": "top",    "warmth": 4,  "weather_prot": ["windy","foggy"],            "stats": {"energy": 3}},
    "vest":         {"name": "🦺 Vest",           "price": 220,   "slot": "top",    "warmth": 2,  "weather_prot": [],                              "stats": {"health": 5}},
    "tuxedo":       {"name": "🤵 Tuxedo",         "price": 3000,  "slot": "top",    "warmth": 3,  "weather_prot": [],                              "stats": {"luck": 7, "charisma": 5}},
    "lab_coat":     {"name": "🥼 Lab Coat",       "price": 1000,  "slot": "top",    "warmth": 2,  "weather_prot": [],                              "stats": {"health": 8, "intelligence": 3}},
    # ─── New Clothing: Legs ───
    "shorts":       {"name": "🩳 Shorts",         "price": 40,    "slot": "legs",   "warmth": 0,  "weather_prot": ["sunny","heatwave"],         "stats": {}},
    "cargo_pants":  {"name": "👖 Cargo Pants",   "price": 180,   "slot": "legs",   "warmth": 3,  "weather_prot": ["windy"],                       "stats": {"energy": 3}},
    "skirt":        {"name": "👗 Skirt",          "price": 120,   "slot": "legs",   "warmth": 1,  "weather_prot": [],                              "stats": {"luck": 2}},
    "overalls":     {"name": "🩰 Overalls",       "price": 280,   "slot": "legs",   "warmth": 3,  "weather_prot": ["rainy","muddy"],            "stats": {"energy": 5}},
    "chinos":       {"name": "👖 Chinos",         "price": 140,   "slot": "legs",   "warmth": 2,  "weather_prot": [],                              "stats": {"luck": 1}},
    # ─── New Clothing: Feet ───
    "sneakers":     {"name": "👟 Sneakers",       "price": 180,   "slot": "feet",   "warmth": 1,  "weather_prot": [],                              "stats": {"energy": 5}},
    "dress_shoes":  {"name": "👞 Dress Shoes",   "price": 350,   "slot": "feet",   "warmth": 1,  "weather_prot": [],                              "stats": {"luck": 3}},
    "combat_boots": {"name": "🥾 Combat Boots",  "price": 700,   "slot": "feet",   "warmth": 4,  "weather_prot": ["rainy","snowy","muddy"],   "stats": {"health": 8, "energy": 3}},
    "hiking_boots": {"name": "🥾 Hiking Boots",  "price": 550,   "slot": "feet",   "warmth": 4,  "weather_prot": ["rainy","snowy","windy","muddy"], "stats": {"energy": 5}},
    # ─── New Clothing: Accessories ───
    "watch":        {"name": "⌚ Watch",           "price": 300,   "slot": "accessory","warmth": 0,"weather_prot": [],                              "stats": {"luck": 2, "energy": 2}},
    "necklace":     {"name": "📿 Necklace",       "price": 800,   "slot": "accessory","warmth": 0,"weather_prot": [],                              "stats": {"luck": 5, "charisma": 3}},
    "ring":         {"name": "💍 Ring",           "price": 600,   "slot": "accessory","warmth": 0,"weather_prot": [],                              "stats": {"luck": 4, "health": 3}},
    "bracelet":     {"name": "🪙 Bracelet",       "price": 400,   "slot": "accessory","warmth": 0,"weather_prot": [],                              "stats": {"luck": 3, "energy": 2}},
    "tie":          {"name": "👔 Tie",            "price": 100,   "slot": "accessory","warmth": 0,"weather_prot": [],                              "stats": {"luck": 2}},
    "belt":         {"name": "🪖 Belt",           "price": 90,    "slot": "accessory","warmth": 1,"weather_prot": [],                              "stats": {"health": 2}},
    "earmuffs":     {"name": "🎧 Earmuffs",       "price": 130,   "slot": "accessory","warmth": 3,"weather_prot": ["snowy","windy","foggy"],     "stats": {"energy": 2}},
}

POSSESSIONS = {
    "phone":        {"name": "📱 Phone",          "price": 800,   "stats": {"luck": 2, "energy": 2},   "description": "Stay connected"},
    "laptop":       {"name": "💻 Laptop",         "price": 2000,  "stats": {"luck": 3, "energy": 3},   "description": "Work from anywhere"},
    "smartwatch":   {"name": "⌚ Smartwatch",     "price": 1200,  "stats": {"health": 5, "energy": 5},   "description": "Track your vitals"},
    "headphones":   {"name": "🎧 Headphones",     "price": 400,   "stats": {"energy": 3},               "description": "Block out the noise"},
    "backpack":     {"name": "🎒 Backpack",       "price": 300,   "stats": {"energy": 5},               "description": "+5 inventory storage"},
    "first_aid_kit":{"name": "🧰 First Aid Kit",  "price": 600,   "stats": {"health": 10},              "description": "Emergency medical supplies"},
    "lucky_coin":   {"name": "🪙 Lucky Coin",     "price": 1000,  "stats": {"luck": 5},                 "description": "A coin that brings fortune"},
    "compass_poss": {"name": "🧭 Explorer Compass","price": 1500, "stats": {"luck": 3, "energy": 3},    "description": "Never lose your way"},
    "power_bank":   {"name": "🔋 Power Bank",     "price": 500,   "stats": {"energy": 8},               "description": "Portable energy"},
    "water_filter": {"name": "💧 Water Filter",   "price": 700,   "stats": {"health": 5, "hygiene": 5}, "description": "Clean water anywhere"},
    "air_purifier": {"name": "🌬️ Air Purifier",  "price": 900,   "stats": {"health": 8},               "description": "Breathe easy"},
    "fitness_band": {"name": "🏃 Fitness Band",  "price": 600,   "stats": {"health": 5, "energy": 3},   "description": "Stay active"},
    # ─── New Possessions: Electronics ───
    "tablet":       {"name": "📱 Tablet",         "price": 1500,  "stats": {"luck": 2, "energy": 5},   "description": "Portable productivity"},
    "drone":        {"name": "🚁 Drone",          "price": 3000,  "stats": {"luck": 5, "energy": 3},   "description": "Aerial exploration companion"},
    "gaming_console":{"name":"🎮 Gaming Console", "price": 2500,  "stats": {"energy": 8, "luck": 3},     "description": "Game on for energy boosts"},
    # ─── New Possessions: Utilities ───
    "robot_vacuum": {"name": "🤖 Robot Vacuum",  "price": 1200,  "stats": {"hygiene": 10, "energy": 3},  "description": "Automated cleaning"},
    "espresso_machine":{"name":"☕ Espresso Machine","price":1800, "stats": {"energy": 10, "health": 3},  "description": "Barista-quality coffee at home"},
    # ─── New Possessions: Lucky Items ───
    "dream_catcher":{"name": "🪶 Dream Catcher",  "price": 800,   "stats": {"luck": 4, "health": 3},   "description": "Catches bad dreams, brings good fortune"},
    "fortune_statue":{"name":"🗿 Fortune Statue","price": 2000,  "stats": {"luck": 7, "energy": 3},   "description": "An ancient statue that radiates luck"},
    # ─── New Possessions: Fitness ───
    "dumbbells":    {"name": "🏋️ Dumbbells",     "price": 400,   "stats": {"health": 8, "energy": 2},   "description": "Build strength at home"},
    "yoga_mat":     {"name": "🧘 Yoga Mat",       "price": 250,   "stats": {"health": 5, "hygiene": 3},  "description": "Find your inner peace"},
    "running_shoes_poss":{"name":"👟 Running Shoes","price": 500, "stats": {"energy": 8, "health": 3},   "description": "For the dedicated runner"},
}

RAW_MATERIALS = {
    "wood":         {"name": "🪵 Wood",         "price": 10,  "type": "material"},
    "cloth":        {"name": "🧵 Cloth",        "price": 15,  "type": "material"},
    "metal_scrap":  {"name": "🔩 Metal Scrap",  "price": 20,  "type": "material"},
    "herbs":        {"name": "🌿 Herbs",        "price": 25,  "type": "material"},
    "fish":         {"name": "🐟 Raw Fish",     "price": 30,  "type": "material"},
    "stone":        {"name": "🪨 Stone",        "price": 5,   "type": "material"},
    "clay":         {"name": "🟫 Clay",         "price": 12,  "type": "material"},
    "gems":         {"name": "💎 Rough Gem",    "price": 100, "type": "material"},
}

CRAFTING_RECIPES = {
    "cooked_fish":    {"ingredients": {"fish": 1, "firewood": 1},    "result": "cooked_fish_item", "name": "🍳 Cooked Fish",   "description": "A freshly cooked fish"},
    "firewood":       {"ingredients": {"wood": 2},                   "result": "firewood",         "name": "🪵 Firewood",      "description": "Dry wood for a fire"},
    "medicine":       {"ingredients": {"herbs": 3, "water": 1},      "result": "herbal_meds",      "name": "🌿 Homemade Medicine", "description": "Crafted herbal remedy"},
    "fishing_lure":   {"ingredients": {"metal_scrap": 2},            "result": "fishing_lure",     "name": "🪝 Fishing Lure",  "description": "Improves fishing luck"},
    "torch":          {"ingredients": {"wood": 1, "cloth": 1},       "result": "torch",            "name": "🔦 Torch",         "description": "Lights up dark places"},
    "rope":           {"ingredients": {"cloth": 3},                  "result": "rope",             "name": "🪢 Rope",          "description": "Useful for climbing"},
    "bandage_craft":  {"ingredients": {"cloth": 2},                  "result": "bandage",          "name": "🩹 makeshift Bandage", "description": "A simple bandage"},
}
