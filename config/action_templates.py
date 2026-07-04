"""Action response templates — 4+ contextual variants for every player-facing action message.
Used by utils/narrative.get_action_text() to provide varied, immersive responses.
All placeholders use {variable} syntax filled in by the calling cog."""

ACTION_TEMPLATES = {
    # ═══════════════════════════════════════════════════════════════
    # SURVIVAL
    # ═══════════════════════════════════════════════════════════════
    "survival": {
        "sleep": [
            "You took a nap and restored {restored} energy!{home_text}\n⚡ Energy: {old} → {new}",
            "You curl up and drift off. When you wake, you feel refreshed. +{restored} energy!{home_text}\n⚡ Energy: {old} → {new}",
            "A deep sleep rejuvenates your body. You gained {restored} energy!{home_text}\n⚡ Energy: {old} → {new}",
            "You rest your eyes for a while. The world fades, then returns. +{restored} energy!{home_text}\n⚡ Energy: {old} → {new}",
            "Sleep takes you like a tide. You surface feeling restored. +{restored} energy!{home_text}\n⚡ Energy: {old} → {new}",
            "You find a comfortable spot and let yourself rest. {restored} energy recovered!{home_text}\n⚡ Energy: {old} → {new}",
        ],
        "sleep_full": [
            "Your energy is already full! You feel wide awake.",
            "You're bursting with energy — no need to rest right now.",
            "You can't sleep. You're too energized already!",
            "No rest needed — you're fully charged and ready to go.",
        ],
        "shower": [
            "You took a shower and restored {restored} hygiene!{home_text}\n🧼 Hygiene: {old} → {new}",
            "Hot water cascades over you, washing away the grime. +{restored} hygiene!{home_text}\n🧼 Hygiene: {old} → {new}",
            "You step out of the shower feeling clean and refreshed. +{restored} hygiene!{home_text}\n🧼 Hygiene: {old} → {new}",
            "The warm spray works wonders. You feel like a new person. +{restored} hygiene!{home_text}\n🧼 Hygiene: {old} → {new}",
            "You scrub away the day's dirt and sweat. Much better. +{restored} hygiene!{home_text}\n🧼 Hygiene: {old} → {new}",
            "A long, hot shower does the trick. You're spotless. +{restored} hygiene!{home_text}\n🧼 Hygiene: {old} → {new}",
        ],
        "shower_full": [
            "Your hygiene is already perfect! You're sparkling clean.",
            "You're already spotless — save the water for later.",
            "No need to shower — you're fresh as a daisy.",
            "You're impeccably clean already. Nothing to wash off.",
        ],
        "heal": [
            "You used {item_name} and restored {restored} HP!\nHealth: {old} → {new}",
            "The {item_name} works quickly, knitting your wounds. +{restored} HP!\nHealth: {old} → {new}",
            "You apply the {item_name}. Relief floods through you. +{restored} HP!\nHealth: {old} → {new}",
            "{item_name} does its job. You feel steadier on your feet. +{restored} HP!\nHealth: {old} → {new}",
            "You use the {item_name} and feel the pain ebb away. +{restored} HP!\nHealth: {old} → {new}",
        ],
        "hospital_info": [
            "If your health drops to 0, you wake up at the hospital.\nYou lose **50% of your unbanked wallet money** and your stats are restored.",
            "The hospital is your safety net. Hit 0 HP and you'll wake up here — but it'll cost you half your unbanked cash.",
            "Flatline and you'll end up in the hospital. They'll patch you up, but 50% of your wallet money goes to the bill.",
            "The hospital takes care of you when you collapse. The price? Half your unbanked wallet. Bank your money to stay safe!",
        ],
        "health_warning": [
            "⚠️ Your health is critically low! Use a medkit or bandage.",
            "⚠️ You're in bad shape — health is dangerously low. Heal up!",
            "⚠️ You can barely stand. Your health is critical. Get help now!",
            "⚠️ Your body is failing. Health is at dangerous levels. Use a healing item!",
        ],
        "hunger_warning": [
            "⚠️ You're starving! Eat some food with `/use`.",
            "⚠️ Your stomach is growling painfully. You need food badly.",
            "⚠️ Hunger is eating you alive. Find something to eat with `/use`.",
            "⚠️ You're on the verge of starvation. Eat something, now!",
        ],
        "thirst_warning": [
            "⚠️ You're dehydrated! Drink something with `/use`.",
            "⚠️ Your throat is parched. You desperately need water.",
            "⚠️ Dehydration is setting in. Drink something with `/use`.",
            "⚠️ You're dizzy from thirst. Hydrate yourself immediately!",
        ],
        "energy_warning": [
            "⚠️ You're exhausted! Use `/sleep` or consume an energy item.",
            "⚠️ You can barely keep your eyes open. Get some rest!",
            "⚠️ Your energy is drained. Sleep or use an energy item.",
            "⚠️ You're running on fumes. `/sleep` or an energy drink will help.",
        ],
        "hygiene_warning": [
            "⚠️ You're filthy! Use `/shower` or buy hygiene items from `/shop`.",
            "⚠️ You smell terrible. People are starting to notice. Shower!",
            "⚠️ Hygiene is at rock bottom. Clean yourself up with `/shower`.",
            "⚠️ You're covered in grime. `/shower` or hygiene items from `/shop`.",
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # ECONOMY
    # ═══════════════════════════════════════════════════════════════
    "economy": {
        "deposit": [
            "Deposited {amount} into your bank.\nWallet: {wallet} | Bank: {bank}",
            "You slide {amount} across the counter and into your bank account.\nWallet: {wallet} | Bank: {bank}",
            "The teller counts your {amount} and stamps the deposit slip.\nWallet: {wallet} | Bank: {bank}",
            "You tuck {amount} safely into the bank. It's protected from hospital fees now.\nWallet: {wallet} | Bank: {bank}",
            "{amount} moves from your wallet to your bank. Smart move.\nWallet: {wallet} | Bank: {bank}",
        ],
        "withdraw": [
            "Withdrew {amount} from your bank.\nWallet: {wallet} | Bank: {bank}",
            "You pull {amount} out of the bank. Cash in hand again.\nWallet: {wallet} | Bank: {bank}",
            "The ATM dispenses {amount} with a satisfying whir.\nWallet: {wallet} | Bank: {bank}",
            "You withdraw {amount}. The bank balance drops, but your wallet feels heavier.\nWallet: {wallet} | Bank: {bank}",
            "{amount} transferred from bank to wallet. Spend it wisely.\nWallet: {wallet} | Bank: {bank}",
        ],
        "pay": [
            "{payer} paid {recipient} {amount}!",
            "{payer} hands {amount} to {recipient}.",
            "{amount} moves from {payer}'s wallet to {recipient}.",
            "{payer} slides {amount} across to {recipient}. Deal done.",
            "{payer} transfers {amount} to {recipient}. Smooth transaction.",
        ],
        "upgrade_bank": [
            "Your bank capacity is now {capacity}!",
            "The bank approves your upgrade. You can now store up to {capacity}.",
            "A quick paperwork shuffle and your bank limit jumps to {capacity}.",
            "Your vault expands. New capacity: {capacity}.",
            "The bank manager nods. Your new limit is {capacity}.",
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # GAMBLING
    # ═══════════════════════════════════════════════════════════════
    "gambling": {
        "coinflip_win": [
            "The coin landed on **{result}**!\nYou bet {bet} and won {winnings}!\nWallet: {wallet}",
            "The coin spins, tumbles, and lands — **{result}**! You called it right!\nYou won {winnings} on a {bet} bet!\nWallet: {wallet}",
            "**{result}**! The coin favored you today. Your {bet} bet turned into {winnings}!\nWallet: {wallet}",
            "The coin flips end over end... **{result}**! You win {winnings}!\nWallet: {wallet}",
        ],
        "coinflip_loss": [
            "The coin landed on **{result}**.\nYou lost {bet}.\nWallet: {wallet}",
            "**{result}**. Not what you hoped. Your {bet} vanishes.\nWallet: {wallet}",
            "The coin lands **{result}** — wrong side. You lose {bet}.\nWallet: {wallet}",
            "Tails or heads, it didn't matter. **{result}** means you're down {bet}.\nWallet: {wallet}",
        ],
        "dice_win": [
            "The dice rolled **{result}**!\nYou bet {bet} and won {winnings}!\nWallet: {wallet}",
            "The dice tumble across the table — **{result}**! You nailed it!\nYou won {winnings} on a {bet} bet!\nWallet: {wallet}",
            "**{result}**! Lady luck is with you. {bet} becomes {winnings}!\nWallet: {wallet}",
            "The dice land on **{result}**. A winner! You take home {winnings}!\nWallet: {wallet}",
        ],
        "dice_loss": [
            "The dice rolled **{result}**.\nYou lost {bet}.\nWallet: {wallet}",
            "**{result}**. Not your number. Your {bet} is gone.\nWallet: {wallet}",
            "The dice settle on **{result}** — wrong call. You're down {bet}.\nWallet: {wallet}",
            "You watch the dice land on **{result}**. Ouch. {bet} lost.\nWallet: {wallet}",
        ],
        "blackjack_win": [
            "{result_text}\nYou won {winnings}!\nWallet: {wallet}",
            "{result_text}\nThe dealer can't compete. You take {winnings}!\nWallet: {wallet}",
            "{result_text}\nA beautiful hand pays off — {winnings} yours!\nWallet: {wallet}",
            "{result_text}\nVictory at the table! {winnings} added to your wallet.\nWallet: {wallet}",
        ],
        "blackjack_loss": [
            "{result_text}\nYou lost {bet}.\nWallet: {wallet}",
            "{result_text}\nThe dealer takes this one. Down {bet}.\nWallet: {wallet}",
            "{result_text}\nNot your hand today. {bet} gone.\nWallet: {wallet}",
            "{result_text}\nThe house wins this round. You lose {bet}.\nWallet: {wallet}",
        ],
        "blackjack_push": [
            "{result_text}\nBet returned.",
            "{result_text}\nA draw — your money comes back.",
            "{result_text}\nNo winner, no loser. Your bet is safe.",
            "{result_text}\nStandoff at the table. Your money is returned.",
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # SOCIAL
    # ═══════════════════════════════════════════════════════════════
    "social": {
        "marry_accept": [
            "{proposer} and {recipient} are now married! 💕\n⭐ Both gained {xp} XP!",
            "The proposal was accepted! {proposer} and {recipient} are officially wed! 💕\n⭐ Both gained {xp} XP!",
            "Love wins! {proposer} and {recipient} tied the knot! 💕\n⭐ Both gained {xp} XP!",
            "They said yes! {proposer} and {recipient} are now partners for life! 💕\n⭐ Both gained {xp} XP!",
        ],
        "marry_reject": [
            "{recipient} declined the proposal.",
            "{recipient} said no. Heartbreaking.",
            "The proposal was turned down. {recipient} wasn't ready.",
            "{recipient} shook their head. It wasn't meant to be.",
        ],
        "divorce": [
            "You are no longer married to {partner}.",
            "The papers are signed. Your marriage to {partner} is over.",
            "You walk away from the marriage. {partner} is now your ex.",
            "It's done. You and {partner} are no longer together.",
        ],
        "gift_sent": [
            "You gifted {amount} to {recipient}!\n⭐ +{xp} XP",
            "You hand {amount} to {recipient}. Their face lights up.\n⭐ +{xp} XP",
            "{amount} transferred to {recipient}. A generous gift!\n⭐ +{xp} XP",
            "You slip {amount} into {recipient}'s hand. They smile gratefully.\n⭐ +{xp} XP",
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # HOUSING
    # ═══════════════════════════════════════════════════════════════
    "housing": {
        "buy": [
            "You bought {home_name} for {price}! It's yours, free and clear.\nUse `/house` to view your home, `/rest` to restore stats, `/upgrade_house` to improve it, and `/decorate` to furnish it!",
            "The keys are in your hand. {home_name} is now your property. Cost: {price}.\nUse `/house` to view your home, `/rest` to restore stats, `/upgrade_house` to improve it, and `/decorate` to furnish it!",
            "Welcome home! You've purchased {home_name} for {price}.\nUse `/house` to view your home, `/rest` to restore stats, `/upgrade_house` to improve it, and `/decorate` to furnish it!",
            "The deed is signed. {home_name} belongs to you. {price} well spent.\nUse `/house` to view your home, `/rest` to restore stats, `/upgrade_house` to improve it, and `/decorate` to furnish it!",
        ],
        "rent": [
            "You're now renting {home_name} for {price}/week.\nRent is paid for 7 days. Use `/pay_rent` to extend, `/rest` to restore stats.",
            "You signed the lease for {home_name}. Rent: {price}/week.\nRent is paid for 7 days. Use `/pay_rent` to extend, `/rest` to restore stats.",
            "Welcome to your new rental — {home_name}. Don't forget the weekly {price}!\nRent is paid for 7 days. Use `/pay_rent` to extend, `/rest` to restore stats.",
            "The landlord hands you the keys to {home_name}. Rent is {price} per week.\nRent is paid for 7 days. Use `/pay_rent` to extend, `/rest` to restore stats.",
        ],
        "pay_rent": [
            "You paid {price} rent for {home_name}. You're covered for another week.\nRent is now paid for {days} more days.",
            "Rent paid! {price} for {home_name}. You're safe for now.\nRent is now paid for {days} more days.",
            "The landlord collects {price}. {home_name} is yours for another week.\nRent is now paid for {days} more days.",
            "You slide {price} across the table. {home_name} is secured for the week.\nRent is now paid for {days} more days.",
        ],
        "sell": [
            "You sold {home_name} for {price} (50% of purchase price). The keys change hands.",
            "The sale is final. {home_name} is gone, but {price} is in your pocket.",
            "You hand over the deed to {home_name}. {price} added to your wallet.",
            "Sold! {home_name} is no longer yours. You walk away with {price}.",
        ],
        "list_market": [
            "Your {home_name} has been listed on the housing market for {price}.\nUse `/housing_market` to view listings.",
            "You put {home_name} on the market for {price}. It'll sell eventually.\nUse `/housing_market` to view listings.",
            "The listing goes up: {home_name} for {price}. Now you wait for a buyer.\nUse `/housing_market` to view listings.",
            "{home_name} is now on the housing market. Asking price: {price}.\nUse `/housing_market` to view listings.",
        ],
        "buy_market": [
            "You bought a **{home_name}** for {price} from the player market!",
            "The market deal closes. {home_name} is yours for {price}.",
            "You snatch up {home_name} from the market for {price}. Smart buy.",
            "Another player's loss is your gain. {home_name} for {price}!",
        ],
        "cancel_listing": [
            "You reclaimed your **{home_name}** from the market.",
            "The listing is pulled. {home_name} is back in your hands.",
            "You take {home_name} off the market. It's yours again.",
            "Listing cancelled. {home_name} returns to you.",
        ],
        "stop_renting": [
            "You stopped renting {home_name}. The keys go back to the landlord. All upgrades and decorations were lost.",
            "You hand in your keys. {home_name} is no longer your home. All upgrades and decorations were lost.",
            "The lease is terminated. You're free of {home_name}. All upgrades and decorations were lost.",
            "You pack up and leave {home_name}. The rental agreement is over. All upgrades and decorations were lost.",
        ],
        "evicted": [
            "You've been evicted from {home_name}! You couldn't keep up with rent.",
            "The landlord kicked you out of {home_name}. Rent was overdue.",
            "Eviction notice posted on {home_name}. You're homeless now.",
            "You return to {home_name} to find the locks changed. Evicted.",
        ],
        "decorate": [
            "You placed a **{decoration}** in your home!\n{description}",
            "{decoration} now brightens up your living space.\n{description}",
            "Your home looks better with the new {decoration}.\n{description}",
            "You place the {decoration} just right. Home sweet home.\n{description}",
        ],
        "upgrade": [
            "{upgrade_name} is now level {level}!\nCost: {cost}\n{description}",
            "The {upgrade_name} is installed — level {level}! Cost: {cost}.\n{description}",
            "Construction noise fades as {upgrade_name} reaches level {level}. Cost: {cost}.\n{description}",
            "Your home now has {upgrade_name} at level {level}. {cost} well spent.\n{description}",
        ],
        "store_item": [
            "You stored {qty}x {item_name} in your home storage.",
            "You tuck {qty}x {item_name} into your home storage. Safe and sound.",
            "{qty}x {item_name} goes into storage. Your home keeps it safe.",
            "You find room for {qty}x {item_name} in your home storage.",
        ],
        "retrieve_item": [
            "You retrieved {qty}x {item_name} from home storage.",
            "You pull {qty}x {item_name} out of storage. Back in your inventory.",
            "{qty}x {item_name} retrieved from home storage.",
            "You grab {qty}x {item_name} from your home. Good to go.",
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # STORE
    # ═══════════════════════════════════════════════════════════════
    "store": {
        "buy": [
            "You bought {qty}x {item_name} for {price}!\nWallet: {wallet}",
            "The cashier rings up {qty}x {item_name}. {price} leaves your wallet.\nWallet: {wallet}",
            "You walk out with {qty}x {item_name}. Cost: {price}.\nWallet: {wallet}",
            "Purchase complete — {qty}x {item_name} for {price}.\nWallet: {wallet}",
            "You bag your new {item_name}{qty_label}. {price} well spent.\nWallet: {wallet}",
        ],
        "buy_collectible": [
            "You bought {item_name} for {price}!\nView it in /collectibles",
            "A fine addition to your collection. {item_name} — {price}.\nView it in /collectibles",
            "You acquire {item_name} for {price}. A true collector's piece.\nView it in /collectibles",
            "{item_name} is now yours for {price}. Display it proudly!\nView it in /collectibles",
        ],
        "sell": [
            "You sold {qty}x {item_name} for {price} (50% refund).\nWallet: {wallet}",
            "You part with {qty}x {item_name}. {price} back in your pocket.\nWallet: {wallet}",
            "The buyback counter gives you {price} for {qty}x {item_name}.\nWallet: {wallet}",
            "Sold: {qty}x {item_name} for {price}. Half price, but better than nothing.\nWallet: {wallet}",
        ],
        "use_item": [
            "You used {item_name}.\n{effects}",
            "You consume the {item_name}. You feel the effects immediately.\n{effects}",
            "The {item_name} is gone, but its effects linger.\n{effects}",
            "You put the {item_name} to good use.\n{effects}",
        ],
        "buy_tool": [
            "You bought a {quality_emoji} **{quality_name}** {item_name} for {price}!\nDurability: {durability} | {description}\nUse `/equip` to equip it, then use activities like `/fish`, `/mine`, `/chop`, `/dig`!",
            "The shopkeeper hands you a {quality_emoji} **{quality_name}** {item_name}. {price} well spent.\nDurability: {durability} | {description}\nUse `/equip` to equip it!",
            "You walk out with a {quality_emoji} **{quality_name}** {item_name}. Not bad for {price}.\nDurability: {durability} | {description}\nUse `/equip` to equip it!",
            "A fine {quality_emoji} **{quality_name}** {item_name} joins your toolkit. Cost: {price}.\nDurability: {durability} | {description}\nUse `/equip` to equip it!",
        ],
        "buy_clothing": [
            "You bought {quality_emoji} **{quality_name}** {item_name} for {price}!\nSlot: {slot} | Warmth: {warmth} | {stats} | {prot}\nUse `/equip` to wear it!",
            "You try on the {quality_emoji} **{quality_name}** {item_name}. Perfect fit. Cost: {price}.\nSlot: {slot} | Warmth: {warmth} | {stats} | {prot}\nUse `/equip` to wear it!",
            "New threads! A {quality_emoji} **{quality_name}** {item_name} for {price}.\nSlot: {slot} | Warmth: {warmth} | {stats} | {prot}\nUse `/equip` to wear it!",
            "The {quality_emoji} **{quality_name}** {item_name} looks great on you. {price} gone.\nSlot: {slot} | Warmth: {warmth} | {stats} | {prot}\nUse `/equip` to wear it!",
        ],
        "buy_possession": [
            "You bought {quality_emoji} **{quality_name}** {item_name} for {price}!\nBonuses: {stats} | {description}\nUse `/equip` to activate its passive bonuses!",
            "A {quality_emoji} **{quality_name}** {item_name} now belongs to you. Cost: {price}.\nBonuses: {stats} | {description}\nUse `/equip` to activate its passive bonuses!",
            "You acquire a {quality_emoji} **{quality_name}** {item_name} for {price}. A wise investment.\nBonuses: {stats} | {description}\nUse `/equip` to activate its passive bonuses!",
            "The {quality_emoji} **{quality_name}** {item_name} is yours. {price} well spent.\nBonuses: {stats} | {description}\nUse `/equip` to activate its passive bonuses!",
        ],
        "sell_equipment": [
            "You sold {quality_emoji} {quality_name} {item_name} for {price}.",
            "You part with your {quality_emoji} {quality_name} {item_name}. {price} in return.",
            "The buyer takes your {quality_emoji} {quality_name} {item_name} for {price}.",
            "Sold: {quality_emoji} {quality_name} {item_name} — {price} added to your wallet.",
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # PETS
    # ═══════════════════════════════════════════════════════════════
    "pets": {
        "adopt": [
            "Welcome {emoji} {pet_name} to your family!\nUse `/pet_feed`, `/pet_play`, and `/pet_battle` to take care of your pet!",
            "You bring {emoji} {pet_name} home. A new companion!\nUse `/pet_feed`, `/pet_play`, and `/pet_battle` to take care of your pet!",
            "{emoji} {pet_name} looks up at you with adoring eyes. You're a pet parent now!\nUse `/pet_feed`, `/pet_play`, and `/pet_battle` to take care of your pet!",
            "The adoption papers are signed. {emoji} {pet_name} is officially yours!\nUse `/pet_feed`, `/pet_play`, and `/pet_battle` to take care of your pet!",
        ],
        "feed": [
            "Your pet's hunger restored! -{cost}",
            "{pet_name} devours the food happily. Hunger restored! -{cost}",
            "You set down the bowl. {pet_name} eats eagerly. -{cost}",
            "{pet_name} licks the bowl clean. Much better! -{cost}",
            "Your pet chows down with enthusiasm. Hunger satisfied! -{cost}",
        ],
        "play": [
            "Happiness +20!\nPet XP +{xp}",
            "You toss a toy and {pet_name} bounds after it. Happiness +20!\nPet XP +{xp}",
            "{pet_name} wags and plays. The joy is infectious. Happiness +20!\nPet XP +{xp}",
            "You and {pet_name} roughhouse and play. Good times! Happiness +20!\nPet XP +{xp}",
            "{pet_name} chases and pounces, full of energy. Happiness +20!\nPet XP +{xp}",
        ],
        "battle_win": [
            "Your {pet_name} defeated {opponent}'s {opponent_pet}!\nReward: {reward}\n⭐ +{xp} XP",
            "{pet_name} fights bravely and triumphs over {opponent}'s {opponent_pet}!\nReward: {reward}\n⭐ +{xp} XP",
            "A fierce battle, but {pet_name} comes out on top against {opponent_pet}!\nReward: {reward}\n⭐ +{xp} XP",
            "{pet_name} outmaneuvers {opponent}'s {opponent_pet} for the win!\nReward: {reward}\n⭐ +{xp} XP",
        ],
        "battle_loss": [
            "Your {pet_name} lost to {opponent}'s {opponent_pet}!\nPet Health: -{hp_loss}",
            "{pet_name} fought hard but couldn't beat {opponent_pet}. Defeat.\nPet Health: -{hp_loss}",
            "It wasn't enough. {pet_name} falls to {opponent}'s {opponent_pet}.\nPet Health: -{hp_loss}",
            "{opponent}'s {opponent_pet} was too strong. Your {pet_name} retreats, injured.\nPet Health: -{hp_loss}",
        ],
        "abandon": [
            "Your pet has been released. You can adopt a new one with `/adopt`.",
            "You say goodbye to your pet. They scamper off into the distance. Use `/adopt` for a new one.",
            "With a heavy heart, you release your pet. `/adopt` if you want a new companion.",
            "Your pet looks back once, then disappears. You're pet-free now. `/adopt` to start over.",
        ],
        "pet_levelup": [
            "Pet is now level {level}!",
            "Your pet grew stronger! Level {level} reached!",
            "{pet_name} levels up! Now at level {level}!",
            "Your pet is getting more powerful — level {level}!",
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # CRIME
    # ═══════════════════════════════════════════════════════════════
    "crime": {
        "success": [
            "You got away with {reward}!\nHealth: -5 (from the adrenaline)",
            "You slip into the shadows, {reward} richer. Your heart races.\nHealth: -5",
            "Clean getaway. {reward} in your pocket before anyone noticed.\nHealth: -5",
            "You make it out with {reward}. The thrill courses through you.\nHealth: -5",
            "Flawless. You pocket {reward} and vanish before the alarm.\nHealth: -5",
        ],
        "caught": [
            "You got caught!\nFine: {fine}\nHealth: -{hp_loss} (from the chase)",
            "Sirens. Flashing lights. You're pinned. Fine: {fine}\nHealth: -{hp_loss}",
            "Busted! They were waiting for you. Fine: {fine}\nHealth: -{hp_loss}",
            "You almost made it, but a tackle brings you down. Fine: {fine}\nHealth: -{hp_loss}",
            "Caught red-handed. The cuffs click on. Fine: {fine}\nHealth: -{hp_loss}",
        ],
        "rob_success": [
            "You stole {amount} from {victim}!",
            "You lift {amount} from {victim}'s wallet. Smooth work.",
            "{victim} doesn't even notice. You pocket {amount} and walk away.",
            "Quick fingers, quick escape. {amount} taken from {victim}.",
            "You bump into {victim} and come away {amount} richer. They never felt a thing.",
        ],
        "rob_fail": [
            "You got caught trying to rob {victim}!\nFine: {fine}\nHealth: -{hp_loss}",
            "{victim} catches your hand in their pocket! Fine: {fine}\nHealth: -{hp_loss}",
            "Your reach was too slow. {victim} grabs your wrist. Fine: {fine}\nHealth: -{hp_loss}",
            "Amateur move. {victim} spots you immediately. Fine: {fine}\nHealth: -{hp_loss}",
        ],
        "warrant": [
            "The police have issued a warrant for your arrest! Be careful during activities — they're coming for you.",
            "Your face is on the bulletin board. There's an active warrant out for you!",
            "The cops have your number. A warrant has been issued. Watch your back.",
            "WARRANT ISSUED: You're a wanted criminal now. Every activity carries risk.",
        ],
        "heat_warning": [
            "Police are taking an interest in you. They may start watching your activities.",
            "You've caught the police's attention. They're watching you now.",
            "Heat is building. The cops have you on their radar.",
            "You feel eyes on your back. The police are tracking your movements.",
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # IMMERSION (npc trade, npc quest, cook)
    # ═══════════════════════════════════════════════════════════════
    "immersion": {
        "npc_trade": [
            "{npc_name} hands you the goods with a nod.\n\nTraded: {give_qty}x {give_name} → {recv_qty}x {recv_name}\n🏪 +1 Merchant Guild reputation",
            "The exchange is quick and quiet. {npc_name} slides over {recv_qty}x {recv_name}.\n\nTraded: {give_qty}x {give_name} → {recv_qty}x {recv_name}\n🏪 +1 Merchant Guild reputation",
            "{npc_name} inspects the goods, then nods approvingly. A fair trade.\n\nTraded: {give_qty}x {give_name} → {recv_qty}x {recv_name}\n🏪 +1 Merchant Guild reputation",
            "Business done. {npc_name} wraps up your {recv_qty}x {recv_name} and hands it over.\n\nTraded: {give_qty}x {give_name} → {recv_qty}x {recv_name}\n🏪 +1 Merchant Guild reputation",
        ],
        "npc_quest_accept": [
            "**{npc_name}** explains what they need.\n\n📋 **Objective:** {quest_desc}\n💰 **Reward:** {reward} + {xp} XP\n\nComplete the objective, then come back with `/npc_complete {npc_id}`!",
            "**{npc_name}** pulls you aside and whispers a request.\n\n📋 **Objective:** {quest_desc}\n💰 **Reward:** {reward} + {xp} XP\n\nComplete the objective, then come back with `/npc_complete {npc_id}`!",
            "**{npc_name}** leans in with a serious look.\n\n📋 **Objective:** {quest_desc}\n💰 **Reward:** {reward} + {xp} XP\n\nComplete the objective, then come back with `/npc_complete {npc_id}`!",
            "**{npc_name}** has a task for you.\n\n📋 **Objective:** {quest_desc}\n💰 **Reward:** {reward} + {xp} XP\n\nComplete the objective, then come back with `/npc_complete {npc_id}`!",
        ],
        "npc_quest_complete": [
            "**{npc_name}** is thrilled!\n\n📜 {quest_desc}\n💰 +{reward}\n⭐ +{xp} XP\n🏆 +5 {faction_name} reputation",
            "**{npc_name}** can't stop smiling. You came through!\n\n📜 {quest_desc}\n💰 +{reward}\n⭐ +{xp} XP\n🏆 +5 {faction_name} reputation",
            "**{npc_name}** shakes your hand firmly. A job well done.\n\n📜 {quest_desc}\n💰 +{reward}\n⭐ +{xp} XP\n🏆 +5 {faction_name} reputation",
            "**{npc_name}** pays up with a grateful nod.\n\n📜 {quest_desc}\n💰 +{reward}\n⭐ +{xp} XP\n🏆 +5 {faction_name} reputation",
        ],
        "cook": [
            "{cooking_text}\n\nYou made {quality_emoji} {quality_name} {recipe_name}!{buff_text}",
            "{cooking_text}\n\nThe {recipe_name} is ready — {quality_emoji} {quality_name} quality!{buff_text}",
            "{cooking_text}\n\nYou plate up a {quality_emoji} {quality_name} {recipe_name}.{buff_text}",
            "{cooking_text}\n\nA {quality_emoji} {quality_name} {recipe_name} — smells amazing!{buff_text}",
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # ACTIVITIES (craft, forage, etc.)
    # ═══════════════════════════════════════════════════════════════
    "activities": {
        "craft": [
            "You crafted {quality_emoji} {quality_name} {item_name}!\n{description}",
            "Your hands move with practiced skill. A {quality_emoji} {quality_name} {item_name} takes shape!\n{description}",
            "The materials transform under your work. {quality_emoji} {quality_name} {item_name} — done!\n{description}",
            "You finish the project: a {quality_emoji} {quality_name} {item_name}. Not bad at all.\n{description}",
            "Crafting complete! You hold up your new {quality_emoji} {quality_name} {item_name}.\n{description}",
        ],
        "forage_success": [
            "You found {quality_emoji} {quality_name} {item_name}!",
            "Your search pays off — {quality_emoji} {quality_name} {item_name}!",
            "Tucked away in the undergrowth: {quality_emoji} {quality_name} {item_name}!",
            "You spot it just in time. {quality_emoji} {quality_name} {item_name} is yours.",
        ],
        "forage_nothing": [
            "You search the area but don't find anything useful.",
            "You comb through the bushes but come up empty-handed.",
            "Nothing worth taking here. Maybe next time.",
            "The area is picked clean. You'll need to try elsewhere.",
        ],
        "chop_success": [
            "You chopped {qty}x 🪵 Wood!\nQuality: {quality_emoji} {quality_name}",
            "The axe bites deep. {qty}x 🪵 Wood falls to the ground!\nQuality: {quality_emoji} {quality_name}",
            "Timber! You've got {qty}x 🪵 Wood.\nQuality: {quality_emoji} {quality_name}",
            "Another log for the pile — {qty}x 🪵 Wood.\nQuality: {quality_emoji} {quality_name}",
        ],
        "dig_success": [
            "You dug up {amount}!\nQuality: {quality_emoji} {quality_name}",
            "The shovel strikes something. You pull out {amount}!\nQuality: {quality_emoji} {quality_name}",
            "Buried treasure? Close enough — {amount}!\nQuality: {quality_emoji} {quality_name}",
            "You unearth a small cache worth {amount}.\nQuality: {quality_emoji} {quality_name}",
        ],
        "dig_nothing": [
            "You dig a hole but find nothing but dirt.",
            "Just dirt and worms. Nothing valuable here.",
            "The shovel hits nothing interesting. Another empty hole.",
            "You fill the hole back in. A wasted effort.",
        ],
        "equip": [
            "You equipped {quality_emoji} {quality_name} {item_name}!",
            "You strap on your {quality_emoji} {quality_name} {item_name}. Ready to go.",
            "The {item_name} is now equipped. {quality_emoji} {quality_name} quality.",
            "You gear up with your {quality_emoji} {quality_name} {item_name}.",
        ],
        "unequip": [
            "You unequipped {item_name}.",
            "You take off your {item_name} and stow it away.",
            "The {item_name} goes back into your bag.",
            "You remove your {item_name}. Unequipped.",
        ],
    },

    # ═══════════════════════════════════════════════════════════════
    # MISC (level up, daily, weekly, job, weather)
    # ═══════════════════════════════════════════════════════════════
    "misc": {
        "levelup": [
            "Level {level}!",
            "You've reached level {level}!",
            "A new milestone — level {level}!",
            "You feel stronger. Level {level} achieved!",
            "The world opens up a little more. Level {level}!",
        ],
        "daily": [
            "You received {amount}!",
            "Your daily reward lands in your wallet: {amount}!",
            "The reward system deposits {amount}. Another day, another payout.",
            "You claim your daily {amount}. The streak continues!",
            "{amount} added to your wallet. See you tomorrow!",
        ],
        "weekly": [
            "You received {amount}!\n⭐ +{xp} XP",
            "Your weekly reward: {amount}! A solid payout for a week's wait.\n⭐ +{xp} XP",
            "The weekly bonus hits your account: {amount}.\n⭐ +{xp} XP",
            "A week's patience pays off — {amount} is yours!\n⭐ +{xp} XP",
        ],
        "job_set": [
            "You are now a {job_name}! Use `/work` to start earning.",
            "New gig! You're officially a {job_name}. Time to get to work.",
            "You accept the position of {job_name}. `/work` when you're ready.",
            "Congratulations on the new role — {job_name}! Use `/work` to earn.",
        ],
        "job_quit": [
            "You quit your job. Use `/jobs` to find a new one.",
            "You hand in your notice. You're a free agent now. `/jobs` to browse.",
            "The badge goes back. You're unemployed. `/jobs` for new opportunities.",
            "You walk out the door. No more shifts — for now. `/jobs` when you're ready.",
        ],
        "work_success": [
            "You earned {amount} working as a {job_name}!",
            "Another shift in the books. {amount} for your time as a {job_name}.",
            "The paycheck hits: {amount} from your {job_name} gig.",
            "You wipe the sweat off your brow. {amount} earned as a {job_name}.",
        ],
        "achievement_unlocked": [
            "{emoji} **{name}** — +{reward}!",
            "Achievement: {emoji} **{name}**! Reward: {reward}!",
            "You've earned {emoji} **{name}**! Bonus: {reward}!",
            "Milestone reached: {emoji} **{name}** — {reward} added!",
        ],
        "quest_claimed": [
            "Claimed {count} quest(s)!\n💰 {reward}\n⭐ +{xp} XP",
            "Quest rewards collected: {count} completed! {reward} and {xp} XP earned.",
            "You turn in {count} completed quest(s). {reward} + {xp} XP — nice haul!",
            "The quest giver pays up: {count} quest(s) for {reward} and {xp} XP!",
        ],
        "quest_refresh": [
            "You have 3 new daily quests! Use `/quests` to view them.",
            "New quests posted on the board! Check `/quests` to see what's available.",
            "Three fresh quests await! Use `/quests` to check them out.",
            "The quest board updates. 3 new tasks are yours. `/quests` to view.",
        ],
    },
}
