from datetime import datetime, timezone
from database.connection import get_db


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
