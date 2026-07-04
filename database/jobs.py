from database.connection import get_db


async def get_player_jobs(user_id: int) -> dict:
    """Return {1: {job_id, job_level, job_xp}, 2: ..., 3: ...} or empty slots as None."""
    db = await get_db()
    result = {1: None, 2: None, 3: None}
    async with db.execute(
        "SELECT slot, job_id, job_level, job_xp FROM player_jobs WHERE user_id = ?", (user_id,)
    ) as cur:
        rows = await cur.fetchall()
    for row in rows:
        result[row["slot"]] = {
            "job_id": row["job_id"],
            "job_level": row["job_level"],
            "job_xp": row["job_xp"],
        }
    return result


async def set_player_job(user_id: int, slot: int, job_id: str):
    """Insert or replace a job into a slot."""
    db = await get_db()
    await db.execute(
        """INSERT INTO player_jobs (user_id, slot, job_id, job_level, job_xp)
           VALUES (?, ?, ?, 1, 0)
           ON CONFLICT(user_id, slot) DO UPDATE SET job_id = excluded.job_id, job_level = 1, job_xp = 0""",
        (user_id, slot, job_id),
    )
    await db.commit()


async def quit_player_job(user_id: int, slot: int):
    """Remove a job from a slot."""
    db = await get_db()
    await db.execute(
        "DELETE FROM player_jobs WHERE user_id = ? AND slot = ?", (user_id, slot)
    )
    await db.commit()


async def update_job_xp(user_id: int, slot: int, job_xp: int, job_level: int):
    """Update XP and level for a job slot."""
    db = await get_db()
    await db.execute(
        "UPDATE player_jobs SET job_xp = ?, job_level = ? WHERE user_id = ? AND slot = ?",
        (job_xp, job_level, user_id, slot),
    )
    await db.commit()


async def count_player_jobs(user_id: int) -> int:
    """Return how many job slots are filled."""
    db = await get_db()
    async with db.execute(
        "SELECT COUNT(*) as cnt FROM player_jobs WHERE user_id = ?", (user_id,)
    ) as cur:
        row = await cur.fetchone()
    return row["cnt"] if row else 0


async def reset_player_jobs(user_id: int):
    """Delete all job slots for a user (used in reset_user)."""
    db = await get_db()
    await db.execute("DELETE FROM player_jobs WHERE user_id = ?", (user_id,))
    await db.commit()
