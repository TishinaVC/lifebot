import aiosqlite
from config import DB_PATH

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
        bank_capacity INTEGER DEFAULT 10000,
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

    CREATE TABLE IF NOT EXISTS police_heat (
        user_id INTEGER PRIMARY KEY,
        heat INTEGER DEFAULT 0,
        last_crime TEXT,
        tailing_stage INTEGER DEFAULT 0,
        tailing_location TEXT,
        tailing_interactions INTEGER DEFAULT 0,
        warrant_active INTEGER DEFAULT 0,
        last_heat_decay TEXT
    );

    CREATE TABLE IF NOT EXISTS player_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        slot INTEGER NOT NULL CHECK(slot IN (1, 2, 3)),
        job_id TEXT NOT NULL,
        job_level INTEGER DEFAULT 1,
        job_xp INTEGER DEFAULT 0,
        UNIQUE(user_id, slot)
    );

    CREATE TABLE IF NOT EXISTS player_stats (
        user_id INTEGER PRIMARY KEY,
        strength INTEGER DEFAULT 10,
        intelligence INTEGER DEFAULT 10,
        dexterity INTEGER DEFAULT 10,
        perception INTEGER DEFAULT 10,
        endurance INTEGER DEFAULT 10,
        charisma INTEGER DEFAULT 10,
        luck INTEGER DEFAULT 10,
        focus INTEGER DEFAULT 10
    );

    CREATE TABLE IF NOT EXISTS player_qualifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        qualification_id TEXT NOT NULL,
        earned_at TEXT,
        UNIQUE(user_id, qualification_id)
    );

    CREATE TABLE IF NOT EXISTS player_training (
        user_id INTEGER NOT NULL,
        stat_name TEXT NOT NULL,
        sessions_count INTEGER DEFAULT 0,
        PRIMARY KEY (user_id, stat_name)
    );

    CREATE TABLE IF NOT EXISTS job_reputation (
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        reputation INTEGER DEFAULT 0,
        UNIQUE(user_id, category)
    );
    """)
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
    try:
        await _db.execute("ALTER TABLE users ADD COLUMN work_count INTEGER DEFAULT 0")
    except Exception:
        pass
    try:
        await _db.execute("ALTER TABLE users ADD COLUMN work_streak INTEGER DEFAULT 0")
    except Exception:
        pass
    try:
        await _db.execute("ALTER TABLE users ADD COLUMN best_grade TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        await _db.execute("ALTER TABLE users ADD COLUMN boss_shifts_won INTEGER DEFAULT 0")
    except Exception:
        pass
    # ── Migrate player_jobs CHECK constraint from (1,2) to (1,2,3) ──
    try:
        await _db.execute("""
            CREATE TABLE IF NOT EXISTS player_jobs_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                slot INTEGER NOT NULL CHECK(slot IN (1, 2, 3)),
                job_id TEXT NOT NULL,
                job_level INTEGER DEFAULT 1,
                job_xp INTEGER DEFAULT 0,
                UNIQUE(user_id, slot)
            )
        """)
        await _db.execute("INSERT OR IGNORE INTO player_jobs_new SELECT * FROM player_jobs")
        await _db.execute("DROP TABLE player_jobs")
        await _db.execute("ALTER TABLE player_jobs_new RENAME TO player_jobs")
    except Exception:
        pass
    await _db.commit()
    try:
        await _db.execute("""
            INSERT OR IGNORE INTO player_jobs (user_id, slot, job_id, job_level, job_xp)
            SELECT user_id, 1, job, job_level, job_xp
            FROM users WHERE job IS NOT NULL AND job != ''
        """)
        await _db.commit()
    except Exception:
        pass


async def get_db():
    if _db is None:
        await init_db()
    return _db
