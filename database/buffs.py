from datetime import datetime, timezone, timedelta
from database.connection import get_db


async def get_weather() -> str:
    db = await get_db()
    async with db.execute("SELECT current_weather FROM weather_state WHERE id = 1") as cur:
        row = await cur.fetchone()
    if not row:
        await db.execute("INSERT OR IGNORE INTO weather_state (id, current_weather) VALUES (1, 'sunny')")
        await db.commit()
        return "sunny"
    return row["current_weather"]


async def set_weather(weather: str, next_change: str = None):
    db = await get_db()
    await db.execute(
        "INSERT INTO weather_state (id, current_weather, next_change) VALUES (1, ?, ?) ON CONFLICT(id) DO UPDATE SET current_weather = ?, next_change = ?",
        (weather, next_change, weather, next_change),
    )
    await db.commit()


async def get_buffs(user_id: int) -> list:
    db = await get_db()
    now = datetime.now(timezone.utc).isoformat()
    await db.execute("DELETE FROM player_buffs WHERE expires_at < ?", (now,))
    await db.commit()
    async with db.execute(
        "SELECT * FROM player_buffs WHERE user_id = ?",
        (user_id,),
    ) as cur:
        rows = await cur.fetchall()
    return [dict(row) for row in rows]


async def add_buff(user_id: int, buff_name: str, buff_stat: str, buff_value: float, duration: int):
    db = await get_db()
    expires = (datetime.now(timezone.utc) + timedelta(seconds=duration)).isoformat()
    await db.execute(
        """INSERT INTO player_buffs (user_id, buff_name, buff_stat, buff_value, expires_at)
           VALUES (?, ?, ?, ?, ?)
           ON CONFLICT(user_id, buff_name) DO UPDATE SET buff_stat = ?, buff_value = ?, expires_at = ?""",
        (user_id, buff_name, buff_stat, buff_value, expires, buff_stat, buff_value, expires),
    )
    await db.commit()


async def get_buff_mult(user_id: int, stat: str) -> float:
    """Get the combined multiplier for a buff stat. Returns 1.0 if no buff."""
    buffs = await get_buffs(user_id)
    mult = 1.0
    for b in buffs:
        if b["buff_stat"] == stat:
            mult *= b["buff_value"]
    return mult


async def get_buff_add(user_id: int, stat: str) -> float:
    """Get the combined additive value for a buff stat (for regen-type buffs)."""
    buffs = await get_buffs(user_id)
    total = 0.0
    for b in buffs:
        if b["buff_stat"] == stat:
            total += b["buff_value"]
    return total


async def remove_buff(user_id: int, buff_name: str):
    db = await get_db()
    await db.execute("DELETE FROM player_buffs WHERE user_id = ? AND buff_name = ?", (user_id, buff_name))
    await db.commit()
