import discord
from discord import app_commands
from discord.ext import commands, tasks
import random
from datetime import datetime, timezone

import database as db
import world
from config import (
    NPCS, LOCATIONS, TIME_PERIODS, COOKING_RECIPES, BUFF_TYPES, FACTIONS,
    RAW_MATERIALS, DAY_NIGHT_INTERVAL, WEATHER_STATES,
)
from utils.embeds import success_embed, error_embed, info_embed, format_money
from utils.helpers import clamp, check_level_up, xp_for_next_level
from utils.quality import roll_quality, quality_name, quality_emoji, quality_multiplier
from utils.narrative import (
    roll_random_event, maybe_random_event, generate_npc_encounter,
    generate_cooking_text, generate_travel_text, generate_npc_dialogue,
    get_action_text,
)


class ImmersionCog(commands.Cog):
    """NPCs, locations, cooking, day/night cycle, buffs, and reputation."""

    def __init__(self, bot):
        self.bot = bot
        self.time_loop.start()

    def cog_unload(self):
        self.time_loop.cancel()

    # ─── Day/Night background loop ───
    @tasks.loop(minutes=30)
    async def time_loop(self):
        await db.advance_game_time(1)

    @time_loop.before_loop
    async def before_time_loop(self):
        await self.bot.wait_until_ready()

    # ─── /time — Check current game time ───
    @app_commands.command(name="time", description="Check the current game time and its effects")
    async def time_cmd(self, interaction: discord.Interaction):
        gt = await db.get_game_time()
        period = TIME_PERIODS.get(gt["time_period"], {})
        effects = period.get("effects", {})

        embed = info_embed(
            f"{period.get('emoji', '🕐')} {period.get('name', 'Unknown')}",
            period.get("description", ""),
        )
        embed.add_field(name="🕐 Game Hour", value=f"{gt['game_hour']:02d}:00", inline=True)

        effect_text = []
        if "energy_regen" in effects and effects["energy_regen"] > 0:
            effect_text.append(f"⚡ +{effects['energy_regen']} energy regen")
        if "work_pay" in effects:
            effect_text.append(f"💼 {int((effects['work_pay'] - 1) * 100):+d}% work pay")
        if "fish_luck" in effects:
            effect_text.append(f"🎣 {int((effects['fish_luck'] - 1) * 100):+d}% fish luck")
        if "crime_success" in effects:
            effect_text.append(f"🦹 {int((effects['crime_success'] - 1) * 100):+d}% crime success")
        if "encounter_chance" in effects:
            effect_text.append(f"🧭 {int((effects['encounter_chance'] - 1) * 100):+d}% encounter rate")
        if "rare_find_chance" in effects:
            effect_text.append(f"💎 {int((effects['rare_find_chance'] - 1) * 100):+d}% rare find chance")

        embed.add_field(
            name="✨ Active Effects",
            value="\n".join(effect_text) if effect_text else "No special effects",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)

    # ─── /travel — Travel to a location ───
    @app_commands.command(name="travel", description="Travel to a location for unique activities and encounters")
    @app_commands.choices(location=[
        app_commands.Choice(name=LOCATIONS[loc]["name"], value=loc) for loc in LOCATIONS
    ])
    async def travel(self, interaction: discord.Interaction, location: app_commands.Choice[str]):
        loc_id = location.value
        loc = LOCATIONS.get(loc_id)
        if not loc:
            await interaction.response.send_message(embed=error_embed("Invalid", "That location doesn't exist."), ephemeral=True)
            return

        data = await db.get_user(interaction.user.id)
        if not data:
            await interaction.response.send_message(embed=error_embed("No Account", "Use `/start` first."), ephemeral=True)
            return

        if data.get("energy", 100) < 10:
            await interaction.response.send_message(embed=error_embed("Too Tired", "You need at least 10 energy to travel."), ephemeral=True)
            return

        # Travel costs energy and advances time
        new_energy = clamp(data.get("energy", 100) - 10, 0, 100)
        await db.update_user(interaction.user.id, energy=new_energy)
        await db.advance_game_time(1)

        travel_text = generate_travel_text(loc["name"])

        # Check for random encounter while traveling
        encounter_text = ""
        encounter_chance = loc["encounter_chance"]
        time_effects = await db.get_time_effects()
        encounter_chance *= time_effects.get("encounter_chance", 1.0)

        if random.random() < encounter_chance:
            event = roll_random_event()
            await db.update_user(
                interaction.user.id,
                wallet=clamp(data["wallet"] + event["coins"], 0, 10**12),
                health=clamp(data["health"] + event.get("hp", 0), 0, 100),
                energy=clamp(data.get("energy", 100) + event.get("energy", 0), 0, 100),
                hunger=clamp(data["hunger"] + event.get("hunger", 0), 0, 100),
                hygiene=clamp(data.get("hygiene", 100) + event.get("hygiene", 0), 0, 100),
            )
            if event["coins"] != 0:
                await db.add_transaction(interaction.user.id, "event", abs(event["coins"]), event["text"])
            encounter_text = f"\n\n🎲 **On the way there:** {event['text']}"

        # Show NPCs at this location
        npc_list = loc.get("npcs", [])
        npc_text = ""
        if npc_list:
            npc_names = [f"{NPCS[n]['emoji']} {NPCS[n]['name']}" for n in npc_list if n in NPCS]
            npc_text = f"\n\n**People here:**\n" + "\n".join(npc_names)

        # Show available activities
        activities = loc.get("activities", [])
        act_text = ", ".join(f"`{a}`" for a in activities)

        embed = success_embed(
            f"{loc['emoji']} {loc['name']}",
            f"{travel_text}\n\n{loc['description']}{encounter_text}{npc_text}",
        )
        embed.add_field(name="🎯 Activities", value=act_text or "None", inline=False)
        embed.add_field(name="⚠️ Danger Level", value=f"{int(loc['danger'] * 100)}%", inline=True)
        embed.add_field(name="⚡ Energy Cost", value="-10", inline=True)

        # World perturbation: traveling increases location population and atmosphere
        await world.perturb_location(interaction.user.id, loc_id, population_delta=0.05, atmosphere_delta=0.02)

        await interaction.response.send_message(embed=embed)

    # ─── /npc (merged talk/trade/quest/complete) ───
    @app_commands.command(name="npc", description="Interact with an NPC: talk, trade, accept quest, or complete quest")
    @app_commands.describe(action="What to do", npc="The NPC", trade_number="Trade number (for trade action)")
    @app_commands.choices(action=[
        app_commands.Choice(name="💬 Talk", value="talk"),
        app_commands.Choice(name="🤝 Trade", value="trade"),
        app_commands.Choice(name="📜 Accept Quest", value="quest"),
        app_commands.Choice(name="✅ Complete Quest", value="complete"),
    ])
    @app_commands.choices(npc=[
        app_commands.Choice(name=f"{NPCS[n]['emoji']} {NPCS[n]['name']}", value=n) for n in NPCS
    ])
    async def npc(self, interaction: discord.Interaction, action: str, npc: str, trade_number: int = None):
        if action == "talk":
            await self._npc_talk(interaction, npc)
        elif action == "trade":
            if trade_number is None:
                await interaction.response.send_message(embed=error_embed("Error", "Provide a trade number."), ephemeral=True)
                return
            await self._npc_trade(interaction, npc, trade_number)
        elif action == "quest":
            await self._npc_quest(interaction, npc)
        elif action == "complete":
            await self._npc_complete(interaction, npc)
        else:
            await interaction.response.send_message(embed=error_embed("Error", "Invalid action."), ephemeral=True)

    async def _npc_talk(self, interaction: discord.Interaction, npc_id: str):
        npc_data = NPCS.get(npc_id)
        if not npc_data:
            await interaction.response.send_message(embed=error_embed("Invalid", "That NPC doesn't exist."), ephemeral=True)
            return

        data = await db.get_user(interaction.user.id)
        if not data:
            await interaction.response.send_message(embed=error_embed("No Account", "Use `/start` first."), ephemeral=True)
            return

        await db.record_npc_interaction(interaction.user.id, npc_id, "talk")

        # World perturbation: talking to an NPC slightly improves their mood, bumps tension
        await world.perturb_npc(interaction.user.id, npc_id, mood_delta=0.02, tension_delta=-0.01)

        # Pick a random greeting and dialogue line
        greeting = random.choice(npc_data["greeting"])
        personality_dialogue = generate_npc_dialogue(npc_data.get("personality", "friendly"))
        static_dialogue = random.choice(npc_data["dialogue"])
        dialogue = random.choice([personality_dialogue, static_dialogue])

        # Check weather for context-aware dialogue
        current_weather = await db.get_weather()
        weather_name = WEATHER_STATES.get(current_weather, {}).get("name", "")

        embed = info_embed(
            f"{npc_data['emoji']} {npc_data['name']}",
            f"*{greeting}*\n\n💬 \"{dialogue}\"",
        )

        # Show available trades
        trades = npc_data.get("trades", [])
        if trades:
            trade_text = []
            for i, t in enumerate(trades):
                give_name = RAW_MATERIALS.get(t["give"], {}).get("name", t["give"])
                recv_name = RAW_MATERIALS.get(t["receive"], {}).get("name", t["receive"])
                trade_text.append(f"**{i+1}.** Trade {t['give_qty']}x {give_name} → {t['receive_qty']}x {recv_name}")
            embed.add_field(name="🤝 Trades Available", value="\n".join(trade_text), inline=False)

        # Show quest if available
        quest = npc_data.get("quest")
        if quest:
            interaction_data = await db.get_npc_interaction(interaction.user.id, npc_id)
            quest_status = ""
            if interaction_data and interaction_data.get("quest_completed"):
                quest_status = " ✅ (Completed)"
            elif interaction_data and interaction_data.get("quest_accepted"):
                quest_status = " 📋 (In Progress)"
            embed.add_field(
                name=f"📜 Quest: {quest['desc']}{quest_status}",
                value=f"Reward: {format_money(quest['reward'])} + {quest['xp']} XP\nUse `/npc` with action Accept Quest to accept!",
                inline=False,
            )

        embed.set_footer(text=f"Weather: {weather_name} | Location: {LOCATIONS.get(npc_data['location'], {}).get('name', 'Unknown')}")
        await interaction.response.send_message(embed=embed)

    async def _npc_trade(self, interaction: discord.Interaction, npc_id: str, trade_number: int):
        npc_data = NPCS.get(npc_id)
        if not npc_data:
            await interaction.response.send_message(embed=error_embed("Invalid", "That NPC doesn't exist."), ephemeral=True)
            return

        trades = npc_data.get("trades", [])
        if trade_number < 1 or trade_number > len(trades):
            await interaction.response.send_message(embed=error_embed("Invalid Trade", f"Choose a trade between 1 and {len(trades)}."), ephemeral=True)
            return

        trade = trades[trade_number - 1]
        data = await db.get_user(interaction.user.id)
        if not data:
            await interaction.response.send_message(embed=error_embed("No Account", "Use `/start` first."), ephemeral=True)
            return

        # Check if player has the required materials
        inv = await db.get_inventory(interaction.user.id)

        give_id = trade["give"]
        give_qty = trade["give_qty"]

        if inv.get(give_id, 0) < give_qty:
            give_name = RAW_MATERIALS.get(give_id, {}).get("name", give_id)
            await interaction.response.send_message(
                embed=error_embed("Not Enough", f"You need {give_qty}x {give_name}. You have {inv.get(give_id, 0)}."),
                ephemeral=True,
            )
            return

        # Execute trade
        await db.remove_from_inventory(interaction.user.id, give_id, give_qty)
        await db.add_to_inventory(interaction.user.id, trade["receive"], trade["receive_qty"])
        await db.record_npc_interaction(interaction.user.id, npc_id, "trade")

        # Reputation gain for trading
        await db.add_reputation(interaction.user.id, "merchants", 1)

        # World perturbation: trading depletes NPC stock, improves mood, bumps market demand
        await world.perturb_npc(interaction.user.id, npc_id, stock_delta=-0.05, mood_delta=0.03)
        await world.perturb_market(interaction.user.id, demand_delta=0.02)

        give_name = RAW_MATERIALS.get(give_id, {}).get("name", give_id)
        recv_name = RAW_MATERIALS.get(trade["receive"], {}).get("name", trade["receive"])

        embed = success_embed(
            f"{npc_data['emoji']} Trade Complete!",
            get_action_text("immersion", "npc_trade", npc_name=npc_data['name'], give_qty=give_qty, give_name=give_name, recv_qty=trade['receive_qty'], recv_name=recv_name),
        )
        await interaction.response.send_message(embed=embed)

    async def _npc_quest(self, interaction: discord.Interaction, npc_id: str):
        npc_data = NPCS.get(npc_id)
        if not npc_data:
            await interaction.response.send_message(embed=error_embed("Invalid", "That NPC doesn't exist."), ephemeral=True)
            return

        quest = npc_data.get("quest")
        if not quest:
            await interaction.response.send_message(embed=error_embed("No Quest", f"{npc_data['name']} has no quest for you."), ephemeral=True)
            return

        interaction_data = await db.get_npc_interaction(interaction.user.id, npc_id)
        if interaction_data and interaction_data.get("quest_accepted"):
            await interaction.response.send_message(
                embed=error_embed("Already Accepted", "You've already accepted this quest. Complete it first!"),
                ephemeral=True,
            )
            return

        if interaction_data and interaction_data.get("quest_completed"):
            await interaction.response.send_message(
                embed=error_embed("Already Done", "You've already completed this quest!"),
                ephemeral=True,
            )
            return

        await db.accept_npc_quest(interaction.user.id, npc_id)

        embed = success_embed(
            f"📜 Quest Accepted: {quest['desc']}",
            get_action_text("immersion", "npc_quest_accept", npc_name=npc_data['name'], quest_desc=quest['desc'], reward=format_money(quest['reward']), xp=quest['xp'], npc_id=npc_id),
        )
        await interaction.response.send_message(embed=embed)

    async def _npc_complete(self, interaction: discord.Interaction, npc_id: str):
        npc_data = NPCS.get(npc_id)
        if not npc_data:
            await interaction.response.send_message(embed=error_embed("Invalid", "That NPC doesn't exist."), ephemeral=True)
            return

        interaction_data = await db.get_npc_interaction(interaction.user.id, npc_id)
        if not interaction_data or not interaction_data.get("quest_accepted"):
            await interaction.response.send_message(
                embed=error_embed("No Active Quest", "You haven't accepted this quest yet. Use `/npc` with action Accept Quest first."),
                ephemeral=True,
            )
            return

        if interaction_data.get("quest_completed"):
            await interaction.response.send_message(
                embed=error_embed("Already Done", "This quest is already completed!"),
                ephemeral=True,
            )
            return

        quest = npc_data["quest"]
        data = await db.get_user(interaction.user.id)

        # Check quest requirements based on type
        quest_type = quest["type"]
        quest_item = quest["item"]
        quest_qty = quest["qty"]

        if quest_type == "deliver":
            inv = await db.get_inventory(interaction.user.id)
            if inv.get(quest_item, 0) < quest_qty:
                item_name = RAW_MATERIALS.get(quest_item, {}).get("name", quest_item)
                await interaction.response.send_message(
                    embed=error_embed("Not Ready", f"You need {quest_qty}x {item_name}. You have {inv.get(quest_item, 0)}."),
                    ephemeral=True,
                )
                return
            await db.remove_from_inventory(interaction.user.id, quest_item, quest_qty)

        elif quest_type in ("catch", "mine", "explore"):
            # Check transaction count for this activity type
            db_conn = await db.get_db()
            async with db_conn.execute(
                "SELECT COUNT(*) as cnt FROM transactions WHERE user_id = ? AND type = ?",
                (interaction.user.id, quest_type),
            ) as cur:
                row = await cur.fetchone()
            if not row or row["cnt"] < quest_qty:
                await interaction.response.send_message(
                    embed=error_embed("Not Ready", f"You need to {quest_type} {quest_qty} times. Check your progress with `/npc {npc_id}`."),
                    ephemeral=True,
                )
                return

        elif quest_type == "crime":
            if data["crimes_committed"] < quest_qty:
                await interaction.response.send_message(
                    embed=error_embed("Not Ready", f"You need to commit {quest_qty} crimes. You've committed {data['crimes_committed']}."),
                    ephemeral=True,
                )
                return

        # Complete the quest
        await db.complete_npc_quest(interaction.user.id, npc_id)

        # Give rewards
        new_wallet = data["wallet"] + quest["reward"]
        new_xp = data["xp"] + quest["xp"]
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))

        await db.update_user(
            interaction.user.id,
            wallet=new_wallet,
            xp=new_xp,
            level=new_level,
            total_earned=data["total_earned"] + quest["reward"],
        )
        await db.add_transaction(interaction.user.id, "quest", quest["reward"], f"NPC Quest: {quest['desc']}")

        # Reputation gain
        faction_map = {
            "fish": "fishers", "catch": "fishers",
            "mine": "miners",
            "explore": "explorers",
            "crime": "underworld",
            "deliver": "merchants",
            "cook": "chefs",
        }
        faction = faction_map.get(quest_type, "explorers")
        await db.add_reputation(interaction.user.id, faction, 5)

        embed = success_embed(
            f"🎉 Quest Complete!",
            get_action_text("immersion", "npc_quest_complete", npc_name=npc_data['name'], quest_desc=quest['desc'], reward=format_money(quest['reward']), xp=quest['xp'], faction_name=FACTIONS.get(faction, {}).get('name', faction)),
        )
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"You are now level {new_level}!", inline=False)
        await interaction.response.send_message(embed=embed)

    # ─── /cook — Cook a meal from ingredients ───
    @app_commands.command(name="cook", description="Cook a meal from raw ingredients for buffs and restoration")
    @app_commands.describe(recipe="The recipe to cook")
    @app_commands.choices(recipe=[
        app_commands.Choice(name=f"{r['emoji']} {r['name']}", value=r_id) for r_id, r in COOKING_RECIPES.items()
    ])
    async def cook(self, interaction: discord.Interaction, recipe: app_commands.Choice[str]):
        recipe_id = recipe.value
        recipe_data = COOKING_RECIPES.get(recipe_id)
        if not recipe_data:
            await interaction.response.send_message(embed=error_embed("Invalid", "That recipe doesn't exist."), ephemeral=True)
            return

        data = await db.get_user(interaction.user.id)
        if not data:
            await interaction.response.send_message(embed=error_embed("No Account", "Use `/start` first."), ephemeral=True)
            return

        if data.get("energy", 100) < 5:
            await interaction.response.send_message(embed=error_embed("Too Tired", "You need at least 5 energy to cook."), ephemeral=True)
            return

        # Check ingredients
        inv = await db.get_inventory(interaction.user.id)

        ingredients = recipe_data["ingredients"]
        missing = []
        for ing_id, ing_qty in ingredients.items():
            if ing_qty > 0 and inv.get(ing_id, 0) < ing_qty:
                ing_name = RAW_MATERIALS.get(ing_id, {}).get("name", ing_id)
                missing.append(f"{ing_qty}x {ing_name} (have {inv.get(ing_id, 0)})")

        if missing:
            await interaction.response.send_message(
                embed=error_embed("Missing Ingredients", "You need:\n" + "\n".join(missing)),
                ephemeral=True,
            )
            return

        # Consume ingredients
        for ing_id, ing_qty in ingredients.items():
            if ing_qty > 0:
                await db.remove_from_inventory(interaction.user.id, ing_id, ing_qty)

        # Roll quality for the cooked meal
        quality = roll_quality()
        qmult = quality_multiplier(quality)

        # Apply effects
        effects = recipe_data["effects"]
        new_hunger = clamp(data["hunger"] + int(effects.get("hunger", 0) * qmult), 0, 100)
        new_health = clamp(data["health"] + int(effects.get("health", 0) * qmult), 0, 100)
        new_energy = clamp(data.get("energy", 100) - 5 + int(effects.get("energy", 0) * qmult), 0, 100)
        new_hygiene = clamp(data.get("hygiene", 100) + int(effects.get("hygiene", 0) * qmult), 0, 100)

        await db.update_user(
            interaction.user.id,
            hunger=new_hunger,
            health=new_health,
            energy=new_energy,
            hygiene=new_hygiene,
        )

        # Apply buff
        buff = recipe_data.get("buff")
        buff_text = ""
        if buff:
            buff_duration = int(buff["duration"] * qmult)
            await db.add_buff(
                interaction.user.id,
                buff["name"],
                buff["stat"],
                buff["value"],
                buff_duration,
            )
            buff_text = f"\n✨ **Buff gained:** {buff['name']} ({BUFF_TYPES.get(buff['stat'], {}).get('name', buff['stat'])}) for {buff_duration // 60} min"

        # Reputation gain
        await db.add_reputation(interaction.user.id, "chefs", 1)

        # World perturbation: cooking improves market atmosphere
        await world.perturb_location(interaction.user.id, "market", atmosphere_delta=0.03)

        # XP gain
        xp_gain = random.randint(10, 25)
        new_xp = data["xp"] + xp_gain
        new_level, leveled_up = check_level_up(new_xp, data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))
        await db.update_user(interaction.user.id, xp=new_xp, level=new_level)

        # Generate cooking narrative
        cooking_text = generate_cooking_text(quality)

        embed = success_embed(
            f"{recipe_data['emoji']} Cooking Success!",
            get_action_text("immersion", "cook", cooking_text=cooking_text, quality_emoji=quality_emoji(quality), quality_name=quality_name(quality), recipe_name=recipe_data['name'], buff_text=buff_text),
        )
        embed.add_field(name="📊 Quality", value=f"{quality_emoji(quality)} {quality_name(quality)}", inline=True)
        embed.add_field(name="⭐ XP", value=f"+{xp_gain}", inline=True)
        embed.add_field(name="👨‍🍳 +1 Culinary Circle rep", value=" ", inline=True)

        if effects.get("hunger"):
            embed.add_field(name="🍖 Hunger", value=f"+{int(effects['hunger'] * qmult)}", inline=True)
        if effects.get("health"):
            embed.add_field(name="❤️ Health", value=f"+{int(effects['health'] * qmult)}", inline=True)
        if effects.get("energy"):
            embed.add_field(name="⚡ Energy", value=f"+{int(effects['energy'] * qmult)}", inline=True)

        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"You are now level {new_level}!", inline=False)

        await interaction.response.send_message(embed=embed)

    # ─── /cookbook — View all cooking recipes ───
    @app_commands.command(name="cookbook", description="View all available cooking recipes")
    async def cookbook(self, interaction: discord.Interaction):
        embed = info_embed("📖 Cookbook", "All available cooking recipes:")
        for recipe_id, recipe in COOKING_RECIPES.items():
            ingredients = []
            for ing_id, qty in recipe["ingredients"].items():
                if qty > 0:
                    ing_name = RAW_MATERIALS.get(ing_id, {}).get("name", ing_id)
                    ingredients.append(f"{qty}x {ing_name}")
            buff = recipe.get("buff", {})
            buff_text = f" → Buff: {buff.get('name', '?')}" if buff else ""
            embed.add_field(
                name=f"{recipe['emoji']} {recipe['name']}",
                value=f"Ingredients: {', '.join(ingredients)}\nEffects: {recipe['description']}{buff_text}",
                inline=False,
            )
        await interaction.response.send_message(embed=embed)

    # ─── /buffs — View active buffs ───
    @app_commands.command(name="buffs", description="View your currently active buffs and their effects")
    async def buffs(self, interaction: discord.Interaction):
        buffs = await db.get_buffs(interaction.user.id)
        if not buffs:
            await interaction.response.send_message(embed=info_embed("✨ Active Buffs", "You have no active buffs. Cook some food to gain buffs!"))
            return

        embed = info_embed("✨ Active Buffs", f"You have {len(buffs)} active buff(s):")
        now = datetime.now(timezone.utc)
        for b in buffs:
            buff_type = BUFF_TYPES.get(b["buff_stat"], {})
            expires = datetime.fromisoformat(b["expires_at"])
            remaining = int((expires - now).total_seconds())
            mins = remaining // 60
            secs = remaining % 60
            embed.add_field(
                name=f"{b['buff_name']}",
                value=f"Type: {buff_type.get('name', b['buff_stat'])}\nValue: {b['buff_value']}\nExpires in: {mins}m {secs}s",
                inline=False,
            )
        await interaction.response.send_message(embed=embed)

    # ─── /reputation — View faction standings ───
    @app_commands.command(name="reputation", description="View your standing with all factions")
    async def reputation(self, interaction: discord.Interaction):
        rep_data = await db.get_all_reputation(interaction.user.id)

        embed = info_embed("🏆 Faction Reputation", "Your standing with the various factions:")
        for faction_id, faction in FACTIONS.items():
            rep = rep_data.get(faction_id, 0)
            benefit = await db.get_faction_benefit(interaction.user.id, faction_id)
            benefit_text = benefit.get("desc", "No benefits yet") if benefit else "No benefits yet"
            embed.add_field(
                name=f"{faction['emoji']} {faction['name']} — {rep} rep",
                value=f"{faction['description']}\nCurrent benefit: {benefit_text}",
                inline=False,
            )
        await interaction.response.send_message(embed=embed)

    # ─── /locations — View all locations ───
    @app_commands.command(name="locations", description="View all available locations to travel to")
    async def locations(self, interaction: discord.Interaction):
        embed = info_embed("🗺️ Available Locations", "Use `/travel` to visit any of these locations:")
        for loc_id, loc in LOCATIONS.items():
            npc_names = []
            for npc_id in loc.get("npcs", []):
                if npc_id in NPCS:
                    npc_names.append(NPCS[npc_id]["name"])
            npc_text = f"\nNPCs: {', '.join(npc_names)}" if npc_names else ""
            embed.add_field(
                name=f"{loc['emoji']} {loc['name']}",
                value=f"{loc['description']}\nActivities: {', '.join(loc['activities'])}{npc_text}",
                inline=False,
            )
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(ImmersionCog(bot))
