"""Weather system cog — dynamic weather that changes every 30 minutes and affects all gameplay.
Includes a background loop that rotates weather states and a /weather command."""

import discord
from discord import app_commands
from discord.ext import commands, tasks
import random
from datetime import datetime, timezone, timedelta
import database as db
import world
from utils.embeds import success_embed, error_embed, info_embed
from config import WEATHER_STATES, WEATHER_INTERVAL


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.weather_loop.start()

    def cog_unload(self):
        self.weather_loop.cancel()

    @tasks.loop(seconds=WEATHER_INTERVAL)
    async def weather_loop(self):
        """Change weather every interval using weighted random selection."""
        states = list(WEATHER_STATES.items())
        total_weight = sum(s["weight"] for _, s in states)
        roll = random.randint(1, total_weight)
        cumulative = 0
        new_weather = "sunny"
        for wid, wdata in states:
            cumulative += wdata["weight"]
            if roll <= cumulative:
                new_weather = wid
                break
        next_change = (datetime.now(timezone.utc) + timedelta(seconds=WEATHER_INTERVAL)).isoformat()
        await db.set_weather(new_weather, next_change)

        # World perturbation: weather change shifts intensity vector
        intensity_map = {
            "sunny": -0.15, "cloudy": -0.05, "rainy": 0.10,
            "stormy": 0.25, "snowy": 0.15, "foggy": 0.05,
            "windy": 0.08, "heatwave": 0.20,
        }
        delta = intensity_map.get(new_weather, 0)
        if delta:
            await world.perturb(0, "weather", "global", "intensity", delta)

    @weather_loop.before_loop
    async def before_weather_loop(self):
        await self.bot.wait_until_ready()
        current = await db.get_weather()
        if not current:
            await db.set_weather("sunny")

    @app_commands.command(name="weather", description="Check the current weather and its effects")
    async def weather(self, interaction: discord.Interaction):
        current = await db.get_weather()
        wdata = WEATHER_STATES.get(current, WEATHER_STATES["sunny"])
        effects = wdata["effects"]

        embed = info_embed(f"{wdata['name']} — Current Weather", wdata["description"])

        effect_text = []
        if effects.get("energy_decay_mult", 1.0) != 1.0:
            pct = int((effects["energy_decay_mult"] - 1.0) * 100)
            effect_text.append(f"⚡ Energy decay: {'+' if pct > 0 else ''}{pct}%")
        if effects.get("hygiene_decay_mult", 1.0) != 1.0:
            pct = int((effects["hygiene_decay_mult"] - 1.0) * 100)
            effect_text.append(f"🧼 Hygiene decay: {'+' if pct > 0 else ''}{pct}%")
        if effects.get("work_pay_mult", 1.0) != 1.0:
            pct = int((effects["work_pay_mult"] - 1.0) * 100)
            effect_text.append(f"💼 Work pay: {'+' if pct > 0 else ''}{pct}%")
        if effects.get("crime_success_mult", 1.0) != 1.0:
            pct = int((effects["crime_success_mult"] - 1.0) * 100)
            effect_text.append(f"🦹 Crime success: {'+' if pct > 0 else ''}{pct}%")

        embed.add_field(name="📊 Effects", value="\n".join(effect_text) if effect_text else "No special effects", inline=False)
        embed.add_field(name="👕 Tip", value="Wear weather-appropriate clothing to mitigate negative effects!", inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Weather(bot))
