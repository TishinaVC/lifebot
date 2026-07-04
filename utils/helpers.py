import discord
from config import XP_PER_LEVEL

def xp_for_next_level(level: int) -> int:
    return int(XP_PER_LEVEL * (1 + (level - 1) * 0.25))

def check_level_up(current_xp: int, current_level: int) -> tuple:
    """Returns (new_level, leveled_up: bool)"""
    level = current_level
    xp = current_xp
    leveled = False
    while xp >= xp_for_next_level(level):
        xp -= xp_for_next_level(level)
        level += 1
        leveled = True
    return level, leveled

def job_pay(base_pay: int, job_level: int, performance: float) -> int:
    """Calculate pay based on job level and minigame performance (0.0 - 1.0)"""
    multiplier = 1.0 + (job_level - 1) * 0.05
    return int(base_pay * multiplier * max(0.2, performance))

def clamp(value: int, minimum: int = 0, maximum: int = 100) -> int:
    return max(minimum, min(maximum, value))


def stat_modifier(data: dict, activity: str) -> dict:
    """Calculate modifiers based on survival stats for a given activity.
    
    Activities: 'work', 'gamble', 'crime', 'pet_battle', 'social', 'all'
    Returns dict with keys: pay_mult, success_bonus, xp_mult, luck_bonus, stat_cost_mult
    
    Low stats reduce output; high stats provide bonuses.
    Each stat contributes a portion based on relevance to the activity.
    """
    energy = data.get("energy", 100)
    hygiene = data.get("hygiene", 100)
    hunger = data.get("hunger", 100)
    thirst = data.get("thirst", 100)
    health = data.get("health", 100)
    
    # Base modifier: each stat at 100 = 1.0 multiplier, at 0 = 0.5 multiplier
    def stat_mult(val):
        return 0.5 + (val / 100) * 0.5  # ranges 0.5 to 1.0
    
    # Activity-specific stat weights (must sum to 1.0)
    weights = {
        "work":       {"energy": 0.40, "health": 0.25, "hunger": 0.15, "thirst": 0.15, "hygiene": 0.05},
        "gamble":     {"energy": 0.30, "health": 0.20, "hunger": 0.15, "thirst": 0.15, "hygiene": 0.20},
        "crime":      {"energy": 0.30, "health": 0.25, "hygiene": 0.20, "hunger": 0.12, "thirst": 0.13},
        "pet_battle": {"energy": 0.35, "health": 0.30, "hunger": 0.15, "thirst": 0.15, "hygiene": 0.05},
        "social":     {"hygiene": 0.40, "energy": 0.20, "health": 0.15, "hunger": 0.12, "thirst": 0.13},
        "all":        {"energy": 0.20, "health": 0.20, "hunger": 0.20, "thirst": 0.20, "hygiene": 0.20},
    }
    
    w = weights.get(activity, weights["all"])
    
    combined = (
        stat_mult(energy) * w["energy"] +
        stat_mult(hygiene) * w["hygiene"] +
        stat_mult(hunger) * w["hunger"] +
        stat_mult(thirst) * w["thirst"] +
        stat_mult(health) * w["health"]
    )
    
    # combined ranges from 0.5 (all stats dead) to 1.0 (all stats full)
    # Convert to a multiplier: 0.5 -> 0.5x output, 1.0 -> 1.2x output (bonus for being healthy)
    pay_mult = 0.5 + combined * 0.7  # 0.5 + 0.35..0.7 = 0.85..1.2
    xp_mult = 0.6 + combined * 0.5   # 0.6 + 0.3..0.5 = 0.9..1.1
    success_bonus = (combined - 0.75) * 0.2  # -0.05..+0.05
    luck_bonus = (combined - 0.75) * 0.1     # -0.025..+0.025
    stat_cost_mult = 2.0 - combined           # low stats = more stat drain (1.0..1.5)
    
    return {
        "pay_mult": pay_mult,
        "xp_mult": xp_mult,
        "success_bonus": success_bonus,
        "luck_bonus": luck_bonus,
        "stat_cost_mult": stat_cost_mult,
        "combined": combined,
    }


async def get_housing_bonus(user_id: int) -> dict:
    """Get gameplay bonuses from the player's home and upgrades.
    Returns dict with: pay_mult, xp_mult, security_bonus, crime_success_penalty
    """
    import database as db
    from config import HOUSING_TIERS, HOME_UPGRADES

    home = await db.get_home(user_id)
    if not home:
        return {"pay_mult": 1.0, "xp_mult": 1.0, "security_bonus": 0.0, "crime_success_penalty": 0.0}

    tier = HOUSING_TIERS.get(home["tier_id"], {})
    tier_level = tier.get("tier", 0)
    upgrades = await db.get_upgrades(user_id)

    # Tier-based bonuses scale with tier level
    pay_mult = 1.0 + (tier_level * 0.005)  # up to +10% at tier 20
    xp_mult = 1.0 + (tier_level * 0.005)   # up to +10% at tier 20
    security_bonus = 0.0

    # Upgrade-based bonuses
    security_lvl = upgrades.get("security", 0)
    security_bonus = security_lvl * 0.10  # -10% crime success against you per level

    return {
        "pay_mult": pay_mult,
        "xp_mult": xp_mult,
        "security_bonus": security_bonus,
        "crime_success_penalty": 0.0,
    }


async def get_equipment_bonuses(user_id: int) -> dict:
    """Get gameplay bonuses from equipped clothing and possessions.
    Quality multiplies the stat bonuses.
    """
    import database as db
    from config import CLOTHING, POSSESSIONS
    from utils.quality import quality_multiplier

    equipped = await db.get_equipped(user_id)
    bonuses = {"luck": 0, "energy": 0, "health": 0, "hygiene": 0, "pay_mult": 1.0, "xp_mult": 1.0}

    for item in equipped:
        qmult = quality_multiplier(item["quality"])
        if item["item_type"] == "clothing":
            stats = CLOTHING.get(item["item_id"], {}).get("stats", {})
        elif item["item_type"] == "possession":
            stats = POSSESSIONS.get(item["item_id"], {}).get("stats", {})
        else:
            continue
        for stat, val in stats.items():
            if stat in bonuses:
                bonuses[stat] += int(val * qmult)

    return bonuses


async def get_all_bonuses(user_id: int) -> dict:
    """Combine housing, equipment, weather, faction, buff, and time bonuses into one dict.
    Returns: pay_mult, xp_mult, luck_bonus, success_bonus, security_bonus,
             energy_bonus, health_bonus, hygiene_bonus, weather,
             fish_luck_mult, mine_luck_mult, crime_success_mult, rare_find_chance
    """
    housing = await get_housing_bonus(user_id)
    equip = await get_equipment_bonuses(user_id)

    import database as db
    from config import WEATHER_STATES
    current_weather = await db.get_weather()
    w_effects = WEATHER_STATES.get(current_weather, {}).get("effects", {})

    pay_mult = housing["pay_mult"] * w_effects.get("work_pay_mult", 1.0)
    xp_mult = housing["xp_mult"]
    luck_bonus = equip.get("luck", 0) * 0.01

    # Equipment xp_mult (from possessions like rabbit/owl bonuses via stats)
    # xp_mult from equipment is applied via luck stat conversion — handled separately

    # Buff multipliers
    buff_pay = await db.get_buff_mult(user_id, "work_pay")
    buff_xp = await db.get_buff_mult(user_id, "xp_mult")
    buff_luck = await db.get_buff_mult(user_id, "luck")
    buff_crime = await db.get_buff_mult(user_id, "crime_success")
    pay_mult *= buff_pay
    xp_mult *= buff_xp
    luck_bonus *= buff_luck

    # Time-of-day effects
    time_effects = await db.get_time_effects()
    pay_mult *= time_effects.get("work_pay", 1.0)
    xp_mult *= time_effects.get("xp_mult", 1.0)

    # Faction benefits
    fish_luck_mult = w_effects.get("fish_luck_mult", 1.0)
    mine_luck_mult = 1.0
    crime_success_mult = w_effects.get("crime_success_mult", 1.0) * time_effects.get("crime_success", 1.0) * buff_crime
    rare_find_chance = time_effects.get("rare_find_chance", 1.0)

    fishers_benefit = await db.get_faction_benefit(user_id, "fishers")
    fish_luck_mult *= fishers_benefit.get("fish_luck", 1.0)
    miners_benefit = await db.get_faction_benefit(user_id, "miners")
    mine_luck_mult *= miners_benefit.get("mine_luck", 1.0)
    underworld_benefit = await db.get_faction_benefit(user_id, "underworld")
    crime_success_mult *= underworld_benefit.get("crime_success", 1.0)

    return {
        "pay_mult": pay_mult,
        "xp_mult": xp_mult,
        "luck_bonus": luck_bonus,
        "success_bonus": 0.0,
        "security_bonus": housing["security_bonus"],
        "energy_bonus": equip.get("energy", 0),
        "health_bonus": equip.get("health", 0),
        "hygiene_bonus": equip.get("hygiene", 0),
        "weather": current_weather,
        "weather_pay_mult": w_effects.get("work_pay_mult", 1.0),
        "weather_crime_mult": w_effects.get("crime_success_mult", 1.0),
        "weather_fish_luck_mult": w_effects.get("fish_luck_mult", 1.0),
        "time_period": await db.get_time_period(),
        "fish_luck_mult": fish_luck_mult,
        "mine_luck_mult": mine_luck_mult,
        "crime_success_mult": crime_success_mult,
        "rare_find_chance": rare_find_chance,
    }

PET_BONUSES = {
    "dog":     {"pay_mult": 1.05},
    "cat":     {"gamble_luck": 0.03},
    "rabbit":  {"xp_mult": 1.08},
    "parrot":  {"quest_reward_mult": 1.10},
    "dragon":  {"pay_mult": 1.15, "gamble_luck": 0.03, "xp_mult": 1.15},
    "unicorn": {"pay_mult": 1.25, "gamble_luck": 0.05, "xp_mult": 1.25, "quest_reward_mult": 1.25},
}

def pet_bonus(pet_id: str | None, bonus_type: str, value: int | float) -> int | float:
    """Apply a pet bonus to a value. bonus_type: 'pay', 'xp', 'quest_reward', 'gamble_luck'"""
    if not pet_id or pet_id not in PET_BONUSES:
        return value
    bonuses = PET_BONUSES[pet_id]
    if bonus_type == "pay" and "pay_mult" in bonuses:
        return int(value * bonuses["pay_mult"])
    if bonus_type == "xp" and "xp_mult" in bonuses:
        return int(value * bonuses["xp_mult"])
    if bonus_type == "quest_reward" and "quest_reward_mult" in bonuses:
        return int(value * bonuses["quest_reward_mult"])
    if bonus_type == "gamble_luck" and "gamble_luck" in bonuses:
        return value + bonuses["gamble_luck"]
    return value
