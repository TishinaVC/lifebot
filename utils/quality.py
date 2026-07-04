import random
from config import ITEM_QUALITIES


def roll_quality() -> str:
    """Roll a random quality based on weighted probabilities."""
    qualities = list(ITEM_QUALITIES.items())
    total_weight = sum(q["weight"] for _, q in qualities)
    roll = random.randint(1, total_weight)
    cumulative = 0
    for qid, qdata in qualities:
        cumulative += qdata["weight"]
        if roll <= cumulative:
            return qid
    return "common"


def quality_multiplier(quality: str) -> float:
    """Get the stat multiplier for a quality."""
    q = ITEM_QUALITIES.get(quality, ITEM_QUALITIES["common"])
    return q["multiplier"]


def quality_value_mult(quality: str) -> float:
    """Get the value multiplier for a quality."""
    q = ITEM_QUALITIES.get(quality, ITEM_QUALITIES["common"])
    return q["value_mult"]


def quality_name(quality: str) -> str:
    """Get the display name for a quality."""
    q = ITEM_QUALITIES.get(quality, ITEM_QUALITIES["common"])
    return q["name"]


def quality_emoji(quality: str) -> str:
    """Get the emoji for a quality."""
    q = ITEM_QUALITIES.get(quality, ITEM_QUALITIES["common"])
    return q["emoji"]
