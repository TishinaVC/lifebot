from datetime import datetime, timezone
from database.connection import get_db
from database.users import get_user


async def unlock_achievement(user_id: int, achievement_id: str) -> bool:
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    try:
        await db.execute(
            "INSERT INTO achievements (user_id, achievement_id, unlocked_at) VALUES (?, ?, ?)",
            (user_id, achievement_id, now),
        )
        await db.commit()
        return True
    except Exception:
        return False


async def get_achievements(user_id: int) -> list:
    db = await get_db()
    async with db.execute(
        "SELECT achievement_id, unlocked_at FROM achievements WHERE user_id = ?", (user_id,)
    ) as cur:
        rows = await cur.fetchall()
    return [dict(row) for row in rows]


async def get_achievement_ids(user_id: int) -> set:
    db = await get_db()
    async with db.execute(
        "SELECT achievement_id FROM achievements WHERE user_id = ?", (user_id,)
    ) as cur:
        rows = await cur.fetchall()
    return {row["achievement_id"] for row in rows}


async def check_achievements(user_id: int) -> list:
    """Check and auto-unlock stat-based achievements. Returns list of newly unlocked achievement IDs."""
    data = await get_user(user_id)
    if not data:
        return []
    existing = await get_achievement_ids(user_id)
    newly = []

    checks = {
        "level_10": data["level"] >= 10,
        "level_25": data["level"] >= 25,
        "level_50": data["level"] >= 50,
        "worker_bee": data["work_count"] >= 100,
        "gambler": data["games_played"] >= 200,
        "rich_beginnings": data["total_earned"] >= 5000,
        "big_spender": data["total_spent"] >= 50000,
        "banker": data["total_deposited"] >= 250000,
        "criminal": data["crimes_successful"] >= 100,
        "pet_owner": data.get("pet_id") is not None,
        "unbreakable": data["health"] >= 100 and data["hunger"] >= 100 and data["thirst"] >= 100 and data.get("energy", 100) >= 100 and data.get("hygiene", 100) >= 100,
        "high_roller": data["total_earned"] >= 25000,
        "pet_master": data.get("battles_won", 0) >= 50,
        "generous": data.get("gifts_given", 0) >= 50,
        "streak_7": data.get("daily_streak", 0) >= 7,
        "streak_30": data.get("daily_streak", 0) >= 30,
        "quest_master": data.get("quests_completed", 0) >= 50,
        "wealthy": (data["wallet"] + data["bank"]) >= 100000,
        "frequent_flyer": data["work_count"] >= 500,
        "crime_lord": data["crimes_successful"] >= 500,
        "lucky": data["games_won"] >= 500,
        "energizer": data.get("energy_items_used", 0) >= 10,
        "clean_freak": data.get("hygiene_items_used", 0) >= 10,
    }

    from database.housing import get_home, get_decorations, get_upgrades
    home = await get_home(user_id)
    if home:
        from config import HOUSING_TIERS
        tier = HOUSING_TIERS.get(home["tier_id"], {})
        checks["homeowner"] = home["ownership"] == "owned"
        checks["property_mogul"] = home["ownership"] == "owned" and tier.get("tier", 0) >= 15
        decorations = await get_decorations(user_id)
        checks["interior_designer"] = len(decorations) >= 5
        upgrades = await get_upgrades(user_id)
        total_upgrades = sum(upgrades.values())
        checks["settled_down"] = total_upgrades >= 3

    from database.inventory import count_collectibles
    collectible_count = await count_collectibles(user_id)
    checks["collector"] = collectible_count >= 3

    db = await get_db()
    async with db.execute("SELECT COUNT(*) as cnt FROM transactions WHERE user_id = ? AND type = 'fish'", (user_id,)) as cur:
        row = await cur.fetchone()
        checks["fisherman"] = row and row["cnt"] >= 25
    async with db.execute("SELECT COUNT(*) as cnt FROM transactions WHERE user_id = ? AND type = 'mine'", (user_id,)) as cur:
        row = await cur.fetchone()
        checks["miner"] = row and row["cnt"] >= 25
    async with db.execute("SELECT COUNT(*) as cnt FROM transactions WHERE user_id = ? AND type = 'explore'", (user_id,)) as cur:
        row = await cur.fetchone()
        checks["explorer"] = row and row["cnt"] >= 25
    async with db.execute("SELECT COUNT(*) as cnt FROM transactions WHERE user_id = ? AND type = 'craft'", (user_id,)) as cur:
        row = await cur.fetchone()
        checks["craftsman"] = row and row["cnt"] >= 10

    from database.equipment import get_discoveries, get_equipped
    discoveries = await get_discoveries(user_id)
    checks["treasure_hunter"] = len(discoveries) >= 10
    unique_qualities = set(d["quality"] for d in discoveries)
    checks["quality_collector"] = len(unique_qualities) >= 5
    checks["mythic_find"] = any(d["quality"] == "mythic" for d in discoveries)

    equipped = await get_equipped(user_id)
    checks["well_equipped"] = len([e for e in equipped if e["equipped"]]) >= 5

    # ─── Phase 5 achievement checks ───
    best_grade = data.get("best_grade", "")
    checks["s_grade"] = best_grade == "S"
    work_streak = data.get("work_streak", 0)
    checks["streak_10"] = work_streak >= 10
    checks["streak_30"] = work_streak >= 30
    boss_wins = data.get("boss_shifts_won", 0)
    checks["boss_slayer"] = boss_wins >= 1
    checks["boss_master"] = boss_wins >= 10

    # Job reputation achievements
    from database.job_reputation import get_all_job_reputation
    all_rep = await get_all_job_reputation(user_id)
    if all_rep:
        max_rep = max(all_rep.values())
        checks["rep_apprentice"] = max_rep >= 10
        checks["rep_expert"] = max_rep >= 50
        checks["rep_legend"] = max_rep >= 200

    # Co-op achievement — check transactions for co-op work
    async with db.execute("SELECT COUNT(*) as cnt FROM transactions WHERE user_id = ? AND description LIKE 'Co-op work%'", (user_id,)) as cur:
        row = await cur.fetchone()
        checks["team_player"] = row and row["cnt"] >= 1

    for ach_id, condition in checks.items():
        if condition and ach_id not in existing:
            unlocked = await unlock_achievement(user_id, ach_id)
            if unlocked:
                newly.append(ach_id)

    return newly
