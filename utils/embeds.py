import discord
from config import CURRENCY_SYMBOL

def success_embed(title: str, description: str = "") -> discord.Embed:
    return discord.Embed(title=title, description=description, color=0x2ECC71)

def error_embed(title: str, description: str = "") -> discord.Embed:
    return discord.Embed(title=title, description=description, color=0xE74C3C)

def info_embed(title: str, description: str = "") -> discord.Embed:
    return discord.Embed(title=title, description=description, color=0x3498DB)

def warning_embed(title: str, description: str = "") -> discord.Embed:
    return discord.Embed(title=title, description=description, color=0xF39C12)

def money_embed(title: str, description: str = "") -> discord.Embed:
    return discord.Embed(title=title, description=description, color=0xF1C40F)

CATEGORY_COLORS = {
    "entry":     0x95A5A6,
    "service":   0xE67E22,
    "trades":    0xD35400,
    "medical":   0xE91E63,
    "tech":      0x2ECC71,
    "business":  0xF1C40F,
    "creative":  0x9B59B6,
    "transport": 0x3498DB,
}

GRADE_COLORS = {
    "S": 0xFFD700,
    "A": 0xFF6B35,
    "B": 0x2ECC71,
    "C": 0x3498DB,
    "D": 0xF39C12,
    "F": 0xE74C3C,
}

def themed_embed(title: str, description: str = "", category: str = None, grade: str = None) -> discord.Embed:
    """Create an embed with color themed to a job category or grade.
    Grade takes priority over category if both provided."""
    if grade and grade in GRADE_COLORS:
        color = GRADE_COLORS[grade]
    elif category and category in CATEGORY_COLORS:
        color = CATEGORY_COLORS[category]
    else:
        color = 0x2ECC71
    return discord.Embed(title=title, description=description, color=color)

def stats_bar(value: int, maximum: int, length: int = 10) -> str:
    filled = int((value / maximum) * length) if maximum > 0 else 0
    filled = max(0, min(length, filled))
    return "█" * filled + "░" * (length - filled)

def format_money(amount: int) -> str:
    return f"{CURRENCY_SYMBOL} {amount:,}"
