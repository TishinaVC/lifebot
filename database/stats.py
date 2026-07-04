from datetime import datetime, timezone
from database.connection import get_db
from config import BASE_STAT_VALUE, MAX_STAT_VALUE, STAT_KEYS


async def get_stats(user_id: int) -> dict:
    """Return dict of all 8 stats for a user. Creates row if missing."""
    db = await get_db()
    async with db.execute("SELECT * FROM player_stats WHERE user_id = ?", (user_id,)) as cur:
        row = await cur.fetchone()
    if row is None:
        await db.execute("INSERT INTO player_stats (user_id) VALUES (?)", (user_id,))
        await db.commit()
        async with db.execute("SELECT * FROM player_stats WHERE user_id = ?", (user_id,)) as cur:
            row = await cur.fetchone()
    return dict(row)


async def get_stat(user_id: int, stat_name: str) -> int:
    """Get a single stat value."""
    stats = await get_stats(user_id)
    return stats.get(stat_name, BASE_STAT_VALUE)


async def update_stat(user_id: int, stat_name: str, value: int):
    """Set a stat to a specific value (clamped to MAX)."""
    value = max(0, min(MAX_STAT_VALUE, value))
    db = await get_db()
    await get_stats(user_id)  # ensure row exists
    await db.execute(
        f"UPDATE player_stats SET {stat_name} = ? WHERE user_id = ?",
        (value, user_id),
    )
    await db.commit()


async def add_stat(user_id: int, stat_name: str, amount: int) -> int:
    """Add amount to a stat, clamped to MAX. Returns new value."""
    stats = await get_stats(user_id)
    new_val = max(0, min(MAX_STAT_VALUE, stats.get(stat_name, BASE_STAT_VALUE) + amount))
    await update_stat(user_id, stat_name, new_val)
    return new_val


async def get_all_stats(user_id: int) -> dict:
    """Return {stat_name: value} for all 8 stats (clean keys only)."""
    stats = await get_stats(user_id)
    return {k: stats.get(k, BASE_STAT_VALUE) for k in STAT_KEYS}


async def get_qualifications(user_id: int) -> list:
    """Return list of qualification IDs the user has earned."""
    db = await get_db()
    async with db.execute(
        "SELECT qualification_id FROM player_qualifications WHERE user_id = ?", (user_id,)
    ) as cur:
        rows = await cur.fetchall()
    return [row["qualification_id"] for row in rows]


async def has_qualification(user_id: int, qual_id: str) -> bool:
    """Check if user has a specific qualification."""
    db = await get_db()
    async with db.execute(
        "SELECT 1 FROM player_qualifications WHERE user_id = ? AND qualification_id = ?",
        (user_id, qual_id),
    ) as cur:
        row = await cur.fetchone()
    return row is not None


async def add_qualification(user_id: int, qual_id: str):
    """Award a qualification to a user."""
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        "INSERT OR IGNORE INTO player_qualifications (user_id, qualification_id, earned_at) VALUES (?, ?, ?)",
        (user_id, qual_id, now),
    )
    await db.commit()


async def get_training_sessions(user_id: int, stat_name: str) -> int:
    """Get how many training sessions a user has done for a specific stat."""
    db = await get_db()
    async with db.execute(
        "SELECT sessions_count FROM player_training WHERE user_id = ? AND stat_name = ?",
        (user_id, stat_name),
    ) as cur:
        row = await cur.fetchone()
    return row["sessions_count"] if row else 0


async def increment_training(user_id: int, stat_name: str) -> int:
    """Increment training session count for a stat. Returns new count."""
    db = await get_db()
    await db.execute(
        """INSERT INTO player_training (user_id, stat_name, sessions_count) VALUES (?, ?, 1)
           ON CONFLICT(user_id, stat_name) DO UPDATE SET sessions_count = sessions_count + 1""",
        (user_id, stat_name),
    )
    await db.commit()
    return await get_training_sessions(user_id, stat_name)


async def get_total_training_sessions(user_id: int) -> int:
    """Get total training sessions across all stats."""
    db = await get_db()
    async with db.execute(
        "SELECT COALESCE(SUM(sessions_count), 0) as total FROM player_training WHERE user_id = ?",
        (user_id,),
    ) as cur:
        row = await cur.fetchone()
    return row["total"] if row else 0


async def check_job_requirements(user_id: int, stat_reqs: dict, qual_reqs: list) -> tuple:
    """Check if user meets stat and qualification requirements for a job.
    Returns (meets: bool, missing_stats: dict, missing_quals: list).
    """
    stats = await get_all_stats(user_id)
    quals = await get_qualifications(user_id)

    missing_stats = {}
    for stat, required in stat_reqs.items():
        if stats.get(stat, BASE_STAT_VALUE) < required:
            missing_stats[stat] = {"have": stats.get(stat, BASE_STAT_VALUE), "need": required}

    missing_quals = [q for q in qual_reqs if q not in quals]

    meets = len(missing_stats) == 0 and len(missing_quals) == 0
    return meets, missing_stats, missing_quals


async def get_effective_stat(user_id: int, stat_name: str) -> int:
    """Get stat value including temporary buff boosts."""
    stats = await get_all_stats(user_id)
    base = stats.get(stat_name, BASE_STAT_VALUE)
    # Check for stat buffs (buff_stat matches stat_name, additive)
    from database.buffs import get_buff_add
    buff_add = await get_buff_add(user_id, f"stat_{stat_name}")
    return max(0, min(MAX_STAT_VALUE + 50, base + buff_add))
