from datetime import datetime, timezone
from database.connection import get_db


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
