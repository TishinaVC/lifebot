import aiosqlite
import json
from datetime import datetime, timezone, timedelta
from config import DB_PATH, STARTING_WALLET, STARTING_BANK_CAPACITY, HEALTH_MAX, HUNGER_MAX, THIRST_MAX, ENERGY_MAX, HYGIENE_MAX

_db = None

async def init_db():
    global _db
    _db = await aiosqlite.connect(DB_PATH)
    _db.row_factory = aiosqlite.Row
    await _db.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        guild_id INTEGER,
        wallet INTEGER DEFAULT 200,
        bank INTEGER DEFAULT 0,
        bank_capacity INTEGER DEFAULT 5000,
        level INTEGER DEFAULT 1,
        xp INTEGER DEFAULT 0,
        health INTEGER DEFAULT 100,
        hunger INTEGER DEFAULT 100,
        thirst INTEGER DEFAULT 100,
        energy INTEGER DEFAULT 100,
        hygiene INTEGER DEFAULT 100,
        energy_items_used INTEGER DEFAULT 0,
        hygiene_items_used INTEGER DEFAULT 0,
        job TEXT,
        job_xp INTEGER DEFAULT 0,
        job_level INTEGER DEFAULT 1,
        daily_streak INTEGER DEFAULT 0,
        last_daily TEXT,
        last_work TEXT,
        last_crime TEXT,
        last_gamble TEXT,
        last_eat TEXT,
        last_drink TEXT,
        last_decay TEXT,
        married_to INTEGER,
        marriage_date TEXT,
        pet_id TEXT,
        pet_name TEXT,
        pet_hunger INTEGER DEFAULT 100,
        pet_happiness INTEGER DEFAULT 100,
        pet_health INTEGER DEFAULT 100,
        pet_level INTEGER DEFAULT 1,
        pet_xp INTEGER DEFAULT 0,
        hospital_visits INTEGER DEFAULT 0,
        total_earned INTEGER DEFAULT 0,
        total_lost INTEGER DEFAULT 0,
        total_spent INTEGER DEFAULT 0,
        total_deposited INTEGER DEFAULT 0,
        total_gambled INTEGER DEFAULT 0,
        crimes_committed INTEGER DEFAULT 0,
        crimes_successful INTEGER DEFAULT 0,
        games_played INTEGER DEFAULT 0,
        games_won INTEGER DEFAULT 0,
        work_count INTEGER DEFAULT 0,
        items_used INTEGER DEFAULT 0,
        items_bought INTEGER DEFAULT 0,
        battles_won INTEGER DEFAULT 0,
        gifts_given INTEGER DEFAULT 0,
        daily_claims INTEGER DEFAULT 0,
        quests_completed INTEGER DEFAULT 0,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_id TEXT,
        quantity INTEGER DEFAULT 0,
        UNIQUE(user_id, item_id)
    );

    CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        achievement_id TEXT,
        unlocked_at TEXT,
        UNIQUE(user_id, achievement_id)
    );

    CREATE TABLE IF NOT EXISTS quests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        quest_id TEXT,
        quest_desc TEXT,
        quest_type TEXT,
        quest_target INTEGER,
        quest_progress INTEGER DEFAULT 0,
        quest_reward INTEGER,
        assigned_at TEXT,
        completed INTEGER DEFAULT 0,
        claimed INTEGER DEFAULT 0,
        UNIQUE(user_id, quest_id)
    );

    CREATE TABLE IF NOT EXISTS cooldowns (
        user_id INTEGER,
        command TEXT,
        expires_at TEXT,
        PRIMARY KEY (user_id, command)
    );

    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,
        amount INTEGER,
        description TEXT,
        timestamp TEXT
    );

    CREATE TABLE IF NOT EXISTS collectibles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_id TEXT,
        acquired_at TEXT,
        UNIQUE(user_id, item_id)
    );

    CREATE TABLE IF NOT EXISTS player_homes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        tier_id TEXT NOT NULL,
        ownership TEXT DEFAULT 'rented',
        rent_paid_until TEXT,
        last_rest TEXT,
        acquired_at TEXT,
        UNIQUE(user_id)
    );

    CREATE TABLE IF NOT EXISTS home_upgrades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        upgrade_id TEXT NOT NULL,
        level INTEGER DEFAULT 0,
        UNIQUE(user_id, upgrade_id)
    );

    CREATE TABLE IF NOT EXISTS home_decorations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        decoration_id TEXT NOT NULL,
        acquired_at TEXT,
        UNIQUE(user_id, decoration_id)
    );

    CREATE TABLE IF NOT EXISTS housing_market (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seller_id INTEGER,
        tier_id TEXT NOT NULL,
        price INTEGER NOT NULL,
        listed_at TEXT,
        sold INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS home_storage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_id TEXT,
        quantity INTEGER DEFAULT 0,
        UNIQUE(user_id, item_id)
    );

    CREATE TABLE IF NOT EXISTS player_equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_id TEXT NOT NULL,
        item_type TEXT NOT NULL,
        quality TEXT DEFAULT 'common',
        durability INTEGER DEFAULT 100,
        max_durability INTEGER DEFAULT 100,
        equipped INTEGER DEFAULT 0,
        acquired_at TEXT,
        UNIQUE(user_id, item_id, quality)
    );

    CREATE TABLE IF NOT EXISTS weather_state (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        current_weather TEXT DEFAULT 'sunny',
        next_change TEXT
    );

    CREATE TABLE IF NOT EXISTS discovered_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_id TEXT,
        quality TEXT,
        source TEXT,
        discovered_at TEXT,
        UNIQUE(user_id, item_id, quality)
    );

    CREATE TABLE IF NOT EXISTS player_buffs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        buff_name TEXT NOT NULL,
        buff_stat TEXT NOT NULL,
        buff_value REAL DEFAULT 0,
        expires_at TEXT NOT NULL,
        UNIQUE(user_id, buff_name)
    );

    CREATE TABLE IF NOT EXISTS player_reputation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        faction TEXT NOT NULL,
        reputation INTEGER DEFAULT 0,
        UNIQUE(user_id, faction)
    );

    CREATE TABLE IF NOT EXISTS npc_interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        npc_id TEXT NOT NULL,
        interaction_type TEXT,
        quest_accepted INTEGER DEFAULT 0,
        quest_completed INTEGER DEFAULT 0,
        last_interaction TEXT,
        UNIQUE(user_id, npc_id)
    );

    CREATE TABLE IF NOT EXISTS game_time (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        game_hour INTEGER DEFAULT 8,
        time_period TEXT DEFAULT 'morning'
    );

    CREATE TABLE IF NOT EXISTS world_vectors (
        entity_type TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        vector_name TEXT NOT NULL,
        value REAL NOT NULL,
        normal REAL NOT NULL,
        velocity REAL DEFAULT 0,
        drift_rate REAL DEFAULT 0.15,
        volatility REAL DEFAULT 0.03,
        min_val REAL DEFAULT 0.0,
        max_val REAL DEFAULT 1.0,
        last_updated TEXT,
        PRIMARY KEY (entity_type, entity_id, vector_name)
    );

    CREATE TABLE IF NOT EXISTS world_tick_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tick_time TEXT NOT NULL,
        elapsed_seconds REAL DEFAULT 0,
        interactions_processed INTEGER DEFAULT 0,
        vectors_updated INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS world_interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        entity_type TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        vector_name TEXT NOT NULL,
        delta REAL NOT NULL,
        timestamp TEXT NOT NULL
    );
    """)
    # Migrations for existing databases
    try:
        await _db.execute("ALTER TABLE users ADD COLUMN energy INTEGER DEFAULT 100")
    except Exception:
        pass
    try:
        await _db.execute("ALTER TABLE users ADD COLUMN hygiene INTEGER DEFAULT 100")
    except Exception:
        pass
    try:
        await _db.execute("ALTER TABLE users ADD COLUMN energy_items_used INTEGER DEFAULT 0")
    except Exception:
        pass
    try:
        await _db.execute("ALTER TABLE users ADD COLUMN hygiene_items_used INTEGER DEFAULT 0")
    except Exception:
        pass
    await _db.commit()


async def get_db():
    if _db is None:
        await init_db()
    return _db


async def get_user(user_id: int) -> dict | None:
    db = await get_db()
    async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cur:
        row = await cur.fetchone()
    return dict(row) if row else None


async def get_or_create_user(user_id: int, guild_id: int = 0) -> dict:
    db = await get_db()
    async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cur:
        row = await cur.fetchone()
    if row is None:
        now = datetime.now(timezone.utc).isoformat()
        await db.execute(
            """INSERT INTO users (user_id, guild_id, wallet, bank_capacity, created_at, last_decay)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, guild_id, STARTING_WALLET, STARTING_BANK_CAPACITY, now, now),
        )
        await db.commit()
        async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
    return dict(row)


async def update_user(user_id: int, **kwargs):
    db = await get_db()
    sets = ", ".join(f"{k} = ?" for k in kwargs)
    vals = list(kwargs.values()) + [user_id]
    await db.execute(f"UPDATE users SET {sets} WHERE user_id = ?", vals)
    await db.commit()


async def add_transaction(user_id: int, ttype: str, amount: int, description: str):
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        "INSERT INTO transactions (user_id, type, amount, description, timestamp) VALUES (?, ?, ?, ?, ?)",
        (user_id, ttype, amount, description, now),
    )
    await db.commit()


async def get_inventory(user_id: int) -> dict:
    db = await get_db()
    async with db.execute(
        "SELECT item_id, quantity FROM inventory WHERE user_id = ? AND quantity > 0", (user_id,)
    ) as cur:
        rows = await cur.fetchall()
    return {row["item_id"]: row["quantity"] for row in rows}


async def add_to_inventory(user_id: int, item_id: str, quantity: int = 1):
    db = await get_db()
    await db.execute(
        """INSERT INTO inventory (user_id, item_id, quantity) VALUES (?, ?, ?)
           ON CONFLICT(user_id, item_id) DO UPDATE SET quantity = quantity + ?""",
        (user_id, item_id, quantity, quantity),
    )
    await db.commit()


async def remove_from_inventory(user_id: int, item_id: str, quantity: int = 1) -> bool:
    db = await get_db()
    async with db.execute(
        "SELECT quantity FROM inventory WHERE user_id = ? AND item_id = ?", (user_id, item_id)
    ) as cur:
        row = await cur.fetchone()
    if row is None or row["quantity"] < quantity:
        return False
    new_qty = row["quantity"] - quantity
    if new_qty <= 0:
        await db.execute(
            "DELETE FROM inventory WHERE user_id = ? AND item_id = ?", (user_id, item_id)
        )
    else:
        await db.execute(
            "UPDATE inventory SET quantity = ? WHERE user_id = ? AND item_id = ?",
            (new_qty, user_id, item_id),
        )
    await db.commit()
    return True


async def get_leaderboard(sort_by: str = "wallet", limit: int = 10) -> list:
    db = await get_db()
    valid = {"wallet", "bank", "level", "xp", "total_earned", "work_count", "games_won", "battles_won", "gifts_given", "daily_claims", "quests_completed", "crimes_successful", "daily_streak"}
    if sort_by not in valid:
        sort_by = "wallet"
    async with db.execute(
        f"SELECT user_id, {sort_by} as score FROM users ORDER BY {sort_by} DESC LIMIT ?", (limit,)
    ) as cur:
        rows = await cur.fetchall()
    return [(row["user_id"], row["score"]) for row in rows]


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


async def get_quest(user_id: int) -> dict | None:
    db = await get_db()
    async with db.execute(
        "SELECT * FROM quests WHERE user_id = ? AND completed = 0 ORDER BY assigned_at DESC LIMIT 1",
        (user_id,),
    ) as cur:
        row = await cur.fetchone()
    return dict(row) if row else None


async def assign_quest(user_id: int, desc: str, qtype: str, target: int, reward: int):
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        """INSERT INTO quests (user_id, quest_desc, quest_type, quest_target, quest_reward, assigned_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (user_id, desc, qtype, target, reward, now),
    )
    await db.commit()


async def update_quest_progress(user_id: int, qtype: str, amount: int = 1):
    db = await get_db()
    async with db.execute(
        "SELECT * FROM quests WHERE user_id = ? AND completed = 0 AND quest_type = ?",
        (user_id, qtype),
    ) as cur:
        rows = await cur.fetchall()
    for row in rows:
        new_progress = row["quest_progress"] + amount
        completed = 1 if new_progress >= row["quest_target"] else 0
        await db.execute(
            "UPDATE quests SET quest_progress = ?, completed = ? WHERE id = ?",
            (new_progress, completed, row["id"]),
        )
    await db.commit()


async def get_completed_quests(user_id: int) -> int:
    db = await get_db()
    async with db.execute(
        "SELECT COUNT(*) as c FROM quests WHERE user_id = ? AND completed = 1", (user_id,)
    ) as cur:
        row = await cur.fetchone()
    return row["c"] if row else 0


async def _get_wallet(user_id: int) -> int:
    db = await get_db()
    async with db.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,)) as cur:
        row = await cur.fetchone()
    return row["wallet"] if row else 0


async def set_cooldown(user_id: int, command: str, seconds: int):
    db = await get_db()
    expires = (datetime.now(timezone.utc).timestamp() + seconds)
    await db.execute(
        """INSERT INTO cooldowns (user_id, command, expires_at)
           VALUES (?, ?, ?)
           ON CONFLICT(user_id, command) DO UPDATE SET expires_at = ?""",
        (user_id, command, str(expires), str(expires)),
    )
    await db.commit()


async def check_cooldown(user_id: int, command: str) -> float:
    db = await get_db()
    async with db.execute(
        "SELECT expires_at FROM cooldowns WHERE user_id = ? AND command = ?", (user_id, command)
    ) as cur:
        row = await cur.fetchone()
    if row is None:
        return 0.0
    expires = float(row["expires_at"])
    now = datetime.now(timezone.utc).timestamp()
    remaining = expires - now
    return max(0.0, remaining)


async def get_active_quests(user_id: int) -> list:
    db = await get_db()
    async with db.execute(
        "SELECT * FROM quests WHERE user_id = ? AND claimed = 0 ORDER BY assigned_at DESC",
        (user_id,),
    ) as cur:
        rows = await cur.fetchall()
    return [dict(row) for row in rows]


async def add_quest(user_id: int, quest_id: str, desc: str, qtype: str, target: int, reward: int):
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        """INSERT INTO quests (user_id, quest_id, quest_desc, quest_type, quest_target, quest_reward, assigned_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (user_id, quest_id, desc, qtype, target, reward, now),
    )
    await db.commit()


async def clear_quests(user_id: int):
    db = await get_db()
    await db.execute("DELETE FROM quests WHERE user_id = ?", (user_id,))
    await db.commit()


async def claim_quest(user_id: int, quest_id: str) -> dict | None:
    db = await get_db()
    async with db.execute(
        "SELECT * FROM quests WHERE user_id = ? AND quest_id = ? AND completed = 1 AND claimed = 0",
        (user_id, quest_id),
    ) as cur:
        row = await cur.fetchone()
    if row is None:
        return None
    await db.execute(
        "UPDATE quests SET claimed = 1 WHERE id = ?", (row["id"],),
    )
    await db.commit()
    return dict(row)


async def get_collectibles(user_id: int) -> list:
    db = await get_db()
    async with db.execute(
        "SELECT item_id, acquired_at FROM collectibles WHERE user_id = ?", (user_id,)
    ) as cur:
        rows = await cur.fetchall()
    return [dict(row) for row in rows]


async def add_collectible(user_id: int, item_id: str) -> bool:
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    try:
        await db.execute(
            "INSERT INTO collectibles (user_id, item_id, acquired_at) VALUES (?, ?, ?)",
            (user_id, item_id, now),
        )
        await db.commit()
        return True
    except Exception:
        return False


async def count_collectibles(user_id: int) -> int:
    db = await get_db()
    async with db.execute(
        "SELECT COUNT(*) as c FROM collectibles WHERE user_id = ?", (user_id,)
    ) as cur:
        row = await cur.fetchone()
    return row["c"] if row else 0


async def reset_user(user_id: int):
    db = await get_db()
    await db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM inventory WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM achievements WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM quests WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM cooldowns WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM collectibles WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM player_homes WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM home_upgrades WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM home_decorations WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM home_storage WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM player_equipment WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM discovered_items WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM player_buffs WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM player_reputation WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM npc_interactions WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM housing_market WHERE seller_id = ?", (user_id,))
    await db.execute("DELETE FROM world_interactions WHERE user_id = ?", (user_id,))
    await db.commit()


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

    # Housing achievements
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

    collectible_count = await count_collectibles(user_id)
    checks["collector"] = collectible_count >= 3

    # Activity-based achievements (from cooldowns/transactions)
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

    # Discovery-based achievements
    discoveries = await get_discoveries(user_id)
    checks["treasure_hunter"] = len(discoveries) >= 10
    unique_qualities = set(d["quality"] for d in discoveries)
    checks["quality_collector"] = len(unique_qualities) >= 5
    checks["mythic_find"] = any(d["quality"] == "mythic" for d in discoveries)

    # Equipment achievements
    equipped = await get_equipped(user_id)
    checks["well_equipped"] = len([e for e in equipped if e["equipped"]]) >= 5

    for ach_id, condition in checks.items():
        if condition and ach_id not in existing:
            unlocked = await unlock_achievement(user_id, ach_id)
            if unlocked:
                newly.append(ach_id)

    return newly


# ============================================================
# EQUIPMENT FUNCTIONS (tools, clothing, possessions)
# ============================================================

async def get_equipment(user_id: int, item_type: str = None) -> list:
    db = await get_db()
    if item_type:
        async with db.execute(
            "SELECT * FROM player_equipment WHERE user_id = ? AND item_type = ? ORDER BY equipped DESC, quality DESC",
            (user_id, item_type),
        ) as cur:
            rows = await cur.fetchall()
    else:
        async with db.execute(
            "SELECT * FROM player_equipment WHERE user_id = ? ORDER BY item_type, equipped DESC, quality DESC",
            (user_id,),
        ) as cur:
            rows = await cur.fetchall()
    return [dict(row) for row in rows]


async def get_equipped(user_id: int) -> list:
    db = await get_db()
    async with db.execute(
        "SELECT * FROM player_equipment WHERE user_id = ? AND equipped = 1",
        (user_id,),
    ) as cur:
        rows = await cur.fetchall()
    return [dict(row) for row in rows]


async def add_equipment(user_id: int, item_id: str, item_type: str, quality: str = "common", durability: int = 100, max_durability: int = 100):
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        """INSERT INTO player_equipment (user_id, item_id, item_type, quality, durability, max_durability, equipped, acquired_at)
           VALUES (?, ?, ?, ?, ?, ?, 0, ?)
           ON CONFLICT(user_id, item_id, quality) DO UPDATE SET durability = ?""",
        (user_id, item_id, item_type, quality, durability, max_durability, now, durability),
    )
    await db.commit()


async def equip_item(user_id: int, item_id: str, quality: str):
    db = await get_db()
    async with db.execute(
        "SELECT item_type FROM player_equipment WHERE user_id = ? AND item_id = ? AND quality = ?",
        (user_id, item_id, quality),
    ) as cur:
        row = await cur.fetchone()
    if not row:
        return False
    item_type = row["item_type"]
    if item_type in ("tool", "possession"):
        await db.execute(
            "UPDATE player_equipment SET equipped = 1 WHERE user_id = ? AND item_id = ? AND quality = ?",
            (user_id, item_id, quality),
        )
    else:
        await db.execute(
            "UPDATE player_equipment SET equipped = 0 WHERE user_id = ? AND item_type = ?",
            (user_id, item_type),
        )
        await db.execute(
            "UPDATE player_equipment SET equipped = 1 WHERE user_id = ? AND item_id = ? AND quality = ?",
            (user_id, item_id, quality),
        )
    await db.commit()
    return True


async def unequip_item(user_id: int, item_id: str, quality: str):
    db = await get_db()
    await db.execute(
        "UPDATE player_equipment SET equipped = 0 WHERE user_id = ? AND item_id = ? AND quality = ?",
        (user_id, item_id, quality),
    )
    await db.commit()


async def damage_equipment(user_id: int, item_id: str, quality: str, amount: int = 1):
    db = await get_db()
    await db.execute(
        "UPDATE player_equipment SET durability = durability - ? WHERE user_id = ? AND item_id = ? AND quality = ?",
        (amount, user_id, item_id, quality),
    )
    await db.execute(
        "DELETE FROM player_equipment WHERE user_id = ? AND item_id = ? AND quality = ? AND durability <= 0",
        (user_id, item_id, quality),
    )
    await db.commit()


async def remove_equipment(user_id: int, item_id: str, quality: str):
    db = await get_db()
    await db.execute(
        "DELETE FROM player_equipment WHERE user_id = ? AND item_id = ? AND quality = ?",
        (user_id, item_id, quality),
    )
    await db.commit()


async def has_tool(user_id: int, tool_id: str) -> dict | None:
    db = await get_db()
    async with db.execute(
        "SELECT * FROM player_equipment WHERE user_id = ? AND item_id = ? AND item_type = 'tool' AND durability > 0 ORDER BY quality DESC LIMIT 1",
        (user_id, tool_id),
    ) as cur:
        row = await cur.fetchone()
    return dict(row) if row else None


# ============================================================
# WEATHER FUNCTIONS
# ============================================================

async def get_weather() -> str:
    db = await get_db()
    async with db.execute("SELECT current_weather FROM weather_state WHERE id = 1") as cur:
        row = await cur.fetchone()
    if not row:
        await db.execute("INSERT OR IGNORE INTO weather_state (id, current_weather) VALUES (1, 'sunny')")
        await db.commit()
        return "sunny"
    return row["current_weather"]


async def set_weather(weather: str, next_change: str = None):
    db = await get_db()
    await db.execute(
        "INSERT INTO weather_state (id, current_weather, next_change) VALUES (1, ?, ?) ON CONFLICT(id) DO UPDATE SET current_weather = ?, next_change = ?",
        (weather, next_change, weather, next_change),
    )
    await db.commit()


# ============================================================
# DISCOVERED ITEMS
# ============================================================

async def record_discovery(user_id: int, item_id: str, quality: str, source: str):
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        "INSERT OR IGNORE INTO discovered_items (user_id, item_id, quality, source, discovered_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, item_id, quality, source, now),
    )
    await db.commit()


async def get_discoveries(user_id: int) -> list:
    db = await get_db()
    async with db.execute(
        "SELECT * FROM discovered_items WHERE user_id = ? ORDER BY discovered_at DESC",
        (user_id,),
    ) as cur:
        rows = await cur.fetchall()
    return [dict(row) for row in rows]


# ============================================================
# BUFF FUNCTIONS
# ============================================================

async def add_buff(user_id: int, buff_name: str, buff_stat: str, buff_value: float, duration: int):
    db = await get_db()
    expires = (datetime.now(timezone.utc) + timedelta(seconds=duration)).isoformat()
    await db.execute(
        """INSERT INTO player_buffs (user_id, buff_name, buff_stat, buff_value, expires_at)
           VALUES (?, ?, ?, ?, ?)
           ON CONFLICT(user_id, buff_name) DO UPDATE SET buff_stat = ?, buff_value = ?, expires_at = ?""",
        (user_id, buff_name, buff_stat, buff_value, expires, buff_stat, buff_value, expires),
    )
    await db.commit()


async def get_buffs(user_id: int) -> list:
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute("DELETE FROM player_buffs WHERE expires_at < ?", (now,))
    await db.commit()
    async with db.execute(
        "SELECT * FROM player_buffs WHERE user_id = ?",
        (user_id,),
    ) as cur:
        rows = await cur.fetchall()
    return [dict(row) for row in rows]


async def get_buff_mult(user_id: int, stat: str) -> float:
    """Get the combined multiplier for a buff stat. Returns 1.0 if no buff."""
    buffs = await get_buffs(user_id)
    mult = 1.0
    for b in buffs:
        if b["buff_stat"] == stat:
            mult *= b["buff_value"]
    return mult


async def get_buff_add(user_id: int, stat: str) -> float:
    """Get the combined additive value for a buff stat (for regen-type buffs)."""
    buffs = await get_buffs(user_id)
    total = 0.0
    for b in buffs:
        if b["buff_stat"] == stat:
            total += b["buff_value"]
    return total


async def remove_buff(user_id: int, buff_name: str):
    db = await get_db()
    await db.execute("DELETE FROM player_buffs WHERE user_id = ? AND buff_name = ?", (user_id, buff_name))
    await db.commit()


# ============================================================
# REPUTATION FUNCTIONS
# ============================================================

async def get_reputation(user_id: int, faction: str) -> int:
    db = await get_db()
    async with db.execute(
        "SELECT reputation FROM player_reputation WHERE user_id = ? AND faction = ?",
        (user_id, faction),
    ) as cur:
        row = await cur.fetchone()
    return row["reputation"] if row else 0


async def get_all_reputation(user_id: int) -> dict:
    db = await get_db()
    async with db.execute(
        "SELECT faction, reputation FROM player_reputation WHERE user_id = ?",
        (user_id,),
    ) as cur:
        rows = await cur.fetchall()
    return {row["faction"]: row["reputation"] for row in rows}


async def add_reputation(user_id: int, faction: str, amount: int):
    db = await get_db()
    await db.execute(
        """INSERT INTO player_reputation (user_id, faction, reputation) VALUES (?, ?, ?)
           ON CONFLICT(user_id, faction) DO UPDATE SET reputation = reputation + ?""",
        (user_id, faction, amount, amount),
    )
    await db.commit()


async def get_faction_benefit(user_id: int, faction: str) -> dict:
    """Get the current benefit tier for a faction based on reputation."""
    from config import FACTIONS
    rep = await get_reputation(user_id, faction)
    fdata = FACTIONS.get(faction, {})
    benefits = fdata.get("benefits", {})
    current_benefit = None
    for threshold in sorted(benefits.keys()):
        if rep >= threshold:
            current_benefit = benefits[threshold]
    return current_benefit or {}


# ============================================================
# NPC INTERACTION FUNCTIONS
# ============================================================

async def get_npc_interaction(user_id: int, npc_id: str) -> dict | None:
    db = await get_db()
    async with db.execute(
        "SELECT * FROM npc_interactions WHERE user_id = ? AND npc_id = ?",
        (user_id, npc_id),
    ) as cur:
        row = await cur.fetchone()
    return dict(row) if row else None


async def record_npc_interaction(user_id: int, npc_id: str, interaction_type: str = "talk"):
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        """INSERT INTO npc_interactions (user_id, npc_id, interaction_type, last_interaction)
           VALUES (?, ?, ?, ?)
           ON CONFLICT(user_id, npc_id) DO UPDATE SET interaction_type = ?, last_interaction = ?""",
        (user_id, npc_id, interaction_type, now, interaction_type, now),
    )
    await db.commit()


async def accept_npc_quest(user_id: int, npc_id: str):
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        """INSERT INTO npc_interactions (user_id, npc_id, quest_accepted, last_interaction)
           VALUES (?, ?, 1, ?)
           ON CONFLICT(user_id, npc_id) DO UPDATE SET quest_accepted = 1, last_interaction = ?""",
        (user_id, npc_id, now, now),
    )
    await db.commit()


async def complete_npc_quest(user_id: int, npc_id: str):
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        "UPDATE npc_interactions SET quest_completed = 1, quest_accepted = 0, last_interaction = ? WHERE user_id = ? AND npc_id = ?",
        (now, user_id, npc_id),
    )
    await db.commit()


# ============================================================
# GAME TIME FUNCTIONS
# ============================================================

async def get_game_time() -> dict:
    db = await get_db()
    async with db.execute("SELECT * FROM game_time WHERE id = 1") as cur:
        row = await cur.fetchone()
    if not row:
        await db.execute("INSERT OR IGNORE INTO game_time (id, game_hour, time_period) VALUES (1, 8, 'morning')")
        await db.commit()
        return {"game_hour": 8, "time_period": "morning"}
    return dict(row)


async def advance_game_time(hours: int = 1):
    db = await get_db()
    current = await get_game_time()
    new_hour = (current["game_hour"] + hours) % 24
    from config import TIME_PERIODS
    new_period = "morning"
    for period, pdata in TIME_PERIODS.items():
        gh = pdata["game_hours"]
        if gh[0] <= gh[1]:
            if gh[0] <= new_hour < gh[1]:
                new_period = period
                break
        else:
            if new_hour >= gh[0] or new_hour < gh[1]:
                new_period = period
                break
    await db.execute(
        "UPDATE game_time SET game_hour = ?, time_period = ? WHERE id = 1",
        (new_hour, new_period),
    )
    await db.commit()


async def get_time_period() -> str:
    gt = await get_game_time()
    return gt["time_period"]


async def get_time_effects() -> dict:
    from config import TIME_PERIODS
    period = await get_time_period()
    return TIME_PERIODS.get(period, {}).get("effects", {})


async def get_home(user_id: int) -> dict | None:
    db = await get_db()
    async with db.execute("SELECT * FROM player_homes WHERE user_id = ?", (user_id,)) as cur:
        row = await cur.fetchone()
    return dict(row) if row else None


async def set_home(user_id: int, tier_id: str, ownership: str = "rented", rent_paid_until: str = None):
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    existing = await get_home(user_id)
    if existing:
        await db.execute(
            "UPDATE player_homes SET tier_id = ?, ownership = ?, rent_paid_until = ?, acquired_at = ? WHERE user_id = ?",
            (tier_id, ownership, rent_paid_until, now, user_id),
        )
    else:
        await db.execute(
            "INSERT INTO player_homes (user_id, tier_id, ownership, rent_paid_until, acquired_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, tier_id, ownership, rent_paid_until, now),
        )
    await db.commit()


async def remove_home(user_id: int):
    db = await get_db()
    await db.execute("DELETE FROM player_homes WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM home_upgrades WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM home_decorations WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM home_storage WHERE user_id = ?", (user_id,))
    await db.commit()


async def update_home(user_id: int, **kwargs):
    db = await get_db()
    sets = ", ".join(f"{k} = ?" for k in kwargs)
    vals = list(kwargs.values()) + [user_id]
    await db.execute(f"UPDATE player_homes SET {sets} WHERE user_id = ?", vals)
    await db.commit()


async def get_upgrades(user_id: int) -> dict:
    db = await get_db()
    async with db.execute("SELECT upgrade_id, level FROM home_upgrades WHERE user_id = ?", (user_id,)) as cur:
        rows = await cur.fetchall()
    return {row["upgrade_id"]: row["level"] for row in rows}


async def set_upgrade_level(user_id: int, upgrade_id: str, level: int):
    db = await get_db()
    await db.execute(
        "INSERT INTO home_upgrades (user_id, upgrade_id, level) VALUES (?, ?, ?) ON CONFLICT(user_id, upgrade_id) DO UPDATE SET level = ?",
        (user_id, upgrade_id, level, level),
    )
    await db.commit()


async def get_decorations(user_id: int) -> list:
    db = await get_db()
    async with db.execute("SELECT decoration_id FROM home_decorations WHERE user_id = ?", (user_id,)) as cur:
        rows = await cur.fetchall()
    return [row["decoration_id"] for row in rows]


async def add_decoration(user_id: int, decoration_id: str):
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        "INSERT OR IGNORE INTO home_decorations (user_id, decoration_id, acquired_at) VALUES (?, ?, ?)",
        (user_id, decoration_id, now),
    )
    await db.commit()


async def get_home_storage(user_id: int) -> dict:
    db = await get_db()
    async with db.execute("SELECT item_id, quantity FROM home_storage WHERE user_id = ?", (user_id,)) as cur:
        rows = await cur.fetchall()
    return {row["item_id"]: row["quantity"] for row in rows}


async def add_to_home_storage(user_id: int, item_id: str, quantity: int = 1):
    db = await get_db()
    await db.execute(
        "INSERT INTO home_storage (user_id, item_id, quantity) VALUES (?, ?, ?) ON CONFLICT(user_id, item_id) DO UPDATE SET quantity = quantity + ?",
        (user_id, item_id, quantity, quantity),
    )
    await db.commit()


async def remove_from_home_storage(user_id: int, item_id: str, quantity: int = 1):
    db = await get_db()
    await db.execute(
        "UPDATE home_storage SET quantity = quantity - ? WHERE user_id = ? AND item_id = ?",
        (quantity, user_id, item_id),
    )
    await db.execute("DELETE FROM home_storage WHERE user_id = ? AND item_id = ? AND quantity <= 0", (user_id, item_id))
    await db.commit()


async def list_market_listings(tier_id: str = None) -> list:
    db = await get_db()
    if tier_id:
        async with db.execute(
            "SELECT * FROM housing_market WHERE sold = 0 AND tier_id = ? ORDER BY price ASC", (tier_id,)
        ) as cur:
            rows = await cur.fetchall()
    else:
        async with db.execute("SELECT * FROM housing_market WHERE sold = 0 ORDER BY listed_at DESC") as cur:
            rows = await cur.fetchall()
    return [dict(row) for row in rows]


async def create_market_listing(seller_id: int, tier_id: str, price: int) -> int:
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    cur = await db.execute(
        "INSERT INTO housing_market (seller_id, tier_id, price, listed_at) VALUES (?, ?, ?, ?)",
        (seller_id, tier_id, price, now),
    )
    await db.commit()
    return cur.lastrowid


async def mark_market_sold(listing_id: int):
    db = await get_db()
    await db.execute("UPDATE housing_market SET sold = 1 WHERE id = ?", (listing_id,))
    await db.commit()


async def cancel_market_listing(listing_id: int):
    db = await get_db()
    await db.execute("DELETE FROM housing_market WHERE id = ? AND sold = 0", (listing_id,))
    await db.commit()


# ============================================================
# WORLD VECTOR FUNCTIONS — living world simulation
# ============================================================

async def get_world_vector(entity_type: str, entity_id: str, vector_name: str) -> dict | None:
    db = await get_db()
    async with db.execute(
        "SELECT * FROM world_vectors WHERE entity_type = ? AND entity_id = ? AND vector_name = ?",
        (entity_type, entity_id, vector_name),
    ) as cur:
        row = await cur.fetchone()
    return dict(row) if row else None


async def get_world_vectors(entity_type: str, entity_id: str = None) -> list:
    db = await get_db()
    if entity_id:
        async with db.execute(
            "SELECT * FROM world_vectors WHERE entity_type = ? AND entity_id = ?",
            (entity_type, entity_id),
        ) as cur:
            rows = await cur.fetchall()
    else:
        async with db.execute(
            "SELECT * FROM world_vectors WHERE entity_type = ?",
            (entity_type,),
        ) as cur:
            rows = await cur.fetchall()
    return [dict(row) for row in rows]


async def get_all_world_vectors() -> list:
    db = await get_db()
    async with db.execute("SELECT * FROM world_vectors") as cur:
        rows = await cur.fetchall()
    return [dict(row) for row in rows]


async def upsert_world_vector(
    entity_type: str, entity_id: str, vector_name: str,
    value: float, normal: float, velocity: float = 0,
    drift_rate: float = 0.15, volatility: float = 0.03,
    min_val: float = 0.0, max_val: float = 1.0,
    last_updated: str = None,
):
    db = await get_db()
    if last_updated is None:
        last_updated = datetime.now(timezone.utc).isoformat()
    await db.execute(
        """INSERT INTO world_vectors (entity_type, entity_id, vector_name, value, normal, velocity, drift_rate, volatility, min_val, max_val, last_updated)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(entity_type, entity_id, vector_name) DO UPDATE SET
             value = excluded.value,
             velocity = excluded.velocity,
             last_updated = excluded.last_updated""",
        (entity_type, entity_id, vector_name, value, normal, velocity, drift_rate, volatility, min_val, max_val, last_updated),
    )
    await db.commit()


async def bulk_upsert_world_vectors(vectors: list):
    """Bulk upsert world vectors. Each item is a dict with all fields."""
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    for v in vectors:
        await db.execute(
            """INSERT INTO world_vectors (entity_type, entity_id, vector_name, value, normal, velocity, drift_rate, volatility, min_val, max_val, last_updated)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(entity_type, entity_id, vector_name) DO UPDATE SET
                 value = excluded.value,
                 velocity = excluded.velocity,
                 last_updated = excluded.last_updated""",
            (v["entity_type"], v["entity_id"], v["vector_name"], v["value"], v["normal"],
             v.get("velocity", 0), v.get("drift_rate", 0.15), v.get("volatility", 0.03),
             v.get("min_val", 0.0), v.get("max_val", 1.0), now),
        )
    await db.commit()


async def log_world_interaction(user_id: int, entity_type: str, entity_id: str, vector_name: str, delta: float):
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        "INSERT INTO world_interactions (user_id, entity_type, entity_id, vector_name, delta, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, entity_type, entity_id, vector_name, delta, now),
    )
    await db.commit()


async def get_pending_interactions(since: str) -> list:
    db = await get_db()
    async with db.execute(
        "SELECT * FROM world_interactions WHERE timestamp > ? ORDER BY timestamp ASC",
        (since,),
    ) as cur:
        rows = await cur.fetchall()
    return [dict(row) for row in rows]


async def clear_interactions_before(timestamp: str):
    db = await get_db()
    await db.execute("DELETE FROM world_interactions WHERE timestamp <= ?", (timestamp,))
    await db.commit()


async def log_world_tick(elapsed_seconds: float, interactions: int, vectors_updated: int):
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        "INSERT INTO world_tick_log (tick_time, elapsed_seconds, interactions_processed, vectors_updated) VALUES (?, ?, ?, ?)",
        (now, elapsed_seconds, interactions, vectors_updated),
    )
    await db.commit()


async def get_last_tick_time() -> str | None:
    db = await get_db()
    async with db.execute("SELECT tick_time FROM world_tick_log ORDER BY id DESC LIMIT 1") as cur:
        row = await cur.fetchone()
    return row["tick_time"] if row else None
