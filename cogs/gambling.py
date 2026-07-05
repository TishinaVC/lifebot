import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import random
import database as db
from utils.embeds import success_embed, error_embed, info_embed, money_embed, format_money
from utils.helpers import check_level_up, xp_for_next_level, clamp, pet_bonus, stat_modifier
from utils.narrative import get_action_text
from config import ACHIEVEMENTS

SLOT_EMOJIS = ["🍒", "🍋", "🍊", "🍇", "🔔", "⭐", "💎", "7️⃣"]
SLOT_PAYOUTS = {"💎": 10, "7️⃣": 7, "⭐": 5, "🔔": 3, "🍇": 2, "🍊": 2, "🍋": 2, "🍒": 1.5}

ROULETTE_COLORS = {"red": [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36],
                   "black": [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35],
                   "green": [0]}


class BlackjackView(discord.ui.View):
    def __init__(self, user_id, timeout=30):
        super().__init__(timeout=timeout)
        self.user_id = user_id
        self.action = None

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.success, emoji="🃏")
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Not your game!", ephemeral=True)
            return
        self.action = "hit"
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.danger, emoji="✋")
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Not your game!", ephemeral=True)
            return
        self.action = "stand"
        await interaction.response.defer()
        self.stop()

    async def on_timeout(self):
        self.action = "stand"
        self.stop()


def card_value(card):
    if card in ["J", "Q", "K"]:
        return 10
    if card == "A":
        return 11
    return int(card)

def hand_value(hand):
    total = sum(card_value(c) for c in hand)
    aces = hand.count("A")
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def draw_card():
    ranks = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
    return random.choice(ranks)


HILO_SUITS = ["♠", "♥", "♦", "♣"]
HILO_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
    "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14,
}


def draw_hilo_card():
    rank = random.choice(list(HILO_VALUES.keys()))
    suit = random.choice(HILO_SUITS)
    return rank, suit, HILO_VALUES[rank]


# ── Keno ──────────────────────────────────────────────────────────────
KENO_PAYOUTS = {
    2: {0: 0,    1: 0,    2: 6},
    3: {0: 0,    1: 0.5,  2: 2,    3: 12},
    4: {0: 0.5,  1: 0.5,  2: 1,    3: 4,    4: 20},
    5: {0: 1,    1: 0.5,  2: 1,    3: 2,    4: 8,    5: 40},
    6: {0: 1,    1: 0.5,  2: 1,    3: 1.5,  4: 3,    5: 10,  6: 60},
    7: {0: 1,    1: 0.5,  2: 1,    3: 1,    4: 2,    5: 5,   6: 20,  7: 80},
    8: {0: 2,    1: 1,    2: 1,    3: 1,    4: 2,    5: 5,   6: 15,  7: 40,  8: 100},
}

KENO_GOLD = 0xFFD700

def keno_payout(num_picks, num_matches, amount):
    table = KENO_PAYOUTS.get(num_picks, {})
    mult = table.get(num_matches, 0)
    return int(amount * mult), mult


def keno_board_embed(picks, drawn=None, amount=None, title="🎰 Keno — Pick Your Numbers!", subtitle=""):
    drawn = drawn or set()
    matches = picks & drawn

    lines = []
    for row_start in range(0, 20, 5):
        cells = []
        for i in range(5):
            num = row_start + i + 1
            if num in matches:
                cells.append(f"**{num:>2}**🎯")
            elif num in drawn:
                cells.append(f"{num:>2}🔴")
            elif num in picks:
                cells.append(f"{num:>2}🔵")
            else:
                cells.append(f"{num:>2}  ")
        lines.append("   ".join(cells))
    board = "\n".join(lines)

    pick_str = ", ".join(str(p) for p in sorted(picks)) if picks else "—"
    match_count = len(matches)

    description = f"```\n{board}\n```\n"
    description += f"**Your picks** ({len(picks)}/8): {pick_str}\n"

    if drawn:
        drawn_str = ", ".join(str(d) for d in sorted(drawn))
        match_str = ", ".join(str(m) for m in sorted(matches)) if matches else "—"
        description += f"**Drawn**: {drawn_str}\n"
        description += f"**Matches**: {match_count} — {match_str}\n"
        if amount and picks:
            payout, mult = keno_payout(len(picks), match_count, amount)
            description += f"**Payout**: {format_money(payout)} ({mult}x)\n"

    if subtitle:
        description += f"\n*{subtitle}*"

    embed = discord.Embed(title=title, description=description, color=KENO_GOLD)
    embed.set_footer(text="🎯 = match  🔴 = drawn miss  🔵 = your pick  plain = open")
    return embed


# ── Lucky Wheel ───────────────────────────────────────────────────────
WHEEL_SEGMENTS = [
    {"label": "0x",     "mult": 0,     "emoji": "💀", "color": 0x2C3E50},
    {"label": "0.5x",   "mult": 0.5,   "emoji": " Penny", "color": 0x95A5A6},
    {"label": "1x",     "mult": 1,     "emoji": "🪙", "color": 0x1ABC9C},
    {"label": "1.5x",   "mult": 1.5,   "emoji": "💵", "color": 0x2ECC71},
    {"label": "2x",     "mult": 2,     "emoji": "💰", "color": 0xF1C40F},
    {"label": "2x",     "mult": 2,     "emoji": "💰", "color": 0xF1C40F},
    {"label": "3x",     "mult": 3,     "emoji": "💎", "color": 0x3498DB},
    {"label": "0.5x",   "mult": 0.5,   "emoji": " Penny", "color": 0x95A5A6},
    {"label": "1x",     "mult": 1,     "emoji": "🪙", "color": 0x1ABC9C},
    {"label": "5x",     "mult": 5,     "emoji": "🔥", "color": 0xE67E22},
    {"label": "0x",     "mult": 0,     "emoji": "💀", "color": 0x2C3E50},
    {"label": "10x",    "mult": 10,    "emoji": "👑", "color": 0x9B59B6},
]

WHEEL_ARROWS = ["↑", "↗", "→", "↘", "↓", "↙", "←", "↖"]


def wheel_display(highlight_idx=-1, spinning=False):
    lines = []
    for i, seg in enumerate(WHEEL_SEGMENTS):
        marker = "▶" if i == highlight_idx else " "
        lines.append(f"{marker} {seg['emoji']} **{seg['label']}**")
    return "\n".join(lines)


def wheel_embed(highlight_idx=-1, amount=None, title="🎡 Lucky Wheel", subtitle=""):
    seg = WHEEL_SEGMENTS[highlight_idx] if highlight_idx >= 0 else None
    description = wheel_display(highlight_idx, spinning=False)
    if seg and amount is not None:
        payout = int(amount * seg["mult"])
        description += f"\n\n**Result**: {seg['emoji']} **{seg['label']}** — Payout: {format_money(payout)}"
    if subtitle:
        description += f"\n\n*{subtitle}*"
    color = seg["color"] if seg else 0xF1C40F
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="👑 = 10x jackpot  🔥 = 5x  💎 = 3x  💰 = 2x  💀 = bust")
    return embed


# ── Plinko ────────────────────────────────────────────────────────────
PLINKO_ROWS = 8
PLINKO_SLOTS = [5, 2, 1, 0.5, 0.2, 0.5, 1, 2, 5]
PLINKO_SLOT_EMOJI = ["🔥", "💎", "💰", "🪙", "💀", "🪙", "💰", "💎", "🔥"]
PLINKO_COLORS = [0xE67E22, 0x3498DB, 0xF1C40F, 0x95A5A6, 0x2C3E50, 0x95A5A6, 0xF1C40F, 0x3498DB, 0xE67E22]


def plinko_board_embed(positions, final_slot=None, amount=None, title="🟡 Plinko", subtitle=""):
    lines = []
    for row in range(PLINKO_ROWS):
        pegs = "  ".join(["●"] * (row + 2))
        if row < len(positions):
            chip_pos = positions[row]
            peg_list = list(pegs.split("  "))
            if 0 <= chip_pos < len(peg_list):
                peg_list[chip_pos] = "🟡"
            pegs = "  ".join(peg_list)
        indent = "  " * (PLINKO_ROWS - row - 1)
        lines.append(f"{indent}{pegs}")

    slot_line = "  ".join(PLINKO_SLOT_EMOJI)
    mult_line = " ".join(f"{m:>4}x" for m in PLINKO_SLOTS)
    lines.append("")
    lines.append(f"  {slot_line}")
    lines.append(f"  {mult_line}")

    description = "```\n" + "\n".join(lines) + "\n```"

    if final_slot is not None:
        mult = PLINKO_SLOTS[final_slot]
        payout = int(amount * mult) if amount else 0
        emoji = PLINKO_SLOT_EMOJI[final_slot]
        description += f"\n**Landed on**: {emoji} **{mult}x** — Payout: {format_money(payout)}\n"
    else:
        description += f"\n**Slot multipliers**: {', '.join(f'{PLINKO_SLOT_EMOJI[i]} {PLINKO_SLOTS[i]}x' for i in range(9))}\n"

    if subtitle:
        description += f"\n*{subtitle}*"

    color = PLINKO_COLORS[final_slot] if final_slot is not None else 0xF1C40F
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="🟡 = chip  ● = peg  Bell-curve distribution — edges pay more!")
    return embed


# ── Over/Under Dice ───────────────────────────────────────────────────
DICE_FACES = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
DICE_TUMBLE = ["🎲", "🎲", "🎲"]
OVERUNDER_PAYOUTS = {
    "over": 1.95,
    "under": 1.95,
    "seven": 5.0,
    "sum": {2: 30, 3: 17, 4: 11, 5: 8, 6: 6, 7: 5, 8: 6, 9: 8, 10: 11, 11: 17, 12: 30},
}


def dice_embed(d1=None, d2=None, rolling=False, amount=None, bet_label="", title="🎲 Over/Under Dice", subtitle=""):
    if rolling or d1 is None:
        display = "🎲 🎲\n\n*Rolling...*"
        color = 0x95A5A6
    else:
        face1 = DICE_FACES[d1 - 1]
        face2 = DICE_FACES[d2 - 1]
        total = d1 + d2
        display = f"# {face1}  {face2}\n\n**Total: {total}**"
        color = 0xF1C40F

    description = display
    if amount and not rolling and d1 is not None:
        description += f"\n**Bet**: {bet_label} — {format_money(amount)}"
    if subtitle:
        description += f"\n\n*{subtitle}*"

    embed = discord.Embed(title=title, description=description, color=color)
    if not rolling and d1 is not None:
        embed.add_field(name="📊 Payout Reference", value="Over/Under 7: **1.95x** | Exactly 7: **5x** | Sum 2 or 12: **30x** | Sum 3 or 11: **17x**", inline=False)
    embed.set_footer(text="⚀⚁⚂⚃⚄⚅ — Bet over, under, exactly 7, or a specific sum")
    return embed


# ── Mystery Box ───────────────────────────────────────────────────────
MYSTERY_PRIZES = [
    {"label": "2x Cash",   "mult": 2,     "emoji": "💰", "weight": 25, "color": 0xF1C40F},
    {"label": "1.5x Cash", "mult": 1.5,   "emoji": "💵", "weight": 30, "color": 0x2ECC71},
    {"label": "1x Back",   "mult": 1,     "emoji": "🪙", "weight": 20, "color": 0x1ABC9C},
    {"label": "0.5x Back", "mult": 0.5,   "emoji": " Penny", "weight": 15, "color": 0x95A5A6},
    {"label": "Bust",      "mult": 0,     "emoji": "💀", "weight": 8,  "color": 0x2C3E50},
    {"label": "5x Jackpot","mult": 5,     "emoji": "🔥", "weight": 1,  "color": 0xE67E22},
    {"label": "10x Mega",  "mult": 10,    "emoji": "👑", "weight": 1,  "color": 0x9B59B6},
]


def weighted_prize():
    total = sum(p["weight"] for p in MYSTERY_PRIZES)
    r = random.randint(1, total)
    cumulative = 0
    for prize in MYSTERY_PRIZES:
        cumulative += prize["weight"]
        if r <= cumulative:
            return prize
    return MYSTERY_PRIZES[0]


def mystery_embed(revealed=None, amount=None, title="🎁 Mystery Box", subtitle=""):
    if revealed is None:
        display = "🎁    🎁    🎁\n\n*Three boxes... choose wisely.*"
        color = 0x9B59B6
    else:
        display = revealed
        color = 0x9B59B6

    description = display
    if amount:
        description += f"\n\n**Entry fee**: {format_money(amount)}"
    if subtitle:
        description += f"\n\n*{subtitle}*"

    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="👑 = 10x mega  🔥 = 5x jackpot  💰 = 2x  💀 = bust  Pick a box!")
    return embed


class MysteryBoxView(discord.ui.View):
    def __init__(self, user_id, timeout=30):
        super().__init__(timeout=timeout)
        self.user_id = user_id
        self.chosen = None
        self.prizes = [weighted_prize(), weighted_prize(), weighted_prize()]

        for i in range(3):
            btn = discord.ui.Button(
                label=f"Box {i + 1}", style=discord.ButtonStyle.primary, emoji="🎁", custom_id=f"mbox_{i}"
            )
            btn.callback = self._make_callback(i)
            self.add_item(btn)

    def _make_callback(self, idx):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("Not your game!", ephemeral=True)
                return
            self.chosen = idx
            await interaction.response.defer()
            self.stop()
        return callback

    async def on_timeout(self):
        self.chosen = 0
        self.stop()


class HigherLowerView(discord.ui.View):
    def __init__(self, user_id, timeout=30):
        super().__init__(timeout=timeout)
        self.user_id = user_id
        self.action = None

    @discord.ui.button(label="Higher", style=discord.ButtonStyle.success, emoji="⬆️")
    async def higher(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Not your game!", ephemeral=True)
            return
        self.action = "higher"
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label="Lower", style=discord.ButtonStyle.primary, emoji="⬇️")
    async def lower(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Not your game!", ephemeral=True)
            return
        self.action = "lower"
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label="Cash Out", style=discord.ButtonStyle.danger, emoji="💰")
    async def cashout(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Not your game!", ephemeral=True)
            return
        self.action = "cashout"
        await interaction.response.defer()
        self.stop()

    async def on_timeout(self):
        self.action = "cashout"
        self.stop()


class CrashView(discord.ui.View):
    def __init__(self, user_id, timeout=60):
        super().__init__(timeout=timeout)
        self.user_id = user_id
        self.action = None
        self.multiplier = 1.0

    @discord.ui.button(label="Cash Out", style=discord.ButtonStyle.danger, emoji="💰")
    async def cashout(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Not your game!", ephemeral=True)
            return
        if self.action is not None:
            return
        self.action = "cashout"
        await interaction.response.defer()
        self.stop()

    async def on_timeout(self):
        self.action = "crashed"
        self.stop()


class KenoView(discord.ui.View):
    def __init__(self, user_id, timeout=60):
        super().__init__(timeout=timeout)
        self.user_id = user_id
        self.picks = set()
        self.confirmed = False

        for i in range(1, 21):
            btn = discord.ui.Button(
                label=str(i),
                style=discord.ButtonStyle.secondary,
                row=(i - 1) // 5,
                custom_id=f"keno_{i}",
            )
            btn.callback = self._make_number_callback(i)
            self.add_item(btn)

        clear_btn = discord.ui.Button(
            label="Clear", style=discord.ButtonStyle.danger, emoji="🗑️", row=4, custom_id="keno_clear"
        )
        clear_btn.callback = self._clear_callback
        self.add_item(clear_btn)

        confirm_btn = discord.ui.Button(
            label="Confirm", style=discord.ButtonStyle.success, emoji="✅", row=4, custom_id="keno_confirm"
        )
        confirm_btn.callback = self._confirm_callback
        self.add_item(confirm_btn)

    def _make_number_callback(self, num):
        async def callback(interaction: discord.Interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("Not your game!", ephemeral=True)
                return
            if num in self.picks:
                self.picks.discard(num)
            else:
                if len(self.picks) >= 8:
                    await interaction.response.send_message("Max 8 picks! Remove one first.", ephemeral=True)
                    return
                self.picks.add(num)
            for child in self.children:
                if child.custom_id == f"keno_{num}":
                    child.style = discord.ButtonStyle.primary if num in self.picks else discord.ButtonStyle.secondary
            await interaction.response.edit_message(embed=keno_board_embed(self.picks), view=self)
        return callback

    async def _clear_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Not your game!", ephemeral=True)
            return
        self.picks.clear()
        for child in self.children:
            if child.custom_id and child.custom_id.startswith("keno_") and child.custom_id != "keno_clear" and child.custom_id != "keno_confirm":
                child.style = discord.ButtonStyle.secondary
        await interaction.response.edit_message(embed=keno_board_embed(self.picks), view=self)

    async def _confirm_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Not your game!", ephemeral=True)
            return
        if len(self.picks) < 2:
            await interaction.response.send_message("Pick at least 2 numbers!", ephemeral=True)
            return
        self.confirmed = True
        await interaction.response.defer()
        self.stop()

    async def on_timeout(self):
        if len(self.picks) >= 2:
            self.confirmed = True
        self.stop()


class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _gamble_common(self, interaction, amount):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if amount <= 0:
            await interaction.response.send_message(embed=error_embed("Error", "Amount must be positive."), ephemeral=True)
            return None, None
        if amount > data["wallet"]:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You only have {format_money(data['wallet'])} in your wallet."), ephemeral=True)
            return None, None

        mods = stat_modifier(data, "gamble")
        return data, data["wallet"], mods

    async def _gamble_result(self, user_id, data, won, amount, game_name, multiplier=0, mods=None):
        new_wallet = data["wallet"]
        xp_mult = mods["xp_mult"] if mods else 1.0
        earned = 0
        if won:
            winnings = int(amount * multiplier) if multiplier else amount
            new_wallet = data["wallet"] + winnings
            earned = winnings
            await db.update_user(user_id,
                wallet=new_wallet,
                total_earned=data["total_earned"] + winnings,
                games_won=data["games_won"] + 1,
                games_played=data["games_played"] + 1,
                total_gambled=data["total_gambled"] + amount,
            )
            await db.add_transaction(user_id, "gamble_win", winnings, f"Won {game_name}")
        else:
            new_wallet = data["wallet"] - amount
            await db.update_user(user_id,
                wallet=new_wallet,
                total_lost=data["total_lost"] + amount,
                games_played=data["games_played"] + 1,
                total_gambled=data["total_gambled"] + amount,
            )
            await db.add_transaction(user_id, "gamble_loss", amount, f"Lost {game_name}")

        await db.update_quest_progress(user_id, "gamble", 1)
        xp_gain = int(random.randint(5, 15) * xp_mult)
        new_xp = data["xp"] + xp_gain
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))
            await db.update_user(user_id, xp=new_xp, level=new_level)
        else:
            await db.update_user(user_id, xp=new_xp)

        new_achievements = await db.check_achievements(user_id)
        if new_achievements:
            total_ach_reward = sum(ACHIEVEMENTS[a]["reward"] for a in new_achievements)
            new_wallet += total_ach_reward
            await db.update_user(user_id, wallet=new_wallet, total_earned=data["total_earned"] + earned + total_ach_reward)

        return new_wallet, leveled_up, new_level, xp_gain, new_achievements

    @app_commands.command(name="coinflip", description="Flip a coin — heads or tails!")
    @app_commands.choices(side=[app_commands.Choice(name="Heads", value="heads"), app_commands.Choice(name="Tails", value="tails")])
    async def coinflip(self, interaction: discord.Interaction, amount: int, side: app_commands.Choice[str]):
        data, _, mods = await self._gamble_common(interaction, amount)
        if data is None:
            return
        result = random.choice(["heads", "tails"])
        won = result == side.value
        new_wallet, leveled_up, new_level, xp_gain, new_achievements = await self._gamble_result(
            interaction.user.id, data, won, amount, "Coinflip", multiplier=2.0 if won else 0, mods=mods
        )
        emoji = "🪙"
        if won:
            embed = success_embed(f"{emoji} Coinflip — You Won!", get_action_text("gambling", "coinflip_win", result=result, bet=format_money(amount), winnings=format_money(amount*2), wallet=format_money(new_wallet)))
        else:
            embed = error_embed(f"{emoji} Coinflip — You Lost!", get_action_text("gambling", "coinflip_loss", result=result, bet=format_money(amount), wallet=format_money(new_wallet)))
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="dice", description="Roll the dice — pick a number 1-6!")
    async def dice(self, interaction: discord.Interaction, amount: int, number: int):
        if number < 1 or number > 6:
            await interaction.response.send_message(embed=error_embed("Error", "Pick a number between 1 and 6."), ephemeral=True)
            return
        data, _, mods = await self._gamble_common(interaction, amount)
        if data is None:
            return
        result = random.randint(1, 6)
        won = result == number
        new_wallet, leveled_up, new_level, xp_gain, new_achievements = await self._gamble_result(
            interaction.user.id, data, won, amount, "Dice", multiplier=6.0 if won else 0, mods=mods
        )
        if won:
            embed = success_embed(f"🎲 Dice — You Won!", get_action_text("gambling", "dice_win", result=result, bet=format_money(amount), winnings=format_money(amount*6), wallet=format_money(new_wallet)))
        else:
            embed = error_embed(f"🎲 Dice — You Lost!", get_action_text("gambling", "dice_loss", result=result, bet=format_money(amount), wallet=format_money(new_wallet)))
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="slots", description="Spin the slot machine!")
    async def slots(self, interaction: discord.Interaction, amount: int):
        data, _, mods = await self._gamble_common(interaction, amount)
        if data is None:
            return
        reel1 = random.choice(SLOT_EMOJIS)
        reel2 = random.choice(SLOT_EMOJIS)
        reel3 = random.choice(SLOT_EMOJIS)

        if reel1 == reel2 == reel3:
            multiplier = SLOT_PAYOUTS.get(reel1, 3)
            won = True
        elif reel1 == reel2 or reel2 == reel3 or reel1 == reel3:
            multiplier = 1.5
            won = True
        else:
            multiplier = 0
            won = False

        new_wallet, leveled_up, new_level, xp_gain, new_achievements = await self._gamble_result(
            interaction.user.id, data, won, amount, "Slots", multiplier=multiplier if won else 0, mods=mods
        )

        slot_display = f"│ {reel1} │ {reel2} │ {reel3} │"
        if won:
            winnings = int(amount * multiplier)
            embed = money_embed("🎰 Slots — You Won!", f"{slot_display}\n\nMultiplier: **{multiplier}x**\nYou won {format_money(winnings)}!\nWallet: {format_money(new_wallet)}")
        else:
            embed = error_embed("🎰 Slots — You Lost!", f"{slot_display}\n\nNo match. You lost {format_money(amount)}.\nWallet: {format_money(new_wallet)}")
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="blackjack", description="Play a game of blackjack against the dealer!")
    async def blackjack(self, interaction: discord.Interaction, amount: int):
        data, _, mods = await self._gamble_common(interaction, amount)
        if data is None:
            return

        player_hand = [draw_card(), draw_card()]
        dealer_hand = [draw_card(), draw_card()]

        await interaction.response.send_message(embed=self._bj_embed(player_hand, dealer_hand, "Your turn! Hit or Stand?", False))
        msg = await interaction.original_response()

        while True:
            view = BlackjackView(interaction.user.id, timeout=30)
            await msg.edit(embed=self._bj_embed(player_hand, dealer_hand, "Your turn! Hit or Stand?", False), view=view)
            await view.wait()

            if view.action == "hit":
                player_hand.append(draw_card())
                if hand_value(player_hand) > 21:
                    break
            else:
                break

        pv = hand_value(player_hand)
        dv = hand_value(dealer_hand)

        if pv > 21:
            won = False
            result_text = f"You busted with {pv}! Dealer wins."
        else:
            while dv < 17:
                dealer_hand.append(draw_card())
                dv = hand_value(dealer_hand)
            if dv > 21:
                won = True
                result_text = f"Dealer busted with {dv}! You win!"
            elif pv > dv:
                won = True
                result_text = f"You have {pv}, dealer has {dv}. You win!"
            elif pv < dv:
                won = False
                result_text = f"You have {pv}, dealer has {dv}. Dealer wins."
            else:
                won = False
                result_text = f"Push! Both have {pv}. Bet returned."
                xp_gain = pet_bonus(data.get("pet_id"), "xp", int(5 * mods["xp_mult"]))
                new_xp = data["xp"] + xp_gain
                new_level, leveled_up = check_level_up(new_xp, data["level"])
                if leveled_up:
                    new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))
                await db.update_user(interaction.user.id,
                    wallet=data["wallet"],
                    games_played=data["games_played"] + 1,
                    total_gambled=data["total_gambled"] + amount,
                    xp=new_xp,
                    level=new_level,
                )
                await db.update_quest_progress(interaction.user.id, "gamble", 1)
                push_embed = info_embed("🃏 Blackjack — Push", get_action_text("gambling", "blackjack_push", result_text=result_text) + f"\n{self._bj_display(player_hand, dealer_hand, True)}")
                push_embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
                if leveled_up:
                    push_embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
                new_achievements = await db.check_achievements(interaction.user.id)
                for ach_id in new_achievements:
                    ach = ACHIEVEMENTS[ach_id]
                    push_embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
                if new_achievements:
                    ach_reward = sum(ACHIEVEMENTS[a]["reward"] for a in new_achievements)
                    await db.update_user(interaction.user.id, wallet=data["wallet"] + ach_reward, total_earned=data["total_earned"] + ach_reward)
                await msg.edit(embed=push_embed, view=None)
                return

        multiplier = 2.0 if won else 0
        new_wallet, leveled_up, new_level, xp_gain, new_achievements = await self._gamble_result(
            interaction.user.id, data, won, amount, "Blackjack", multiplier=multiplier, mods=mods
        )

        if won:
            embed = success_embed("🃏 Blackjack — You Won!", get_action_text("gambling", "blackjack_win", result_text=result_text, winnings=format_money(amount*2), wallet=format_money(new_wallet)) + f"\n{self._bj_display(player_hand, dealer_hand, True)}")
        else:
            embed = error_embed("🃏 Blackjack — You Lost!", get_action_text("gambling", "blackjack_loss", result_text=result_text, bet=format_money(amount), wallet=format_money(new_wallet)) + f"\n{self._bj_display(player_hand, dealer_hand, True)}")
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        await msg.edit(embed=embed, view=None)

    @app_commands.command(name="higherlower", description="Bet on whether the next card is higher or lower!")
    async def higherlower(self, interaction: discord.Interaction, amount: int):
        data, _, mods = await self._gamble_common(interaction, amount)
        if data is None:
            return

        current_rank, current_suit, current_val = draw_hilo_card()
        multiplier = 1.0
        max_multiplier = 10.0

        await interaction.response.send_message(embed=self._hilo_embed(current_rank, current_suit, multiplier, amount, "Higher or Lower?"))
        msg = await interaction.original_response()

        while True:
            view = HigherLowerView(interaction.user.id, timeout=30)
            await msg.edit(embed=self._hilo_embed(current_rank, current_suit, multiplier, amount, "Your turn! Higher, Lower, or Cash Out?"), view=view)
            await view.wait()

            if view.action == "cashout":
                break

            prev_val = current_val
            current_rank, current_suit, current_val = draw_hilo_card()
            diff = current_val - prev_val
            if view.action == "higher":
                correct = diff > 0
            else:
                correct = diff < 0

            if not correct:
                multiplier = 0
                break

            multiplier = min(multiplier + 0.5, max_multiplier)
            if multiplier >= max_multiplier:
                break

        won = multiplier > 0
        if multiplier >= max_multiplier:
            result_text = f"You hit the max {multiplier}x multiplier and cashed out automatically!"
        elif won:
            result_text = f"You cashed out at {multiplier}x!"
        else:
            result_text = f"The card was **{current_rank}{current_suit}** — wrong call. You lost your bet."

        new_wallet, leveled_up, new_level, xp_gain, new_achievements = await self._gamble_result(
            interaction.user.id, data, won, amount, "Higher/Lower", multiplier=multiplier, mods=mods
        )

        if won:
            embed = success_embed("🎰 Higher/Lower — You Won!", get_action_text("gambling", "higherlower_win", result_text=result_text, winnings=format_money(int(amount * multiplier)), wallet=format_money(new_wallet)) + f"\n\n**Current card:** {current_rank}{current_suit}")
        else:
            embed = error_embed("🎰 Higher/Lower — You Lost!", get_action_text("gambling", "higherlower_loss", result_text=result_text, bet=format_money(amount), wallet=format_money(new_wallet)) + f"\n\n**The card was:** {current_rank}{current_suit}")
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        await msg.edit(embed=embed, view=None)

    HORSES = {
        1: {"emoji": "🐎", "name": "Thunder"},
        2: {"emoji": "🐴", "name": "Bolt"},
        3: {"emoji": "🏇", "name": "Flash"},
        4: {"emoji": "🦄", "name": "Spirit"},
    }

    @app_commands.command(name="crash", description="Bet on the rocket multiplier before it crashes!")
    async def crash(self, interaction: discord.Interaction, amount: int):
        data, _, mods = await self._gamble_common(interaction, amount)
        if data is None:
            return

        crash_at = max(1.1, round(1.0 + random.expovariate(1.0), 2))
        view = CrashView(interaction.user.id, timeout=60)
        await interaction.response.send_message(embed=self._crash_embed(1.0, amount, "Rocket launching... Cash out before it crashes!"), view=view)
        msg = await interaction.original_response()
        task = asyncio.create_task(self._crash_loop(view, msg, crash_at, amount))
        await view.wait()
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

        if view.action == "crashed":
            won = False
            multiplier = 0
            result_text = f"The rocket crashed at **{crash_at}x**! You lost your bet."
        else:
            won = True
            multiplier = view.multiplier
            result_text = f"You cashed out at **{multiplier}x** before the crash!"

        new_wallet, leveled_up, new_level, xp_gain, new_achievements = await self._gamble_result(
            interaction.user.id, data, won, amount, "Crash", multiplier=multiplier, mods=mods
        )

        if won:
            embed = success_embed("🚀 Crash — You Won!", get_action_text("gambling", "crash_win", result_text=result_text, winnings=format_money(int(amount * multiplier)), wallet=format_money(new_wallet)))
        else:
            embed = error_embed("🚀 Crash — You Crashed!", get_action_text("gambling", "crash_loss", result_text=result_text, bet=format_money(amount), wallet=format_money(new_wallet)))
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        await msg.edit(embed=embed, view=None)

    async def _crash_loop(self, view, msg, crash_at, amount):
        await asyncio.sleep(1.0)
        while view.action is None:
            view.multiplier = round(view.multiplier + 0.1, 2)
            if view.multiplier >= crash_at:
                view.action = "crashed"
                try:
                    await msg.edit(embed=self._crash_embed(view.multiplier, amount, "💥 The rocket crashed!"), view=None)
                except discord.HTTPException:
                    pass
                view.stop()
                break
            try:
                await msg.edit(embed=self._crash_embed(view.multiplier, amount, "Rocket is rising! Cash out anytime!"), view=view)
            except discord.HTTPException:
                pass
            await asyncio.sleep(1.0)

    @app_commands.command(name="horse_race", description="Pick a horse and bet on the race!")
    @app_commands.choices(horse=[
        app_commands.Choice(name="🐎 Thunder", value=1),
        app_commands.Choice(name="🐴 Bolt", value=2),
        app_commands.Choice(name="🏇 Flash", value=3),
        app_commands.Choice(name="🦄 Spirit", value=4),
    ])
    async def horse_race(self, interaction: discord.Interaction, amount: int, horse: app_commands.Choice[int]):
        data, _, mods = await self._gamble_common(interaction, amount)
        if data is None:
            return

        winner = random.randint(1, 4)
        won = horse.value == winner
        winner_horse = self.HORSES[winner]
        chosen_horse = self.HORSES[horse.value]

        new_wallet, leveled_up, new_level, xp_gain, new_achievements = await self._gamble_result(
            interaction.user.id, data, won, amount, "Horse Race", multiplier=4.0 if won else 0, mods=mods
        )

        if won:
            result_text = f"Your horse **{chosen_horse['emoji']} {chosen_horse['name']}** won the race!"
            embed = success_embed("🏇 Horse Race — You Won!", get_action_text("gambling", "horse_race_win", result_text=result_text, winnings=format_money(amount * 4), wallet=format_money(new_wallet)))
        else:
            result_text = f"**{winner_horse['emoji']} {winner_horse['name']}** won the race. Your horse **{chosen_horse['emoji']} {chosen_horse['name']}** came up short."
            embed = error_embed("🏇 Horse Race — You Lost!", get_action_text("gambling", "horse_race_loss", result_text=result_text, bet=format_money(amount), wallet=format_money(new_wallet)))
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="keno", description="Pick numbers and match the draw — up to 100x payout!")
    async def keno(self, interaction: discord.Interaction, amount: int):
        data, _, mods = await self._gamble_common(interaction, amount)
        if data is None:
            return

        view = KenoView(interaction.user.id, timeout=60)
        await interaction.response.send_message(
            embed=keno_board_embed(view.picks, title="🎰 Keno — Pick 2–8 Numbers!", subtitle="Click numbers to select, then hit Confirm."),
            view=view,
        )
        msg = await interaction.original_response()
        await view.wait()

        if not view.confirmed or len(view.picks) < 2:
            await msg.edit(embed=error_embed("🎰 Keno — Cancelled", "Not enough picks or timed out. Game cancelled."), view=None)
            return

        picks = view.picks

        # ── Draw animation ──
        all_nums = list(range(1, 21))
        random.shuffle(all_nums)
        draw_order = all_nums[:10]
        drawn = set()

        for i, num in enumerate(draw_order):
            drawn.add(num)
            subtitle = f"🎲 Drawing number {i + 1}/10..." if i < 9 else "✅ Final draw!"
            try:
                await msg.edit(embed=keno_board_embed(picks, drawn, amount, "🎰 Keno — Drawing Numbers!", subtitle), view=None)
            except discord.HTTPException:
                pass
            if i < 9:
                await asyncio.sleep(1.2)

        # ── Calculate result ──
        matches = picks & drawn
        match_count = len(matches)
        payout, mult = keno_payout(len(picks), match_count, amount)
        won = payout > 0

        new_wallet, leveled_up, new_level, xp_gain, new_achievements = await self._gamble_result(
            interaction.user.id, data, won, amount, "Keno",
            multiplier=mult if won else 0, mods=mods,
        )

        match_str = ", ".join(str(m) for m in sorted(matches)) if matches else "None"
        drawn_str = ", ".join(str(d) for d in sorted(drawn))

        if won:
            result_text = f"You matched {match_count}/{len(picks)} numbers for a {mult}x payout!"
            embed = discord.Embed(
                title="🎰 Keno — You Won!",
                description=get_action_text("gambling", "keno_win", result_text=result_text, winnings=format_money(payout), wallet=format_money(new_wallet)),
                color=KENO_GOLD,
            )
        else:
            result_text = f"You matched {match_count}/{len(picks)} numbers. No payout this time."
            embed = discord.Embed(
                title="🎰 Keno — No Win",
                description=get_action_text("gambling", "keno_loss", result_text=result_text, bet=format_money(amount), wallet=format_money(new_wallet)),
                color=0x95A5A6,
            )

        embed.add_field(name="🎯 Your Picks", value=", ".join(str(p) for p in sorted(picks)), inline=True)
        embed.add_field(name="🎲 Drawn", value=drawn_str, inline=True)
        embed.add_field(name="✅ Matches", value=f"{match_str} ({match_count})", inline=True)
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        embed.set_footer(text="🎯 = match  🔴 = drawn miss  🔵 = your pick")
        await msg.edit(embed=embed, view=None)

    @app_commands.command(name="lucky_wheel", description="Spin the wheel of fortune for a random multiplier!")
    async def lucky_wheel(self, interaction: discord.Interaction, amount: int):
        data, _, mods = await self._gamble_common(interaction, amount)
        if data is None:
            return

        result_idx = random.randint(0, 11)
        await interaction.response.send_message(
            embed=wheel_embed(-1, amount, "🎡 Lucky Wheel — Spinning...", "The wheel is spinning..."),
        )
        msg = await interaction.original_response()

        # ── Spin animation ──
        total_steps = 20
        for step in range(total_steps):
            highlight = step % 12
            subtitle = "The wheel is spinning..." if step < total_steps - 3 else "Slowing down..."
            try:
                await msg.edit(embed=wheel_embed(highlight, amount, "🎡 Lucky Wheel — Spinning...", subtitle))
            except discord.HTTPException:
                pass
            delay = 0.15 + (step / total_steps) * 0.35
            await asyncio.sleep(delay)

        # ── Final result ──
        seg = WHEEL_SEGMENTS[result_idx]
        payout = int(amount * seg["mult"])
        won = payout > 0

        new_wallet, leveled_up, new_level, xp_gain, new_achievements = await self._gamble_result(
            interaction.user.id, data, won, amount, "Lucky Wheel",
            multiplier=seg["mult"] if won else 0, mods=mods,
        )

        if won:
            result_text = f"The wheel landed on {seg['emoji']} **{seg['label']}** — you won {format_money(payout)}!"
            embed = discord.Embed(
                title="🎡 Lucky Wheel — You Won!",
                description=get_action_text("gambling", "lucky_wheel_win", result_text=result_text, winnings=format_money(payout), wallet=format_money(new_wallet)),
                color=seg["color"],
            )
        else:
            result_text = f"The wheel landed on {seg['emoji']} **{seg['label']}** — bust! You lost your bet."
            embed = discord.Embed(
                title="🎡 Lucky Wheel — Bust!",
                description=get_action_text("gambling", "lucky_wheel_loss", result_text=result_text, bet=format_money(amount), wallet=format_money(new_wallet)),
                color=0x2C3E50,
            )

        embed.add_field(name="🎯 Segment", value=f"{seg['emoji']} **{seg['label']}**", inline=True)
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        embed.set_footer(text="👑 = 10x jackpot  🔥 = 5x  💎 = 3x  💰 = 2x  💀 = bust")
        await msg.edit(embed=embed, view=None)

    @app_commands.command(name="plinko", description="Drop a chip down the pegboard — edges pay up to 5x!")
    async def plinko(self, interaction: discord.Interaction, amount: int):
        data, _, mods = await self._gamble_common(interaction, amount)
        if data is None:
            return

        await interaction.response.send_message(
            embed=plinko_board_embed([], None, amount, "🟡 Plinko — Dropping...", "The chip is falling..."),
        )
        msg = await interaction.original_response()

        # ── Simulate drop ──
        positions = []
        chip_pos = 0
        for row in range(PLINKO_ROWS):
            chip_pos += random.randint(0, 1)
            positions.append(chip_pos)
            subtitle = f"Row {row + 1}/{PLINKO_ROWS} — bouncing..." if row < PLINKO_ROWS - 1 else "Landing..."
            try:
                await msg.edit(embed=plinko_board_embed(positions, None, amount, "🟡 Plinko — Dropping...", subtitle))
            except discord.HTTPException:
                pass
            await asyncio.sleep(0.6)

        final_slot = min(chip_pos, 8)
        mult = PLINKO_SLOTS[final_slot]
        payout = int(amount * mult)
        won = payout > 0

        new_wallet, leveled_up, new_level, xp_gain, new_achievements = await self._gamble_result(
            interaction.user.id, data, won, amount, "Plinko",
            multiplier=mult if won else 0, mods=mods,
        )

        emoji = PLINKO_SLOT_EMOJI[final_slot]
        if won:
            result_text = f"The chip landed on {emoji} **{mult}x** — you won {format_money(payout)}!"
            title = "🟡 Plinko — You Won!"
            narrative = get_action_text("gambling", "plinko_win", result_text=result_text, winnings=format_money(payout), wallet=format_money(new_wallet))
            color = PLINKO_COLORS[final_slot]
        else:
            result_text = f"The chip landed on {emoji} **{mult}x** — bust! You lost your bet."
            title = "🟡 Plinko — Bust!"
            narrative = get_action_text("gambling", "plinko_loss", result_text=result_text, bet=format_money(amount), wallet=format_money(new_wallet))
            color = 0x2C3E50

        # Build final embed with board + narrative + fields
        board_embed = plinko_board_embed(positions, final_slot, amount, title, "")
        final_embed = discord.Embed(title=title, description=board_embed.description + f"\n\n{narrative}", color=color)
        final_embed.add_field(name="🎯 Slot", value=f"{emoji} **{mult}x**", inline=True)
        final_embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            final_embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            final_embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        final_embed.set_footer(text="🟡 = chip  ● = peg  Bell-curve distribution — edges pay more!")
        await msg.edit(embed=final_embed, view=None)

    @app_commands.command(name="overunder", description="Bet on whether two dice sum over, under, or exactly 7!")
    @app_commands.choices(bet_type=[
        app_commands.Choice(name="📈 Over 7 (1.95x)", value="over"),
        app_commands.Choice(name="📉 Under 7 (1.95x)", value="under"),
        app_commands.Choice(name="🎯 Exactly 7 (5x)", value="seven"),
        app_commands.Choice(name="🔢 Specific Sum 2-12", value="sum"),
    ])
    async def overunder(self, interaction: discord.Interaction, amount: int, bet_type: app_commands.Choice[str], target_sum: int = 7):
        if bet_type.value == "sum" and (target_sum < 2 or target_sum > 12):
            await interaction.response.send_message(embed=error_embed("Error", "Pick a sum between 2 and 12."), ephemeral=True)
            return
        data, _, mods = await self._gamble_common(interaction, amount)
        if data is None:
            return

        bet_label_map = {"over": "Over 7", "under": "Under 7", "seven": "Exactly 7", "sum": f"Sum {target_sum}"}
        bet_label = bet_label_map[bet_type.value]

        await interaction.response.send_message(
            embed=dice_embed(rolling=True, subtitle=f"Bet: {bet_label} — {format_money(amount)}\nRolling the dice..."),
        )
        msg = await interaction.original_response()

        # ── Dice roll animation (3 frames) ──
        for _ in range(3):
            rand1, rand2 = random.randint(1, 6), random.randint(1, 6)
            try:
                await msg.edit(embed=dice_embed(rand1, rand2, rolling=True, subtitle="The dice are tumbling..."))
            except discord.HTTPException:
                pass
            await asyncio.sleep(0.4)

        # ── Final roll ──
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        total = d1 + d2

        if bet_type.value == "over":
            won = total > 7
            mult = OVERUNDER_PAYOUTS["over"]
        elif bet_type.value == "under":
            won = total < 7
            mult = OVERUNDER_PAYOUTS["under"]
        elif bet_type.value == "seven":
            won = total == 7
            mult = OVERUNDER_PAYOUTS["seven"]
        else:
            won = total == target_sum
            mult = OVERUNDER_PAYOUTS["sum"][target_sum]

        new_wallet, leveled_up, new_level, xp_gain, new_achievements = await self._gamble_result(
            interaction.user.id, data, won, amount, "Over/Under",
            multiplier=mult if won else 0, mods=mods,
        )

        face1 = DICE_FACES[d1 - 1]
        face2 = DICE_FACES[d2 - 1]
        if won:
            result_text = f"Rolled {face1} {face2} = **{total}** — {bet_label} wins at {mult}x!"
            embed = discord.Embed(
                title="🎲 Over/Under — You Won!",
                description=get_action_text("gambling", "overunder_win", result_text=result_text, winnings=format_money(int(amount * mult)), wallet=format_money(new_wallet)),
                color=0xF1C40F,
            )
        else:
            result_text = f"Rolled {face1} {face2} = **{total}** — {bet_label} loses."
            embed = discord.Embed(
                title="🎲 Over/Under — You Lost!",
                description=get_action_text("gambling", "overunder_loss", result_text=result_text, bet=format_money(amount), wallet=format_money(new_wallet)),
                color=0xE74C3C,
            )

        embed.add_field(name="🎲 Dice", value=f"{face1} {face2} = **{total}**", inline=True)
        embed.add_field(name="🎯 Bet", value=bet_label, inline=True)
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        embed.set_footer(text="⚀⚁⚂⚃⚄⚅ — Bet over, under, exactly 7, or a specific sum")
        await msg.edit(embed=embed, view=None)

    @app_commands.command(name="mystery_box", description="Pick one of three boxes — what's inside?")
    async def mystery_box(self, interaction: discord.Interaction, amount: int):
        data, _, mods = await self._gamble_common(interaction, amount)
        if data is None:
            return

        view = MysteryBoxView(interaction.user.id, timeout=30)
        await interaction.response.send_message(
            embed=mystery_embed(None, amount, "🎁 Mystery Box — Choose a Box!", "Three mysterious boxes... pick one to reveal your prize."),
            view=view,
        )
        msg = await interaction.original_response()
        await view.wait()

        chosen = view.chosen
        prize = view.prizes[chosen]
        payout = int(amount * prize["mult"])
        won = payout > 0

        # ── Reveal animation ──
        reveal_display = "🎁    🎁    🎁\n\n*Opening your box...*"
        try:
            await msg.edit(embed=mystery_embed(reveal_display, amount, "🎁 Mystery Box — Revealing...", "Something is inside..."), view=None)
        except discord.HTTPException:
            pass
        await asyncio.sleep(1.0)

        # ── Build final reveal ──
        box_displays = []
        for i in range(3):
            p = view.prizes[i]
            if i == chosen:
                box_displays.append(f"**{p['emoji']} {p['label']}** ✅")
            else:
                box_displays.append(f"~~{p['emoji']} {p['label']}~~")
        reveal = "    ".join(box_displays)

        new_wallet, leveled_up, new_level, xp_gain, new_achievements = await self._gamble_result(
            interaction.user.id, data, won, amount, "Mystery Box",
            multiplier=prize["mult"] if won else 0, mods=mods,
        )

        if won:
            result_text = f"You opened Box {chosen + 1} and found {prize['emoji']} **{prize['label']}** — {prize['mult']}x your bet!"
            embed = discord.Embed(
                title="🎁 Mystery Box — You Won!",
                description=get_action_text("gambling", "mystery_box_win", result_text=result_text, winnings=format_money(payout), wallet=format_money(new_wallet)),
                color=prize["color"],
            )
        else:
            result_text = f"You opened Box {chosen + 1} and found {prize['emoji']} **{prize['label']}** — bust!"
            embed = discord.Embed(
                title="🎁 Mystery Box — Bust!",
                description=get_action_text("gambling", "mystery_box_loss", result_text=result_text, bet=format_money(amount), wallet=format_money(new_wallet)),
                color=0x2C3E50,
            )

        embed.add_field(name="🎁 Your Box", value=f"Box {chosen + 1}: {prize['emoji']} **{prize['label']}** ({prize['mult']}x)", inline=True)
        other1 = view.prizes[(chosen + 1) % 3]
        other2 = view.prizes[(chosen + 2) % 3]
        embed.add_field(name="❓ What Could Have Been", value=f"Box {(chosen + 1) % 3 + 1}: {other1['emoji']} {other1['label']}\nBox {(chosen + 2) % 3 + 1}: {other2['emoji']} {other2['label']}", inline=True)
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        embed.set_footer(text="👑 = 10x mega  🔥 = 5x jackpot  💰 = 2x  💀 = bust")
        await msg.edit(embed=embed, view=None)

    def _bj_display(self, player, dealer, reveal=False):
        dealer_str = " ".join(dealer) if reveal else f"{dealer[0]} ❓"
        return f"**Dealer**: {dealer_str} ({hand_value(dealer) if reveal else '?'})\n**You**: {' '.join(player)} ({hand_value(player)})"

    def _bj_embed(self, player, dealer, title, reveal=False):
        display = self._bj_display(player, dealer, reveal)
        return info_embed(f"🃏 Blackjack", f"{display}\n\n{title}")

    def _hilo_embed(self, rank, suit, multiplier, amount, title):
        display = f"**Current card:** {rank}{suit}\n**Multiplier:** {multiplier}x\n**Potential win:** {format_money(int(amount * multiplier))}"
        return info_embed("🎰 Higher or Lower", f"{display}\n\n{title}")

    def _crash_embed(self, multiplier, amount, title):
        display = f"**Multiplier:** {multiplier}x\n**Potential win:** {format_money(int(amount * multiplier))}"
        return info_embed("🚀 Crash", f"{display}\n\n{title}")

    @app_commands.command(name="roulette", description="Play roulette — bet on colors, ranges, or a specific number!")
    @app_commands.choices(bet_type=[
        app_commands.Choice(name="🔴 Red (2x)", value="red"),
        app_commands.Choice(name="⚫ Black (2x)", value="black"),
        app_commands.Choice(name="🟢 Green 0 (14x)", value="green"),
        app_commands.Choice(name="🔢 Specific Number 0-36 (36x)", value="number"),
        app_commands.Choice(name="⚖️ Even (1.95x)", value="even"),
        app_commands.Choice(name="🎲 Odd (1.95x)", value="odd"),
        app_commands.Choice(name="⬇️ Low 1-18 (1.95x)", value="low"),
        app_commands.Choice(name="⬆️ High 19-36 (1.95x)", value="high"),
        app_commands.Choice(name="📊 1st Dozen 1-12 (2.9x)", value="dozen1"),
        app_commands.Choice(name="📊 2nd Dozen 13-24 (2.9x)", value="dozen2"),
        app_commands.Choice(name="📊 3rd Dozen 25-36 (2.9x)", value="dozen3"),
        app_commands.Choice(name="📋 Column 1 (2.9x)", value="col1"),
        app_commands.Choice(name="📋 Column 2 (2.9x)", value="col2"),
        app_commands.Choice(name="📋 Column 3 (2.9x)", value="col3"),
    ])
    async def roulette(self, interaction: discord.Interaction, amount: int, bet_type: app_commands.Choice[str], number: int = -1):
        if bet_type.value == "number" and (number < 0 or number > 36):
            await interaction.response.send_message(embed=error_embed("Error", "Pick a number between 0 and 36."), ephemeral=True)
            return
        data, _, mods = await self._gamble_common(interaction, amount)
        if data is None:
            return

        bet_label_map = {
            "red": "Red", "black": "Black", "green": "Green 0", "number": f"Number {number}",
            "even": "Even", "odd": "Odd", "low": "Low 1-18", "high": "High 19-36",
            "dozen1": "1st Dozen", "dozen2": "2nd Dozen", "dozen3": "3rd Dozen",
            "col1": "Column 1", "col2": "Column 2", "col3": "Column 3",
        }
        bet_label = bet_label_map[bet_type.value]

        await interaction.response.send_message(
            embed=info_embed("🎡 Roulette — Spinning...", f"**Bet**: {bet_label} — {format_money(amount)}\n\n*The wheel is spinning...*"),
        )
        msg = await interaction.original_response()

        # ── Spin animation ──
        for i in range(5):
            rand_num = random.randint(0, 36)
            rand_color = "green" if rand_num == 0 else ("red" if rand_num in ROULETTE_COLORS["red"] else "black")
            rand_emoji = {"red": "🔴", "black": "⚫", "green": "🟢"}[rand_color]
            try:
                await msg.edit(embed=info_embed("🎡 Roulette — Spinning...", f"**Bet**: {bet_label} — {format_money(amount)}\n\n*The wheel is spinning...*\n\n{rand_emoji} {rand_num}"))
            except discord.HTTPException:
                pass
            await asyncio.sleep(0.5)

        # ── Final result ──
        result_num = random.randint(0, 36)
        if result_num in ROULETTE_COLORS["green"]:
            color = "green"
        elif result_num in ROULETTE_COLORS["red"]:
            color = "red"
        else:
            color = "black"

        color_emoji = {"red": "🔴", "black": "⚫", "green": "🟢"}[color]

        # ── Determine win/loss ──
        if bet_type.value == "number":
            won = result_num == number
            multiplier = 36.0
        elif bet_type.value == "green":
            won = color == "green"
            multiplier = 14.0
        elif bet_type.value in ("red", "black"):
            won = color == bet_type.value
            multiplier = 2.0
        elif bet_type.value == "even":
            won = result_num != 0 and result_num % 2 == 0
            multiplier = 1.95
        elif bet_type.value == "odd":
            won = result_num % 2 == 1
            multiplier = 1.95
        elif bet_type.value == "low":
            won = 1 <= result_num <= 18
            multiplier = 1.95
        elif bet_type.value == "high":
            won = 19 <= result_num <= 36
            multiplier = 1.95
        elif bet_type.value == "dozen1":
            won = 1 <= result_num <= 12
            multiplier = 2.9
        elif bet_type.value == "dozen2":
            won = 13 <= result_num <= 24
            multiplier = 2.9
        elif bet_type.value == "dozen3":
            won = 25 <= result_num <= 36
            multiplier = 2.9
        elif bet_type.value in ("col1", "col2", "col3"):
            col_num = int(bet_type.value[-1])
            won = result_num != 0 and result_num % 3 == (col_num % 3 if col_num != 3 else 0)
            multiplier = 2.9
        else:
            won = False
            multiplier = 0

        new_wallet, leveled_up, new_level, xp_gain, new_achievements = await self._gamble_result(
            interaction.user.id, data, won, amount, "Roulette", multiplier=multiplier if won else 0, mods=mods
        )

        if won:
            winnings = int(amount * multiplier)
            result_text = f"The ball landed on **{color_emoji} {result_num}** — {bet_label} wins at {multiplier}x!"
            embed = discord.Embed(
                title="🎡 Roulette — You Won!",
                description=get_action_text("gambling", "roulette_win", result_text=result_text, winnings=format_money(winnings), wallet=format_money(new_wallet)),
                color=0xF1C40F,
            )
        else:
            result_text = f"The ball landed on **{color_emoji} {result_num}** — {bet_label} loses."
            embed = discord.Embed(
                title="🎡 Roulette — You Lost!",
                description=get_action_text("gambling", "roulette_loss", result_text=result_text, bet=format_money(amount), wallet=format_money(new_wallet)),
                color=0xE74C3C,
            )

        embed.add_field(name="🎯 Result", value=f"{color_emoji} **{result_num}**", inline=True)
        embed.add_field(name="🎲 Your Bet", value=bet_label, inline=True)
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        embed.set_footer(text="🎡 European Roulette — 0-36 | Colors 2x | Even/Odd/High/Low 1.95x | Dozens/Columns 2.9x | Number 36x")
        await msg.edit(embed=embed, view=None)


async def setup(bot):
    await bot.add_cog(Gambling(bot))
