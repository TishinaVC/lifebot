from datetime import datetime, timezone
from database.connection import get_db
from config.police import HEAT_MAX, HEAT_DECAY_PER_TICK


async def get_police_state(user_id: int) -> dict | None:
    db = await get_db()
    async with db.execute("SELECT * FROM police_heat WHERE user_id = ?", (user_id,)) as cur:
        row = await cur.fetchone()
    return dict(row) if row else None


async def add_heat(user_id: int, amount: int):
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    existing = await get_police_state(user_id)
    if existing is None:
        await db.execute(
            """INSERT INTO police_heat (user_id, heat, last_crime, tailing_stage, tailing_location, tailing_interactions, warrant_active, last_heat_decay)
               VALUES (?, ?, ?, 0, NULL, 0, 0, ?)""",
            (user_id, min(amount, HEAT_MAX), now, now),
        )
    else:
        new_heat = min(existing["heat"] + amount, HEAT_MAX)
        await db.execute(
            "UPDATE police_heat SET heat = ?, last_crime = ? WHERE user_id = ?",
            (new_heat, now, user_id),
        )
    await db.commit()


async def decay_all_heat():
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    async with db.execute("SELECT user_id, heat, tailing_stage FROM police_heat WHERE heat > 0", ()) as cur:
        rows = await cur.fetchall()
    for row in rows:
        new_heat = max(0, row["heat"] - HEAT_DECAY_PER_TICK)
        # If heat drops below tailing threshold, clear tailing
        tailing_stage = row["tailing_stage"]
        if new_heat < 50:
            tailing_stage = 0
        await db.execute(
            "UPDATE police_heat SET heat = ?, tailing_stage = ?, last_heat_decay = ? WHERE user_id = ?",
            (new_heat, tailing_stage, now, row["user_id"]),
        )
    await db.commit()


async def set_tailing(user_id: int, stage: int, location: str):
    db = await get_db()
    await db.execute(
        "UPDATE police_heat SET tailing_stage = ?, tailing_location = ?, tailing_interactions = 0 WHERE user_id = ?",
        (stage, location, user_id),
    )
    await db.commit()


async def clear_tailing(user_id: int):
    db = await get_db()
    await db.execute(
        "UPDATE police_heat SET tailing_stage = 0, tailing_location = NULL, tailing_interactions = 0 WHERE user_id = ?",
        (user_id,),
    )
    await db.commit()


async def increment_tailing_interactions(user_id: int) -> int:
    db = await get_db()
    async with db.execute("SELECT tailing_interactions FROM police_heat WHERE user_id = ?", (user_id,)) as cur:
        row = await cur.fetchone()
    if row is None:
        return 0
    new_count = row["tailing_interactions"] + 1
    await db.execute("UPDATE police_heat SET tailing_interactions = ? WHERE user_id = ?", (new_count, user_id))
    await db.commit()
    return new_count


async def set_warrant(user_id: int, active: bool):
    db = await get_db()
    await db.execute("UPDATE police_heat SET warrant_active = ? WHERE user_id = ?", (1 if active else 0, user_id))
    await db.commit()


async def reset_heat(user_id: int):
    db = await get_db()
    await db.execute(
        "UPDATE police_heat SET heat = 0, tailing_stage = 0, tailing_location = NULL, tailing_interactions = 0, warrant_active = 0 WHERE user_id = ?",
        (user_id,),
    )
    await db.commit()


async def reduce_heat(user_id: int, amount: int):
    db = await get_db()
    existing = await get_police_state(user_id)
    if existing is None:
        return
    new_heat = max(0, existing["heat"] - amount)
    await db.execute("UPDATE police_heat SET heat = ? WHERE user_id = ?", (new_heat, user_id))
    await db.commit()


async def clear_police_record(user_id: int):
    db = await get_db()
    await db.execute("DELETE FROM police_heat WHERE user_id = ?", (user_id,))
    await db.commit()
