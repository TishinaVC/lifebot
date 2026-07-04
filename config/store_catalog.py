"""
Hierarchical store catalog with categories, subcategories, and special deals.
This structure allows infinite expansion beyond Discord's 25-choice limit
by using interactive button navigation instead of slash command choices.

Each category maps to subcategories, which map to item IDs.
Item IDs reference entries in STORE_ITEMS, TOOLS, CLOTHING, or POSSESSIONS.
"""

# ─── Catalog Structure ───
# source: "store_items" → look up in STORE_ITEMS
# source: "tools" → look up in TOOLS
# source: "clothing" → look up in CLOTHING
# source: "possessions" → look up in POSSESSIONS

STORE_CATALOG = {
    "food": {
        "name": "Food & Snacks",
        "emoji": "🍞",
        "color": 0xE67E22,
        "source": "store_items",
        "subcategories": {
            "snacks": {
                "name": "Quick Snacks",
                "emoji": "🥨",
                "item_ids": ["bread", "taco", "protein_bar", "donut", "cookie", "chips", "popcorn", "pretzel"],
            },
            "meals": {
                "name": "Full Meals",
                "emoji": "🍽️",
                "item_ids": ["burger", "steak", "pizza", "ramen", "sushi", "pasta", "curry", "fried_chicken", "kebab", "noodle_bowl"],
            },
            "desserts": {
                "name": "Desserts",
                "emoji": "🍰",
                "item_ids": ["ice_cream", "cake", "pie", "pudding", "chocolate_bar", "cheesecake", "brownie"],
            },
            "breakfast": {
                "name": "Breakfast",
                "emoji": "🥞",
                "item_ids": ["eggs", "pancakes", "waffles", "oatmeal", "bagel", "croissant", "muffin"],
            },
            "healthy": {
                "name": "Healthy & Fresh",
                "emoji": "🥗",
                "item_ids": ["salad", "fruit_bowl", "veggie_platter", "quinoa_salad", "yogurt", "granola_bar"],
            },
        },
    },
    "drinks": {
        "name": "Drinks",
        "emoji": "🥤",
        "color": 0x3498DB,
        "source": "store_items",
        "subcategories": {
            "water": {
                "name": "Water",
                "emoji": "💧",
                "item_ids": ["water", "sparkling_water", "mineral_water", "coconut_water"],
            },
            "soda": {
                "name": "Soda & Cold",
                "emoji": "🥤",
                "item_ids": ["soda", "cola", "lemonade", "root_beer", "energy_drink"],
            },
            "hot": {
                "name": "Hot Drinks",
                "emoji": "☕",
                "item_ids": ["coffee", "tea", "hot_chocolate", "espresso", "matcha_latte"],
            },
            "juice": {
                "name": "Juice & Smoothies",
                "emoji": "🧃",
                "item_ids": ["juice", "smoothie", "orange_juice", "berry_smoothie", "green_juice"],
            },
            "alcohol": {
                "name": "Alcohol",
                "emoji": "🍺",
                "item_ids": ["beer", "wine", "whiskey", "cocktail", "sake"],
            },
        },
    },
    "medical": {
        "name": "Medical",
        "emoji": "🩹",
        "color": 0xE74C3C,
        "source": "store_items",
        "subcategories": {
            "basic": {
                "name": "Basic Aid",
                "emoji": "🩹",
                "item_ids": ["bandage", "painkiller", "herbal_meds", "antiseptic", "cough_syrup"],
            },
            "advanced": {
                "name": "Advanced Kits",
                "emoji": "🧰",
                "item_ids": ["medkit", "first_aid", "vitamin", "vitamin_c", "antibiotics"],
            },
            "emergency": {
                "name": "Emergency",
                "emoji": "💉",
                "item_ids": ["adrenaline_shot", "surgery_kit", "defibrillator", "trauma_kit"],
            },
        },
    },
    "boosters": {
        "name": "Boosters",
        "emoji": "⚡",
        "color": 0x9B59B6,
        "source": "store_items",
        "subcategories": {
            "gamble": {
                "name": "Gambling Luck",
                "emoji": "🍀",
                "item_ids": ["lucky_charm", "four_leaf_clover", "fortune_cookie"],
            },
            "xp_energy": {
                "name": "XP & Energy",
                "emoji": "🧪",
                "item_ids": ["xp_potion", "energy_drink", "mega_xp_potion", "hyper_energy"],
            },
            "crime_defense": {
                "name": "Crime Defense",
                "emoji": "🛡️",
                "item_ids": ["shield", "super_shield", "alarm_system"],
            },
        },
    },
    "stat_boosters": {
        "name": "Stat Boosters",
        "emoji": "📊",
        "color": 0x1ABC9C,
        "source": "store_items",
        "subcategories": {
            "physical": {
                "name": "Physical",
                "emoji": "💪",
                "item_ids": ["protein_shake", "endurance_shot", "hand_warmup_cream", "muscle_relaxant"],
            },
            "mental": {
                "name": "Mental",
                "emoji": "🧠",
                "item_ids": ["nootropic", "caffeine_pill", "eye_drops", "focus_crystal"],
            },
            "luck_charm": {
                "name": "Luck & Charm",
                "emoji": "🍀",
                "item_ids": ["lucky_rabbit_foot", "confidence_potion", "charm_bracelet_boost", "lucky_pen"],
            },
        },
    },
    "hygiene": {
        "name": "Hygiene",
        "emoji": "🧼",
        "color": 0x95A5A6,
        "source": "store_items",
        "subcategories": {
            "basic": {
                "name": "Basic Care",
                "emoji": "🧼",
                "item_ids": ["soap", "deodorant", "hand_sanitizer", "dental_kit"],
            },
            "premium": {
                "name": "Premium Care",
                "emoji": "🧴",
                "item_ids": ["shampoo", "bath_bomb", "perfume", "luxury_lotion", "spa_kit"],
            },
        },
    },
    "tools": {
        "name": "Tools",
        "emoji": "🔧",
        "color": 0xF39C12,
        "source": "tools",
        "subcategories": {
            "gathering": {
                "name": "Gathering Tools",
                "emoji": "🌾",
                "item_ids": ["fishing_rod", "pickaxe", "shovel", "axe", "bug_net"],
            },
            "exploration": {
                "name": "Exploration Gear",
                "emoji": "🧭",
                "item_ids": ["compass", "metal_detector", "camera", "telescope", "binoculars", "flashlight"],
            },
            "hunting": {
                "name": "Hunting Gear",
                "emoji": "🎯",
                "item_ids": ["hunting_rifle", "bow", "trap", "tracking_device"],
            },
            "specialty": {
                "name": "Specialty Tools",
                "emoji": "🔓",
                "item_ids": ["lockpick", "diving_gear", "grappling_hook", "seismograph"],
            },
        },
    },
    "clothing": {
        "name": "Clothing",
        "emoji": "👕",
        "color": 0xE91E63,
        "source": "clothing",
        "subcategories": {
            "tops": {
                "name": "Tops",
                "emoji": "👕",
                "item_ids": ["tshirt", "jacket", "raincoat", "winter_coat", "dress", "suit", "armor", "designer_outfit", "thermal_suit", "hazmat_suit", "hoodie", "vest", "tuxedo", "lab_coat"],
            },
            "legs": {
                "name": "Legs",
                "emoji": "👖",
                "item_ids": ["jeans", "shorts", "cargo_pants", "skirt", "overalls", "chinos"],
            },
            "feet": {
                "name": "Footwear",
                "emoji": "🥾",
                "item_ids": ["boots", "sandals", "rain_boots", "snow_boots", "sneakers", "dress_shoes", "combat_boots", "hiking_boots"],
            },
            "accessories": {
                "name": "Accessories",
                "emoji": "🕶️",
                "item_ids": ["sunglasses", "umbrella", "hat", "scarf", "gloves", "watch", "necklace", "ring", "bracelet", "tie", "belt", "earmuffs"],
            },
        },
    },
    "possessions": {
        "name": "Possessions",
        "emoji": "📦",
        "color": 0x2ECC71,
        "source": "possessions",
        "subcategories": {
            "electronics": {
                "name": "Electronics",
                "emoji": "📱",
                "item_ids": ["phone", "laptop", "smartwatch", "headphones", "tablet", "drone", "gaming_console"],
            },
            "utilities": {
                "name": "Utilities",
                "emoji": "🔋",
                "item_ids": ["backpack", "power_bank", "water_filter", "air_purifier", "first_aid_kit", "robot_vacuum", "espresso_machine"],
            },
            "lucky_items": {
                "name": "Lucky Items",
                "emoji": "🍀",
                "item_ids": ["lucky_coin", "compass_poss", "dream_catcher", "fortune_statue"],
            },
            "fitness": {
                "name": "Fitness & Health",
                "emoji": "🏃",
                "item_ids": ["fitness_band", "dumbbells", "yoga_mat", "running_shoes_poss"],
            },
        },
    },
    "collectibles": {
        "name": "Collectibles",
        "emoji": "💎",
        "color": 0xF1C40F,
        "source": "store_items",
        "subcategories": {
            "gems": {
                "name": "Gems & Jewels",
                "emoji": "💎",
                "item_ids": ["diamond", "ruby", "emerald", "sapphire", "amethyst", "pearl", "opal", "topaz"],
            },
            "trophies": {
                "name": "Trophies & Awards",
                "emoji": "🏆",
                "item_ids": ["trophy", "gold_medal", "championship_belt", "platinum_cup"],
            },
            "art": {
                "name": "Art & Antiques",
                "emoji": "🎨",
                "item_ids": ["painting", "sculpture", "vintage_vase", "antique_clock", "vinyl_record", "rare_book"],
            },
            "rare_finds": {
                "name": "Rare Finds",
                "emoji": "🏺",
                "item_ids": ["crown", "golden_idol", "meteor_fragment", "ancient_relic", "dragon_egg", "pharaoh_mask"],
            },
        },
    },
}

# ─── Special Deals ───

MYSTERY_BOX = {
    "name": "Mystery Box",
    "emoji": "🎁",
    "price": 500,
    "description": "A mysterious box containing a random store item. Could be anything — from bread to a diamond!",
    "rarity_weights": {
        "common": 50,
        "uncommon": 25,
        "rare": 15,
        "epic": 7,
        "legendary": 2.5,
        "mythic": 0.5,
    },
}

DAILY_DEAL = {
    "discount_percent": 40,
    "description": "One special item at a huge discount. Changes every day at midnight!",
}

FLASH_SALE = {
    "discount_percent": 25,
    "description": "A random category goes on sale. Changes every 6 hours!",
    "interval_hours": 6,
}

LUCKY_DIP = {
    "name": "Lucky Dip",
    "emoji": "🎰",
    "price": 200,
    "description": "A cheap dip that gives you a random low-value item. Great for stocking up!",
}

TRAVELER_PACK = {
    "name": "Traveler's Pack",
    "emoji": "🎒",
    "price": 1000,
    "description": "A bundle of useful items for explorers. Contains food, water, medical supplies, and a chance at a rare item!",
    "contents": {
        "guaranteed": ["bread", "water", "bandage", "energy_drink"],
        "chance_items": [
            {"item_id": "compass", "chance": 0.15, "source": "tools"},
            {"item_id": "metal_detector", "chance": 0.05, "source": "tools"},
            {"item_id": "lucky_charm", "chance": 0.10, "source": "store_items"},
            {"item_id": "diamond", "chance": 0.01, "source": "store_items"},
        ],
    },
}

# ─── Flash sale category rotation ───
FLASH_SALE_CATEGORIES = ["food", "drinks", "medical", "hygiene", "boosters", "stat_boosters", "tools", "clothing", "possessions"]

# ─── Helper functions for special deals ───

import datetime
import random as _random


def get_daily_deal_item():
    """Returns (item_id, source, original_price, discounted_price) for today's daily deal.
    Seeded by date so it's consistent for the whole day."""
    from config.items import STORE_ITEMS
    today = datetime.date.today().toordinal()
    eligible = [(k, v) for k, v in STORE_ITEMS.items() if v["type"] not in ("collectible",) and v["price"] >= 50]
    rng = _random.Random(today * 42)
    item_id, item_data = rng.choice(eligible)
    original = item_data["price"]
    discounted = int(original * (1 - DAILY_DEAL["discount_percent"] / 100))
    return item_id, "store_items", original, discounted


def get_flash_sale_category():
    """Returns the category_id that's currently on flash sale.
    Changes every FLASH_SALE_INTERVAL_HOURS hours."""
    now = datetime.datetime.now()
    slot = (now.hour // FLASH_SALE["interval_hours"]) + (now.day * 24 // FLASH_SALE["interval_hours"])
    rng = _random.Random(slot * 17)
    return rng.choice(FLASH_SALE_CATEGORIES)


def get_flash_sale_discount():
    """Returns the discount multiplier (e.g. 0.75 for 25% off)."""
    return 1.0 - (FLASH_SALE["discount_percent"] / 100)


def get_mystery_box_item():
    """Returns (item_id, item_data) from the mystery box.
    Weighted by rarity tiers."""
    from config.items import STORE_ITEMS
    eligible = [(k, v) for k, v in STORE_ITEMS.items() if v["type"] != "collectible"]
    rng = _random.Random()
    roll = rng.random() * 100
    if roll < 0.5:
        pool = [(k, v) for k, v in eligible if v["price"] >= 5000]
    elif roll < 3.0:
        pool = [(k, v) for k, v in eligible if v["price"] >= 2000]
    elif roll < 10.0:
        pool = [(k, v) for k, v in eligible if v["price"] >= 800]
    elif roll < 25.0:
        pool = [(k, v) for k, v in eligible if v["price"] >= 300]
    elif roll < 50.0:
        pool = [(k, v) for k, v in eligible if v["price"] >= 100]
    else:
        pool = [(k, v) for k, v in eligible if v["price"] < 100]
    if not pool:
        pool = eligible
    return rng.choice(pool)


def get_lucky_dip_item():
    """Returns (item_id, item_data) from the lucky dip. Only cheap items."""
    from config.items import STORE_ITEMS
    eligible = [(k, v) for k, v in STORE_ITEMS.items() if v["type"] not in ("collectible", "stat_booster") and v["price"] <= 100]
    rng = _random.Random()
    if not eligible:
        eligible = [(k, v) for k, v in STORE_ITEMS.items() if v["price"] <= 200]
    return rng.choice(eligible)
