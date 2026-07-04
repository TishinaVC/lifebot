from database.connection import get_db


async def get_job_reputation(user_id: int, category: str) -> int:
    db = await get_db()
    async with db.execute(
        "SELECT reputation FROM job_reputation WHERE user_id = ? AND category = ?",
        (user_id, category),
    ) as cur:
        row = await cur.fetchone()
    return row["reputation"] if row else 0


async def get_all_job_reputation(user_id: int) -> dict:
    db = await get_db()
    async with db.execute(
        "SELECT category, reputation FROM job_reputation WHERE user_id = ?", (user_id,)
    ) as cur:
        rows = await cur.fetchall()
    return {row["category"]: row["reputation"] for row in rows}


async def add_job_reputation(user_id: int, category: str, amount: int):
    db = await get_db()
    await db.execute(
        """INSERT INTO job_reputation (user_id, category, reputation) VALUES (?, ?, ?)
           ON CONFLICT(user_id, category) DO UPDATE SET reputation = reputation + ?""",
        (user_id, category, amount, amount),
    )
    await db.commit()


async def get_job_rep_benefits(user_id: int, category: str) -> dict:
    from config.job_reputation import get_rep_tier
    rep = await get_job_reputation(user_id, category)
    _, _, _, benefits = get_rep_tier(rep)
    return benefits
