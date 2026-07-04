"""World Cog — the living world simulation listener and commands.

This cog:
1. Listens to every Discord interaction and ticks the world before processing
2. Runs a background loop that ticks every 5 minutes even without interactions
3. Provides /world command to view the current world state or inspect specific entities
"""

import discord
from discord import app_commands
from discord.ext import commands, tasks
import logging
from utils.embeds import info_embed, success_embed, error_embed
from config import NPCS, LOCATIONS, TIME_PERIODS
import world
import database as db

logger = logging.getLogger("Lifebot.WorldCog")


class WorldCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tick_count = 0

    async def cog_load(self):
        await world.init_world()
        self.world_loop.start()
        logger.info("World cog loaded — living world simulation active.")

    async def cog_unload(self):
        self.world_loop.cancel()

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        """Tick the world on every interaction. This is the heartbeat —
        every time someone talks to the bot, the entire world moves."""
        if interaction.type == discord.InteractionType.application_command:
            try:
                await world.tick_world()
                self.tick_count += 1
            except Exception as e:
                logger.warning(f"World tick on interaction failed: {e}")

    @tasks.loop(minutes=5)
    async def world_loop(self):
        """Background tick — keeps the world breathing even when nobody is interacting."""
        try:
            await world.tick_world(force=True)
        except Exception as e:
            logger.warning(f"Background world tick failed: {e}")

    @world_loop.before_loop
    async def before_world_loop(self):
        await self.bot.wait_until_ready()

    @app_commands.command(name="world", description="View the living world, or inspect a specific NPC or location")
    @app_commands.describe(view="What to view", npc="NPC to inspect (for npc view)", location="Location to inspect (for location view)")
    @app_commands.choices(view=[
        app_commands.Choice(name="🌍 Full World Overview", value="overview"),
        app_commands.Choice(name="🧑‍💼 Inspect NPC", value="npc"),
        app_commands.Choice(name="🗺️ Inspect Location", value="location"),
    ])
    @app_commands.choices(npc=[
        app_commands.Choice(name=f"{NPCS[n]['emoji']} {NPCS[n]['name']}", value=n) for n in NPCS
    ])
    @app_commands.choices(location=[
        app_commands.Choice(name=f"{LOCATIONS[l]['emoji']} {LOCATIONS[l]['name']}", value=l) for l in LOCATIONS
    ])
    async def world(self, interaction: discord.Interaction, view: str = "overview", npc: str = None, location: str = None):
        if view == "npc":
            if not npc:
                await interaction.response.send_message(embed=error_embed("Error", "Select an NPC to inspect."), ephemeral=True)
                return
            await self._world_npc(interaction, npc)
        elif view == "location":
            if not location:
                await interaction.response.send_message(embed=error_embed("Error", "Select a location to inspect."), ephemeral=True)
                return
            await self._world_location(interaction, location)
        else:
            await self._world_overview(interaction)

    async def _world_overview(self, interaction: discord.Interaction):
        # Tick the world first to get the most current state
        await world.tick_world(force=True)

        snapshot = await world.get_world_snapshot()
        gt = await db.get_game_time()
        weather = await db.get_weather()
        from config import WEATHER_STATES
        wdata = WEATHER_STATES.get(weather, {})
        period = TIME_PERIODS.get(gt["time_period"], {})
        intensity = await world.get_weather_intensity()

        embed = info_embed(
            f"🌍 The Living World",
            f"🕐 {period.get('name', '?')} (Hr {gt['game_hour']}) | 🌤️ {wdata.get('name', weather)} ({world.weather_intensity_label(intensity)})"
        )

        # Market state
        market = snapshot.get("market", {}).get("global", {})
        if market:
            demand = market.get("demand", {}).get("value", 0.5)
            vol = market.get("volatility", {}).get("value", 0.3)
            price_mult, demand_lbl = world.demand_label(demand)
            embed.add_field(
                name="🏪 Market",
                value=f"Demand: {demand_lbl} ({demand:.0%})\nVolatility: {vol:.0%}\nPrice Mod: {price_mult:.2f}x",
                inline=True,
            )

        # Weather intensity
        embed.add_field(
            name="🌬️ Weather Intensity",
            value=f"{world.weather_intensity_label(intensity)} ({intensity:.0%})",
            inline=True,
        )

        # Locations summary
        loc_lines = []
        for loc_id, loc_data in LOCATIONS.items():
            loc_state = snapshot.get("location", {}).get(loc_id, {})
            if loc_state:
                pop = loc_state.get("population", {}).get("value", 0.25)
                res = loc_state.get("resources", {}).get("value", 0.6)
                danger = loc_state.get("danger", {}).get("value", 0.1)
                loc_lines.append(
                    f"{loc_data['emoji']} {loc_data['name']}: "
                    f"{world.population_label(pop)}, {world.resources_label(res)}, {world.danger_label(danger)}"
                )
        if loc_lines:
            embed.add_field(
                name="🗺️ Locations",
                value="\n".join(loc_lines),
                inline=False,
            )

        # NPCs summary
        npc_lines = []
        for npc_id, npc_data in NPCS.items():
            npc_state = snapshot.get("npc", {}).get(npc_id, {})
            if npc_state:
                mood = npc_state.get("mood", {}).get("value", 0.5)
                stock = npc_state.get("stock", {}).get("value", 0.7)
                npc_lines.append(
                    f"{npc_data['emoji']} {npc_data['name']}: {world.mood_label(mood)}, {world.stock_label(stock)}"
                )
        if npc_lines:
            embed.add_field(
                name="🧑‍💼 NPCs",
                value="\n".join(npc_lines),
                inline=False,
            )

        embed.set_footer(text="The world moves in real time. Every interaction shifts the balance.")
        await interaction.response.send_message(embed=embed)

    async def _world_npc(self, interaction: discord.Interaction, npc_id: str):
        npc_data = NPCS.get(npc_id, {})
        state = await world.get_npc_state(npc_id)

        mood = state.get("mood", 0.5)
        stock = state.get("stock", 0.7)
        tension = state.get("tension", 0.3)

        embed = info_embed(
            f"{npc_data.get('emoji', '🧑')} {npc_data.get('name', npc_id)} — World State",
            f"Located at: {LOCATIONS.get(npc_data.get('location', ''), {}).get('name', '?')}"
        )

        embed.add_field(name="😊 Mood", value=f"{world.mood_label(mood)} ({mood:.0%})", inline=True)
        embed.add_field(name="📦 Stock", value=f"{world.stock_label(stock)} ({stock:.0%})", inline=True)
        embed.add_field(name="⚡ Tension", value=f"{world.tension_label(tension)} ({tension:.0%})", inline=True)

        # Interpret effects
        effects = []
        if mood < 0.3:
            effects.append("May offer worse trades due to bad mood")
        elif mood > 0.7:
            effects.append("May offer better trades due to good mood")
        if stock < 0.2:
            effects.append("Running low on goods — trades may be refused")
        if tension > 0.6:
            effects.append("High tension — quests may be harder")

        if effects:
            embed.add_field(name="📋 Effects", value="\n".join(effects), inline=False)

        embed.set_footer(text="These values drift toward normal over time. Interacting shifts them.")
        await interaction.response.send_message(embed=embed)

    async def _world_location(self, interaction: discord.Interaction, loc_id: str):
        loc_data = LOCATIONS.get(loc_id, {})
        state = await world.get_location_state(loc_id)

        pop = state.get("population", 0.25)
        danger = state.get("danger", 0.1)
        res = state.get("resources", 0.6)
        atmos = state.get("atmosphere", 0.5)

        embed = info_embed(
            f"{loc_data.get('emoji', '🗺️')} {loc_data.get('name', loc_id)} — World State",
            loc_data.get("description", "")
        )

        embed.add_field(name="👥 Population", value=f"{world.population_label(pop)} ({pop:.0%})", inline=True)
        embed.add_field(name="⚠️ Danger", value=f"{world.danger_label(danger)} ({danger:.0%})", inline=True)
        embed.add_field(name="💎 Resources", value=f"{world.resources_label(res)} ({res:.0%})", inline=True)
        embed.add_field(name="🎭 Atmosphere", value=f"{world.atmosphere_label(atmos)} ({atmos:.0%})", inline=True)

        # Interpret effects
        effects = []
        if res < 0.2:
            effects.append("Resources depleted — fewer items found")
        elif res > 0.8:
            effects.append("Resources abundant — better loot rolls")
        if danger > 0.4:
            effects.append("High danger — increased HP risk")
        if pop > 0.7:
            effects.append("Crowded — more NPC encounters, more competition")
        elif pop < 0.1:
            effects.append("Deserted — fewer encounters, eerie atmosphere")
        if atmos > 0.7:
            effects.append("Vibrant atmosphere — bonus XP from activities")
        elif atmos < 0.2:
            effects.append("Gloomy atmosphere — reduced energy from activities")

        if effects:
            embed.add_field(name="📋 Effects", value="\n".join(effects), inline=False)

        embed.set_footer(text="Resources deplete as players gather. They regenerate over real time.")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(WorldCog(bot))
