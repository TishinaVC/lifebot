import asyncio
import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
import database as db
from config import PREFIX, BOT_DESCRIPTION

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("Lifebot")

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    logger.error("No DISCORD_TOKEN found in environment. Copy .env.example to .env and fill in your token.")
    raise SystemExit(1)

COGS = [
    "cogs.core",
    "cogs.economy",
    "cogs.jobs",
    "cogs.gambling",
    "cogs.store",
    "cogs.survival",
    "cogs.leveling",
    "cogs.daily",
    "cogs.crime",
    "cogs.social",
    "cogs.pets",
    "cogs.achievements",
    "cogs.quests",
    "cogs.housing",
    "cogs.weather",
    "cogs.activities",
    "cogs.immersion",
    "cogs.world",
    "cogs.chase",
    "cogs.stats",
    "cogs.coop",
    "cogs.poker",
]

GUILD_ID = os.getenv("GUILD_ID")


class Lifebot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(PREFIX),
            description=BOT_DESCRIPTION,
            intents=discord.Intents.all(),
            help_command=None,
        )

    async def setup_hook(self):
        await db.init_db()
        logger.info("Database initialized.")
        for cog in COGS:
            try:
                await self.load_extension(cog)
                logger.info(f"Loaded cog: {cog}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog}: {e}")

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logger.info(f"Connected to {len(self.guilds)} guild(s).")
        await self.tree.sync()
        logger.info("Slash commands synced globally.")
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.playing, name="Lifebot | /help"),
            status=discord.Status.online,
        )


bot = Lifebot()


if __name__ == "__main__":
    bot.run(TOKEN)
