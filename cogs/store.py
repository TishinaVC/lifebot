import discord
from discord import app_commands
from discord.ext import commands
import random
import database as db
import world
from utils.embeds import success_embed, error_embed, info_embed, format_money
from utils.helpers import clamp, check_level_up, xp_for_next_level
from utils.narrative import get_action_text
from utils.quality import roll_quality, quality_name, quality_emoji, quality_multiplier
from config import (
    STORE_ITEMS, TOOLS, CLOTHING, POSSESSIONS, RAW_MATERIALS, CRAFTING_RECIPES,
    HEALTH_MAX, HUNGER_MAX, THIRST_MAX, ACHIEVEMENTS,
    STORE_CATALOG, MYSTERY_BOX, DAILY_DEAL, FLASH_SALE, LUCKY_DIP, TRAVELER_PACK,
)
from config.store_catalog import (
    get_daily_deal_item, get_flash_sale_category, get_flash_sale_discount,
    get_mystery_box_item, get_lucky_dip_item,
)


# ─── Helpers ───

def _resolve_item(item_id, source):
    if source == "store_items":
        return STORE_ITEMS.get(item_id)
    elif source == "tools":
        return TOOLS.get(item_id)
    elif source == "clothing":
        return CLOTHING.get(item_id)
    elif source == "possessions":
        return POSSESSIONS.get(item_id)
    return None


def _item_effects(item_data):
    effects = []
    if item_data.get("hunger", 0) != 0:
        effects.append(f"\U0001F356 {item_data['hunger']:+d}")
    if item_data.get("thirst", 0) != 0:
        effects.append(f"\U0001F4A7 {item_data['thirst']:+d}")
    if item_data.get("health", 0) != 0:
        effects.append(f"\u2764\uFE0F {item_data['health']:+d}")
    if item_data.get("energy", 0) != 0:
        effects.append(f"\u26A1 {item_data['energy']:+d}")
    if item_data.get("hygiene", 0) != 0:
        effects.append(f"\U0001F9F9 {item_data['hygiene']:+d}")
    if item_data.get("effect"):
        effects.append(f"\u2728 {item_data['effect']}")
    if item_data.get("stat"):
        effects.append(f"\U0001F4CA {item_data['stat'].title()} +{item_data['boost']}")
    return effects


async def _item_autocomplete(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    """Autocomplete for store items by name. Searches all STORE_ITEMS."""
    matches = []
    for item_id, item in STORE_ITEMS.items():
        if current.lower() in item["name"].lower() or current.lower() in item_id.lower():
            matches.append(app_commands.Choice(name=f"{item['name']} ({item['price']} coins)", value=item_id))
    return matches[:25]


async def _tool_autocomplete(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    matches = []
    for tid, t in TOOLS.items():
        if current.lower() in t["name"].lower() or current.lower() in tid.lower():
            matches.append(app_commands.Choice(name=f"{t['name']} ({t['price']} coins)", value=tid))
    return matches[:25]


async def _clothing_autocomplete(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    matches = []
    for cid, c in CLOTHING.items():
        if current.lower() in c["name"].lower() or current.lower() in cid.lower():
            matches.append(app_commands.Choice(name=f"{c['name']} ({c['price']} coins)", value=cid))
    return matches[:25]


async def _possession_autocomplete(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    matches = []
    for pid, p in POSSESSIONS.items():
        if current.lower() in p["name"].lower() or current.lower() in pid.lower():
            matches.append(app_commands.Choice(name=f"{p['name']} ({p['price']} coins)", value=pid))
    return matches[:25]


_USABLE_CATEGORIES = ["food", "drink", "medical", "booster", "hygiene", "stat_booster"]
_ALL_CATEGORIES = _USABLE_CATEGORIES + ["collectible"]


async def _usable_item_autocomplete(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    matches = []
    for item_id, item in STORE_ITEMS.items():
        if item.get("type") in _USABLE_CATEGORIES and (current.lower() in item["name"].lower() or current.lower() in item_id.lower()):
            matches.append(app_commands.Choice(name=f"{item['name']} ({item['price']} coins)", value=item_id))
    return matches[:25]


async def _equipment_autocomplete(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    matches = []
    for tid, t in TOOLS.items():
        if current.lower() in t["name"].lower() or current.lower() in tid.lower():
            matches.append(app_commands.Choice(name=f"\U0001F527 {t['name']} ({t['price']} coins)", value=f"tool:{tid}"))
    for cid, c in CLOTHING.items():
        if current.lower() in c["name"].lower() or current.lower() in cid.lower():
            matches.append(app_commands.Choice(name=f"\U0001F455 {c['name']} ({c['price']} coins)", value=f"clothing:{cid}"))
    for pid, p in POSSESSIONS.items():
        if current.lower() in p["name"].lower() or current.lower() in pid.lower():
            matches.append(app_commands.Choice(name=f"\U0001F4E6 {p['name']} ({p['price']} coins)", value=f"possession:{pid}"))
    return matches[:25]

ITEMS_PER_PAGE = 10


# ─── Views ───

class CategoryView(discord.ui.View):
    def __init__(self, cog, user_id):
        super().__init__(timeout=180)
        self.cog = cog
        self.user_id = user_id
        for cat_id, cat_data in STORE_CATALOG.items():
            btn = discord.ui.Button(
                label=cat_data["name"], emoji=cat_data["emoji"],
                style=discord.ButtonStyle.primary, custom_id=f"shop_cat_{cat_id}",
            )
            btn.callback = self._make_cat_callback(cat_id)
            self.add_item(btn)
        deals_btn = discord.ui.Button(
            label="Special Deals", emoji="\U0001F525",
            style=discord.ButtonStyle.danger, custom_id="shop_deals",
        )
        deals_btn.callback = self._deals_callback
        self.add_item(deals_btn)

    def _make_cat_callback(self, cat_id):
        async def callback(interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your shop session!", ephemeral=True)
                return
            cat = STORE_CATALOG[cat_id]
            view = SubcategoryView(self.cog, self.user_id, cat_id)
            embed = discord.Embed(
                title=f"{cat['emoji']} {cat['name']}",
                description="Select a subcategory to browse items:",
                color=cat.get("color", 0x3498DB),
            )
            await interaction.response.edit_message(embed=embed, view=view)
        return callback

    async def _deals_callback(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your shop session!", ephemeral=True)
            return
        view = DealsView(self.cog, self.user_id)
        await interaction.response.edit_message(embed=view.build_embed(), view=view)


class SubcategoryView(discord.ui.View):
    def __init__(self, cog, user_id, cat_id):
        super().__init__(timeout=180)
        self.cog = cog
        self.user_id = user_id
        self.cat_id = cat_id
        cat = STORE_CATALOG[cat_id]
        for sub_id, sub_data in cat["subcategories"].items():
            btn = discord.ui.Button(
                label=sub_data["name"], emoji=sub_data["emoji"],
                style=discord.ButtonStyle.secondary, custom_id=f"shop_sub_{cat_id}_{sub_id}",
            )
            btn.callback = self._make_sub_callback(sub_id)
            self.add_item(btn)
        back_btn = discord.ui.Button(
            label="Back to Categories", emoji="\u2B05\uFE0F",
            style=discord.ButtonStyle.danger, custom_id="shop_back_cat",
        )
        back_btn.callback = self._back_callback
        self.add_item(back_btn)

    def _make_sub_callback(self, sub_id):
        async def callback(interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your shop session!", ephemeral=True)
                return
            view = ItemListView(self.cog, self.user_id, self.cat_id, sub_id, 0)
            await interaction.response.edit_message(embed=view.build_embed(), view=view)
        return callback

    async def _back_callback(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your shop session!", ephemeral=True)
            return
        await _send_main_menu(interaction, self.cog, self.user_id)


class ItemListView(discord.ui.View):
    def __init__(self, cog, user_id, cat_id, sub_id, page=0):
        super().__init__(timeout=180)
        self.cog = cog
        self.user_id = user_id
        self.cat_id = cat_id
        self.sub_id = sub_id
        self.page = page
        cat = STORE_CATALOG[cat_id]
        sub = cat["subcategories"][sub_id]
        item_ids = sub["item_ids"]
        source = cat["source"]
        total_pages = max(1, (len(item_ids) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
        start = page * ITEMS_PER_PAGE
        page_items = item_ids[start:start + ITEMS_PER_PAGE]
        for item_id in page_items:
            item_data = _resolve_item(item_id, source)
            if not item_data:
                continue
            price = item_data["price"]
            flash_cat = get_flash_sale_category()
            if flash_cat == cat_id:
                price = int(price * get_flash_sale_discount())
            btn = discord.ui.Button(
                label=f"{item_data['name']} \u2014 {format_money(price)}",
                style=discord.ButtonStyle.success,
                custom_id=f"shop_item_{cat_id}_{sub_id}_{item_id}",
            )
            btn.callback = self._make_item_callback(item_id, source)
            self.add_item(btn)
        if page > 0:
            prev_btn = discord.ui.Button(label="Previous", emoji="\u25C0\uFE0F", style=discord.ButtonStyle.primary, custom_id="shop_prev")
            prev_btn.callback = self._prev_callback
            self.add_item(prev_btn)
        if page < total_pages - 1:
            next_btn = discord.ui.Button(label="Next", emoji="\u25B6\uFE0F", style=discord.ButtonStyle.primary, custom_id="shop_next")
            next_btn.callback = self._next_callback
            self.add_item(next_btn)
        back_btn = discord.ui.Button(
            label=f"Back to {cat['name']}", emoji="\u2B05\uFE0F",
            style=discord.ButtonStyle.danger, custom_id="shop_back_sub",
        )
        back_btn.callback = self._back_callback
        self.add_item(back_btn)

    def _make_item_callback(self, item_id, source):
        async def callback(interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your shop session!", ephemeral=True)
                return
            view = ItemDetailView(self.cog, self.user_id, self.cat_id, self.sub_id, item_id, source, self.page)
            await interaction.response.edit_message(embed=view.build_embed(), view=view)
        return callback

    async def _prev_callback(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your shop session!", ephemeral=True)
            return
        new_view = ItemListView(self.cog, self.user_id, self.cat_id, self.sub_id, self.page - 1)
        await interaction.response.edit_message(embed=new_view.build_embed(), view=new_view)

    async def _next_callback(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your shop session!", ephemeral=True)
            return
        new_view = ItemListView(self.cog, self.user_id, self.cat_id, self.sub_id, self.page + 1)
        await interaction.response.edit_message(embed=new_view.build_embed(), view=new_view)

    async def _back_callback(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your shop session!", ephemeral=True)
            return
        cat = STORE_CATALOG[self.cat_id]
        view = SubcategoryView(self.cog, self.user_id, self.cat_id)
        embed = discord.Embed(
            title=f"{cat['emoji']} {cat['name']}",
            description="Select a subcategory to browse items:",
            color=cat.get("color", 0x3498DB),
        )
        await interaction.response.edit_message(embed=embed, view=view)

    def build_embed(self):
        cat = STORE_CATALOG[self.cat_id]
        sub = cat["subcategories"][self.sub_id]
        item_ids = sub["item_ids"]
        source = cat["source"]
        total_pages = max(1, (len(item_ids) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)
        start = self.page * ITEMS_PER_PAGE
        page_items = item_ids[start:start + ITEMS_PER_PAGE]
        embed = discord.Embed(
            title=f"{sub['emoji']} {sub['name']}",
            description=f"Page {self.page + 1}/{total_pages} \u2014 Click an item to view details and buy.",
            color=cat.get("color", 0x3498DB),
        )
        flash_cat = get_flash_sale_category()
        if flash_cat == self.cat_id:
            embed.add_field(name="\U0001F525 Flash Sale Active!", value=f"All items in this category are **{FLASH_SALE['discount_percent']}% OFF**!", inline=False)
        for item_id in page_items:
            item_data = _resolve_item(item_id, source)
            if not item_data:
                continue
            effects = _item_effects(item_data)
            price = item_data["price"]
            if flash_cat == self.cat_id:
                discounted = int(price * get_flash_sale_discount())
                price_text = f"~~{format_money(price)}~~ **{format_money(discounted)}**"
            else:
                price_text = format_money(price)
            extra = ""
            if source == "tools":
                extra = f" | Durability: {item_data.get('durability', '?')}"
            elif source == "clothing":
                stats = item_data.get("stats", {})
                stat_text = ", ".join(f"{k} +{v}" for k, v in stats.items()) if stats else "No bonuses"
                extra = f" | Slot: {item_data.get('slot', '?')} | {stat_text}"
            elif source == "possessions":
                stats = item_data.get("stats", {})
                stat_text = ", ".join(f"{k} +{v}" for k, v in stats.items()) if stats else "No bonuses"
                extra = f" | {stat_text}"
            embed.add_field(
                name=f"{item_data['name']} \u2014 {price_text}",
                value=f"{' | '.join(effects) if effects else 'No effects'}{extra}",
                inline=False,
            )
        return embed


class ItemDetailView(discord.ui.View):
    def __init__(self, cog, user_id, cat_id, sub_id, item_id, source, page=0):
        super().__init__(timeout=180)
        self.cog = cog
        self.user_id = user_id
        self.cat_id = cat_id
        self.sub_id = sub_id
        self.item_id = item_id
        self.source = source
        self.page = page
        buy1 = discord.ui.Button(label="Buy 1x", emoji="\U0001F6D2", style=discord.ButtonStyle.success, custom_id="shop_buy1")
        buy1.callback = self._make_buy_callback(1)
        self.add_item(buy1)
        buy5 = discord.ui.Button(label="Buy 5x", emoji="\U0001F4E6", style=discord.ButtonStyle.success, custom_id="shop_buy5")
        buy5.callback = self._make_buy_callback(5)
        self.add_item(buy5)
        buy10 = discord.ui.Button(label="Buy 10x", emoji="\U0001F4E6", style=discord.ButtonStyle.success, custom_id="shop_buy10")
        buy10.callback = self._make_buy_callback(10)
        self.add_item(buy10)
        back_btn = discord.ui.Button(label="Back to Items", emoji="\u2B05\uFE0F", style=discord.ButtonStyle.danger, custom_id="shop_back_items")
        back_btn.callback = self._back_callback
        self.add_item(back_btn)

    def _make_buy_callback(self, qty):
        async def callback(interaction):
            if interaction.user.id != self.user_id:
                await interaction.response.send_message("This isn't your shop session!", ephemeral=True)
                return
            await self._do_button_buy(interaction, qty)
        return callback

    async def _do_button_buy(self, interaction, quantity):
        item_data = _resolve_item(self.item_id, self.source)
        if not item_data:
            await interaction.response.send_message(embed=error_embed("Error", "Item not found."), ephemeral=True)
            return
        price = item_data["price"]
        flash_cat = get_flash_sale_category()
        if flash_cat == self.cat_id:
            price = int(price * get_flash_sale_discount())
        total_cost = price * quantity
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if data["wallet"] < total_cost:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You need {format_money(total_cost)} but only have {format_money(data['wallet'])}."), ephemeral=True)
            return
        if self.source == "store_items":
            if item_data["type"] == "collectible":
                already = await db.get_collectibles(interaction.user.id)
                if any(c["item_id"] == self.item_id for c in already):
                    await interaction.response.send_message(embed=error_embed("Already Owned", "You already own this collectible!"), ephemeral=True)
                    return
                await db.update_user(interaction.user.id, wallet=data["wallet"] - total_cost, total_spent=data["total_spent"] + total_cost, items_bought=data["items_bought"] + 1)
                await db.add_collectible(interaction.user.id, self.item_id)
                await db.add_transaction(interaction.user.id, "buy_collectible", total_cost, f"Bought collectible {item_data['name']}")
                await db.update_quest_progress(interaction.user.id, "buy", 1)
                xp_gain = 10
                new_xp = data["xp"] + xp_gain
                new_level, leveled_up = check_level_up(new_xp, data["level"])
                if leveled_up:
                    new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))
                    await db.update_user(interaction.user.id, xp=new_xp, level=new_level)
                else:
                    await db.update_user(interaction.user.id, xp=new_xp)
                embed = success_embed("\U0001F48E Collectible Acquired!", get_action_text("store", "buy_collectible", item_name=item_data['name'], price=format_money(total_cost)))
                if leveled_up:
                    embed.add_field(name="\U0001F389 Level Up!", value=f"Level {new_level}!", inline=False)
                new_achievements = await db.check_achievements(interaction.user.id)
                for ach_id in new_achievements:
                    ach = ACHIEVEMENTS[ach_id]
                    embed.add_field(name="\U0001F3C6 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** \u2014 +{format_money(ach['reward'])}!", inline=False)
                if new_achievements:
                    ach_reward = sum(ACHIEVEMENTS[a]["reward"] for a in new_achievements)
                    await db.update_user(interaction.user.id, wallet=data["wallet"] - total_cost + ach_reward, total_earned=data["total_earned"] + ach_reward)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            await db.update_user(interaction.user.id, wallet=data["wallet"] - total_cost, total_spent=data["total_spent"] + total_cost, items_bought=data["items_bought"] + quantity)
            await db.add_to_inventory(interaction.user.id, self.item_id, quantity)
            await db.add_transaction(interaction.user.id, "buy", total_cost, f"Bought {quantity}x {item_data['name']}")
            await db.update_quest_progress(interaction.user.id, "buy", quantity)
            await world.perturb_market(interaction.user.id, demand_delta=0.02 * quantity)
            xp_gain = 5 * quantity
            new_xp = data["xp"] + xp_gain
            new_level, leveled_up = check_level_up(new_xp, data["level"])
            if leveled_up:
                new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))
                await db.update_user(interaction.user.id, xp=new_xp, level=new_level)
            else:
                await db.update_user(interaction.user.id, xp=new_xp)
            embed = success_embed("\U0001F6D2 Purchase Complete", get_action_text("store", "buy", qty=quantity, item_name=item_data['name'], price=format_money(total_cost), wallet=format_money(data['wallet'] - total_cost), qty_label=f" ({quantity}x)" if quantity > 1 else ""))
            if leveled_up:
                embed.add_field(name="\U0001F389 Level Up!", value=f"Level {new_level}!", inline=False)
            new_achievements = await db.check_achievements(interaction.user.id)
            for ach_id in new_achievements:
                ach = ACHIEVEMENTS[ach_id]
                embed.add_field(name="\U0001F3C6 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** \u2014 +{format_money(ach['reward'])}!", inline=False)
            if new_achievements:
                ach_reward = sum(ACHIEVEMENTS[a]["reward"] for a in new_achievements)
                await db.update_user(interaction.user.id, wallet=data["wallet"] - total_cost + ach_reward, total_earned=data["total_earned"] + ach_reward)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.source == "tools":
            quality = roll_quality()
            await db.update_user(interaction.user.id, wallet=data["wallet"] - price, total_spent=data["total_spent"] + price)
            await db.add_equipment(interaction.user.id, self.item_id, "tool", quality, item_data["durability"], item_data["durability"])
            await db.record_discovery(interaction.user.id, self.item_id, quality, "shop")
            await db.add_transaction(interaction.user.id, "buy_tool", price, f"Bought {quality_name(quality)} {item_data['name']}")
            embed = success_embed("\U0001F527 Tool Purchased!", get_action_text("store", "buy_tool", quality_emoji=quality_emoji(quality), quality_name=quality_name(quality), item_name=item_data['name'], price=format_money(price), durability=item_data['durability'], description=item_data['description']))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.source == "clothing":
            quality = roll_quality()
            await db.update_user(interaction.user.id, wallet=data["wallet"] - price, total_spent=data["total_spent"] + price)
            await db.add_equipment(interaction.user.id, self.item_id, "clothing", quality, 100, 100)
            await db.record_discovery(interaction.user.id, self.item_id, quality, "shop")
            await db.add_transaction(interaction.user.id, "buy_clothing", price, f"Bought {quality_name(quality)} {item_data['name']}")
            stats_text = ", ".join(f"{k} +{int(v * quality_multiplier(quality))}" for k, v in item_data.get("stats", {}).items()) if item_data.get("stats") else "No stat bonuses"
            prot_text = f"Weather protection: {', '.join(item_data['weather_prot'])}" if item_data.get("weather_prot") else "No weather protection"
            embed = success_embed("\U0001F455 Clothing Purchased!", get_action_text("store", "buy_clothing", quality_emoji=quality_emoji(quality), quality_name=quality_name(quality), item_name=item_data['name'], price=format_money(price), slot=item_data['slot'], warmth=item_data['warmth'], stats=stats_text, prot=prot_text))
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.source == "possessions":
            quality = roll_quality()
            await db.update_user(interaction.user.id, wallet=data["wallet"] - price, total_spent=data["total_spent"] + price)
            await db.add_equipment(interaction.user.id, self.item_id, "possession", quality, 999, 999)
            await db.record_discovery(interaction.user.id, self.item_id, quality, "shop")
            await db.add_transaction(interaction.user.id, "buy_possession", price, f"Bought {quality_name(quality)} {item_data['name']}")
            stats_text = ", ".join(f"{k} +{int(v * quality_multiplier(quality))}" for k, v in item_data.get("stats", {}).items())
            embed = success_embed("\U0001F4E6 Possession Purchased!", get_action_text("store", "buy_possession", quality_emoji=quality_emoji(quality), quality_name=quality_name(quality), item_name=item_data['name'], price=format_money(price), stats=stats_text, description=item_data['description']))
            await interaction.response.send_message(embed=embed, ephemeral=True)

    async def _back_callback(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your shop session!", ephemeral=True)
            return
        view = ItemListView(self.cog, self.user_id, self.cat_id, self.sub_id, self.page)
        await interaction.response.edit_message(embed=view.build_embed(), view=view)

    def build_embed(self):
        item_data = _resolve_item(self.item_id, self.source)
        cat = STORE_CATALOG[self.cat_id]
        price = item_data["price"]
        flash_cat = get_flash_sale_category()
        on_sale = flash_cat == self.cat_id
        if on_sale:
            discounted = int(price * get_flash_sale_discount())
            price_text = f"~~{format_money(price)}~~ **{format_money(discounted)}**"
        else:
            price_text = format_money(price)
        embed = discord.Embed(title=f"{item_data['name']}", description=f"**Price:** {price_text}", color=cat.get("color", 0x2ECC71))
        if on_sale:
            embed.add_field(name="\U0001F525 Flash Sale!", value=f"{FLASH_SALE['discount_percent']}% off!", inline=False)
        effects = _item_effects(item_data)
        if effects:
            embed.add_field(name="Effects", value="\n".join(effects), inline=False)
        if self.source == "tools":
            embed.add_field(name="Durability", value=str(item_data.get("durability", "?")), inline=True)
            embed.add_field(name="Activity", value=item_data.get("activity", "?").title(), inline=True)
            embed.add_field(name="Description", value=item_data.get("description", ""), inline=False)
        elif self.source == "clothing":
            embed.add_field(name="Slot", value=item_data.get("slot", "?").title(), inline=True)
            embed.add_field(name="Warmth", value=str(item_data.get("warmth", 0)), inline=True)
            stats = item_data.get("stats", {})
            if stats:
                embed.add_field(name="Stat Bonuses", value=", ".join(f"{k} +{v}" for k, v in stats.items()), inline=False)
            prot = item_data.get("weather_prot", [])
            if prot:
                embed.add_field(name="Weather Protection", value=", ".join(prot), inline=False)
        elif self.source == "possessions":
            stats = item_data.get("stats", {})
            if stats:
                embed.add_field(name="Stat Bonuses", value=", ".join(f"{k} +{v}" for k, v in stats.items()), inline=False)
            embed.add_field(name="Description", value=item_data.get("description", ""), inline=False)
        embed.set_footer(text="Click a button below to buy, or go back to browse more items.")
        return embed


class DealsView(discord.ui.View):
    def __init__(self, cog, user_id):
        super().__init__(timeout=180)
        self.cog = cog
        self.user_id = user_id
        mb_btn = discord.ui.Button(label=f"Mystery Box ({format_money(MYSTERY_BOX['price'])})", emoji="\U0001F381", style=discord.ButtonStyle.primary, custom_id="deal_mystery")
        mb_btn.callback = self._mystery_callback
        self.add_item(mb_btn)
        dd_btn = discord.ui.Button(label="Daily Deal", emoji="\U0001F4C5", style=discord.ButtonStyle.success, custom_id="deal_daily")
        dd_btn.callback = self._daily_callback
        self.add_item(dd_btn)
        ld_btn = discord.ui.Button(label=f"Lucky Dip ({format_money(LUCKY_DIP['price'])})", emoji="\U0001F3B0", style=discord.ButtonStyle.primary, custom_id="deal_lucky")
        ld_btn.callback = self._lucky_callback
        self.add_item(ld_btn)
        tp_btn = discord.ui.Button(label=f"Traveler's Pack ({format_money(TRAVELER_PACK['price'])})", emoji="\U0001F392", style=discord.ButtonStyle.primary, custom_id="deal_traveler")
        tp_btn.callback = self._traveler_callback
        self.add_item(tp_btn)
        back_btn = discord.ui.Button(label="Back to Categories", emoji="\u2B05\uFE0F", style=discord.ButtonStyle.danger, custom_id="deal_back")
        back_btn.callback = self._back_callback
        self.add_item(back_btn)

    def build_embed(self):
        embed = discord.Embed(title="\U0001F525 Special Deals", description="Limited-time offers and mystery items!", color=0xE74C3C)
        embed.add_field(name=f"{MYSTERY_BOX['emoji']} {MYSTERY_BOX['name']} \u2014 {format_money(MYSTERY_BOX['price'])}", value=MYSTERY_BOX['description'], inline=False)
        deal_item_id, _, orig_price, disc_price = get_daily_deal_item()
        deal_item = STORE_ITEMS[deal_item_id]
        embed.add_field(name=f"\U0001F4C5 Daily Deal \u2014 {deal_item['name']}", value=f"~~{format_money(orig_price)}~~ **{format_money(disc_price)}** \u2014 {DAILY_DEAL['discount_percent']}% off! Changes daily!", inline=False)
        flash_cat = get_flash_sale_category()
        flash_cat_name = STORE_CATALOG[flash_cat]["name"]
        embed.add_field(name=f"\u26A1 Flash Sale \u2014 {flash_cat_name}", value=f"{FLASH_SALE['discount_percent']}% off all items in {flash_cat_name}! Changes every {FLASH_SALE['interval_hours']} hours!", inline=False)
        embed.add_field(name=f"{LUCKY_DIP['emoji']} {LUCKY_DIP['name']} \u2014 {format_money(LUCKY_DIP['price'])}", value=LUCKY_DIP['description'], inline=False)
        embed.add_field(name=f"{TRAVELER_PACK['emoji']} {TRAVELER_PACK['name']} \u2014 {format_money(TRAVELER_PACK['price'])}", value=TRAVELER_PACK['description'], inline=False)
        return embed

    async def _mystery_callback(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your shop session!", ephemeral=True)
            return
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if data["wallet"] < MYSTERY_BOX["price"]:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You need {format_money(MYSTERY_BOX['price'])}."), ephemeral=True)
            return
        item_id, item_data = get_mystery_box_item()
        await db.update_user(interaction.user.id, wallet=data["wallet"] - MYSTERY_BOX["price"], total_spent=data["total_spent"] + MYSTERY_BOX["price"], items_bought=data["items_bought"] + 1)
        if item_data["type"] == "collectible":
            await db.add_collectible(interaction.user.id, item_id)
        else:
            await db.add_to_inventory(interaction.user.id, item_id, 1)
        await db.add_transaction(interaction.user.id, "mystery_box", MYSTERY_BOX["price"], f"Mystery box: got {item_data['name']}")
        embed = success_embed("\U0001F381 Mystery Box Opened!", f"You open the mystery box and find... **{item_data['name']}**! (Value: {format_money(item_data['price'])})")
        if item_data["price"] > MYSTERY_BOX["price"]:
            embed.add_field(name="\U0001F4B0 Lucky!", value="You got an item worth more than you paid!", inline=False)
        elif item_data["price"] < MYSTERY_BOX["price"] * 0.3:
            embed.add_field(name="\U0001F605 Better luck next time...", value="The box wasn't very generous today.", inline=False)
        await interaction.response.send_message(embed=embed)

    async def _daily_callback(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your shop session!", ephemeral=True)
            return
        deal_item_id, _, orig_price, disc_price = get_daily_deal_item()
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if data["wallet"] < disc_price:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You need {format_money(disc_price)}."), ephemeral=True)
            return
        item_data = STORE_ITEMS[deal_item_id]
        if item_data["type"] == "collectible":
            already = await db.get_collectibles(interaction.user.id)
            if any(c["item_id"] == deal_item_id for c in already):
                await interaction.response.send_message(embed=error_embed("Already Owned", "You already own this collectible!"), ephemeral=True)
                return
            await db.add_collectible(interaction.user.id, deal_item_id)
        else:
            await db.add_to_inventory(interaction.user.id, deal_item_id, 1)
        await db.update_user(interaction.user.id, wallet=data["wallet"] - disc_price, total_spent=data["total_spent"] + disc_price, items_bought=data["items_bought"] + 1)
        await db.add_transaction(interaction.user.id, "daily_deal", disc_price, f"Daily deal: {item_data['name']}")
        embed = success_embed("\U0001F4C5 Daily Deal Claimed!", f"You bought **{item_data['name']}** for ~~{format_money(orig_price)}~~ **{format_money(disc_price)}** \u2014 saved {format_money(orig_price - disc_price)}!")
        await interaction.response.send_message(embed=embed)

    async def _lucky_callback(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your shop session!", ephemeral=True)
            return
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if data["wallet"] < LUCKY_DIP["price"]:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You need {format_money(LUCKY_DIP['price'])}."), ephemeral=True)
            return
        item_id, item_data = get_lucky_dip_item()
        await db.update_user(interaction.user.id, wallet=data["wallet"] - LUCKY_DIP["price"], total_spent=data["total_spent"] + LUCKY_DIP["price"], items_bought=data["items_bought"] + 1)
        await db.add_to_inventory(interaction.user.id, item_id, 1)
        await db.add_transaction(interaction.user.id, "lucky_dip", LUCKY_DIP["price"], f"Lucky dip: got {item_data['name']}")
        embed = success_embed("\U0001F3B0 Lucky Dip!", f"You reach into the dip and pull out... **{item_data['name']}**! (Value: {format_money(item_data['price'])})")
        await interaction.response.send_message(embed=embed)

    async def _traveler_callback(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your shop session!", ephemeral=True)
            return
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if data["wallet"] < TRAVELER_PACK["price"]:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You need {format_money(TRAVELER_PACK['price'])}."), ephemeral=True)
            return
        await db.update_user(interaction.user.id, wallet=data["wallet"] - TRAVELER_PACK["price"], total_spent=data["total_spent"] + TRAVELER_PACK["price"], items_bought=data["items_bought"] + 1)
        got_items = []
        for item_id in TRAVELER_PACK["contents"]["guaranteed"]:
            item_data = STORE_ITEMS.get(item_id)
            if item_data:
                await db.add_to_inventory(interaction.user.id, item_id, 1)
                got_items.append(item_data["name"])
        bonus_items = []
        for chance_item in TRAVELER_PACK["contents"]["chance_items"]:
            if random.random() < chance_item["chance"]:
                cid = chance_item["item_id"]
                csource = chance_item["source"]
                cdata = _resolve_item(cid, csource)
                if cdata:
                    if csource == "store_items":
                        if cdata["type"] == "collectible":
                            await db.add_collectible(interaction.user.id, cid)
                        else:
                            await db.add_to_inventory(interaction.user.id, cid, 1)
                    elif csource == "tools":
                        quality = roll_quality()
                        await db.add_equipment(interaction.user.id, cid, "tool", quality, cdata["durability"], cdata["durability"])
                    else:
                        await db.add_to_inventory(interaction.user.id, cid, 1)
                    bonus_items.append(f"**{cdata['name']}** (BONUS!)")
        await db.add_transaction(interaction.user.id, "traveler_pack", TRAVELER_PACK["price"], f"Traveler's pack: {', '.join(got_items)}")
        all_items = got_items + bonus_items
        embed = success_embed("\U0001F392 Traveler's Pack Opened!", f"You unpack your traveler's pack and find:\n" + "\n".join(f"\u2022 {i}" for i in all_items))
        if bonus_items:
            embed.add_field(name="\U0001F389 Bonus Items!", value="You got lucky and found some extra items!", inline=False)
        await interaction.response.send_message(embed=embed)

    async def _back_callback(self, interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your shop session!", ephemeral=True)
            return
        await _send_main_menu(interaction, self.cog, self.user_id)


async def _send_main_menu(interaction, cog, user_id):
    embed = discord.Embed(title="\U0001F6D2 Store", description="Welcome to the store! Select a category to browse:", color=0x2ECC71)
    flash_cat = get_flash_sale_category()
    flash_cat_name = STORE_CATALOG[flash_cat]["name"]
    embed.add_field(name="\U0001F525 Flash Sale!", value=f"**{flash_cat_name}** is **{FLASH_SALE['discount_percent']}% OFF** for a limited time!", inline=False)
    deal_item_id, _, orig_price, disc_price = get_daily_deal_item()
    deal_item = STORE_ITEMS[deal_item_id]
    embed.add_field(name="\U0001F4C5 Daily Deal", value=f"{deal_item['name']} \u2014 ~~{format_money(orig_price)}~~ **{format_money(disc_price)}** ({DAILY_DEAL['discount_percent']}% off!)", inline=False)
    embed.add_field(name="\U0001F381 Special Deals Available!", value="Check out Mystery Boxes, Lucky Dips, and Traveler's Packs in the Special Deals section!", inline=False)
    view = CategoryView(cog, user_id)
    await interaction.response.edit_message(embed=embed, view=view)


class Store(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shop", description="Browse the store with interactive menus")
    async def shop(self, interaction: discord.Interaction):
        flash_cat = get_flash_sale_category()
        flash_cat_name = STORE_CATALOG[flash_cat]["name"]
        deal_item_id, _, orig_price, disc_price = get_daily_deal_item()
        deal_item = STORE_ITEMS[deal_item_id]
        embed = discord.Embed(
            title="� Store",
            description="Welcome to the store! Select a category to browse:",
            color=0x2ECC71,
        )
        embed.add_field(name="🔥 Flash Sale!", value=f"**{flash_cat_name}** is **{FLASH_SALE['discount_percent']}% OFF** for a limited time!", inline=False)
        embed.add_field(name="� Daily Deal", value=f"{deal_item['name']} — ~~{format_money(orig_price)}~~ **{format_money(disc_price)}** ({DAILY_DEAL['discount_percent']}% off!)", inline=False)
        embed.add_field(name="🎁 Special Deals Available!", value="Check out Mystery Boxes, Lucky Dips, and Traveler's Packs in the Special Deals section!", inline=False)
        view = CategoryView(self, interaction.user.id)
        await interaction.response.send_message(embed=embed, view=view)

    async def _do_buy(self, interaction: discord.Interaction, item_id: str, quantity: int = 1):
        if quantity < 1:
            await interaction.response.send_message(embed=error_embed("Error", "Quantity must be at least 1."), ephemeral=True)
            return
        if item_id not in STORE_ITEMS:
            await interaction.response.send_message(embed=error_embed("Error", "Invalid item."), ephemeral=True)
            return

        item_data = STORE_ITEMS[item_id]
        total_cost = item_data["price"] * quantity
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        cd = await db.check_cooldown(interaction.user.id, "buy")
        if cd > 0:
            secs = int(cd)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"You're shopping too fast. Try again in {secs}s."), ephemeral=True)
            return

        if data["wallet"] < total_cost:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You need {format_money(total_cost)} but only have {format_money(data['wallet'])}."), ephemeral=True)
            return

        if item_data["type"] == "collectible":
            already = await db.get_collectibles(interaction.user.id)
            if any(c["item_id"] == item_id for c in already):
                await interaction.response.send_message(embed=error_embed("Already Owned", "You already own this collectible! Collectibles are unique."), ephemeral=True)
                return
            await db.update_user(interaction.user.id,
                wallet=data["wallet"] - total_cost,
                total_spent=data["total_spent"] + total_cost,
                items_bought=data["items_bought"] + 1,
            )
            await db.add_collectible(interaction.user.id, item_id)
            await db.add_transaction(interaction.user.id, "buy_collectible", total_cost, f"Bought collectible {item_data['name']}")
            await db.update_quest_progress(interaction.user.id, "buy", 1)
            await db.set_cooldown(interaction.user.id, "buy", 60)

            xp_gain = 10
            new_xp = data["xp"] + xp_gain
            new_level, leveled_up = check_level_up(new_xp, data["level"])
            if leveled_up:
                new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))
                await db.update_user(interaction.user.id, xp=new_xp, level=new_level)
            else:
                await db.update_user(interaction.user.id, xp=new_xp)

            embed = success_embed("💎 Collectible Acquired!", get_action_text("store", "buy_collectible", item_name=item_data['name'], price=format_money(total_cost)))
            if leveled_up:
                embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
            new_achievements = await db.check_achievements(interaction.user.id)
            for ach_id in new_achievements:
                ach = ACHIEVEMENTS[ach_id]
                embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
            if new_achievements:
                ach_reward = sum(ACHIEVEMENTS[a]["reward"] for a in new_achievements)
                await db.update_user(interaction.user.id, wallet=data["wallet"] - total_cost + ach_reward, total_earned=data["total_earned"] + ach_reward)
            await interaction.response.send_message(embed=embed)
            return

        await db.update_user(interaction.user.id,
            wallet=data["wallet"] - total_cost,
            total_spent=data["total_spent"] + total_cost,
            items_bought=data["items_bought"] + quantity,
        )
        await db.add_to_inventory(interaction.user.id, item_id, quantity)
        await db.add_transaction(interaction.user.id, "buy", total_cost, f"Bought {quantity}x {item_data['name']}")
        await db.update_quest_progress(interaction.user.id, "buy", quantity)
        await db.set_cooldown(interaction.user.id, "buy", 60)

        await world.perturb_market(interaction.user.id, demand_delta=0.02 * quantity)

        xp_gain = 5 * quantity
        new_xp = data["xp"] + xp_gain
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))
            await db.update_user(interaction.user.id, xp=new_xp, level=new_level)
        else:
            await db.update_user(interaction.user.id, xp=new_xp)

        embed = success_embed("🛒 Purchase Complete", get_action_text("store", "buy", qty=quantity, item_name=item_data['name'], price=format_money(total_cost), wallet=format_money(data['wallet'] - total_cost), qty_label=f" ({quantity}x)" if quantity > 1 else ""))
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        new_achievements = await db.check_achievements(interaction.user.id)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        if new_achievements:
            ach_reward = sum(ACHIEVEMENTS[a]["reward"] for a in new_achievements)
            await db.update_user(interaction.user.id, wallet=data["wallet"] - total_cost + ach_reward, total_earned=data["total_earned"] + ach_reward)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="buy", description="Buy items from the store")
    @app_commands.autocomplete(item=_item_autocomplete)
    async def buy(self, interaction: discord.Interaction, item: str, quantity: int = 1):
        await self._do_buy(interaction, item, quantity)

    @app_commands.command(name="inventory", description="View your inventory")
    async def inventory(self, interaction: discord.Interaction):
        inv = await db.get_inventory(interaction.user.id)
        if not inv:
            await interaction.response.send_message(embed=info_embed("🎒 Inventory", "Your inventory is empty. Use `/shop` to buy items!"))
            return
        embed = info_embed("🎒 Your Inventory")
        for item_id, qty in inv.items():
            item = (
                STORE_ITEMS.get(item_id)
                or RAW_MATERIALS.get(item_id)
                or CRAFTING_RECIPES.get(item_id)
                or TOOLS.get(item_id)
                or CLOTHING.get(item_id)
                or POSSESSIONS.get(item_id)
            )
            if item:
                name = item.get("name", item_id)
                use_cmd = f"`/use item:{item_id}`" if item_id in STORE_ITEMS and STORE_ITEMS[item_id].get("type") != "collectible" else ""
                embed.add_field(name=name, value=f"Quantity: {qty} {use_cmd}", inline=True)
            else:
                embed.add_field(name=item_id, value=f"Quantity: {qty}", inline=True)
        await interaction.response.send_message(embed=embed)

    async def _do_use(self, interaction: discord.Interaction, item_id: str):
        inv = await db.get_inventory(interaction.user.id)
        if item_id not in inv or inv[item_id] <= 0:
            await interaction.response.send_message(embed=error_embed("Not Owned", "You don't have any of that item. Use `/shop` to buy some."), ephemeral=True)
            return

        item_data = STORE_ITEMS[item_id]
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        new_health = clamp(data["health"] + item_data.get("health", 0), 0, HEALTH_MAX)
        new_hunger = clamp(data["hunger"] + item_data.get("hunger", 0), 0, HUNGER_MAX)
        new_thirst = clamp(data["thirst"] + item_data.get("thirst", 0), 0, THIRST_MAX)
        new_energy = clamp(data.get("energy", 100) + item_data.get("energy", 0), 0, 100)
        new_hygiene = clamp(data.get("hygiene", 100) + item_data.get("hygiene", 0), 0, 100)

        update_fields = dict(
            health=new_health,
            hunger=new_hunger,
            thirst=new_thirst,
            energy=new_energy,
            hygiene=new_hygiene,
            items_used=data["items_used"] + 1,
        )

        if item_data.get("energy", 0) > 0:
            update_fields["energy_items_used"] = data.get("energy_items_used", 0) + 1
        if item_data.get("hygiene", 0) > 0:
            update_fields["hygiene_items_used"] = data.get("hygiene_items_used", 0) + 1

        effects = []
        if item_data.get("type") == "stat_booster":
            stat_name = item_data.get("stat", "")
            boost = item_data.get("boost", 0)
            duration_sec = item_data.get("duration", 1800)
            if stat_name and boost:
                await db.add_buff(interaction.user.id, f"stat_{stat_name}", f"stat_{stat_name}", float(boost), duration_sec)
                stat_display = stat_name.title()
                effects.append(f"📊 {stat_display}: +{boost} for {duration_sec // 60}min")

        await db.update_user(interaction.user.id, **update_fields)
        await db.remove_from_inventory(interaction.user.id, item_id, 1)
        await db.update_quest_progress(interaction.user.id, "use_item", 1)

        xp_gain = 2
        new_xp = data["xp"] + xp_gain
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))
            await db.update_user(interaction.user.id, xp=new_xp, level=new_level)
        else:
            await db.update_user(interaction.user.id, xp=new_xp)

        if item_data.get("health", 0) != 0:
            effects.append(f"❤️ Health: {data['health']} → {new_health}")
        if item_data.get("hunger", 0) != 0:
            effects.append(f"🍖 Hunger: {data['hunger']} → {new_hunger}")
        if item_data.get("thirst", 0) != 0:
            effects.append(f"💧 Thirst: {data['thirst']} → {new_thirst}")
        if item_data.get("energy", 0) != 0:
            effects.append(f"⚡ Energy: {data.get('energy', 100)} → {new_energy}")
        if item_data.get("hygiene", 0) != 0:
            effects.append(f"🧼 Hygiene: {data.get('hygiene', 100)} → {new_hygiene}")

        embed = success_embed(f"✅ Used {item_data['name']}", get_action_text("store", "use_item", item_name=item_data['name'], effects="\n".join(effects)))
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="use", description="Use an item from your inventory")
    @app_commands.autocomplete(item=_usable_item_autocomplete)
    async def use(self, interaction: discord.Interaction, item: str):
        await self._do_use(interaction, item)

    async def _do_sell(self, interaction: discord.Interaction, item_id: str, quantity: int = 1):
        if quantity < 1:
            await interaction.response.send_message(embed=error_embed("Error", "Quantity must be at least 1."), ephemeral=True)
            return
        inv = await db.get_inventory(interaction.user.id)
        if item_id not in inv or inv[item_id] < quantity:
            await interaction.response.send_message(embed=error_embed("Not Enough", "You don't have that many to sell."), ephemeral=True)
            return

        item_data = STORE_ITEMS[item_id]
        refund = (item_data["price"] // 2) * quantity
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)

        await db.remove_from_inventory(interaction.user.id, item_id, quantity)
        await db.update_user(interaction.user.id, wallet=data["wallet"] + refund, total_earned=data["total_earned"] + refund)
        await db.add_transaction(interaction.user.id, "sell", refund, f"Sold {quantity}x {item_data['name']}")

        await world.perturb_market(interaction.user.id, demand_delta=-0.01 * quantity)

        await interaction.response.send_message(embed=success_embed("💰 Sold!", get_action_text("store", "sell", qty=quantity, item_name=item_data['name'], price=format_money(refund), wallet=format_money(data['wallet'] + refund))))

    @app_commands.command(name="sell", description="Sell an item back (50% refund)")
    @app_commands.autocomplete(item=_item_autocomplete)
    async def sell(self, interaction: discord.Interaction, item: str, quantity: int = 1):
        await self._do_sell(interaction, item, quantity)

    @app_commands.command(name="collectibles", description="View your collectible items")
    async def collectibles(self, interaction: discord.Interaction):
        owned = await db.get_collectibles(interaction.user.id)
        if not owned:
            await interaction.response.send_message(embed=info_embed("💎 Collectibles", "You don't own any collectibles yet. Use `/shop` and browse the Collectibles category to buy some!"))
            return
        embed = info_embed("💎 Your Collection", f"You own {len(owned)} collectible(s)!")
        for c in owned:
            item = STORE_ITEMS.get(c["item_id"], {})
            name = item.get("name", c["item_id"])
            price = item.get("price", 0)
            embed.add_field(name=name, value=f"Value: {format_money(price)}", inline=True)
        total_value = sum(STORE_ITEMS.get(c["item_id"], {}).get("price", 0) for c in owned)
        embed.add_field(name="📊 Total Collection Value", value=format_money(total_value), inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="buy_equipment", description="Buy tools, clothing, or possessions (quality is random!)")
    @app_commands.autocomplete(item=_equipment_autocomplete)
    async def buy_equipment(self, interaction: discord.Interaction, item: str):
        parts = item.split(":", 1)
        if len(parts) != 2:
            await interaction.response.send_message(embed=error_embed("Error", "Invalid equipment selection."), ephemeral=True)
            return
        equip_type, item_id = parts
        if equip_type == "tool":
            await self._do_buy_tool(interaction, item_id)
        elif equip_type == "clothing":
            await self._do_buy_clothing(interaction, item_id)
        elif equip_type == "possession":
            await self._do_buy_possession(interaction, item_id)
        else:
            await interaction.response.send_message(embed=error_embed("Error", "Invalid equipment type."), ephemeral=True)

    async def _do_buy_tool(self, interaction: discord.Interaction, tool_id: str):
        tool_data = TOOLS.get(tool_id)
        if not tool_data:
            await interaction.response.send_message(embed=error_embed("Error", "Invalid tool."), ephemeral=True)
            return

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if data["wallet"] < tool_data["price"]:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You need {format_money(tool_data['price'])}."), ephemeral=True)
            return

        quality = roll_quality()
        await db.update_user(interaction.user.id, wallet=data["wallet"] - tool_data["price"], total_spent=data["total_spent"] + tool_data["price"])
        await db.add_equipment(interaction.user.id, tool_id, "tool", quality, tool_data["durability"], tool_data["durability"])
        await db.record_discovery(interaction.user.id, tool_id, quality, "shop")
        await db.add_transaction(interaction.user.id, "buy_tool", tool_data["price"], f"Bought {quality_name(quality)} {tool_data['name']}")

        embed = success_embed(
            f"🔧 Tool Purchased!",
            get_action_text("store", "buy_tool", quality_emoji=quality_emoji(quality), quality_name=quality_name(quality), item_name=tool_data['name'], price=format_money(tool_data['price']), durability=tool_data['durability'], description=tool_data['description']),
        )
        await interaction.response.send_message(embed=embed)

    async def _do_buy_clothing(self, interaction: discord.Interaction, item_id: str):
        item_data = CLOTHING.get(item_id)
        if not item_data:
            await interaction.response.send_message(embed=error_embed("Error", "Invalid clothing."), ephemeral=True)
            return

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if data["wallet"] < item_data["price"]:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You need {format_money(item_data['price'])}."), ephemeral=True)
            return

        quality = roll_quality()
        await db.update_user(interaction.user.id, wallet=data["wallet"] - item_data["price"], total_spent=data["total_spent"] + item_data["price"])
        await db.add_equipment(interaction.user.id, item_id, "clothing", quality, 100, 100)
        await db.record_discovery(interaction.user.id, item_id, quality, "shop")
        await db.add_transaction(interaction.user.id, "buy_clothing", item_data["price"], f"Bought {quality_name(quality)} {item_data['name']}")

        stats_text = ", ".join(f"{k} +{int(v * quality_multiplier(quality))}" for k, v in item_data.get("stats", {}).items()) if item_data.get("stats") else "No stat bonuses"
        prot_text = f"Weather protection: {', '.join(item_data['weather_prot'])}" if item_data.get("weather_prot") else "No weather protection"

        embed = success_embed(
            f"👕 Clothing Purchased!",
            get_action_text("store", "buy_clothing", quality_emoji=quality_emoji(quality), quality_name=quality_name(quality), item_name=item_data['name'], price=format_money(item_data['price']), slot=item_data['slot'], warmth=item_data['warmth'], stats=stats_text, prot=prot_text),
        )
        await interaction.response.send_message(embed=embed)

    async def _do_buy_possession(self, interaction: discord.Interaction, item_id: str):
        item_data = POSSESSIONS.get(item_id)
        if not item_data:
            await interaction.response.send_message(embed=error_embed("Error", "Invalid possession."), ephemeral=True)
            return

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if data["wallet"] < item_data["price"]:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You need {format_money(item_data['price'])}."), ephemeral=True)
            return

        quality = roll_quality()
        await db.update_user(interaction.user.id, wallet=data["wallet"] - item_data["price"], total_spent=data["total_spent"] + item_data["price"])
        await db.add_equipment(interaction.user.id, item_id, "possession", quality, 999, 999)
        await db.record_discovery(interaction.user.id, item_id, quality, "shop")
        await db.add_transaction(interaction.user.id, "buy_possession", item_data["price"], f"Bought {quality_name(quality)} {item_data['name']}")

        stats_text = ", ".join(f"{k} +{int(v * quality_multiplier(quality))}" for k, v in item_data.get("stats", {}).items())

        embed = success_embed(
            f"📦 Possession Purchased!",
            get_action_text("store", "buy_possession", quality_emoji=quality_emoji(quality), quality_name=quality_name(quality), item_name=item_data['name'], price=format_money(item_data['price']), stats=stats_text, description=item_data['description']),
        )
        await interaction.response.send_message(embed=embed)

    # ─── /sell_equipment ───
    @app_commands.command(name="sell_equipment", description="Sell a tool, clothing, or possession")
    async def sell_equipment(self, interaction: discord.Interaction, item_id: str, quality: str = "common"):
        equip = await db.get_equipment(interaction.user.id)
        item = next((e for e in equip if e["item_id"] == item_id and e["quality"] == quality), None)
        if not item:
            await interaction.response.send_message(embed=error_embed("Not Found", "You don't have that equipment."), ephemeral=True)
            return

        item_data = TOOLS.get(item_id, CLOTHING.get(item_id, POSSESSIONS.get(item_id, {})))
        base_price = item_data.get("price", 100)
        from utils.quality import quality_value_mult
        sell_price = int(base_price * 0.5 * quality_value_mult(quality))

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        await db.remove_equipment(interaction.user.id, item_id, quality)
        await db.update_user(interaction.user.id, wallet=data["wallet"] + sell_price, total_earned=data["total_earned"] + sell_price)
        await db.add_transaction(interaction.user.id, "sell_equipment", sell_price, f"Sold {quality_name(quality)} {item_data.get('name', item_id)}")

        await interaction.response.send_message(
            embed=success_embed("💰 Sold!", get_action_text("store", "sell_equipment", quality_emoji=quality_emoji(quality), quality_name=quality_name(quality), item_name=item_data.get('name', item_id), price=format_money(sell_price))),
        )


async def setup(bot):
    await bot.add_cog(Store(bot))
