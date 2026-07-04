import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN", "")
DB_PATH = os.getenv("DB_PATH", "lifebot.db")
PREFIX = os.getenv("PREFIX", "!")

BOT_DESCRIPTION = "A full-featured Discord economy & survival bot with jobs, gambling, pets, quests, and more!"

STARTING_WALLET = 200
STARTING_BANK_CAPACITY = 5000

HEALTH_MAX = 100
HUNGER_MAX = 100
THIRST_MAX = 100
ENERGY_MAX = 100
HYGIENE_MAX = 100

DECAY_INTERVAL = 240  # seconds between survival stat decay ticks
DECAY_AMOUNT = 3      # hunger/thirst lost per tick
ENERGY_DECAY = 2      # energy lost per tick
HYGIENE_DECAY = 2     # hygiene lost per tick
HEALTH_DAMAGE_FROM_STARVATION = 5  # health lost when hunger or thirst is 0
ENERGY_DAMAGE_FROM_EXHAUSTION = 3  # health lost when energy is 0
HYGIENE_DAMAGE_FROM_FILTH = 2     # health lost when hygiene is 0

HOSPITAL_FEE_PERCENT = 0.5  # lose 50% of unbanked wallet money on hospital wakeup

XP_PER_LEVEL = 2000
XP_MULTIPLIER = 1.0

CURRENCY = "coins"
CURRENCY_SYMBOL = "🪙"
