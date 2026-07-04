from datetime import datetime, timezone
from database.connection import get_db


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
