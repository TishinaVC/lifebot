"""Living World Engine — a persistent simulation where every entity has vectors
that drift toward normality (mean reversion), get perturbed by player interactions,
and tick in sync with real time.

Each vector has:
  - value: current state (0.0 to 1.0 typically)
  - normal: equilibrium target it drifts toward
  - velocity: momentum from recent perturbations
  - drift_rate: how fast it returns to normal (per hour of real time)
  - volatility: random noise magnitude per tick
  - min_val / max_val: bounds

On every interaction (someone talks to the bot), the world ticks:
  1. Real seconds since last tick are calculated
  2. Each vector drifts toward normal: value += (normal - value) * drift_rate * time_factor
  3. Random noise is added: value += gauss(0, volatility) * sqrt(time_factor)
  4. Pending perturbations from interactions are applied
  5. Velocity decays
  6. Results are persisted

This means the world is always moving, always breathing — even when nobody is watching.
When someone interacts, they see a snapshot of a world that has been evolving in real time."""

import random
import math
import logging
from datetime import datetime, timezone
from config import NPCS, LOCATIONS, WEATHER_STATES
import database as db

logger = logging.getLogger("Lifebot.World")

# Time factor: 1 hour of real time = 1.0 drift cycle
# This means vectors fully revert to normal in ~6-7 hours of real time
TIME_NORMALIZATION = 3600.0  # seconds per "full drift unit"

# Tick cooldown — don't tick more than once per 30 seconds even if many interactions
MIN_TICK_INTERVAL = 30.0

_last_tick = None
_initialized = False


async def init_world():
    """Initialize world vectors from config if they don't exist yet."""
    global _initialized
    if _initialized:
        return

    existing = await db.get_all_world_vectors()
    existing_keys = {(v["entity_type"], v["entity_id"], v["vector_name"]) for v in existing}

    vectors_to_create = []

    # NPC vectors: mood, stock, tension
    for npc_id in NPCS:
        for vname, config in _NPC_VECTOR_DEFS.items():
            key = ("npc", npc_id, vname)
            if key not in existing_keys:
                vectors_to_create.append({
                    "entity_type": "npc", "entity_id": npc_id, "vector_name": vname,
                    "value": config["normal"], "normal": config["normal"],
                    "velocity": 0, "drift_rate": config["drift_rate"],
                    "volatility": config["volatility"],
                    "min_val": config["min"], "max_val": config["max"],
                })

    # Location vectors: population, danger, resources, atmosphere
    for loc_id, loc_data in LOCATIONS.items():
        for vname, config in _LOCATION_VECTOR_DEFS.items():
            key = ("location", loc_id, vname)
            if key not in existing_keys:
                # Use location-specific normals where available
                normal = config["normal"]
                if vname == "danger":
                    normal = loc_data.get("danger", 0.1)
                elif vname == "population":
                    normal = 0.3 if loc_data.get("npcs") else 0.15
                vectors_to_create.append({
                    "entity_type": "location", "entity_id": loc_id, "vector_name": vname,
                    "value": normal, "normal": normal,
                    "velocity": 0, "drift_rate": config["drift_rate"],
                    "volatility": config["volatility"],
                    "min_val": config["min"], "max_val": config["max"],
                })

    # Global market vectors: demand, volatility
    for vname, config in _MARKET_VECTOR_DEFS.items():
        key = ("market", "global", vname)
        if key not in existing_keys:
            vectors_to_create.append({
                "entity_type": "market", "entity_id": "global", "vector_name": vname,
                "value": config["normal"], "normal": config["normal"],
                "velocity": 0, "drift_rate": config["drift_rate"],
                "volatility": config["volatility"],
                "min_val": config["min"], "max_val": config["max"],
            })

    # Global weather vector: intensity
    for vname, config in _WEATHER_VECTOR_DEFS.items():
        key = ("weather", "global", vname)
        if key not in existing_keys:
            vectors_to_create.append({
                "entity_type": "weather", "entity_id": "global", "vector_name": vname,
                "value": config["normal"], "normal": config["normal"],
                "velocity": 0, "drift_rate": config["drift_rate"],
                "volatility": config["volatility"],
                "min_val": config["min"], "max_val": config["max"],
            })

    if vectors_to_create:
        await db.bulk_upsert_world_vectors(vectors_to_create)
        logger.info(f"World initialized with {len(vectors_to_create)} vectors across "
                     f"{len(NPCS)} NPCs, {len(LOCATIONS)} locations, market, and weather.")

    _initialized = True


# ─── Vector definitions ───────────────────────────────────────────

_NPC_VECTOR_DEFS = {
    "mood":      {"normal": 0.5, "drift_rate": 0.20, "volatility": 0.04, "min": 0.0, "max": 1.0},
    "stock":     {"normal": 0.7, "drift_rate": 0.15, "volatility": 0.03, "min": 0.0, "max": 1.0},
    "tension":   {"normal": 0.3, "drift_rate": 0.25, "volatility": 0.05, "min": 0.0, "max": 1.0},
}

_LOCATION_VECTOR_DEFS = {
    "population":  {"normal": 0.25, "drift_rate": 0.12, "volatility": 0.05, "min": 0.0, "max": 1.0},
    "danger":      {"normal": 0.15, "drift_rate": 0.10, "volatility": 0.03, "min": 0.0, "max": 1.0},
    "resources":   {"normal": 0.60, "drift_rate": 0.08, "volatility": 0.02, "min": 0.0, "max": 1.0},
    "atmosphere":  {"normal": 0.50, "drift_rate": 0.18, "volatility": 0.06, "min": 0.0, "max": 1.0},
}

_MARKET_VECTOR_DEFS = {
    "demand":      {"normal": 0.50, "drift_rate": 0.15, "volatility": 0.04, "min": 0.0, "max": 1.0},
    "volatility":  {"normal": 0.30, "drift_rate": 0.20, "volatility": 0.03, "min": 0.0, "max": 1.0},
}

_WEATHER_VECTOR_DEFS = {
    "intensity":   {"normal": 0.50, "drift_rate": 0.25, "volatility": 0.08, "min": 0.0, "max": 1.0},
}


# ─── Core tick engine ─────────────────────────────────────────────

async def tick_world(force: bool = False) -> dict:
    """Advance the world simulation. Called on every interaction and by the background loop.

    Returns a dict with tick stats: elapsed_seconds, vectors_updated, interactions_applied.
    """
    global _last_tick

    now = datetime.now(timezone.utc)
    now_iso = now.isoformat()

    # Get last tick time
    last_tick_str = await db.get_last_tick_time()
    if last_tick_str:
        try:
            last_tick_dt = datetime.fromisoformat(last_tick_str)
            elapsed = (now - last_tick_dt).total_seconds()
        except Exception:
            elapsed = 300.0  # default to 5 min if parse fails
    else:
        elapsed = 0.0
        last_tick_dt = now

    # Don't tick too frequently unless forced
    if not force and elapsed < MIN_TICK_INTERVAL:
        return {"elapsed_seconds": 0, "vectors_updated": 0, "interactions_applied": 0, "skipped": True}

    # Time factor: how many "drift units" have passed
    time_factor = min(elapsed / TIME_NORMALIZATION, 2.0)  # cap at 2x for long gaps
    sqrt_tf = math.sqrt(max(time_factor, 0.01))

    # Get all vectors
    all_vectors = await db.get_all_world_vectors()
    if not all_vectors:
        await init_world()
        all_vectors = await db.get_all_world_vectors()

    # Get pending interactions since last tick
    pending = await db.get_pending_interactions(last_tick_str) if last_tick_str else []
    # Group perturbations by vector key
    perturbations = {}
    for p in pending:
        key = (p["entity_type"], p["entity_id"], p["vector_name"])
        perturbations[key] = perturbations.get(key, 0) + p["delta"]

    updated = 0
    updates = []

    for v in all_vectors:
        value = v["value"]
        normal = v["normal"]
        velocity = v.get("velocity", 0)
        drift_rate = v.get("drift_rate", 0.15)
        volatility = v.get("volatility", 0.03)
        min_val = v.get("min_val", 0.0)
        max_val = v.get("max_val", 1.0)

        # 1. Mean reversion: drift toward normal
        drift = (normal - value) * drift_rate * time_factor

        # 2. Apply velocity (momentum from past perturbations)
        momentum = velocity * time_factor * 0.5  # velocity decays

        # 3. Random noise (volatility)
        noise = random.gauss(0, volatility) * sqrt_tf

        # 4. Apply pending perturbations
        key = (v["entity_type"], v["entity_id"], v["vector_name"])
        perturb = perturbations.get(key, 0)

        # Calculate new value
        new_value = value + drift + momentum + noise + perturb

        # Clamp to bounds
        new_value = max(min_val, min(max_val, new_value))

        # Update velocity: perturbations add velocity, drift reduces it
        new_velocity = (velocity + perturb * 2) * (1 - drift_rate * time_factor)
        new_velocity = max(-0.5, min(0.5, new_velocity))  # clamp velocity

        if abs(new_value - value) > 0.001 or abs(new_velocity - velocity) > 0.001 or perturb != 0:
            updates.append({
                "entity_type": v["entity_type"],
                "entity_id": v["entity_id"],
                "vector_name": v["vector_name"],
                "value": new_value,
                "normal": normal,
                "velocity": new_velocity,
                "drift_rate": drift_rate,
                "volatility": volatility,
                "min_val": min_val,
                "max_val": max_val,
            })
            updated += 1

    if updates:
        await db.bulk_upsert_world_vectors(updates)

    # Clear processed interactions
    if last_tick_str:
        await db.clear_interactions_before(now_iso)

    # Log the tick
    await db.log_world_tick(elapsed, len(pending), updated)

    _last_tick = now_iso

    result = {
        "elapsed_seconds": elapsed,
        "vectors_updated": updated,
        "interactions_applied": len(pending),
        "time_factor": time_factor,
        "skipped": False,
    }
    logger.debug(f"World tick: {result}")
    return result


# ─── Perturbation API ─────────────────────────────────────────────

async def perturb(user_id: int, entity_type: str, entity_id: str, vector_name: str, delta: float):
    """Perturb a world vector by delta. The perturbation is queued and applied on the next tick.
    Also immediately adjusts the stored value for responsiveness."""
    await db.log_world_interaction(user_id, entity_type, entity_id, vector_name, delta)

    # Also immediately nudge the value for instant feedback
    v = await db.get_world_vector(entity_type, entity_id, vector_name)
    if v:
        new_val = max(v["min_val"], min(v["max_val"], v["value"] + delta))
        new_vel = v.get("velocity", 0) + delta * 2
        new_vel = max(-0.5, min(0.5, new_vel))
        await db.upsert_world_vector(
            entity_type, entity_id, vector_name,
            new_val, v["normal"], new_vel,
            v.get("drift_rate", 0.15), v.get("volatility", 0.03),
            v.get("min_val", 0.0), v.get("max_val", 1.0),
        )


async def perturb_npc(user_id: int, npc_id: str, mood_delta: float = 0, stock_delta: float = 0, tension_delta: float = 0):
    """Convenience: perturb multiple NPC vectors at once."""
    if mood_delta:
        await perturb(user_id, "npc", npc_id, "mood", mood_delta)
    if stock_delta:
        await perturb(user_id, "npc", npc_id, "stock", stock_delta)
    if tension_delta:
        await perturb(user_id, "npc", npc_id, "tension", tension_delta)


async def perturb_location(user_id: int, loc_id: str, population_delta: float = 0,
                           danger_delta: float = 0, resources_delta: float = 0, atmosphere_delta: float = 0):
    """Convenience: perturb multiple location vectors at once."""
    if population_delta:
        await perturb(user_id, "location", loc_id, "population", population_delta)
    if danger_delta:
        await perturb(user_id, "location", loc_id, "danger", danger_delta)
    if resources_delta:
        await perturb(user_id, "location", loc_id, "resources", resources_delta)
    if atmosphere_delta:
        await perturb(user_id, "location", loc_id, "atmosphere", atmosphere_delta)


async def perturb_market(user_id: int, demand_delta: float = 0, volatility_delta: float = 0):
    """Convenience: perturb market vectors."""
    if demand_delta:
        await perturb(user_id, "market", "global", "demand", demand_delta)
    if volatility_delta:
        await perturb(user_id, "market", "global", "volatility", volatility_delta)


# ─── Read API ─────────────────────────────────────────────────────

async def get_npc_state(npc_id: str) -> dict:
    """Get all vectors for an NPC as a simple dict: {vector_name: value}."""
    vectors = await db.get_world_vectors("npc", npc_id)
    return {v["vector_name"]: v["value"] for v in vectors}


async def get_location_state(loc_id: str) -> dict:
    """Get all vectors for a location as a simple dict."""
    vectors = await db.get_world_vectors("location", loc_id)
    return {v["vector_name"]: v["value"] for v in vectors}


async def get_market_state() -> dict:
    """Get market vectors."""
    vectors = await db.get_world_vectors("market", "global")
    return {v["vector_name"]: v["value"] for v in vectors}


async def get_weather_intensity() -> float:
    """Get current weather intensity vector."""
    v = await db.get_world_vector("weather", "global", "intensity")
    return v["value"] if v else 0.5


async def get_world_snapshot() -> dict:
    """Get a full snapshot of the world state, grouped by entity."""
    all_vectors = await db.get_all_world_vectors()
    snapshot = {}
    for v in all_vectors:
        etype = v["entity_type"]
        eid = v["entity_id"]
        if etype not in snapshot:
            snapshot[etype] = {}
        if eid not in snapshot[etype]:
            snapshot[etype][eid] = {}
        snapshot[etype][eid][v["vector_name"]] = {
            "value": v["value"],
            "normal": v["normal"],
            "velocity": v.get("velocity", 0),
        }
    return snapshot


# ─── Interpretation helpers ───────────────────────────────────────

def mood_label(mood: float) -> str:
    """Convert mood vector (0-1) to a text label."""
    if mood < 0.15:
        return "furious"
    elif mood < 0.30:
        return "irritated"
    elif mood < 0.45:
        return "unsettled"
    elif mood < 0.55:
        return "neutral"
    elif mood < 0.70:
        return "content"
    elif mood < 0.85:
        return "cheerful"
    else:
        return "elated"


def stock_label(stock: float) -> str:
    """Convert stock vector (0-1) to a text label."""
    if stock < 0.15:
        return "nearly empty"
    elif stock < 0.35:
        return "running low"
    elif stock < 0.65:
        return "well-stocked"
    else:
        return "overflowing"


def tension_label(tension: float) -> str:
    """Convert tension vector (0-1) to a text label."""
    if tension < 0.15:
        return "relaxed"
    elif tension < 0.30:
        return "calm"
    elif tension < 0.50:
        return "wary"
    elif tension < 0.70:
        return "tense"
    else:
        return "on edge"


def population_label(pop: float) -> str:
    """Convert population vector (0-1) to a text label."""
    if pop < 0.10:
        return "deserted"
    elif pop < 0.25:
        return "quiet"
    elif pop < 0.45:
        return "sparse"
    elif pop < 0.65:
        return "moderate"
    elif pop < 0.80:
        return "busy"
    else:
        return "bustling"


def danger_label(danger: float) -> str:
    """Convert danger vector (0-1) to a text label."""
    if danger < 0.05:
        return "safe"
    elif danger < 0.15:
        return "low risk"
    elif danger < 0.30:
        return "moderate risk"
    elif danger < 0.50:
        return "dangerous"
    else:
        return "perilous"


def resources_label(resources: float) -> str:
    """Convert resources vector (0-1) to a text label."""
    if resources < 0.15:
        return "depleted"
    elif resources < 0.35:
        return "scarce"
    elif resources < 0.60:
        return "available"
    elif resources < 0.80:
        return "abundant"
    else:
        return "teeming"


def atmosphere_label(atmos: float) -> str:
    """Convert atmosphere vector (0-1) to a text label."""
    if atmos < 0.20:
        return "gloomy"
    elif atmos < 0.35:
        return "somber"
    elif atmos < 0.50:
        return "mellow"
    elif atmos < 0.65:
        return "lively"
    elif atmos < 0.80:
        return "vibrant"
    else:
        return "electric"


def demand_label(demand: float) -> str:
    """Convert market demand (0-1) to a price multiplier and label."""
    if demand < 0.25:
        return 0.85, "buyer's market"
    elif demand < 0.45:
        return 0.95, "slow trade"
    elif demand < 0.55:
        return 1.0, "stable"
    elif demand < 0.75:
        return 1.10, "high demand"
    else:
        return 1.25, "seller's market"


def weather_intensity_label(intensity: float) -> str:
    """Convert weather intensity (0-1) to a label."""
    if intensity < 0.25:
        return "mild"
    elif intensity < 0.50:
        return "moderate"
    elif intensity < 0.75:
        return "strong"
    else:
        return "extreme"
