from database.connection import get_db
from config import TIME_PERIODS


async def get_game_time() -> dict:
    db = await get_db()
    async with db.execute("SELECT * FROM game_time WHERE id = 1") as cur:
        row = await cur.fetchone()
    if not row:
        await db.execute("INSERT OR IGNORE INTO game_time (id, game_hour, time_period) VALUES (1, 8, 'morning')")
        await db.commit()
        return {"game_hour": 8, "time_period": "morning"}
    return dict(row)


async def advance_game_time(hours: int = 1):
    db = await get_db()
    current = await get_game_time()
    new_hour = (current["game_hour"] + hours) % 24
    new_period = "morning"
    for period, pdata in TIME_PERIODS.items():
        gh = pdata["game_hours"]
        if gh[0] <= gh[1]:
            if gh[0] <= new_hour < gh[1]:
                new_period = period
                break
        else:
            if new_hour >= gh[0] or new_hour < gh[1]:
                new_period = period
                break
    await db.execute(
        "UPDATE game_time SET game_hour = ?, time_period = ? WHERE id = 1",
        (new_hour, new_period),
    )
    await db.commit()


async def get_time_period() -> str:
    gt = await get_game_time()
    return gt["time_period"]


async def get_time_effects() -> dict:
    from config import TIME_PERIODS
    period = await get_time_period()
    return TIME_PERIODS.get(period, {}).get("effects", {})
