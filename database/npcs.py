from datetime import datetime, timezone
from database.connection import get_db


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
