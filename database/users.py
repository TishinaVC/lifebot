from datetime import datetime, timezone
from database.connection import get_db
from config import STARTING_WALLET


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
            """INSERT INTO users (user_id, guild_id, wallet, created_at, last_decay)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, guild_id, STARTING_WALLET, now, now),
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


async def _get_wallet(user_id: int) -> int:
    db = await get_db()
    async with db.execute("SELECT wallet FROM users WHERE user_id = ?", (user_id,)) as cur:
        row = await cur.fetchone()
    return row["wallet"] if row else 0


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
    await db.execute("DELETE FROM world_interactions WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM police_heat WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM player_jobs WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM player_stats WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM player_qualifications WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM player_training WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM job_reputation WHERE user_id = ?", (user_id,))
    await db.commit()
