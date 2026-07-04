from datetime import datetime, timezone
from database.connection import get_db


async def get_home(user_id: int) -> dict | None:
    db = await get_db()
    async with db.execute("SELECT * FROM player_homes WHERE user_id = ?", (user_id,)) as cur:
        row = await cur.fetchone()
    return dict(row) if row else None


async def set_home(user_id: int, tier_id: str, ownership: str = "rented", rent_paid_until: str = None):
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    existing = await get_home(user_id)
    if existing:
        await db.execute(
            "UPDATE player_homes SET tier_id = ?, ownership = ?, rent_paid_until = ?, acquired_at = ? WHERE user_id = ?",
            (tier_id, ownership, rent_paid_until, now, user_id),
        )
    else:
        await db.execute(
            "INSERT INTO player_homes (user_id, tier_id, ownership, rent_paid_until, acquired_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, tier_id, ownership, rent_paid_until, now),
        )
    await db.commit()


async def remove_home(user_id: int):
    db = await get_db()
    await db.execute("DELETE FROM player_homes WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM home_upgrades WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM home_decorations WHERE user_id = ?", (user_id,))
    await db.execute("DELETE FROM home_storage WHERE user_id = ?", (user_id,))
    await db.commit()


async def update_home(user_id: int, **kwargs):
    db = await get_db()
    sets = ", ".join(f"{k} = ?" for k in kwargs)
    vals = list(kwargs.values()) + [user_id]
    await db.execute(f"UPDATE player_homes SET {sets} WHERE user_id = ?", vals)
    await db.commit()


async def get_upgrades(user_id: int) -> dict:
    db = await get_db()
    async with db.execute(
        "SELECT upgrade_id, level FROM home_upgrades WHERE user_id = ?", (user_id,)
    ) as cur:
        rows = await cur.fetchall()
    return {row["upgrade_id"]: row["level"] for row in rows}


async def set_upgrade_level(user_id: int, upgrade_id: str, level: int):
    db = await get_db()
    await db.execute(
        "INSERT INTO home_upgrades (user_id, upgrade_id, level) VALUES (?, ?, ?) ON CONFLICT(user_id, upgrade_id) DO UPDATE SET level = ?",
        (user_id, upgrade_id, level, level),
    )
    await db.commit()


async def get_decorations(user_id: int) -> list:
    db = await get_db()
    async with db.execute(
        "SELECT decoration_id FROM home_decorations WHERE user_id = ?", (user_id,)
    ) as cur:
        rows = await cur.fetchall()
    return [row["decoration_id"] for row in rows]


async def add_decoration(user_id: int, decoration_id: str):
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        "INSERT OR IGNORE INTO home_decorations (user_id, decoration_id, acquired_at) VALUES (?, ?, ?)",
        (user_id, decoration_id, now),
    )
    await db.commit()


async def get_home_storage(user_id: int) -> dict:
    db = await get_db()
    async with db.execute(
        "SELECT item_id, quantity FROM home_storage WHERE user_id = ? AND quantity > 0",
        (user_id,),
    ) as cur:
        rows = await cur.fetchall()
    return {row["item_id"]: row["quantity"] for row in rows}


async def add_to_home_storage(user_id: int, item_id: str, quantity: int = 1):
    db = await get_db()
    await db.execute(
        """INSERT INTO home_storage (user_id, item_id, quantity) VALUES (?, ?, ?)
           ON CONFLICT(user_id, item_id) DO UPDATE SET quantity = quantity + ?""",
        (user_id, item_id, quantity, quantity),
    )
    await db.commit()


async def remove_from_home_storage(user_id: int, item_id: str, quantity: int = 1):
    db = await get_db()
    await db.execute(
        "UPDATE home_storage SET quantity = quantity - ? WHERE user_id = ? AND item_id = ?",
        (quantity, user_id, item_id),
    )
    await db.execute("DELETE FROM home_storage WHERE user_id = ? AND item_id = ? AND quantity <= 0", (user_id, item_id))
    await db.commit()


async def list_market_listings(tier_id: str = None) -> list:
    db = await get_db()
    if tier_id:
        async with db.execute(
            "SELECT * FROM housing_market WHERE sold = 0 AND tier_id = ? ORDER BY price ASC", (tier_id,)
        ) as cur:
            rows = await cur.fetchall()
    else:
        async with db.execute("SELECT * FROM housing_market WHERE sold = 0 ORDER BY listed_at DESC") as cur:
            rows = await cur.fetchall()
    return [dict(row) for row in rows]


async def create_market_listing(seller_id: int, tier_id: str, price: int) -> int:
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    cur = await db.execute(
        "INSERT INTO housing_market (seller_id, tier_id, price, listed_at) VALUES (?, ?, ?, ?)",
        (seller_id, tier_id, price, now),
    )
    await db.commit()
    return cur.lastrowid


async def mark_market_sold(listing_id: int):
    db = await get_db()
    await db.execute("UPDATE housing_market SET sold = 1 WHERE id = ?", (listing_id,))
    await db.commit()


async def cancel_market_listing(listing_id: int):
    db = await get_db()
    await db.execute("DELETE FROM housing_market WHERE id = ? AND sold = 0", (listing_id,))
    await db.commit()
