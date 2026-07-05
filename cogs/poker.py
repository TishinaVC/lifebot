import asyncio
import random
from collections import Counter
from itertools import combinations

import discord
from discord import app_commands
from discord.ext import commands

import database as db
from utils.embeds import success_embed, error_embed, info_embed, money_embed, format_money
from config import ACHIEVEMENTS
from utils.helpers import check_level_up, xp_for_next_level, stat_modifier, pet_bonus

# ═══════════════════════════════════════════════════════════════════════
# CARD ENGINE
# ═══════════════════════════════════════════════════════════════════════

SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
RANK_VALUES = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
               "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13, "A": 14}

RED_SUITS = {"♥", "♦"}


def card_str(card):
    rank, suit = card
    return f"{rank}{suit}"


def card_emoji(card):
    rank, suit = card
    color_str = "red" if suit in RED_SUITS else "blk"
    return f"[{rank}{suit}]"


def create_deck():
    deck = [(r, s) for r in RANKS for s in SUITS]
    random.shuffle(deck)
    return deck


# ═══════════════════════════════════════════════════════════════════════
# HAND EVALUATOR
# ═══════════════════════════════════════════════════════════════════════

HAND_NAMES = {
    9: "Royal Flush", 8: "Straight Flush", 7: "Four of a Kind",
    6: "Full House", 5: "Flush", 4: "Straight",
    3: "Three of a Kind", 2: "Two Pair", 1: "One Pair", 0: "High Card",
}


def evaluate_5(cards):
    """Evaluate exactly 5 cards. Returns (rank_int, tiebreak_list)."""
    values = sorted([RANK_VALUES[c[0]] for c in cards], reverse=True)
    suits = [c[1] for c in cards]
    is_flush = len(set(suits)) == 1

    unique = sorted(set(values), reverse=True)
    is_straight = False
    straight_high = 0
    if len(unique) == 5:
        if unique[0] - unique[4] == 4:
            is_straight = True
            straight_high = unique[0]
        elif unique == [14, 5, 4, 3, 2]:
            is_straight = True
            straight_high = 5

    counts = Counter(values)
    cs = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)

    if is_straight and is_flush:
        if straight_high == 14:
            return (9, [14])
        return (8, [straight_high])
    if cs[0][1] == 4:
        return (7, [cs[0][0], cs[1][0]])
    if cs[0][1] == 3 and cs[1][1] == 2:
        return (6, [cs[0][0], cs[1][0]])
    if is_flush:
        return (5, values)
    if is_straight:
        return (4, [straight_high])
    if cs[0][1] == 3:
        return (3, [cs[0][0], cs[1][0], cs[2][0]])
    if cs[0][1] == 2 and cs[1][1] == 2:
        return (2, [cs[0][0], cs[1][0], cs[2][0]])
    if cs[0][1] == 2:
        return (1, [cs[0][0], cs[1][0], cs[2][0], cs[3][0]])
    return (0, values)


def best_hand(hole_cards, community_cards):
    """Find best 5-card hand from 7 cards. Returns (rank_int, tiebreak_list)."""
    all_cards = hole_cards + community_cards
    if len(all_cards) < 5:
        return None
    best = None
    for combo in combinations(all_cards, 5):
        r = evaluate_5(list(combo))
        if best is None or r > best:
            best = r
    return best


def hand_name(rank_tuple):
    return HAND_NAMES[rank_tuple[0]]


# ═══════════════════════════════════════════════════════════════════════
# POKER PLAYER
# ═══════════════════════════════════════════════════════════════════════

class PokerPlayer:
    def __init__(self, user, buy_in):
        self.user = user
        self.id = user.id
        self.name = user.display_name
        self.stack = buy_in
        self.hole_cards = []
        self.current_bet = 0
        self.total_bet = 0
        self.folded = False
        self.all_in = False
        self.acted = False
        self.standing = False
        self.last_action = ""
        self.hand_result = None

    @property
    def active(self):
        return not self.folded and not self.standing

    @property
    def can_act(self):
        return not self.folded and not self.all_in and not self.standing and self.stack > 0


# ═══════════════════════════════════════════════════════════════════════
# EMBED HELPERS
# ═══════════════════════════════════════════════════════════════════════

def poker_lobby_embed(players, buy_in, time_left=60):
    seats = ""
    for i in range(4):
        if i < len(players):
            seats += f"  🪑 Seat {i+1}: **{players[i].display_name}**\n"
        else:
            seats += f"  🪑 Seat {i+1}: *Empty*\n"

    embed = discord.Embed(
        title="🃏 Texas Hold'em Poker — Waiting for Players",
        description=(
            f"**Buy-in**: {format_money(buy_in)}\n"
            f"**Time left**: {time_left}s\n\n"
            f"**Seats** ({len(players)}/4):\n{seats}\n"
            f"Click **Join Table** to sit down! Need at least 2 players to start."
        ),
        color=0x9B59B6,
    )
    embed.set_footer(text="🎮 Multiplayer Poker | Up to 4 players | Wallet only — not bank!")
    return embed


def poker_game_embed(players, community_cards, pot, current_player, current_bet,
                     hand_num, phase, dealer_pos):
    """Main game state embed."""
    phase_names = {
        "preflop": "Pre-Flop", "flop": "Flop", "turn": "Turn",
        "river": "River", "showdown": "Showdown", "dealing": "Dealing...",
    }
    phase_name = phase_names.get(phase, phase)

    # Community cards
    if community_cards:
        comm = "  ".join(card_str(c) for c in community_cards)
    else:
        comm = "🂠  🂠  🂠  🂠  🂠"

    # Seats
    seat_lines = []
    for i, p in enumerate(players):
        indicator = ""
        if i == dealer_pos:
            indicator = "🃏 "
        if p is current_player and p.can_act:
            indicator += "▶️ "
        if p.folded:
            seat_lines.append(f"  {indicator}~~{p.name}~~ — Folded 🚫")
        elif p.all_in:
            seat_lines.append(f"  {indicator}**{p.name}** — 💰 {format_money(p.stack)} | All In 💥 | Bet: {format_money(p.current_bet)}")
        elif p.standing:
            seat_lines.append(f"  {indicator}**{p.name}** — 💰 {format_money(p.stack)} | Standing up 🪑 | Bet: {format_money(p.current_bet)}")
        else:
            status = p.last_action if p.last_action else "Waiting"
            seat_lines.append(f"  {indicator}**{p.name}** — 💰 {format_money(p.stack)} | Bet: {format_money(p.current_bet)} | {status}")

    seats = "\n".join(seat_lines)

    to_call = current_bet - (current_player.current_bet if current_player else 0)

    description = (
        f"**Hand #{hand_num}** | **Phase**: {phase_name}\n\n"
        f"**Community Cards**: {comm}\n\n"
        f"**Pot**: {format_money(pot)}\n\n"
        f"**Seats**:\n{seats}\n"
    )
    if current_player and current_player.can_act and phase not in ("showdown", "dealing"):
        description += f"\n🎯 **{current_player.name}'s turn** — To call: {format_money(max(0, to_call))}"

    embed = discord.Embed(
        title="🃏 Texas Hold'em Poker",
        description=description,
        color=0x2ECC71 if current_player and current_player.can_act else 0x9B59B6,
    )
    embed.set_footer(text="🂠 = hidden card | Click 'My Cards' to see your hand (private) | 'Stand Up' to leave after this hand")
    return embed


def poker_showdown_embed(players, community_cards, pot, hand_num, winners, all_hands):
    """Showdown results embed."""
    comm = "  ".join(card_str(c) for c in community_cards)

    lines = []
    for p in all_hands:
        cards = " ".join(card_str(c) for c in p.hole_cards)
        hname = hand_name(p.hand_result) if p.hand_result else "—"
        if p in winners:
            share = pot // len(winners)
            lines.append(f"  🏆 **{p.name}** — {cards} — {hname} — Wins {format_money(share)}!")
        elif p.folded:
            lines.append(f"  ~~{p.name}~~ — Folded 🚫")
        else:
            lines.append(f"  **{p.name}** — {cards} — {hname}")

    description = (
        f"**Hand #{hand_num} — Showdown!**\n\n"
        f"**Community Cards**: {comm}\n\n"
        f"**Pot**: {format_money(pot)}\n\n"
        f"**Results**:\n" + "\n".join(lines)
    )

    embed = discord.Embed(
        title="🃏 Texas Hold'em — Showdown!",
        description=description,
        color=0xF1C40F,
    )
    embed.set_footer(text="Next hand starting in 6 seconds... Click 'Stand Up' to leave!")
    return embed


# ═══════════════════════════════════════════════════════════════════════
# VIEWS
# ═══════════════════════════════════════════════════════════════════════

class PokerLobbyView(discord.ui.View):
    def __init__(self, host_id, buy_in, timeout=60):
        super().__init__(timeout=timeout)
        self.host_id = host_id
        self.buy_in = buy_in
        self.players = []
        self.started = False

    @discord.ui.button(label="Join Table", style=discord.ButtonStyle.success, emoji="🪑")
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        if len(self.players) >= 4:
            await interaction.response.send_message("Table is full! (4/4)", ephemeral=True)
            return
        if any(p.id == interaction.user.id for p in self.players):
            await interaction.response.send_message("You're already seated!", ephemeral=True)
            return
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if data["wallet"] < self.buy_in:
            await interaction.response.send_message(
                f"You need {format_money(self.buy_in)} in your wallet to join! (Bank money doesn't count.)",
                ephemeral=True,
            )
            return
        self.players.append(interaction.user)
        embed = poker_lobby_embed(self.players, self.buy_in, int(self.timeout - self._elapsed))
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Start Now", style=discord.ButtonStyle.primary, emoji="▶️")
    async def start_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.host_id:
            await interaction.response.send_message("Only the host can start early!", ephemeral=True)
            return
        if len(self.players) < 2:
            await interaction.response.send_message("Need at least 2 players to start!", ephemeral=True)
            return
        self.started = True
        await interaction.response.defer()
        self.stop()

    async def on_timeout(self):
        self.started = len(self.players) >= 2
        self.stop()

    @property
    def _elapsed(self):
        # Approximate elapsed time (not precise but good enough for display)
        return 0


class RaiseModal(discord.ui.Modal):
    def __init__(self, action_view):
        super().__init__(title="Raise Amount")
        self.action_view = action_view
        self.amount_input = discord.ui.TextInput(
            label="Raise to (total bet amount)",
            placeholder="e.g. 100",
            required=True,
            min_length=1,
            max_length=10,
        )
        self.add_item(self.amount_input)

    async def on_submit(self, interaction: discord.Interaction):
        if self.action_view.action is not None:
            await interaction.response.send_message("Too late — action already taken!", ephemeral=True)
            return
        try:
            amount = int(self.amount_input.value)
        except ValueError:
            await interaction.response.send_message("Invalid amount! Must be a number.", ephemeral=True)
            return
        if amount <= 0:
            await interaction.response.send_message("Amount must be positive!", ephemeral=True)
            return
        self.action_view.action = "raise"
        self.action_view.raise_amount = amount
        await interaction.response.defer()
        self.action_view.stop()


class PokerActionView(discord.ui.View):
    """Action buttons shown during a player's turn. Utility buttons available to all."""

    def __init__(self, game, player, current_bet, timeout=30):
        super().__init__(timeout=timeout)
        self.game = game
        self.player = player
        self.current_bet = current_bet
        self.action = None
        self.raise_amount = 0

        # Update Call/Check button label
        call_amount = current_bet - player.current_bet
        for child in self.children:
            if hasattr(child, 'custom_id') and child.custom_id == "poker_call":
                if call_amount <= 0:
                    child.label = "Check"
                    child.emoji = "✋"
                else:
                    actual_call = min(call_amount, player.stack)
                    child.label = f"Call {format_money(actual_call)}"
                    child.emoji = "📞"

    @discord.ui.button(label="Fold", style=discord.ButtonStyle.danger, emoji="🚫", custom_id="poker_fold")
    async def fold(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.player.id:
            await interaction.response.send_message("Not your turn!", ephemeral=True)
            return
        self.action = "fold"
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label="Call", style=discord.ButtonStyle.success, emoji="📞", custom_id="poker_call")
    async def call(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.player.id:
            await interaction.response.send_message("Not your turn!", ephemeral=True)
            return
        self.action = "call"
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label="Raise", style=discord.ButtonStyle.primary, emoji="⬆️", custom_id="poker_raise")
    async def raise_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.player.id:
            await interaction.response.send_message("Not your turn!", ephemeral=True)
            return
        if self.player.stack <= 0:
            await interaction.response.send_message("You have no chips to raise!", ephemeral=True)
            return
        modal = RaiseModal(self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="All In", style=discord.ButtonStyle.danger, emoji="💥", custom_id="poker_allin")
    async def all_in(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.player.id:
            await interaction.response.send_message("Not your turn!", ephemeral=True)
            return
        self.action = "allin"
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label="My Cards", style=discord.ButtonStyle.secondary, emoji="🂠", custom_id="poker_mycards")
    async def my_cards(self, interaction: discord.Interaction, button: discord.ui.Button):
        p = next((p for p in self.game.players if p.id == interaction.user.id), None)
        if p is None:
            await interaction.response.send_message("You're not in this game!", ephemeral=True)
            return
        if not p.hole_cards:
            await interaction.response.send_message("No cards dealt yet.", ephemeral=True)
            return
        cards = "  ".join(card_str(c) for c in p.hole_cards)
        await interaction.response.send_message(f"🃏 Your hole cards: **{cards}**", ephemeral=True)

    @discord.ui.button(label="Stand Up", style=discord.ButtonStyle.secondary, emoji="🪑", custom_id="poker_standup")
    async def stand_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        p = next((p for p in self.game.players if p.id == interaction.user.id), None)
        if p is None:
            await interaction.response.send_message("You're not in this game!", ephemeral=True)
            return
        if p.standing:
            await interaction.response.send_message("You're already marked to stand up.", ephemeral=True)
            return
        p.standing = True
        p.last_action = "Standing up 🪑"
        await interaction.response.send_message(
            "You'll stand up and receive your remaining chips after this hand ends.",
            ephemeral=True,
        )

    async def on_timeout(self):
        if self.action is None:
            self.action = "fold"
        self.stop()


class PokerStandupView(discord.ui.View):
    """View shown between hands — only utility buttons."""

    def __init__(self, game, timeout=8):
        super().__init__(timeout=timeout)
        self.game = game

    @discord.ui.button(label="My Cards", style=discord.ButtonStyle.secondary, emoji="🂠", custom_id="poker_su_mycards")
    async def my_cards(self, interaction: discord.Interaction, button: discord.ui.Button):
        p = next((p for p in self.game.players if p.id == interaction.user.id), None)
        if p is None:
            await interaction.response.send_message("You're not in this game!", ephemeral=True)
            return
        if not p.hole_cards:
            await interaction.response.send_message("No cards dealt yet.", ephemeral=True)
            return
        cards = "  ".join(card_str(c) for c in p.hole_cards)
        await interaction.response.send_message(f"🃏 Your hole cards: **{cards}**", ephemeral=True)

    @discord.ui.button(label="Stand Up", style=discord.ButtonStyle.danger, emoji="🪑", custom_id="poker_su_standup")
    async def stand_up(self, interaction: discord.Interaction, button: discord.ui.Button):
        p = next((p for p in self.game.players if p.id == interaction.user.id), None)
        if p is None:
            await interaction.response.send_message("You're not in this game!", ephemeral=True)
            return
        if p.standing:
            await interaction.response.send_message("You're already marked to stand up.", ephemeral=True)
            return
        p.standing = True
        await interaction.response.send_message(
            "You'll stand up and receive your remaining chips after this hand.",
            ephemeral=True,
        )


# ═══════════════════════════════════════════════════════════════════════
# POKER GAME CONTROLLER
# ═══════════════════════════════════════════════════════════════════════

class PokerGame:
    def __init__(self, bot, channel, players_data, buy_in):
        self.bot = bot
        self.channel = channel
        self.players = [PokerPlayer(user, buy_in) for user in players_data]
        self.buy_in = buy_in
        self.deck = []
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.dealer_pos = 0
        self.hand_num = 0
        self.message = None
        self.sb_amount = max(1, buy_in // 50)
        self.bb_amount = max(2, buy_in // 25)

    @property
    def active_players(self):
        return [p for p in self.players if not p.folded]

    @property
    def seated_players(self):
        return [p for p in self.players if not p.standing]

    async def send_hole_cards_dm(self):
        """Try to DM each player their hole cards."""
        for p in self.players:
            if p.folded or p.standing:
                continue
            cards = "  ".join(card_str(c) for c in p.hole_cards)
            try:
                await p.user.send(f"🃏 **Poker — Hand #{self.hand_num}**\nYour hole cards: **{cards}**")
            except (discord.Forbidden, discord.HTTPException):
                pass  # They can use the "My Cards" button instead

    def reset_hand_state(self):
        for p in self.players:
            p.hole_cards = []
            p.current_bet = 0
            p.total_bet = 0
            p.folded = False
            p.all_in = False
            p.acted = False
            p.last_action = ""
            p.hand_result = None

    def post_blinds(self):
        seated = self.seated_players
        if len(seated) < 2:
            return

        sb_pos = (self.dealer_pos + 1) % len(seated)
        bb_pos = (self.dealer_pos + 2) % len(seated)

        sb_player = seated[sb_pos]
        bb_player = seated[bb_pos]

        sb_amount = min(self.sb_amount, sb_player.stack)
        sb_player.stack -= sb_amount
        sb_player.current_bet = sb_amount
        sb_player.total_bet = sb_amount
        sb_player.last_action = f"SB {format_money(sb_amount)}"
        self.pot += sb_amount

        bb_amount = min(self.bb_amount, bb_player.stack)
        bb_player.stack -= bb_amount
        bb_player.current_bet = bb_amount
        bb_player.total_bet = bb_amount
        bb_player.last_action = f"BB {format_money(bb_amount)}"
        self.pot += bb_amount

        self.current_bet = bb_amount

    async def betting_round(self, phase):
        """Run a full betting round."""
        seated = self.seated_players
        if len(seated) < 2:
            return

        # Determine starting position
        if phase == "preflop":
            start = (self.dealer_pos + 3) % len(seated)  # UTG = after BB
        else:
            start = (self.dealer_pos + 1) % len(seated)  # SB first

        # Reset acted flags
        for p in seated:
            p.acted = False

        pos = start
        last_raiser = None
        consecutive_passes = 0
        max_iterations = 50  # Safety limit

        while max_iterations > 0:
            max_iterations -= 1

            # Check if round is over
            can_act = [p for p in seated if p.can_act]
            if len(can_act) <= 1:
                break

            not_acted = [p for p in can_act if not p.acted]
            all_equal = all(p.current_bet == self.current_bet for p in can_act)

            if not not_acted and all_equal:
                break

            p = seated[pos % len(seated)]

            if not p.can_act:
                pos = (pos + 1) % len(seated)
                consecutive_passes += 1
                if consecutive_passes > len(seated) * 2:
                    break
                continue

            consecutive_passes = 0

            # Show game state and wait for action
            view = PokerActionView(self, p, self.current_bet, timeout=30)
            embed = poker_game_embed(
                self.players, self.community_cards, self.pot,
                p, self.current_bet, self.hand_num, phase, self.dealer_pos,
            )
            try:
                await self.message.edit(embed=embed, view=view)
            except discord.HTTPException:
                pass

            await view.wait()

            # Process action
            if view.action == "fold":
                p.folded = True
                p.last_action = "Folded 🚫"

            elif view.action == "call":
                call_amount = min(self.current_bet - p.current_bet, p.stack)
                p.stack -= call_amount
                p.current_bet += call_amount
                p.total_bet += call_amount
                self.pot += call_amount
                if p.stack == 0:
                    p.all_in = True
                    p.last_action = "All In 💥"
                else:
                    p.last_action = f"Called {format_money(call_amount)}"

            elif view.action == "raise":
                raise_to = min(view.raise_amount, p.current_bet + p.stack)
                raise_amount = raise_to - p.current_bet
                if raise_amount <= 0:
                    # Invalid raise, treat as call
                    call_amount = min(self.current_bet - p.current_bet, p.stack)
                    p.stack -= call_amount
                    p.current_bet += call_amount
                    p.total_bet += call_amount
                    self.pot += call_amount
                    p.last_action = f"Called {format_money(call_amount)}"
                else:
                    p.stack -= raise_amount
                    p.current_bet += raise_amount
                    p.total_bet += raise_amount
                    self.pot += raise_amount
                    self.current_bet = p.current_bet
                    last_raiser = p
                    # Reset acted for all other active players
                    for other in seated:
                        if other is not p and other.can_act:
                            other.acted = False
                    if p.stack == 0:
                        p.all_in = True
                        p.last_action = "All In 💥"
                    else:
                        p.last_action = f"Raised to {format_money(p.current_bet)}"

            elif view.action == "allin":
                all_in_amount = p.stack
                p.current_bet += all_in_amount
                p.total_bet += all_in_amount
                self.pot += all_in_amount
                p.stack = 0
                p.all_in = True
                p.last_action = "All In 💥"
                if p.current_bet > self.current_bet:
                    self.current_bet = p.current_bet
                    last_raiser = p
                    for other in seated:
                        if other is not p and other.can_act:
                            other.acted = False

            elif view.action is None:
                # Timeout = auto-fold
                p.folded = True
                p.last_action = "Auto-folded (timeout) ⏰"

            p.acted = True
            pos = (pos + 1) % len(seated)

            # Check if only one player remains
            if len(self.active_players) <= 1:
                break

    def award_pot(self):
        """Award pot to winner(s). Handles side pots."""
        active = self.active_players
        if len(active) == 1:
            winner = active[0]
            winner.stack += self.pot
            winner.hand_result = best_hand(winner.hole_cards, self.community_cards) or (0, [])
            return [winner], self.pot

        # Evaluate all active players' hands
        for p in active:
            p.hand_result = best_hand(p.hole_cards, self.community_cards)

        # Side pot calculation
        # Sort by total contribution
        contributors = sorted([p for p in self.players if p.total_bet > 0],
                              key=lambda x: x.total_bet)
        side_pots = []
        prev_level = 0
        for i, p in enumerate(contributors):
            level = p.total_bet
            if level <= prev_level:
                continue
            layer_amount = level - prev_level
            # All players who contributed at least 'level' contribute to this pot layer
            contributors_at_level = [c for c in contributors if c.total_bet >= level]
            pot_layer = layer_amount * len(contributors_at_level)
            # Eligible winners: active (non-folded) players who contributed at least 'level'
            eligible = [c for c in contributors_at_level if not c.folded]
            if eligible and pot_layer > 0:
                side_pots.append((pot_layer, eligible))
            prev_level = level

        # Award each side pot
        winners = []
        total_won = {}
        for pot_amount, eligible in side_pots:
            if not eligible:
                continue
            best = None
            round_winners = []
            for p in eligible:
                if best is None or p.hand_result > best:
                    best = p.hand_result
                    round_winners = [p]
                elif p.hand_result == best:
                    round_winners.append(p)
            share = pot_amount // len(round_winners)
            remainder = pot_amount % len(round_winners)
            for i, w in enumerate(round_winners):
                amount = share + (1 if i < remainder else 0)
                w.stack += amount
                total_won[w.id] = total_won.get(w.id, 0) + amount
                if w not in winners:
                    winners.append(w)

        return winners, sum(total_won.values())

    async def run(self):
        """Main game loop — runs until 1 or 0 players remain."""
        while True:
            seated = self.seated_players
            if len(seated) < 2:
                break

            self.hand_num += 1
            self.community_cards = []
            self.pot = 0
            self.current_bet = 0
            self.reset_hand_state()
            self.deck = create_deck()

            # Rotate dealer
            if self.hand_num > 1:
                self.dealer_pos = (self.dealer_pos + 1) % len(seated)

            # Post blinds
            self.post_blinds()

            # Deal hole cards
            for p in seated:
                p.hole_cards = [self.deck.pop(), self.deck.pop()]

            # Send hole cards via DM (private)
            await self.send_hole_cards_dm()

            # Pre-flop
            await self.betting_round("preflop")

            # Flop
            if len(self.active_players) > 1:
                self.community_cards = [self.deck.pop() for _ in range(3)]
                self.current_bet = 0
                for p in seated:
                    p.current_bet = 0
                    p.acted = False
                await self.betting_round("flop")

            # Turn
            if len(self.active_players) > 1:
                self.community_cards.append(self.deck.pop())
                self.current_bet = 0
                for p in seated:
                    p.current_bet = 0
                    p.acted = False
                await self.betting_round("turn")

            # River
            if len(self.active_players) > 1:
                self.community_cards.append(self.deck.pop())
                self.current_bet = 0
                for p in seated:
                    p.current_bet = 0
                    p.acted = False
                await self.betting_round("river")

            # Showdown
            if len(self.active_players) == 1:
                # Only one player left — wins without showdown
                winner = self.active_players[0]
                winner.stack += self.pot
                embed = poker_game_embed(
                    self.players, self.community_cards, self.pot,
                    None, 0, self.hand_num, "showdown", self.dealer_pos,
                )
                embed.description += f"\n\n🏆 **{winner.name}** wins {format_money(self.pot)} (everyone else folded!)"
                await self.message.edit(embed=embed, view=None)
            else:
                # Showdown — reveal all cards
                winners, total_won = self.award_pot()
                all_hands = [p for p in self.players if not p.standing]
                embed = poker_showdown_embed(
                    self.players, self.community_cards, self.pot,
                    self.hand_num, winners, all_hands,
                )
                await self.message.edit(embed=embed, view=None)

            # Process standing up and busts
            standup_view = PokerStandupView(self, timeout=6)
            try:
                await self.message.edit(embed=embed, view=standup_view)
            except discord.HTTPException:
                pass
            await standup_view.wait()

            # Return chips to standing/broke players and remove them
            for p in self.players:
                if p.standing and not p.folded:
                    pass  # Their stack is already theirs
                # Mark players with 0 stack as standing
                if p.stack <= 0 and not p.standing:
                    p.standing = True

            # Update wallets for standing players
            for p in self.players:
                if p.standing:
                    if p.stack > 0:
                        data = await db.get_or_create_user(p.id, 0)
                        await db.update_user(p.id, wallet=data["wallet"] + p.stack)
                    p.stack = 0

            # Remove standing players
            self.players = [p for p in self.players if not p.standing]

            if len(self.players) < 2:
                break

        # Game over — return remaining chips
        for p in self.players:
            if p.stack > 0:
                data = await db.get_or_create_user(p.id, 0)
                await db.update_user(p.id, wallet=data["wallet"] + p.stack)

        # Final embed
        if len(self.players) == 1:
            winner = self.players[0]
            final_embed = success_embed(
                "🃏 Poker — Game Over!",
                f"🏆 **{winner.name}** is the last player standing with {format_money(winner.stack)}!\n"
                f"Chips have been returned to your wallets.",
            )
        else:
            final_embed = info_embed(
                "🃏 Poker — Game Over!",
                "Not enough players to continue. Chips have been returned to your wallets.",
            )
        try:
            await self.message.edit(embed=final_embed, view=None)
        except discord.HTTPException:
            try:
                await self.channel.send(embed=final_embed)
            except discord.HTTPException:
                pass


# ═══════════════════════════════════════════════════════════════════════
# COG
# ═══════════════════════════════════════════════════════════════════════

class Poker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="poker", description="Start a multiplayer Texas Hold'em poker table! Up to 4 players.")
    @app_commands.choices(blind_level=[
        app_commands.Choice(name="💵 Low Blinds (10/20)", value="low"),
        app_commands.Choice(name="💰 Medium Blinds (25/50)", value="medium"),
        app_commands.Choice(name="💎 High Blinds (50/100)", value="high"),
    ])
    async def poker(self, interaction: discord.Interaction, buy_in: int, blind_level: app_commands.Choice[str] = None):
        if buy_in < 50:
            await interaction.response.send_message(
                embed=error_embed("Error", "Minimum buy-in is $50."),
                ephemeral=True,
            )
            return

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if data["wallet"] < buy_in:
            await interaction.response.send_message(
                embed=error_embed("Insufficient Funds", f"You need {format_money(buy_in)} in your wallet to host a poker table. (Bank money doesn't count!)"),
                ephemeral=True,
            )
            return

        # Deduct buy-in from host
        await db.update_user(interaction.user.id, wallet=data["wallet"] - buy_in)

        # Set blind amounts
        if blind_level and blind_level.value == "medium":
            sb, bb = 25, 50
        elif blind_level and blind_level.value == "high":
            sb, bb = 50, 100
        else:
            sb, bb = 10, 20

        # Create lobby
        lobby_view = PokerLobbyView(interaction.user.id, buy_in, timeout=60)
        lobby_view.players.append(interaction.user)

        await interaction.response.send_message(
            embed=poker_lobby_embed(lobby_view.players, buy_in, 60),
            view=lobby_view,
        )
        msg = await interaction.original_response()
        await lobby_view.wait()

        if not lobby_view.started or len(lobby_view.players) < 2:
            # Refund host
            host_data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
            await db.update_user(interaction.user.id, wallet=host_data["wallet"] + buy_in)
            await msg.edit(
                embed=error_embed("🃏 Poker — Cancelled", "Not enough players joined. Buy-in refunded."),
                view=None,
            )
            return

        # Deduct buy-in from all players (host already deducted)
        for user in lobby_view.players:
            if user.id != interaction.user.id:
                p_data = await db.get_or_create_user(user.id, interaction.guild.id if interaction.guild else 0)
                if p_data["wallet"] < buy_in:
                    # Can't afford anymore — skip them
                    lobby_view.players.remove(user)
                    continue
                await db.update_user(user.id, wallet=p_data["wallet"] - buy_in)

        if len(lobby_view.players) < 2:
            # Refund everyone
            for user in lobby_view.players:
                p_data = await db.get_or_create_user(user.id, interaction.guild.id if interaction.guild else 0)
                await db.update_user(user.id, wallet=p_data["wallet"] + buy_in)
            await msg.edit(
                embed=error_embed("🃏 Poker — Cancelled", "Not enough players could afford the buy-in. Refunds issued."),
                view=None,
            )
            return

        # Start the game
        game = PokerGame(self.bot, interaction.channel, lobby_view.players, buy_in)
        game.sb_amount = sb
        game.bb_amount = bb
        game.message = msg

        await msg.edit(
            embed=info_embed("🃏 Poker — Starting!", f"Table starting with {len(lobby_view.players)} players! Dealing hand #1...\n\n**Check your DMs for your hole cards**, or click **My Cards** during your turn."),
            view=None,
        )
        await asyncio.sleep(2)

        await game.run()

        # Award XP to all participants
        for user in lobby_view.players:
            try:
                p_data = await db.get_or_create_user(user.id, interaction.guild.id if interaction.guild else 0)
                xp_gain = random.randint(10, 25)
                new_xp = p_data["xp"] + xp_gain
                new_level, leveled_up = check_level_up(new_xp, p_data["level"])
                if leveled_up:
                    new_xp -= sum(xp_for_next_level(l) for l in range(p_data["level"], new_level))
                await db.update_user(user.id, xp=new_xp, level=new_level)
                await db.update_quest_progress(user.id, "gamble", 1)
            except Exception:
                pass


async def setup(bot):
    await bot.add_cog(Poker(bot))
