"""Police chase system — heat tracking, tailing hints, and chase state management.

This module provides the core logic for the police evasion minigame.
It follows the same pattern as world.py — a root-level module imported by cogs.

Heat System:
    - Crimes add heat (tracked in police_heat table)
    - Heat decays over time via background loop
    - At HEAT_TAILING_THRESHOLD, police may start tailing during activities
    - At HEAT_WARRANT_THRESHOLD, a warrant is issued (guaranteed arrest attempt)

Tailing System:
    - 3 escalating stages of narrator hints
    - Stage 1: Subtle environmental clues (appended to activity results)
    - Stage 2: Obvious police presence (appended to activity results)
    - Stage 3: Arrest attempt (interactive comply/run buttons)
    - Traveling to a new location clears tailing

Chase Minigame:
    - Multi-stage text adventure with button choices
    - Escape chance based on stats, choices, and help from other players
    - Outcomes: escape, caught, injured escape, injured & caught
"""

import random
import database as db
from config.police import (
    HEAT_TAILING_THRESHOLD,
    HEAT_WARRANT_THRESHOLD,
    HEAT_MAX,
    TAILING_CHANCE_BASE,
    TAILING_CHANCE_HEAT_SCALE,
    TAILING_INTERACTIONS_TO_ESCALATE,
    TAILING_HINTS,
    ARREST_NARRATIVES,
    CHASE_STAGES,
    CHASE_OUTCOMES,
    HELP_ACTIONS,
    ESCAPE_BASE_CHANCE,
    ESCAPE_ENERGY_BONUS,
    ESCAPE_HEALTH_BONUS,
    ESCAPE_LEVEL_BONUS,
    ESCAPE_HELP_BONUS,
    ESCAPE_HELP_MAX,
    ESCAPE_HEAT_PENALTY,
    CHASE_ENERGY_COST_PER_STAGE,
    CHASE_HEALTH_RISK_BASE,
    CHASE_HEALTH_RISK_MAX,
    FINE_PER_HEAT,
    JAIL_COOLDOWN_BASE,
    JAIL_COOLDOWN_PER_HEAT,
    JAIL_COOLDOWN_MAX,
    WARRANT_NOTICES,
)
from utils.helpers import clamp
from config import HEALTH_MAX, ENERGY_MAX


# ============================================================
# HEAT MANAGEMENT
# ============================================================

async def add_crime_heat(user_id: int, crime_type: str):
    """Add heat after a crime is committed."""
    from config.police import HEAT_PER_CRIME
    amount = HEAT_PER_CRIME.get(crime_type, 10)
    await db.add_heat(user_id, amount)


async def decay_heat():
    """Decay all players' heat. Called by background loop."""
    await db.decay_all_heat()


async def get_heat(user_id: int) -> int:
    """Get a player's current heat level."""
    state = await db.get_police_state(user_id)
    return state["heat"] if state else 0


async def has_warrant(user_id: int) -> bool:
    """Check if a warrant is active for this player."""
    state = await db.get_police_state(user_id)
    return bool(state and state["warrant_active"])


# ============================================================
# TAILING SYSTEM
# ============================================================

async def check_tailing(user_id: int, location_id: str) -> dict | None:
    """Check if police should start or escalate tailing during an activity.

    Called by activity commands after their main logic.
    Returns a dict with hint text to append to the activity embed, or None.

    Return dict format:
        {"type": "hint"|"arrest", "text": str, "stage": int}
    """
    state = await db.get_police_state(user_id)
    if state is None:
        return None

    heat = state["heat"]
    current_stage = state["tailing_stage"]
    tailing_location = state.get("tailing_location")
    warrant = bool(state.get("warrant_active", 0))

    # If warrant is active, force arrest attempt
    if warrant and current_stage < 3:
        await db.set_tailing(user_id, 3, location_id)
        return {
            "type": "arrest",
            "text": random.choice(ARREST_NARRATIVES),
            "stage": 3,
        }

    # No tailing yet — check if police should start
    if current_stage == 0:
        if heat < HEAT_TAILING_THRESHOLD:
            return None

        # Roll for tailing chance
        chance = TAILING_CHANCE_BASE + (heat - HEAT_TAILING_THRESHOLD) * TAILING_CHANCE_HEAT_SCALE
        if random.random() > chance:
            return None

        # Start tailing at stage 1
        await db.set_tailing(user_id, 1, location_id)
        return {
            "type": "hint",
            "text": random.choice(TAILING_HINTS[1]),
            "stage": 1,
        }

    # Already being tailed — check if location changed
    if tailing_location and tailing_location != location_id:
        # Player moved to a new area — they shook the tail
        await db.clear_tailing(user_id)
        # Reduce heat slightly for successfully evading
        await db.reduce_heat(user_id, 10)
        return {
            "type": "hint",
            "text": "You've moved to a new area. For now, it seems like you've shaken whoever was watching you.",
            "stage": 0,
        }

    # Same location — escalate
    interactions = await db.increment_tailing_interactions(user_id)
    new_stage = current_stage + 1 if interactions >= TAILING_INTERACTIONS_TO_ESCALATE else current_stage

    if new_stage >= 3:
        # Arrest attempt!
        await db.set_tailing(user_id, 3, location_id)
        return {
            "type": "arrest",
            "text": random.choice(ARREST_NARRATIVES),
            "stage": 3,
        }
    elif new_stage > current_stage:
        # Escalate to next hint stage
        await db.set_tailing(user_id, new_stage, location_id)
        return {
            "type": "hint",
            "text": random.choice(TAILING_HINTS[new_stage]),
            "stage": new_stage,
        }
    else:
        # Same stage, another hint
        return {
            "type": "hint",
            "text": random.choice(TAILING_HINTS[current_stage]),
            "stage": current_stage,
        }


async def clear_tailing_on_travel(user_id: int, new_location: str):
    """Called when a player travels — clears tailing if they were being followed."""
    state = await db.get_police_state(user_id)
    if state and state["tailing_stage"] > 0:
        old_location = state.get("tailing_location")
        if old_location and old_location != new_location:
            await db.clear_tailing(user_id)
            await db.reduce_heat(user_id, 10)
            return True
    return False


# ============================================================
# WARRANT SYSTEM
# ============================================================

async def check_warrant_eligible(user_id: int) -> bool:
    """Check if a warrant should be issued (heat >= warrant threshold)."""
    heat = await get_heat(user_id)
    if heat >= HEAT_WARRANT_THRESHOLD:
        state = await db.get_police_state(user_id)
        if state and not state.get("warrant_active"):
            await db.set_warrant(user_id, True)
            return True
    return False


async def get_warrant_notice(user_id: int) -> str | None:
    """Get a warrant notice if one is active."""
    if await has_warrant(user_id):
        return random.choice(WARRANT_NOTICES)
    return None


# ============================================================
# CHASE MINIGAME — Escape chance calculation
# ============================================================

async def calculate_escape_chance(user_id: int, user_data: dict, choice_mod: float, helpers: int) -> float:
    """Calculate the probability of escaping the chase.

    Factors:
        - Base chance
        - Energy level
        - Health level
        - Player level
        - Choice modifier (from chase stage choice)
        - Helper bonus (other players assisting)
        - Heat penalty
    """
    energy = user_data.get("energy", 100)
    health = user_data.get("health", 100)
    level = user_data.get("level", 1)
    heat = await get_heat(user_id)

    energy_bonus = (energy / ENERGY_MAX) * ESCAPE_ENERGY_BONUS
    health_bonus = (health / HEALTH_MAX) * ESCAPE_HEALTH_BONUS
    level_bonus = min(level / 50, 1.0) * ESCAPE_LEVEL_BONUS
    help_bonus = min(helpers, ESCAPE_HELP_MAX) * ESCAPE_HELP_BONUS
    heat_penalty = max(0, heat - HEAT_TAILING_THRESHOLD) * ESCAPE_HEAT_PENALTY

    chance = (
        ESCAPE_BASE_CHANCE
        + energy_bonus
        + health_bonus
        + level_bonus
        + help_bonus
        + choice_mod
        - heat_penalty
    )

    return clamp(chance, 0.05, 0.95)


async def calculate_fine(user_id: int) -> int:
    """Calculate the fine if caught."""
    heat = await get_heat(user_id)
    return heat * FINE_PER_HEAT


async def calculate_jail_cooldown(user_id: int) -> int:
    """Calculate jail cooldown if caught."""
    heat = await get_heat(user_id)
    return min(JAIL_COOLDOWN_BASE + heat * JAIL_COOLDOWN_PER_HEAT, JAIL_COOLDOWN_MAX)


async def apply_chase_outcome(user_id: int, outcome: str, health_loss: int, energy_loss: int):
    """Apply the outcome of a chase to the player's stats."""
    user_data = await db.get_user(user_id)
    if user_data is None:
        return

    new_health = clamp(user_data["health"] - health_loss, 0, HEALTH_MAX)
    new_energy = clamp(user_data.get("energy", 100) - energy_loss, 0, ENERGY_MAX)

    if outcome in ("caught", "injured_caught"):
        fine = await calculate_fine(user_id)
        if fine > user_data["wallet"]:
            fine = user_data["wallet"]
        jail_time = await calculate_jail_cooldown(user_id)
        await db.update_user(
            user_id,
            health=new_health,
            energy=new_energy,
            wallet=user_data["wallet"] - fine,
            total_lost=user_data["total_lost"] + fine,
        )
        await db.add_transaction(user_id, "police_fine", fine, "Police fine after chase")
        await db.set_cooldown(user_id, "jail", jail_time)
        await db.reset_heat(user_id)
        return {"fine": fine, "jail_time": jail_time}
    elif outcome == "escape":
        # Small money loss (dropped while running)
        dropped = min(random.randint(20, 100), user_data["wallet"])
        await db.update_user(
            user_id,
            health=new_health,
            energy=new_energy,
            wallet=user_data["wallet"] - dropped,
            total_lost=user_data["total_lost"] + dropped,
        )
        if dropped > 0:
            await db.add_transaction(user_id, "chase_loss", dropped, "Dropped while fleeing police")
        await db.reset_heat(user_id)
        # Reward XP for escaping
        xp_gain = random.randint(30, 60)
        from utils.helpers import check_level_up, xp_for_next_level
        new_xp = user_data["xp"] + xp_gain
        new_level, leveled_up = check_level_up(new_xp, user_data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(user_data["level"], new_level))
        await db.update_user(user_id, xp=new_xp, level=new_level)
        await db.add_reputation(user_id, "underworld", 5)
        return {"dropped": dropped, "xp": xp_gain, "leveled_up": leveled_up, "new_level": new_level}
    elif outcome == "injured_escape":
        await db.update_user(
            user_id,
            health=new_health,
            energy=new_energy,
        )
        # Reduce heat but don't fully clear
        await db.reduce_heat(user_id, 30)
        await db.clear_tailing(user_id)
        await db.add_reputation(user_id, "underworld", 3)
        return {"health_loss": health_loss}


# ============================================================
# CHASE STAGE DATA
# ============================================================

def get_chase_stage(stage_num: int) -> dict:
    """Get the chase stage data for a given stage number (1-3)."""
    return CHASE_STAGES.get(stage_num, {})


def get_stage_narrative(stage_num: int, prev_choice_key: str | None = None) -> str:
    """Get narrative text for a chase stage."""
    stage = CHASE_STAGES.get(stage_num, {})
    if stage_num == 2 and prev_choice_key:
        narratives = stage.get("narratives", {})
        if isinstance(narratives, dict):
            texts = narratives.get(prev_choice_key, stage.get("narratives", {}).get("alleys", ["..."]))
            return random.choice(texts)
    narratives = stage.get("narratives", [])
    if isinstance(narratives, list):
        return random.choice(narratives)
    return "..."


def get_outcome_text(outcome: str) -> str:
    """Get narrative text for a chase outcome."""
    texts = CHASE_OUTCOMES.get(outcome, ["The chase ends."])
    return random.choice(texts)


def get_help_action(action_id: str) -> dict | None:
    """Get a help action by ID."""
    for action in HELP_ACTIONS:
        if action["id"] == action_id:
            return action
    return None
