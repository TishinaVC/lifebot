import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN", "")
DB_PATH = os.getenv("DB_PATH", "lifebot.db")
PREFIX = os.getenv("PREFIX", "!")

BOT_DESCRIPTION = "A full-featured Discord economy & survival bot with jobs, gambling, pets, quests, and more!"

STARTING_WALLET = 200
STARTING_BANK_CAPACITY = 5000

HEALTH_MAX = 100
HUNGER_MAX = 100
THIRST_MAX = 100
ENERGY_MAX = 100
HYGIENE_MAX = 100

DECAY_INTERVAL = 240  # seconds between survival stat decay ticks
DECAY_AMOUNT = 3      # hunger/thirst lost per tick
ENERGY_DECAY = 2      # energy lost per tick
HYGIENE_DECAY = 2     # hygiene lost per tick
HEALTH_DAMAGE_FROM_STARVATION = 5  # health lost when hunger or thirst is 0
ENERGY_DAMAGE_FROM_EXHAUSTION = 3  # health lost when energy is 0
HYGIENE_DAMAGE_FROM_FILTH = 2     # health lost when hygiene is 0

HOSPITAL_FEE_PERCENT = 0.5  # lose 50% of unbanked wallet money on hospital wakeup

XP_PER_LEVEL = 2000
XP_MULTIPLIER = 1.0

CURRENCY = "coins"
CURRENCY_SYMBOL = "🪙"

# Store items: id -> {name, description, price, type, effect}
# type: food, drink, medical, booster, misc
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
    # New food items
    "sushi":       {"name": "🍣 Sushi",        "price": 150,   "type": "food",    "hunger": 40, "thirst": 5,  "health": 10},
    "taco":        {"name": "🌮 Taco",         "price": 70,    "type": "food",    "hunger": 30, "thirst": -5, "health": 3},
    "ramen":       {"name": "🍜 Ramen",        "price": 90,    "type": "food",    "hunger": 35, "thirst": 10, "health": 5},
    "ice_cream":   {"name": "🍨 Ice Cream",    "price": 50,    "type": "food",    "hunger": 15, "thirst": 10, "health": 0},
    # New drinks
    "smoothie":    {"name": "🥤 Smoothie",     "price": 65,    "type": "drink",   "hunger": 10, "thirst": 30, "health": 5},
    "tea":         {"name": "🍵 Tea",          "price": 35,    "type": "drink",   "hunger": 0,  "thirst": 20, "health": 3},
    # New medical
    "first_aid":   {"name": "🧰 First Aid Kit","price": 500,   "type": "medical", "hunger": 0,  "thirst": 0,  "health": 75},
    "herbal_meds": {"name": "🌿 Herbal Remedy","price": 220,   "type": "medical", "hunger": 5,  "thirst": 5,  "health": 35},
    # New boosters
    "xp_potion":   {"name": "🧪 XP Potion",     "price": 300,   "type": "booster", "hunger": 0,  "thirst": 0,  "health": 0, "energy": 0,  "hygiene": 0,  "effect": "xp_boost"},
    "shield":      {"name": "🛡️ Shield Charm",  "price": 400,   "type": "booster", "hunger": 0,  "thirst": 0,  "health": 0, "energy": 0,  "hygiene": 0,  "effect": "crime_protection"},
    # Energy items
    "energy_drink":{"name": "⚡ Energy Drink", "price": 100,   "type": "booster", "hunger": 0,  "thirst": 15, "health": 0, "energy": 40, "hygiene": 0,  "effect": "work_cooldown_reduce"},
    "protein_bar": {"name": "🍫 Protein Bar",  "price": 60,    "type": "food",    "hunger": 15, "thirst": 0,  "health": 0, "energy": 25, "hygiene": 0},
    "coffee":      {"name": "☕ Coffee",       "price": 55,    "type": "drink",   "hunger": 0,   "thirst": 20, "health": 0, "energy": 30, "hygiene": 0},
    # Hygiene items
    "soap":        {"name": "🧼 Soap",         "price": 25,    "type": "hygiene", "hunger": 0,  "thirst": 0,  "health": 0, "energy": 0,  "hygiene": 40},
    "shampoo":     {"name": "🧴 Shampoo",      "price": 50,    "type": "hygiene", "hunger": 0,  "thirst": 0,  "health": 0, "energy": 0,  "hygiene": 60},
    "deodorant":   {"name": "🧻 Deodorant",    "price": 20,    "type": "hygiene", "hunger": 0,  "thirst": 0,  "health": 0, "energy": 0,  "hygiene": 25},
    # Collectibles — rare items for showing off, no functional effect
    "gold_watch":  {"name": "⌚ Gold Watch",    "price": 5000,  "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "diamond":     {"name": "💎 Diamond",       "price": 15000, "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "crown":       {"name": "👑 Golden Crown",  "price": 50000, "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "trophy":      {"name": "🏆 Champion Trophy","price": 10000, "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "painting":    {"name": "🎨 Rare Painting","price": 8000,  "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
    "ruby":        {"name": "❤️ Ruby",          "price": 12000, "type": "collectible", "hunger": 0, "thirst": 0, "health": 0},
}

# Jobs: id -> {name, base_pay, min_level, cooldown, description}
JOBS = {
    "beggar":     {"name": "🧎 Beggar",          "base_pay": 5,    "min_level": 1,  "cooldown": 120,   "description": "Beg on the streets for spare change."},
    "delivery":   {"name": "📦 Delivery Driver", "base_pay": 25,   "min_level": 3,  "cooldown": 600,   "description": "Deliver packages around the city."},
    "chef":       {"name": "👨‍🍳 Chef",            "base_pay": 40,   "min_level": 5,  "cooldown": 1200,  "description": "Cook meals at a fancy restaurant."},
    "mechanic":   {"name": "🔧 Mechanic",        "base_pay": 60,   "min_level": 8,  "cooldown": 1800,  "description": "Fix cars in the auto shop."},
    "barista":    {"name": "☕ Barista",         "base_pay": 35,   "min_level": 4,  "cooldown": 900,   "description": "Brew coffee and serve customers."},
    "electrician":{"name": "⚡ Electrician",     "base_pay": 80,   "min_level": 10, "cooldown": 2400,  "description": "Wire buildings and fix electrical systems."},
    "doctor":     {"name": "👨‍⚕️ Doctor",          "base_pay": 100,  "min_level": 12, "cooldown": 3600,  "description": "Save lives at the hospital."},
    "programmer": {"name": "💻 Programmer",      "base_pay": 150,  "min_level": 15, "cooldown": 3600,  "description": "Write code for tech companies."},
    "pilot":      {"name": "✈️ Pilot",            "base_pay": 250,  "min_level": 20, "cooldown": 7200,  "description": "Fly planes across the world."},
    "astronaut":  {"name": "🚀 Astronaut",       "base_pay": 350,  "min_level": 25, "cooldown": 7200,  "description": "Explore space and conduct research."},
    "ceo":        {"name": "👔 CEO",              "base_pay": 500,  "min_level": 30, "cooldown": 7200,  "description": "Run a multi-million dollar company."},
}

# Pets available for adoption
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

# Achievements: id -> {name, emoji, description, reward}
ACHIEVEMENTS = {
    "first_steps":     {"name": "First Steps",        "emoji": "👶", "description": "Use your first command",                  "reward": 25},
    "rich_beginnings": {"name": "Rich Beginnings",    "emoji": "💰", "description": "Earn your first 5,000 coins",            "reward": 50},
    "high_roller":     {"name": "High Roller",        "emoji": "🎲", "description": "Win 25,000 coins in a single gamble",    "reward": 250},
    "gambler":         {"name": "Gambler",            "emoji": "🎰", "description": "Play 200 gambling games",               "reward": 150},
    "worker_bee":      {"name": "Worker Bee",         "emoji": "🐝", "description": "Complete 100 work shifts",              "reward": 200},
    "survivor":        {"name": "Survivor",           "emoji": "🛡️", "description": "Survive 24 hours without hospital",     "reward": 125},
    "level_10":        {"name": "Rising Star",        "emoji": "⭐", "description": "Reach level 10",                        "reward": 250},
    "level_25":        {"name": "Veteran",            "emoji": "🏅", "description": "Reach level 25",                        "reward": 500},
    "level_50":        {"name": "Legend",             "emoji": "👑", "description": "Reach level 50",                        "reward": 2500},
    "pet_owner":       {"name": "Pet Owner",          "emoji": "🐾", "description": "Adopt a pet",                           "reward": 100},
    "married":         {"name": "Tied the Knot",      "emoji": "💍", "description": "Get married",                           "reward": 150},
    "criminal":        {"name": "Criminal Mastermind","emoji": "🦹", "description": "Commit 100 successful crimes",          "reward": 375},
    "big_spender":     {"name": "Big Spender",        "emoji": "🛍️", "description": "Spend 50,000 coins in the store",      "reward": 250},
    "banker":          {"name": "Banker",             "emoji": "🏦", "description": "Deposit 250,000 coins total",           "reward": 500},
    "unbreakable":     {"name": "Unbreakable",        "emoji": "💪", "description": "Reach max health, hunger, thirst, energy, and hygiene",  "reward": 300},
    # New achievements
    "pet_master":      {"name": "Pet Master",         "emoji": "🏆", "description": "Win 50 pet battles",                    "reward": 300},
    "generous":        {"name": "Generous Soul",      "emoji": "🎁", "description": "Gift coins 50 times",                   "reward": 200},
    "streak_7":        {"name": "Weekly Warrior",     "emoji": "🔥", "description": "Maintain a 7-day daily streak",         "reward": 175},
    "streak_30":       {"name": "Unstoppable",        "emoji": "📆", "description": "Maintain a 30-day daily streak",        "reward": 750},
    "quest_master":    {"name": "Quest Master",       "emoji": "📜", "description": "Complete 50 quests",                    "reward": 400},
    "collector":       {"name": "Collector",          "emoji": "💎", "description": "Own 3 or more collectibles",            "reward": 500},
    "wealthy":         {"name": "Wealthy",            "emoji": "🤑", "description": "Have 100,000 coins in wallet + bank",   "reward": 500},
    "frequent_flyer":  {"name": "Frequent Flyer",     "emoji": "✈️", "description": "Work 500 times",                        "reward": 1000},
    "crime_lord":      {"name": "Crime Lord",         "emoji": "🏴", "description": "Commit 500 successful crimes",          "reward": 1000},
    "lucky":           {"name": "Lucky Duck",         "emoji": "🦆", "description": "Win 500 gambling games",                "reward": 500},
    "energizer":       {"name": "Energizer Bunny",    "emoji": "🔋", "description": "Use 10 energy-restoring items",          "reward": 150},
    "clean_freak":     {"name": "Clean Freak",        "emoji": "🧼", "description": "Use 10 hygiene-restoring items",         "reward": 150},
    "homeowner":       {"name": "Homeowner",          "emoji": "🏠", "description": "Buy your first home",                    "reward": 200},
    "property_mogul":  {"name": "Property Mogul",     "emoji": "🏙️", "description": "Own a tier 15+ home",                   "reward": 1000},
    "interior_designer":{"name":"Interior Designer",  "emoji": "🎨", "description": "Own 5 or more decorations",              "reward": 300},
    "settled_down":    {"name": "Settled Down",       "emoji": "🏡", "description": "Upgrade your home 3 times",               "reward": 250},
    "fisherman":       {"name": "Angler",            "emoji": "🎣", "description": "Catch 25 fish",                          "reward": 200},
    "miner":           {"name": "Prospector",        "emoji": "⛏️", "description": "Mine 25 times",                          "reward": 200},
    "explorer":        {"name": "Explorer",          "emoji": "🧭", "description": "Explore 25 times",                       "reward": 250},
    "craftsman":       {"name": "Craftsman",         "emoji": "🔨", "description": "Craft 10 items",                         "reward": 200},
    "treasure_hunter": {"name": "Treasure Hunter",   "emoji": "🗺️", "description": "Find 10 items through exploration",     "reward": 300},
    "quality_collector":{"name":"Quality Collector", "emoji": "🌈", "description": "Discover items of 5 different qualities", "reward": 400},
    "mythic_find":     {"name": "Mythic Discovery",  "emoji": "🔴", "description": "Find a Mythic quality item",             "reward": 1000},
    "well_equipped":   {"name": "Well Equipped",     "emoji": "🎒", "description": "Equip 5 items at once",                  "reward": 200},
}

# Daily quest templates
QUEST_TEMPLATES = [
    {"desc": "Work {n} times",           "type": "work",       "target": lambda n: n,  "range": (1, 3),   "reward": (50, 150)},
    {"desc": "Gamble {n} times",         "type": "gamble",     "target": lambda n: n,  "range": (1, 5),   "reward": (25, 100)},
    {"desc": "Buy {n} items from store", "type": "buy",        "target": lambda n: n,  "range": (1, 3),   "reward": (40, 125)},
    {"desc": "Earn {n} coins",           "type": "earn",       "target": lambda n: n,  "range": (200, 1000), "reward": (25, 100)},
    {"desc": "Commit {n} crimes",        "type": "crime",      "target": lambda n: n,  "range": (1, 3),   "reward": (50, 175)},
    {"desc": "Use {n} items",            "type": "use_item",   "target": lambda n: n,  "range": (1, 5),   "reward": (25, 75)},
    {"desc": "Fish {n} times",           "type": "fish",       "target": lambda n: n,  "range": (1, 5),   "reward": (40, 150)},
    {"desc": "Mine {n} times",           "type": "mine",       "target": lambda n: n,  "range": (1, 3),   "reward": (50, 175)},
    {"desc": "Explore {n} times",        "type": "explore",    "target": lambda n: n,  "range": (1, 3),   "reward": (75, 200)},
    {"desc": "Craft {n} items",          "type": "craft",      "target": lambda n: n,  "range": (1, 3),   "reward": (50, 150)},
]

# Quests: id -> {name, description, target, reward, xp, type}
QUESTS = {
    "work_3":      {"name": "Hard Worker",       "description": "Work 3 times",            "target": 3,   "reward": 100,  "xp": 25,  "type": "work"},
    "work_5":      {"name": "Dedicated Employee","description": "Work 5 times",            "target": 5,   "reward": 200,  "xp": 50,  "type": "work"},
    "gamble_3":    {"name": "Risk Taker",        "description": "Gamble 3 times",          "target": 3,   "reward": 75,   "xp": 25,  "type": "gamble"},
    "gamble_5":    {"name": "Lucky Streak",      "description": "Gamble 5 times",          "target": 5,   "reward": 150,  "xp": 40,  "type": "gamble"},
    "buy_2":       {"name": "Shopping Spree",    "description": "Buy 2 items from store",  "target": 2,   "reward": 75,   "xp": 25,  "type": "buy"},
    "buy_5":       {"name": "Shopaholic",        "description": "Buy 5 items from store",  "target": 5,   "reward": 175,  "xp": 40,  "type": "buy"},
    "earn_500":    {"name": "Money Maker",       "description": "Earn 500 coins",          "target": 500, "reward": 100,  "xp": 30,  "type": "earn"},
    "earn_1000":   {"name": "Big Earner",        "description": "Earn 1,000 coins",        "target": 1000,"reward": 200,  "xp": 50,  "type": "earn"},
    "crime_2":     {"name": "Petty Criminal",    "description": "Commit 2 crimes",         "target": 2,   "reward": 125,  "xp": 30,  "type": "crime"},
    "crime_5":     {"name": "Crime Spree",       "description": "Commit 5 crimes",         "target": 5,   "reward": 250,  "xp": 60,  "type": "crime"},
    "use_3":       {"name": "Item User",         "description": "Use 3 items",             "target": 3,   "reward": 50,   "xp": 20,  "type": "use_item"},
    "use_5":       {"name": "Consumer",           "description": "Use 5 items",             "target": 5,   "reward": 100,  "xp": 30,  "type": "use_item"},
    # New quests
    "earn_2500":   {"name": "Big Spender Quest",  "description": "Earn 2,500 coins",        "target": 2500,"reward": 400,  "xp": 80,  "type": "earn"},
    "work_10":     {"name": "Workaholic",        "description": "Work 10 times",           "target": 10,  "reward": 350,  "xp": 75,  "type": "work"},
    "gamble_10":   {"name": "High Roller Quest",  "description": "Gamble 10 times",         "target": 10,  "reward": 250,  "xp": 60,  "type": "gamble"},
    "buy_10":      {"name": "Bulk Buyer",        "description": "Buy 10 items from store", "target": 10,  "reward": 300,  "xp": 60,  "type": "buy"},
    "crime_10":    {"name": "Crime Lord Quest",   "description": "Commit 10 crimes",        "target": 10,  "reward": 400,  "xp": 80,  "type": "crime"},
    "use_10":      {"name": "Power User",        "description": "Use 10 items",            "target": 10,  "reward": 175,  "xp": 40,  "type": "use_item"},
}

# ============================================================
# HOUSING SYSTEM
# ============================================================
# 20 tiers from tent to penthouse
# stats_bonus: passive bonuses applied when resting at home
# storage: number of extra inventory slots
# rent: weekly rent for NPC-owned properties (0 = no rent available)
# buy_price: purchase price to own outright (0 = not purchasable)
# advantage/disadvantage: occasional random events

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

# Home upgrades: id -> {name, description, price, effect, max_level}
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

# Home decorations: id -> {name, emoji, price, description}
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

# Rent collection interval (seconds) — 7 days
RENT_INTERVAL = 604800

# ============================================================
# QUALITY / RARITY SYSTEM
# ============================================================
# Qualities modify item effects and value. When an item is found/bought/crafted,
# it gets assigned a quality which multiplies its effects.
# multiplier: scales stat effects (1.0 = normal, 1.5 = 50% better)
# value_mult: scales sell/trade value
# weight: probability weight for random assignment

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

# ============================================================
# TOOLS — enable new activities, have durability
# ============================================================
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
}

# ============================================================
# CLOTHING — weather protection + stat bonuses, has durability
# ============================================================
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
}

# ============================================================
# POSSESSIONS — passive bonuses while in inventory
# ============================================================
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
}

# ============================================================
# WEATHER SYSTEM
# ============================================================
# Weather changes every WEATHER_INTERVAL seconds
# Each weather state has effects on gameplay

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

# ============================================================
# PROCEDURAL NARRATIVE ENGINE ("tiny LLM")
# ============================================================
# Template-based procedural text generation that runs entirely in-bot.
# Generates dynamic event descriptions, NPC encounters, item finds, etc.

NARRATIVE_TEMPLATES = {
    "explore": {
        "intro": [
            "You venture into {location}, {mood}.",
            "Your footsteps echo through {location} as you look around, {mood}.",
            "The path leads you to {location}. You feel {mood}.",
            "{location} stretches before you, {mood}.",
        ],
        "locations": [
            "an abandoned warehouse", "a dense forest", "a crumbling alleyway",
            "the old docks", "a forgotten park", "the city outskirts",
            "a mysterious cave", "the rooftops", "an underground tunnel",
            "a quiet meadow", "the ruins of an old building", "a narrow canyon",
            "the beach at low tide", "a foggy marshland", "an overgrown garden",
            "the train yard", "a dried riverbed", "the edge of a cliff",
        ],
        "moods": [
            "unsure what to expect", "with a sense of adventure",
            "feeling cautious", "heart pounding with excitement",
            "trying to stay quiet", "scanning for danger",
            "ready for anything", "with weary determination",
        ],
        "find_item": [
            "Something catches your eye — a {item}!",
            "Tucked away in a corner, you spot a {item}.",
            "Half-buried in debris, you find a {item}.",
            "Glinting in the light, you discover a {item}.",
            "You almost miss it, but there's a {item} here.",
        ],
        "find_nothing": [
            "You search around but find nothing of value.",
            "The area is picked clean. Nothing here.",
            "Your search comes up empty.",
            "You spend time looking but it's a dead end.",
        ],
        "encounter_npc": [
            "A {npc} appears from the shadows!",
            "You come face to face with a {npc}.",
            "A {npc} blocks your path.",
            "You hear a noise — it's a {npc}.",
        ],
        "npcs": [
            "wandering trader", "suspicious stranger", "friendly hiker",
            "lost tourist", "scruffy scavenger", "nervous courier",
            "old fisherman", "mysterious hooded figure", "panicked runner",
            "calm meditator", "excited child", "weary traveler",
        ],
        "npc_outcomes": {
            "wandering trader": ["offers to trade", "gives you a tip", "sells you something", "ignores you"],
            "suspicious stranger": ["challenges you", "offers a shady deal", "warns you of danger", "disappears"],
            "friendly hiker": ["shares supplies", "points out a landmark", "gives directions", "offers company"],
            "lost tourist": ["asks for directions", "offers a reward for help", "looks confused", "drops something"],
            "scruffy scavenger": ["competes for loot", "offers to split finds", "tries to scam you", "shares gossip"],
            "nervous courier": ["drops a package", "asks you to deliver something", "rushes past", "pays you to stay quiet"],
            "old fisherman": ["shares fishing tips", "gives you bait", "tells a story", "offers a spare fish"],
            "mysterious hooded figure": ["offers a quest", "gives a cryptic warning", "vanishes mysteriously", "sells a rare item"],
            "panicked runner": ["warns of danger ahead", "drops coins while running", "asks for help", "knocks you over"],
            "calm meditator": ["teaches you breathing", "gives you peace of mind", "offers wisdom", "shares energy"],
            "excited child": ["shows you a hiding spot", "gives you a trinket", "points at something shiny", "giggles and runs off"],
            "weary traveler": ["shares a meal", "tells of distant lands", "offers to rest together", "trades stories"],
        },
        "danger": [
            "You slip and twist your ankle! -{hp} HP",
            "A wild animal lunges at you! -{hp} HP",
            "You fall into a hidden hole! -{hp} HP",
            "Debris falls on you! -{hp} HP",
            "You cut yourself on sharp metal! -{hp} HP",
        ],
        "reward": [
            "You feel accomplished! +{xp} XP",
            "Your efforts pay off! +{xp} XP",
            "You learned something new! +{xp} XP",
            "A successful expedition! +{xp} XP",
        ],
    },
    "fish": {
        "cast": [
            "You cast your line into the {spot}, waiting patiently...",
            "Your hook plops into the {spot}. You wait...",
            "You flick your rod and the line sails into the {spot}.",
        ],
        "spots": ["calm waters", "rushing river", "murky pond", "deep lake", "rocky shoreline", "gentle stream"],
        "catch": [
            "You feel a tug! You reel in a {fish}!",
            "Something's biting! You pull up a {fish}!",
            "Your rod bends — got one! A {fish}!",
            "A strong pull! You wrestle in a {fish}!",
        ],
        "fish_types": [
            ("tiny minnow", 5), ("small perch", 15), ("decent bass", 30),
            ("fat catfish", 50), ("shiny trout", 40), ("rare salmon", 80),
            ("golden koi", 150), ("ancient carp", 100), ("electric eel", 60),
            ("mysterious boot", 2), ("waterlogged wallet", 25), ("old bottle with a note", 10),
        ],
        "nothing": [
            "Nothing bites. You wait...",
            "The line sits still. No luck.",
            "Hours pass with no catch.",
            "A fish nibbles but gets away!",
        ],
    },
    "mine": {
        "swing": [
            "You swing your pickaxe at the {vein}, chips flying!",
            "Your pickaxe strikes the {vein} with a clang!",
            "You chip away at the {vein}, sweat on your brow.",
        ],
        "veins": ["rocky wall", "dark tunnel", "glittering seam", "cave wall", "underground deposit", "ancient stone"],
        "find": [
            "You extract a {ore}!",
            "A {ore} tumbles out of the rubble!",
            "You uncover a {ore}!",
            "Hidden in the stone, you find a {ore}!",
        ],
        "ore_types": [
            ("chunk of coal", 10), ("piece of iron", 25), ("hunk of copper", 20),
            ("chunk of silver", 60), ("nugget of gold", 120), ("raw diamond", 300),
            ("shiny gemstone", 80), ("rare crystal", 200), ("chunk of obsidian", 40),
            ("worthless rock", 1), ("old coin", 15), ("fossil", 50),
        ],
        "cave_in": [
            "Rocks shift dangerously above you!",
            "You hear a rumble — the cave is unstable!",
            "Dust falls from the ceiling as the ground shakes!",
        ],
    },
    "random_event": {
        "events": [
            {"text": "A street performer plays music nearby. You toss them some coins. -{coins} coins, +{xp} XP", "coins": (5, 30), "xp": (5, 15), "weight": 10},
            {"text": "You find a wallet on the ground! +{coins} coins", "coins": (20, 100), "xp": 0, "weight": 8},
            {"text": "A sudden gust of wind blows dust in your eyes. -{hp} HP", "coins": 0, "hp": (1, 5), "weight": 7},
            {"text": "You witness a random act of kindness. You feel inspired! +{xp} XP", "coins": 0, "xp": (10, 25), "weight": 8},
            {"text": "A stray cat follows you for a while. You feel less lonely. +{hygiene} hygiene", "coins": 0, "hygiene": (3, 8), "weight": 6},
            {"text": "You stumble on a curb and scrape your knee. -{hp} HP", "coins": 0, "hp": (2, 8), "weight": 7},
            {"text": "Someone hands you a flyer. On the back is a coupon! +{coins} coins next purchase", "coins": (10, 50), "xp": 0, "weight": 6},
            {"text": "You help an elderly person cross the street. +{xp} XP, +{hygiene} hygiene", "coins": 0, "xp": (5, 20), "hygiene": (2, 5), "weight": 7},
            {"text": "A bird drops something on your head. Gross! -{hygiene} hygiene", "coins": 0, "hygiene": (5, 15), "weight": 5},
            {"text": "You find loose change in a vending machine slot! +{coins} coins", "coins": (2, 15), "xp": 0, "weight": 9},
            {"text": "A flash mob appears and dances! You join in. +{energy} energy, +{xp} XP", "coins": 0, "energy": (5, 15), "xp": (5, 15), "weight": 4},
            {"text": "You get caught in a sudden downpour. -{hygiene} hygiene", "coins": 0, "hygiene": (10, 20), "weight": 5},
            {"text": "A street vendor gives you a free sample! +{hunger} hunger", "coins": 0, "hunger": (5, 15), "weight": 6},
            {"text": "You find a four-leaf clover! +{xp} XP, feeling lucky!", "coins": 0, "xp": (10, 20), "weight": 3},
            {"text": "Your phone buzzes — it's a scam call. Annoying! -{energy} energy", "coins": 0, "energy": (2, 5), "weight": 5},
            {"text": "You see a shooting star! You make a wish. +{xp} XP", "coins": 0, "xp": (15, 30), "weight": 2},
            {"text": "A kid bumps into you and apologizes, handing you a coin. +{coins} coins", "coins": (1, 10), "xp": 0, "weight": 5},
            {"text": "You step in a puddle. Your socks are wet. -{energy} energy, -{hygiene} hygiene", "coins": 0, "energy": (3, 8), "hygiene": (3, 8), "weight": 5},
        ],
    },
}

# Crafting recipes: combine items to create new ones
CRAFTING_RECIPES = {
    "cooked_fish":    {"ingredients": {"fish": 1, "firewood": 1},    "result": "cooked_fish_item", "name": "🍳 Cooked Fish",   "description": "A freshly cooked fish"},
    "firewood":       {"ingredients": {"wood": 2},                   "result": "firewood",         "name": "🪵 Firewood",      "description": "Dry wood for a fire"},
    "medicine":       {"ingredients": {"herbs": 3, "water": 1},      "result": "herbal_meds",      "name": "🌿 Homemade Medicine", "description": "Crafted herbal remedy"},
    "fishing_lure":   {"ingredients": {"metal_scrap": 2},            "result": "fishing_lure",     "name": "🪝 Fishing Lure",  "description": "Improves fishing luck"},
    "torch":          {"ingredients": {"wood": 1, "cloth": 1},       "result": "torch",            "name": "🔦 Torch",         "description": "Lights up dark places"},
    "rope":           {"ingredients": {"cloth": 3},                  "result": "rope",             "name": "🪢 Rope",          "description": "Useful for climbing"},
    "bandage_craft":  {"ingredients": {"cloth": 2},                  "result": "bandage",          "name": "🩹 makeshift Bandage", "description": "A simple bandage"},
}

# Raw materials that can be found through activities
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

# ============================================================
# NPC SYSTEM — NPCs with personalities, dialogue, trades, quests
# ============================================================
NPCS = {
    "merchant_sam": {
        "name": "Sam the Merchant", "emoji": "🧑‍💼",
        "location": "market", "personality": "shrewd",
        "greeting": ["Ah, a customer! Step right up.", "Welcome, welcome! Best deals in town!", "You look like someone who appreciates quality."],
        "dialogue": [
            "Business has been good lately. The weather helps.",
            "I once found a legendary gem in these parts. Never again, though.",
            "You hear about the storm last night? Wiped out half my stock.",
            "I'll give you a fair price — but only because I like you.",
        ],
        "trades": [
            {"give": "wood", "give_qty": 3, "receive": "herbs", "receive_qty": 1},
            {"give": "stone", "give_qty": 5, "receive": "cloth", "receive_qty": 2},
            {"give": "metal_scrap", "give_qty": 2, "receive": "fish", "receive_qty": 1},
        ],
        "quest": {"type": "deliver", "item": "cloth", "qty": 5, "reward": 200, "xp": 50, "desc": "Sam needs 5 cloth for a new tent"},
    },
    "fisherman_joe": {
        "name": "Old Joe", "emoji": "🧓",
        "location": "docks", "personality": "wise",
        "greeting": ["Ah, another young angler.", "Sit a while. The fish aren't going anywhere.", "I've been fishing these waters for 40 years."],
        "dialogue": [
            "The big ones come out at dawn, you know.",
            "Stormy weather scares the fish away. Try again when it clears.",
            "I once caught a golden koi that weighed 20 pounds. Let it go, though.",
            "You using the right bait? Try near the rocks.",
            "There's a legend about a monster fish in the deep lake. Never seen it myself.",
        ],
        "trades": [
            {"give": "fish", "give_qty": 3, "receive": "cooked_fish_item", "receive_qty": 1},
            {"give": "fish", "give_qty": 5, "receive": "fishing_lure", "receive_qty": 1},
        ],
        "quest": {"type": "catch", "item": "fish", "qty": 10, "reward": 300, "xp": 80, "desc": "Joe wants you to catch 10 fish to prove you're serious"},
    },
    "miner_kate": {
        "name": "Kate the Miner", "emoji": "👩‍🏭",
        "location": "mines", "personality": "tough",
        "greeting": ["Watch your step down here.", "New to mining? Stick close.", "The deep tunnels aren't for the faint-hearted."],
        "dialogue": [
            "I found a diamond last week. Sold it for a fortune.",
            "The cave-ins are getting worse lately. Be careful.",
            "You hear that rumbling? Could be trouble. Could be treasure.",
            "My pickaxe has been in my family for three generations.",
            "There's a seam of gold deep in tunnel 7, but it's dangerous.",
        ],
        "trades": [
            {"give": "stone", "give_qty": 10, "receive": "metal_scrap", "receive_qty": 2},
            {"give": "gems", "give_qty": 1, "receive": "torch", "receive_qty": 3},
        ],
        "quest": {"type": "mine", "item": "gems", "qty": 3, "reward": 500, "xp": 100, "desc": "Kate needs 3 rough gems for a special project"},
    },
    "chef_marie": {
        "name": "Chef Marie", "emoji": "👩‍🍳",
        "location": "market", "personality": "cheerful",
        "greeting": ["Bonjour! Hungry?", "Ah, come in! I just made something special.", "You look like you need a good meal!"],
        "dialogue": [
            "Cooking is an art. You must feel the ingredients.",
            "Fresh herbs make all the difference, you know.",
            "I can teach you a recipe — if you bring me the right materials.",
            "The storm ruined my vegetable garden. Such is life!",
            "A good meal can change your whole day. Remember that.",
        ],
        "trades": [
            {"give": "herbs", "give_qty": 2, "receive": "herbal_meds", "receive_qty": 1},
            {"give": "fish", "give_qty": 2, "receive": "cooked_fish_item", "receive_qty": 2},
        ],
        "quest": {"type": "deliver", "item": "herbs", "qty": 8, "reward": 250, "xp": 60, "desc": "Marie needs 8 herbs for her signature dish"},
    },
    "mystic_elara": {
        "name": "Elara the Mystic", "emoji": "🔮",
        "location": "forest", "personality": "mysterious",
        "greeting": ["I sensed you coming...", "The spirits whispered your name.", "You seek knowledge, traveler?"],
        "dialogue": [
            "There are things in this world beyond your understanding.",
            "The weather is a reflection of the spiritual realm.",
            "I see... a great fortune in your future. But also great danger.",
            "Bring me gems, and I will read your fortune.",
            "The old ruins hold secrets. But not all secrets should be uncovered.",
        ],
        "trades": [
            {"give": "gems", "give_qty": 2, "receive": "lucky_coin", "receive_qty": 1},
            {"give": "stone", "give_qty": 5, "receive": "torch", "receive_qty": 2},
        ],
        "quest": {"type": "explore", "item": "gems", "qty": 5, "reward": 600, "xp": 150, "desc": "Elara wants 5 gems from the ancient ruins for a ritual"},
    },
    "ranger_tom": {
        "name": "Ranger Tom", "emoji": "🧑‍🌾",
        "location": "forest", "personality": "friendly",
        "greeting": ["Nice day for a walk, isn't it?", "Mind the trails — some are overgrown.", "Always good to see a friendly face out here."],
        "dialogue": [
            "I've seen bears in these woods. Keep your distance.",
            "The foraging is excellent after rain. Try the meadow.",
            "I maintain all the trails out here. It's a labor of love.",
            "If you're exploring, bring a compass. People get lost.",
            "Saw some strange tracks near the canyon yesterday. Big ones.",
        ],
        "trades": [
            {"give": "wood", "give_qty": 5, "receive": "rope", "receive_qty": 1},
            {"give": "herbs", "give_qty": 3, "receive": "bandage", "receive_qty": 1},
        ],
        "quest": {"type": "explore", "item": "wood", "qty": 15, "reward": 350, "xp": 90, "desc": "Tom needs 15 wood to repair the trail bridges"},
    },
    "blacksmith_gus": {
        "name": "Gus the Blacksmith", "emoji": "🧑‍🏭",
        "location": "market", "personality": "gruff",
        "greeting": ["What do you need?", "Make it quick, I'm busy.", "Don't touch the forge."],
        "dialogue": [
            "Good metal is hard to find these days.",
            "I can sharpen your tools — for a price.",
            "The storm damaged my anvil. Cost me a week's work.",
            "You bring me metal scrap, I'll make it worth your while.",
            "A legendary pickaxe? Maybe. If you bring me the right materials.",
        ],
        "trades": [
            {"give": "metal_scrap", "give_qty": 5, "receive": "stone", "receive_qty": 10},
            {"give": "metal_scrap", "give_qty": 10, "receive": "rope", "receive_qty": 2},
        ],
        "quest": {"type": "deliver", "item": "metal_scrap", "qty": 20, "reward": 400, "xp": 100, "desc": "Gus needs 20 metal scrap to forge a special tool"},
    },
    "drifter_vex": {
        "name": "Vex the Drifter", "emoji": "🧥",
        "location": "alley", "personality": "suspicious",
        "greeting": ["...You shouldn't be here.", "Keep your voice down.", "What do you want?"],
        "dialogue": [
            "There are easier ways to make money. Dangerous ones.",
            "The fog is perfect for... certain activities.",
            "I know people. I know things. That's all you need to know.",
            "Stormy nights are the best nights. Nobody's watching.",
            "You didn't see me. I wasn't here. Understand?",
        ],
        "trades": [
            {"give": "cloth", "give_qty": 3, "receive": "lockpick", "receive_qty": 1},
            {"give": "metal_scrap", "give_qty": 3, "receive": "torch", "receive_qty": 1},
        ],
        "quest": {"type": "crime", "item": "any", "qty": 5, "reward": 500, "xp": 120, "desc": "Vex wants you to commit 5 crimes to prove you're useful"},
    },
}

# ============================================================
# LOCATION SYSTEM — distinct areas with unique encounters
# ============================================================
LOCATIONS = {
    "market": {
        "name": "🏪 Town Market", "emoji": "🏪",
        "description": "A bustling marketplace filled with merchants and goods.",
        "activities": ["trade", "buy", "sell", "npc"],
        "npcs": ["merchant_sam", "chef_marie", "blacksmith_gus"],
        "encounter_chance": 0.3,
        "loot_table": ["cloth", "herbs", "metal_scrap", "stone"],
        "danger": 0.0,
    },
    "docks": {
        "name": "⚓ The Docks", "emoji": "⚓",
        "description": "Weathered piers and the smell of salt water. Perfect for fishing.",
        "activities": ["fish", "npc", "explore"],
        "npcs": ["fisherman_joe"],
        "encounter_chance": 0.25,
        "loot_table": ["fish", "cloth", "metal_scrap"],
        "danger": 0.05,
    },
    "mines": {
        "name": "⛏️ The Mines", "emoji": "⛏️",
        "description": "Dark tunnels stretching deep underground. Rich with ore.",
        "activities": ["mine", "npc", "explore"],
        "npcs": ["miner_kate"],
        "encounter_chance": 0.35,
        "loot_table": ["stone", "metal_scrap", "gems", "clay"],
        "danger": 0.15,
    },
    "forest": {
        "name": "🌲 Whispering Forest", "emoji": "🌲",
        "description": "Ancient trees and hidden clearings. Full of life and mystery.",
        "activities": ["forage", "chop", "explore", "npc"],
        "npcs": ["mystic_elara", "ranger_tom"],
        "encounter_chance": 0.4,
        "loot_table": ["wood", "herbs", "stone", "cloth"],
        "danger": 0.10,
    },
    "alley": {
        "name": "🏚️ Back Alleys", "emoji": "🏚️",
        "description": "Narrow, shadowy passages. Not a place for the unwary.",
        "activities": ["explore", "crime", "npc"],
        "npcs": ["drifter_vex"],
        "encounter_chance": 0.45,
        "loot_table": ["metal_scrap", "cloth", "stone"],
        "danger": 0.20,
    },
    "beach": {
        "name": "🌅 Sunset Beach", "emoji": "🌅",
        "description": "Golden sands and rolling waves. Relaxing, but watch the tide.",
        "activities": ["fish", "forage", "explore"],
        "npcs": [],
        "encounter_chance": 0.2,
        "loot_table": ["stone", "clay", "fish", "cloth"],
        "danger": 0.05,
    },
    "ruins": {
        "name": "🏛️ Ancient Ruins", "emoji": "🏛️",
        "description": "Crumbling stone structures from a forgotten age. Secrets lie within.",
        "activities": ["explore", "dig", "mine"],
        "npcs": [],
        "encounter_chance": 0.5,
        "loot_table": ["stone", "gems", "metal_scrap", "clay"],
        "danger": 0.25,
    },
    "mountains": {
        "name": "⛰️ Misty Mountains", "emoji": "⛰️",
        "description": "Towering peaks shrouded in fog. The brave are rewarded here.",
        "activities": ["mine", "explore", "chop"],
        "npcs": [],
        "encounter_chance": 0.35,
        "loot_table": ["stone", "gems", "wood", "metal_scrap"],
        "danger": 0.20,
    },
    "lake": {
        "name": "🏞️ Crystal Lake", "emoji": "🏞️",
        "description": "Clear, still waters surrounded by wildflowers. A peaceful spot.",
        "activities": ["fish", "forage", "explore"],
        "npcs": [],
        "encounter_chance": 0.15,
        "loot_table": ["fish", "herbs", "wood", "clay"],
        "danger": 0.03,
    },
    "canyon": {
        "name": "🏜️ Red Canyon", "emoji": "🏜️",
        "description": "Sweeping rock formations and narrow passes. Treasure hunters' paradise.",
        "activities": ["explore", "dig", "mine"],
        "npcs": [],
        "encounter_chance": 0.4,
        "loot_table": ["stone", "gems", "metal_scrap", "clay"],
        "danger": 0.18,
    },
}

# ============================================================
# DAY / NIGHT CYCLE
# ============================================================
# Game time advances faster than real time. Each real hour = 2 game hours.
# Different times of day have different gameplay modifiers.

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

# ============================================================
# COOKING SYSTEM — combine raw ingredients into meals with buffs
# ============================================================
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

# ============================================================
# BUFFS / DEBUFFS SYSTEM — temporary status effects
# ============================================================
# Buffs are applied from food, weather, activities, or random events
# They last for a duration (in seconds) and modify gameplay stats

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

# ============================================================
# WEATHER-TRIGGERED BUFFS / DEBUFFS
# ============================================================
# During severe weather, players may receive temporary debuffs.
# Clothing with weather_prot for the current weather reduces the chance.
# Applied during survival decay loop.

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

# ============================================================
# REPUTATION / FACTION SYSTEM
# ============================================================
# Players build standing with different factions through activities
# High reputation unlocks benefits; low reputation has consequences

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
