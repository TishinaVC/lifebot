from database.connection import get_db


async def get_reputation(user_id: int, faction: str) -> int:
    db = await get_db()
    async with db.execute(
        "SELECT reputation FROM player_reputation WHERE user_id = ? AND faction = ?",
        (user_id, faction),
    ) as cur:
        row = await cur.fetchone()
    return row["reputation"] if row else 0


async def get_all_reputation(user_id: int) -> dict:
    db = await get_db()
    async with db.execute(
        "SELECT faction, reputation FROM player_reputation WHERE user_id = ?", (user_id,)
    ) as cur:
        rows = await cur.fetchall()
    return {row["faction"]: row["reputation"] for row in rows}


async def add_reputation(user_id: int, faction: str, amount: int):
    db = await get_db()
    await db.execute(
        """INSERT INTO player_reputation (user_id, faction, reputation) VALUES (?, ?, ?)
           ON CONFLICT(user_id, faction) DO UPDATE SET reputation = reputation + ?""",
        (user_id, faction, amount, amount),
    )
    await db.commit()


async def get_faction_benefit(user_id: int, faction: str) -> dict:
    from config import FACTIONS
    rep = await get_reputation(user_id, faction)
    fdata = FACTIONS.get(faction, {})
    benefits = fdata.get("benefits", {})
    current_benefit = None
    for threshold in sorted(benefits.keys()):
        if rep >= threshold:
            current_benefit = benefits[threshold]
    return current_benefit or {}
