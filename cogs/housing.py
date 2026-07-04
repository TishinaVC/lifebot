import discord
from discord import app_commands
from discord.ext import commands, tasks
import random
from datetime import datetime, timezone, timedelta
import database as db
from utils.embeds import success_embed, error_embed, info_embed, format_money
from utils.helpers import clamp
from utils.narrative import get_action_text
from config import (
    HOUSING_TIERS, HOME_UPGRADES, HOME_DECORATIONS,
    ENERGY_MAX, HYGIENE_MAX, HEALTH_MAX, HUNGER_MAX, THIRST_MAX,
    RENT_INTERVAL, STORE_ITEMS,
)


async def _store_item_autocomplete(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    matches = [
        app_commands.Choice(name=v["name"], value=k)
        for k, v in STORE_ITEMS.items()
        if current.lower() in v["name"].lower() or current.lower() in k.lower()
    ]
    return matches[:25]


class Housing(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.rent_loop.start()

    def cog_unload(self):
        self.rent_loop.cancel()

    # ─── Helper: compute home bonuses ───
    def _compute_home_bonuses(self, home_data: dict, upgrades: dict) -> dict:
        tier = HOUSING_TIERS.get(home_data["tier_id"], {})
        bonus = dict(tier.get("stats_bonus", {"energy": 0, "hygiene": 0, "health": 0}))
        bonus["hunger"] = 0

        upgrade_effects = {
            "kitchen": "hunger",
            "bathroom": "hygiene",
            "bedroom": "energy",
            "garden": "health",
            "gym": "health",
        }
        upgrade_amounts = {
            "kitchen": 5,
            "bathroom": 10,
            "bedroom": 10,
            "garden": 5,
            "gym": 3,
        }
        for upg_id, level in upgrades.items():
            if upg_id in upgrade_effects and level > 0:
                eff = upgrade_effects[upg_id]
                amt = upgrade_amounts[upg_id]
                bonus[eff] = bonus.get(eff, 0) + amt * level

        return bonus

    def _compute_storage(self, home_data: dict, upgrades: dict) -> int:
        tier = HOUSING_TIERS.get(home_data["tier_id"], {})
        storage = tier.get("storage", 0)
        extra_room_lvl = upgrades.get("extra_room", 0)
        storage += extra_room_lvl * 10
        return storage

    def _compute_rent(self, home_data: dict, upgrades: dict) -> int:
        tier = HOUSING_TIERS.get(home_data["tier_id"], {})
        rent = tier.get("rent", 0)
        solar_lvl = upgrades.get("solar_panels", 0)
        rent = int(rent * (1 - solar_lvl * 0.2))
        return max(0, rent)

    # ─── /house ───
    @app_commands.command(name="house", description="View your home, upgrades, decorations, and storage")
    async def house(self, interaction: discord.Interaction):
        home = await db.get_home(interaction.user.id)
        if not home:
            await interaction.response.send_message(
                embed=error_embed("No Home", "You don't have a home yet! Use `/buy_house` or `/rent_house` to get one."),
                ephemeral=True,
            )
            return

        tier = HOUSING_TIERS.get(home["tier_id"], {})
        upgrades = await db.get_upgrades(interaction.user.id)
        decorations = await db.get_decorations(interaction.user.id)
        bonuses = self._compute_home_bonuses(home, upgrades)
        storage_cap = self._compute_storage(home, upgrades)
        rent = self._compute_rent(home, upgrades)

        ownership_emoji = "🏠 Owned" if home["ownership"] == "owned" else "🔑 Rented"
        embed = info_embed(f"{tier.get('name', 'Home')} — {ownership_emoji}", f"Tier {tier.get('tier', 1)} housing")

        embed.add_field(name="📊 Rest Bonuses", value=(
            f"⚡ Energy: +{bonuses.get('energy', 0)}\n"
            f"🧼 Hygiene: +{bonuses.get('hygiene', 0)}\n"
            f"❤️ Health: +{bonuses.get('health', 0)}\n"
            f"🍖 Hunger: +{bonuses.get('hunger', 0)}"
        ), inline=True)

        embed.add_field(name="📦 Storage", value=f"{storage_cap} slots", inline=True)

        if home["ownership"] == "rented":
            rent_due = rent
            embed.add_field(name="🔑 Weekly Rent", value=format_money(rent_due), inline=True)
            if home.get("rent_paid_until"):
                rpu = datetime.fromisoformat(home["rent_paid_until"])
                now = datetime.now(timezone.utc)
                days_left = (rpu - now).days
                if days_left < 0:
                    embed.add_field(name="⚠️ Rent Overdue!", value=f"Pay rent with `/pay_rent` or you'll lose your home!", inline=False)
                else:
                    embed.add_field(name="📅 Rent Paid Until", value=f"{days_left} days remaining", inline=False)

        embed.add_field(name="✨ Advantage", value=tier.get("advantage", "None"), inline=False)
        if tier.get("disadvantage") and "None" not in tier.get("disadvantage", ""):
            embed.add_field(name="⚠️ Disadvantage", value=tier.get("disadvantage"), inline=False)

        if upgrades:
            upg_text = "\n".join(f"{HOME_UPGRADES[uid]['name']} Lv.{lvl}" for uid, lvl in upgrades.items() if lvl > 0)
            if upg_text:
                embed.add_field(name="🔧 Upgrades", value=upg_text, inline=False)

        if decorations:
            dec_text = " ".join(HOME_DECORATIONS.get(d, {}).get("emoji", "?") for d in decorations)
            embed.add_field(name="🎨 Decorations", value=dec_text or "None", inline=False)

        await interaction.response.send_message(embed=embed)

    # ─── /housing_list ───
    @app_commands.command(name="housing_list", description="Browse all 20 housing tiers")
    async def housing_list(self, interaction: discord.Interaction):
        embed = info_embed("🏠 Housing Tiers", "All 20 housing tiers from tent to sky mansion!")
        for tier_id, tier in HOUSING_TIERS.items():
            price_text = f"Buy: {format_money(tier['buy_price'])}"
            if tier["rent"] > 0:
                price_text += f" | Rent: {format_money(tier['rent'])}/wk"
            bonus = tier["stats_bonus"]
            bonus_text = f"⚡+{bonus['energy']} 🧼+{bonus['hygiene']} ❤️+{bonus['health']}"
            embed.add_field(
                name=f"T{tier['tier']} {tier['name']} — {price_text}",
                value=f"📦 {tier['storage']} storage | Rest: {bonus_text}\n✨ {tier['advantage']}",
                inline=False,
            )
        await interaction.response.send_message(embed=embed)

    # ─── /buy_house ───
    @app_commands.command(name="buy_house", description="Buy a house outright")
    @app_commands.choices(tier=[
        app_commands.Choice(name=f"T{t['tier']} {t['name']} ({t['buy_price']} coins)", value=tid)
        for tid, t in HOUSING_TIERS.items()
    ])
    async def buy_house(self, interaction: discord.Interaction, tier: app_commands.Choice[str]):
        tier_id = tier.value
        tier_data = HOUSING_TIERS.get(tier_id)
        if not tier_data:
            await interaction.response.send_message(embed=error_embed("Error", "Invalid housing tier."), ephemeral=True)
            return

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        price = tier_data["buy_price"]

        if data["wallet"] + data["bank"] < price:
            await interaction.response.send_message(
                embed=error_embed("Insufficient Funds", f"You need {format_money(price)} but only have {format_money(data['wallet'] + data['bank'])}."),
                ephemeral=True,
            )
            return

        existing = await db.get_home(interaction.user.id)
        if existing:
            if existing["ownership"] == "owned":
                await interaction.response.send_message(
                    embed=error_embed("Already Own", "You already own a home! Sell it first with `/sell_house`."),
                    ephemeral=True,
                )
                return
            else:
                await interaction.response.send_message(
                    embed=error_embed("Already Renting", "You're already renting a home! Stop renting first with `/stop_renting`."),
                    ephemeral=True,
                )
                return

        if data["wallet"] >= price:
            new_wallet = data["wallet"] - price
            await db.update_user(interaction.user.id, wallet=new_wallet, total_spent=data["total_spent"] + price)
        else:
            remaining = price - data["wallet"]
            new_wallet = 0
            new_bank = data["bank"] - remaining
            await db.update_user(interaction.user.id, wallet=new_wallet, bank=new_bank, total_spent=data["total_spent"] + price)

        await db.set_home(interaction.user.id, tier_id, ownership="owned")
        await db.add_transaction(interaction.user.id, "buy_house", price, f"Bought {tier_data['name']}")

        embed = success_embed(
            f"🏠 Home Purchased!",
            get_action_text("housing", "buy", home_name=tier_data['name'], price=format_money(price)),
        )
        await interaction.response.send_message(embed=embed)

    # ─── /rent_house ───
    @app_commands.command(name="rent_house", description="Rent a house (pay weekly rent)")
    @app_commands.choices(tier=[
        app_commands.Choice(name=f"T{t['tier']} {t['name']} ({t['rent']}/wk)", value=tid)
        for tid, t in HOUSING_TIERS.items() if t["rent"] > 0
    ])
    async def rent_house(self, interaction: discord.Interaction, tier: app_commands.Choice[str]):
        tier_id = tier.value
        tier_data = HOUSING_TIERS.get(tier_id)
        if not tier_data or tier_data["rent"] <= 0:
            await interaction.response.send_message(embed=error_embed("Error", "This property can't be rented."), ephemeral=True)
            return

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        rent = tier_data["rent"]

        if data["wallet"] < rent:
            await interaction.response.send_message(
                embed=error_embed("Insufficient Funds", f"You need {format_money(rent)} for the first week's rent."),
                ephemeral=True,
            )
            return

        existing = await db.get_home(interaction.user.id)
        if existing:
            if existing["ownership"] == "owned":
                await interaction.response.send_message(
                    embed=error_embed("Already Own", "You already own a home! Sell it first with `/sell_house`."),
                    ephemeral=True,
                )
                return
            else:
                await interaction.response.send_message(
                    embed=error_embed("Already Renting", "You're already renting a home! Stop renting first with `/stop_renting`."),
                    ephemeral=True,
                )
                return

        rent_paid_until = (datetime.now(timezone.utc) + timedelta(seconds=RENT_INTERVAL)).isoformat()
        await db.update_user(interaction.user.id, wallet=data["wallet"] - rent, total_spent=data["total_spent"] + rent)
        await db.set_home(interaction.user.id, tier_id, ownership="rented", rent_paid_until=rent_paid_until)
        await db.add_transaction(interaction.user.id, "rent_house", rent, f"Rented {tier_data['name']} (1 week)")

        embed = success_embed(
            f"🔑 Home Rented!",
            get_action_text("housing", "rent", home_name=tier_data['name'], price=format_money(rent)),
        )
        await interaction.response.send_message(embed=embed)

    # ─── /pay_rent ───
    @app_commands.command(name="pay_rent", description="Pay another week of rent")
    async def pay_rent(self, interaction: discord.Interaction):
        home = await db.get_home(interaction.user.id)
        if not home or home["ownership"] != "rented":
            await interaction.response.send_message(embed=error_embed("No Rental", "You don't have a rented home."), ephemeral=True)
            return

        tier_data = HOUSING_TIERS.get(home["tier_id"], {})
        upgrades = await db.get_upgrades(interaction.user.id)
        rent = self._compute_rent(home, upgrades)

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if data["wallet"] < rent:
            await interaction.response.send_message(
                embed=error_embed("Insufficient Funds", f"You need {format_money(rent)} for rent."),
                ephemeral=True,
            )
            return

        now = datetime.now(timezone.utc)
        current_until = datetime.fromisoformat(home["rent_paid_until"]) if home.get("rent_paid_until") else now
        if current_until > now:
            new_until = current_until + timedelta(seconds=RENT_INTERVAL)
        else:
            new_until = now + timedelta(seconds=RENT_INTERVAL)

        await db.update_user(interaction.user.id, wallet=data["wallet"] - rent, total_spent=data["total_spent"] + rent)
        await db.update_home(interaction.user.id, rent_paid_until=new_until.isoformat())
        await db.add_transaction(interaction.user.id, "rent", rent, f"Paid rent for {tier_data.get('name', 'home')}")

        days = (new_until - now).days
        await interaction.response.send_message(
            embed=success_embed("🔑 Rent Paid!", get_action_text("housing", "pay_rent", home_name=tier_data.get('name', 'home'), price=format_money(rent), days=days)),
        )

    # ─── /sell_house ───
    @app_commands.command(name="sell_house", description="Sell your owned home (50% refund) or list it on the market")
    async def sell_house(self, interaction: discord.Interaction, list_on_market: bool = False):
        home = await db.get_home(interaction.user.id)
        if not home:
            await interaction.response.send_message(embed=error_embed("No Home", "You don't have a home to sell."), ephemeral=True)
            return

        if home["ownership"] != "owned":
            await interaction.response.send_message(embed=error_embed("Not Owned", "You can only sell homes you own. Use `/stop_renting` to end a rental."), ephemeral=True)
            return

        tier_data = HOUSING_TIERS.get(home["tier_id"], {})
        refund = tier_data["buy_price"] // 2

        if list_on_market:
            price = tier_data["buy_price"]
            await db.create_market_listing(interaction.user.id, home["tier_id"], price)
            await db.remove_home(interaction.user.id)
            await interaction.response.send_message(
                embed=success_embed("📋 Listed on Market", get_action_text("housing", "list_market", home_name=tier_data['name'], price=format_money(price))),
            )
        else:
            data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
            await db.update_user(interaction.user.id, wallet=data["wallet"] + refund, total_earned=data["total_earned"] + refund)
            await db.remove_home(interaction.user.id)
            await db.add_transaction(interaction.user.id, "sell_house", refund, f"Sold {tier_data['name']} (50% refund)")
            await interaction.response.send_message(
                embed=success_embed("💰 Home Sold", get_action_text("housing", "sell", home_name=tier_data['name'], price=format_money(refund))),
            )

    # ─── /stop_renting ───
    @app_commands.command(name="stop_renting", description="Stop renting your current home")
    async def stop_renting(self, interaction: discord.Interaction):
        home = await db.get_home(interaction.user.id)
        if not home or home["ownership"] != "rented":
            await interaction.response.send_message(embed=error_embed("No Rental", "You don't have a rented home."), ephemeral=True)
            return
        tier_data = HOUSING_TIERS.get(home["tier_id"], {})
        await db.remove_home(interaction.user.id)
        await interaction.response.send_message(
            embed=info_embed("🔑 Rental Ended", get_action_text("housing", "stop_renting", home_name=tier_data.get('name', 'home'))),
        )

    # ─── /rest ───
    @app_commands.command(name="rest", description="Rest at home to restore stats (uses housing bonuses)")
    async def rest(self, interaction: discord.Interaction):
        home = await db.get_home(interaction.user.id)
        if not home:
            await interaction.response.send_message(embed=error_embed("No Home", "You need a home to rest! Buy or rent one first."), ephemeral=True)
            return

        cd = await db.check_cooldown(interaction.user.id, "rest")
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"You rested recently. Try again in {mins}m {secs}s."), ephemeral=True)
            return

        tier_data = HOUSING_TIERS.get(home["tier_id"], {})
        upgrades = await db.get_upgrades(interaction.user.id)
        bonuses = self._compute_home_bonuses(home, upgrades)
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        energy_gain = bonuses.get("energy", 0)
        hygiene_gain = bonuses.get("hygiene", 0)
        health_gain = bonuses.get("health", 0)
        hunger_gain = bonuses.get("hunger", 0)

        new_energy = clamp(data.get("energy", 100) + energy_gain, 0, ENERGY_MAX)
        new_hygiene = clamp(data.get("hygiene", 100) + hygiene_gain, 0, HYGIENE_MAX)
        new_health = clamp(data["health"] + health_gain, 0, HEALTH_MAX)
        new_hunger = clamp(data["hunger"] + hunger_gain, 0, HUNGER_MAX)

        await db.update_user(interaction.user.id, energy=new_energy, hygiene=new_hygiene, health=new_health, hunger=new_hunger)
        await db.update_home(interaction.user.id, last_rest=datetime.now(timezone.utc).isoformat())
        await db.set_cooldown(interaction.user.id, "rest", 3600)

        effects = []
        if energy_gain != 0:
            effects.append(f"⚡ Energy: {data.get('energy', 100)} → {new_energy}")
        if hygiene_gain != 0:
            effects.append(f"🧼 Hygiene: {data.get('hygiene', 100)} → {new_hygiene}")
        if health_gain != 0:
            effects.append(f"❤️ Health: {data['health']} → {new_health}")
        if hunger_gain != 0:
            effects.append(f"🍖 Hunger: {data['hunger']} → {new_hunger}")

        embed = success_embed(f"😴 Rested at {tier_data.get('name', 'Home')}", "\n".join(effects) if effects else "You feel refreshed!")

        if random.random() < 0.15 and "None" not in tier_data.get("disadvantage", "None"):
            embed.add_field(name="⚠️ Event", value=tier_data.get("disadvantage", ""), inline=False)
        elif random.random() < 0.20:
            embed.add_field(name="✨ Bonus", value=tier_data.get("advantage", ""), inline=False)

        await interaction.response.send_message(embed=embed)

    # ─── /upgrade_house ───
    @app_commands.command(name="upgrade_house", description="Upgrade your home with improvements")
    @app_commands.choices(upgrade=[
        app_commands.Choice(name=f"{u['name']} — {u['description']}", value=uid)
        for uid, u in HOME_UPGRADES.items()
    ])
    async def upgrade_house(self, interaction: discord.Interaction, upgrade: app_commands.Choice[str]):
        home = await db.get_home(interaction.user.id)
        if not home:
            await interaction.response.send_message(embed=error_embed("No Home", "You need a home first!"), ephemeral=True)
            return

        upg_id = upgrade.value
        upg_data = HOME_UPGRADES.get(upg_id)
        if not upg_data:
            await interaction.response.send_message(embed=error_embed("Error", "Invalid upgrade."), ephemeral=True)
            return

        upgrades = await db.get_upgrades(interaction.user.id)
        current_level = upgrades.get(upg_id, 0)
        if current_level >= upg_data["max_level"]:
            await interaction.response.send_message(embed=error_embed("Max Level", f"{upg_data['name']} is already at max level!"), ephemeral=True)
            return

        cost = int(upg_data["price"] * (upg_data["price_mult"] ** current_level))
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        if data["wallet"] < cost:
            await interaction.response.send_message(
                embed=error_embed("Insufficient Funds", f"You need {format_money(cost)} for this upgrade."),
                ephemeral=True,
            )
            return

        await db.update_user(interaction.user.id, wallet=data["wallet"] - cost, total_spent=data["total_spent"] + cost)
        await db.set_upgrade_level(interaction.user.id, upg_id, current_level + 1)
        await db.add_transaction(interaction.user.id, "upgrade", cost, f"{upg_data['name']} Lv.{current_level + 1}")

        await interaction.response.send_message(
            embed=success_embed(
                f"🔧 Upgraded!",
                get_action_text("housing", "upgrade", upgrade_name=upg_data['name'], level=current_level + 1, cost=format_money(cost), description=upg_data['description']),
            ),
        )

    # ─── /decorate ───
    @app_commands.command(name="decorate", description="Buy a decoration for your home")
    @app_commands.choices(decoration=[
        app_commands.Choice(name=f"{d['emoji']} {d['name']} ({d['price']} coins)", value=did)
        for did, d in HOME_DECORATIONS.items()
    ])
    async def decorate(self, interaction: discord.Interaction, decoration: app_commands.Choice[str]):
        home = await db.get_home(interaction.user.id)
        if not home:
            await interaction.response.send_message(embed=error_embed("No Home", "You need a home first!"), ephemeral=True)
            return

        dec_id = decoration.value
        dec_data = HOME_DECORATIONS.get(dec_id)
        if not dec_data:
            await interaction.response.send_message(embed=error_embed("Error", "Invalid decoration."), ephemeral=True)
            return

        existing = await db.get_decorations(interaction.user.id)
        if dec_id in existing:
            await interaction.response.send_message(embed=error_embed("Already Owned", "You already have this decoration!"), ephemeral=True)
            return

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if data["wallet"] < dec_data["price"]:
            await interaction.response.send_message(
                embed=error_embed("Insufficient Funds", f"You need {format_money(dec_data['price'])}."),
                ephemeral=True,
            )
            return

        await db.update_user(interaction.user.id, wallet=data["wallet"] - dec_data["price"], total_spent=data["total_spent"] + dec_data["price"])
        await db.add_decoration(interaction.user.id, dec_id)
        await db.add_transaction(interaction.user.id, "decorate", dec_data["price"], f"Bought {dec_data['name']}")

        await interaction.response.send_message(
            embed=success_embed(f"{dec_data['emoji']} Decoration Added!", get_action_text("housing", "decorate", decoration=dec_data['name'], description=dec_data['description'])),
        )

    # ─── /housing_market ───
    @app_commands.command(name="housing_market", description="Browse player-listed homes for sale")
    async def housing_market(self, interaction: discord.Interaction):
        listings = await db.list_market_listings()
        if not listings:
            await interaction.response.send_message(embed=info_embed("📋 Housing Market", "No homes are currently listed for sale."), ephemeral=True)
            return

        embed = info_embed("📋 Housing Market", "Homes listed by players. Use `/buy_from_market` to purchase.")
        for listing in listings[:10]:
            tier = HOUSING_TIERS.get(listing["tier_id"], {})
            seller = self.bot.get_user(listing["seller_id"])
            seller_name = seller.display_name if seller else f"User {listing['seller_id']}"
            embed.add_field(
                name=f"{tier.get('name', 'Unknown')} — {format_money(listing['price'])}",
                value=f"Seller: {seller_name}\nListing ID: {listing['id']}\n`/buy_from_market id:{listing['id']}`",
                inline=False,
            )
        await interaction.response.send_message(embed=embed)

    # ─── /buy_from_market ───
    @app_commands.command(name="buy_from_market", description="Buy a home from the player housing market")
    async def buy_from_market(self, interaction: discord.Interaction, listing_id: int):
        listings = await db.list_market_listings()
        listing = next((l for l in listings if l["id"] == listing_id), None)
        if not listing:
            await interaction.response.send_message(embed=error_embed("Not Found", "That listing doesn't exist or is already sold."), ephemeral=True)
            return

        if listing["seller_id"] == interaction.user.id:
            await interaction.response.send_message(embed=error_embed("Your Listing", "You can't buy your own listing. Use `/cancel_listing` to remove it."), ephemeral=True)
            return

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if data["wallet"] + data["bank"] < listing["price"]:
            await interaction.response.send_message(
                embed=error_embed("Insufficient Funds", f"You need {format_money(listing['price'])}."),
                ephemeral=True,
            )
            return

        existing = await db.get_home(interaction.user.id)
        if existing:
            await interaction.response.send_message(
                embed=error_embed("Already Have Home", "Sell or stop renting your current home first."),
                ephemeral=True,
            )
            return

        if data["wallet"] >= listing["price"]:
            new_wallet = data["wallet"] - listing["price"]
            await db.update_user(interaction.user.id, wallet=new_wallet, total_spent=data["total_spent"] + listing["price"])
        else:
            remaining = listing["price"] - data["wallet"]
            await db.update_user(interaction.user.id, wallet=0, bank=data["bank"] - remaining, total_spent=data["total_spent"] + listing["price"])

        await db.mark_market_sold(listing["id"])
        await db.set_home(interaction.user.id, listing["tier_id"], ownership="owned")

        seller_data = await db.get_or_create_user(listing["seller_id"], 0)
        if seller_data:
            await db.update_user(listing["seller_id"], wallet=seller_data["wallet"] + listing["price"], total_earned=seller_data["total_earned"] + listing["price"])
            await db.add_transaction(listing["seller_id"], "sell_house_market", listing["price"], f"Sold {HOUSING_TIERS.get(listing['tier_id'], {}).get('name', 'home')} on market")

        await db.add_transaction(interaction.user.id, "buy_house_market", listing["price"], f"Bought from market: {HOUSING_TIERS.get(listing['tier_id'], {}).get('name', 'home')}")

        tier_name = HOUSING_TIERS.get(listing["tier_id"], {}).get("name", "Home")
        await interaction.response.send_message(
            embed=success_embed("🏠 Purchased from Market!", get_action_text("housing", "buy_market", home_name=tier_name, price=format_money(listing['price']))),
        )

    # ─── /cancel_listing ───
    @app_commands.command(name="cancel_listing", description="Cancel your housing market listing and reclaim the home")
    async def cancel_listing(self, interaction: discord.Interaction, listing_id: int):
        listings = await db.list_market_listings()
        listing = next((l for l in listings if l["id"] == listing_id), None)
        if not listing or listing["seller_id"] != interaction.user.id:
            await interaction.response.send_message(embed=error_embed("Not Yours", "You don't have a listing with that ID."), ephemeral=True)
            return

        existing = await db.get_home(interaction.user.id)
        if existing:
            await interaction.response.send_message(embed=error_embed("Have Home", "You already have a home. Sell or stop renting first."), ephemeral=True)
            return

        await db.cancel_market_listing(listing["id"])
        await db.set_home(interaction.user.id, listing["tier_id"], ownership="owned")
        tier_name = HOUSING_TIERS.get(listing["tier_id"], {}).get("name", "Home")
        await interaction.response.send_message(
            embed=success_embed("📋 Listing Cancelled", get_action_text("housing", "cancel_listing", home_name=tier_name)),
        )

    # ─── /store_item ───
    async def _do_store_item(self, interaction: discord.Interaction, item_id: str, quantity: int = 1):
        home = await db.get_home(interaction.user.id)
        if not home:
            await interaction.response.send_message(embed=error_embed("No Home", "You need a home to store items."), ephemeral=True)
            return

        if quantity < 1:
            await interaction.response.send_message(embed=error_embed("Error", "Quantity must be at least 1."), ephemeral=True)
            return

        inv = await db.get_inventory(interaction.user.id)
        if item_id not in inv or inv[item_id] < quantity:
            await interaction.response.send_message(embed=error_embed("Not Enough", f"You don't have {quantity} of that item."), ephemeral=True)
            return

        upgrades = await db.get_upgrades(interaction.user.id)
        storage_cap = self._compute_storage(home, upgrades)
        stored = await db.get_home_storage(interaction.user.id)
        current_stored = sum(stored.values())
        if current_stored + quantity > storage_cap:
            space_left = storage_cap - current_stored
            await interaction.response.send_message(
                embed=error_embed("Storage Full", f"Your home storage only has {space_left} slots left."),
                ephemeral=True,
            )
            return

        await db.remove_from_inventory(interaction.user.id, item_id, quantity)
        await db.add_to_home_storage(interaction.user.id, item_id, quantity)
        await interaction.response.send_message(
            embed=success_embed("📦 Stored", get_action_text("housing", "store_item", qty=quantity, item_name=STORE_ITEMS.get(item_id, {}).get("name", item_id))),
        )

    @app_commands.command(name="store_item", description="Store an item from your inventory into your home storage")
    @app_commands.autocomplete(item=_store_item_autocomplete)
    async def store_item(self, interaction: discord.Interaction, item: str, quantity: int = 1):
        await self._do_store_item(interaction, item, quantity)

    # ─── /retrieve_item ───
    @app_commands.command(name="retrieve_item", description="Retrieve an item from your home storage")
    async def retrieve_item(self, interaction: discord.Interaction, item_id: str, quantity: int = 1):
        if quantity < 1:
            await interaction.response.send_message(embed=error_embed("Error", "Quantity must be at least 1."), ephemeral=True)
            return
        home = await db.get_home(interaction.user.id)
        if not home:
            await interaction.response.send_message(embed=error_embed("No Home", "You don't have a home."), ephemeral=True)
            return

        stored = await db.get_home_storage(interaction.user.id)
        if item_id not in stored or stored[item_id] < quantity:
            await interaction.response.send_message(embed=error_embed("Not Enough", f"You don't have {quantity} of that item in storage."), ephemeral=True)
            return

        await db.remove_from_home_storage(interaction.user.id, item_id, quantity)
        await db.add_to_inventory(interaction.user.id, item_id, quantity)
        from config import STORE_ITEMS
        name = STORE_ITEMS.get(item_id, {}).get("name", item_id)
        await interaction.response.send_message(
            embed=success_embed("📦 Retrieved", get_action_text("housing", "retrieve_item", qty=quantity, item_name=name)),
        )

    # ─── /home_storage ───
    @app_commands.command(name="home_storage", description="View items stored in your home")
    async def home_storage(self, interaction: discord.Interaction):
        home = await db.get_home(interaction.user.id)
        if not home:
            await interaction.response.send_message(embed=error_embed("No Home", "You don't have a home."), ephemeral=True)
            return

        stored = await db.get_home_storage(interaction.user.id)
        upgrades = await db.get_upgrades(interaction.user.id)
        storage_cap = self._compute_storage(home, upgrades)
        from config import STORE_ITEMS

        embed = info_embed("📦 Home Storage", f"{sum(stored.values())}/{storage_cap} slots used")
        if not stored:
            embed.add_field(name="Empty", value="No items stored. Use `/store_item` to put items in your home.", inline=False)
        else:
            for item_id, qty in stored.items():
                name = STORE_ITEMS.get(item_id, {}).get("name", item_id)
                embed.add_field(name=name, value=f"x{qty}", inline=True)
        await interaction.response.send_message(embed=embed)

    # ─── Rent collection loop ───
    @tasks.loop(seconds=3600)
    async def rent_loop(self):
        dbobj = await db.get_db()
        now = datetime.now(timezone.utc)
        async with dbobj.execute("SELECT user_id, tier_id, rent_paid_until FROM player_homes WHERE ownership = 'rented'") as cur:
            rows = await cur.fetchall()
        for row in rows:
            rpu_str = row["rent_paid_until"]
            if not rpu_str:
                continue
            rpu = datetime.fromisoformat(rpu_str)
            if rpu < now:
                uid = row["user_id"]
                tier = HOUSING_TIERS.get(row["tier_id"], {})
                await db.remove_home(uid)
                await db.add_transaction(uid, "evicted", 0, f"Evicted from {tier.get('name', 'home')} — rent overdue")

    @rent_loop.before_loop
    async def before_rent_loop(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Housing(bot))
