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
        self.stop()

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.danger, emoji="✋")
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("Not your game!", ephemeral=True)
            return
        self.action = "stand"
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

        while True:
            view = BlackjackView(interaction.user.id, timeout=30)
            msg = await interaction.original_response()
            await msg.edit(view=view)
            await view.wait()

            if view.action == "hit":
                player_hand.append(draw_card())
                pv = hand_value(player_hand)
                if pv > 21:
                    break
                await msg.edit(embed=self._bj_embed(player_hand, dealer_hand, f"Your hand: {pv}. Hit or Stand?", False), view=view)
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
                await db.update_user(interaction.user.id, games_played=data["games_played"] + 1, xp=new_xp, level=new_level)
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
                await interaction.followup.send(embed=push_embed)
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
        await interaction.followup.send(embed=embed)

    def _bj_display(self, player, dealer, reveal=False):
        dealer_str = " ".join(dealer) if reveal else f"{dealer[0]} ❓"
        return f"**Dealer**: {dealer_str} ({hand_value(dealer) if reveal else '?'})\n**You**: {' '.join(player)} ({hand_value(player)})"

    def _bj_embed(self, player, dealer, title, reveal=False):
        display = self._bj_display(player, dealer, reveal)
        return info_embed(f"🃏 Blackjack", f"{display}\n\n{title}")

    @app_commands.command(name="roulette", description="Play roulette — bet on red, black, green, or a specific number!")
    @app_commands.choices(bet_type=[
        app_commands.Choice(name="🔴 Red", value="red"),
        app_commands.Choice(name="⚫ Black", value="black"),
        app_commands.Choice(name="🟢 Green (0)", value="green"),
        app_commands.Choice(name="🔢 Specific Number (0-36)", value="number"),
    ])
    async def roulette(self, interaction: discord.Interaction, amount: int, bet_type: app_commands.Choice[str], number: int = -1):
        if bet_type.value == "number" and (number < 0 or number > 36):
            await interaction.response.send_message(embed=error_embed("Error", "Pick a number between 0 and 36."), ephemeral=True)
            return
        data, _, mods = await self._gamble_common(interaction, amount)
        if data is None:
            return

        result_num = random.randint(0, 36)
        if result_num in ROULETTE_COLORS["green"]:
            color = "green"
        elif result_num in ROULETTE_COLORS["red"]:
            color = "red"
        else:
            color = "black"

        color_emoji = {"red": "🔴", "black": "⚫", "green": "🟢"}[color]

        if bet_type.value == "number":
            won = result_num == number
            multiplier = 36.0
        elif bet_type.value == "green":
            won = color == "green"
            multiplier = 14.0
        else:
            won = color == bet_type.value
            multiplier = 2.0

        new_wallet, leveled_up, new_level, xp_gain, new_achievements = await self._gamble_result(
            interaction.user.id, data, won, amount, "Roulette", multiplier=multiplier if won else 0, mods=mods
        )

        if won:
            winnings = int(amount * multiplier)
            embed = money_embed("🎡 Roulette — You Won!", f"The ball landed on **{color_emoji} {result_num}**!\nYou won {format_money(winnings)}!\nWallet: {format_money(new_wallet)}")
        else:
            embed = error_embed("🎡 Roulette — You Lost!", f"The ball landed on **{color_emoji} {result_num}**.\nYou lost {format_money(amount)}.\nWallet: {format_money(new_wallet)}")
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Gambling(bot))
