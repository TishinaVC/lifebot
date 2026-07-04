from datetime import datetime, timezone
from database.connection import get_db


async def set_cooldown(user_id: int, command: str, seconds: int):
    db = await get_db()
    expires = (datetime.now(timezone.utc).timestamp() + seconds)
    await db.execute(
        """INSERT INTO cooldowns (user_id, command, expires_at)
           VALUES (?, ?, ?)
           ON CONFLICT(user_id, command) DO UPDATE SET expires_at = ?""",
        (user_id, command, str(expires), str(expires)),
    )
    await db.commit()


async def check_cooldown(user_id: int, command: str) -> float:
    db = await get_db()
    async with db.execute(
        "SELECT expires_at FROM cooldowns WHERE user_id = ? AND command = ?", (user_id, command)
    ) as cur:
        row = await cur.fetchone()
    if row is None:
        return 0.0
    expires = float(row["expires_at"])
    now = datetime.now(timezone.utc).timestamp()
    remaining = expires - now
    return max(0.0, remaining)
