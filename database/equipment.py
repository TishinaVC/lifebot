from datetime import datetime, timezone
from database.connection import get_db


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
