"""
Procedural minigame content generator — pure Python, no external dependencies.
Generates unique scenarios each playthrough by combining job-specific templates
with randomized variables (names, numbers, locations, twists).

This replaces the Ollama LLM approach with a purpose-built generator that's
fast, self-contained, and produces infinite variety.
"""
import random
import re

from config.jobs import JOBS
from config.job_flavor import SUBCATEGORY_FLAVOR

# ═══════════════════════════════════════════════════════════════
# Shared random element pools
# ═══════════════════════════════════════════════════════════════

_NAMES = ["Sarah", "Mike", "Jenny", "Carlos", "Aisha", "Tom", "Lisa", "Dave",
          "Priya", "Jake", "Emma", "Luis", "Nora", "Rick", "Maya", "Ben",
          "Yuki", "Omar", "Zoe", "Frank", "Hana", "Leo", "Iris", "Sam"]

_LOCATIONS = ["the main entrance", "aisle 3", "the loading dock", "the back office",
              "the break room", "the front counter", "the storage room", "the roof",
              "the parking lot", "the west wing", "the east gate", "the basement",
              "the workshop", "the reception desk", "the server room", "the kitchen"]

_ITEMS = ["the red container", "the blue crate", "the equipment case", "the supply box",
          "the tool bag", "the delivery cart", "the maintenance panel", "the safety kit",
          "the inventory folder", "the spare parts bin", "the cleaning cart", "the first aid kit"]

_TIMES = ["9am", "10:30am", "noon", "1:15pm", "2pm", "3:45pm", "4:30pm", "5pm",
          "just before closing", "during the lunch rush", "right at shift start",
          "mid-morning", "early afternoon", "just before your break"]

_WEATHER = ["rainy", "scorching hot", "freezing cold", "windy", "humid", "foggy",
            "snowy", "stormy", "muggy", "overcast"]

_COMPLICATIONS = [
    "but you're short-staffed", "but the power just went out", "but your supervisor is watching",
    "but you're running behind schedule", "but a critical tool is missing",
    "but a customer is waiting impatiently", "but the system is lagging",
    "but you forgot your safety gear", "but the weather is making it harder",
    "but you're being timed", "but a coworker called in sick",
    "but the supplies are running low", "but the deadline was moved up",
    "but there's a surprise inspection today", "but the equipment is acting up",
]

# ═══════════════════════════════════════════════════════════════
# Flavor lookup — subcategory-based for job-specific content
# ═══════════════════════════════════════════════════════════════

# Fallback flavor for any subcategory not in the dict
_FALLBACK_FLAVOR = {
    "objects": ["equipment", "supply box", "tool kit", "work order", "safety gear",
                "inventory sheet", "maintenance log", "task clipboard"],
    "actions": ["handle", "organize", "inspect", "prepare", "manage", "process", "complete", "review"],
    "people": ["supervisor", "coworker", "customer", "manager", "client", "colleague", "inspector", "trainee"],
}


def _get_flavor(job_id: str) -> dict:
    """Get flavor pool for a job based on its subcategory."""
    job = JOBS.get(job_id, {})
    subcat = job.get("subcategory", "")
    # "management" appears in 3 categories — disambiguate by prefixing with category
    if subcat == "management":
        cat = job.get("category", "")
        if cat == "service":
            subcat = "svc_management"
        elif cat == "trades":
            subcat = "trades_management"
        elif cat == "transport":
            subcat = "trans_management"
    return SUBCATEGORY_FLAVOR.get(subcat, _FALLBACK_FLAVOR)


def _pick(pool, n=1):
    """Pick n unique items from a pool."""
    if n == 1:
        return random.choice(pool)
    return random.sample(pool, min(n, len(pool)))


def _make_replacements(job_id: str) -> dict:
    """Generate one set of random replacements for a job."""
    job = JOBS.get(job_id, {})
    flavor = _get_flavor(job_id)

    replacements = {
        "name": _pick(_NAMES),
        "name2": _pick(_NAMES),
        "location": _pick(_LOCATIONS),
        "item": _pick(flavor["objects"]),
        "item2": _pick(flavor["objects"]),
        "action": _pick(flavor["actions"]),
        "person": _pick(flavor["people"]),
        "time": _pick(_TIMES),
        "weather": _pick(_WEATHER),
        "complication": _pick(_COMPLICATIONS),
        "number": str(random.randint(3, 47)),
        "number2": str(random.randint(2, 20)),
        "job_name": job.get("name", job_id).replace("\U0001f3b6 ", "").replace("🎸 ", "").strip(),
    }

    # Ensure unique picks for item/item2 and name/name2
    while replacements["item2"] == replacements["item"]:
        replacements["item2"] = _pick(flavor["objects"])
    while replacements["name2"] == replacements["name"]:
        replacements["name2"] = _pick(_NAMES)

    return replacements


def _fill_template(template: str, job_id: str) -> str:
    """Fill in {placeholders} in a template string with random values."""
    return _fill_with(template, _make_replacements(job_id))


def _fill_with(template: str, replacements: dict) -> str:
    """Fill a template string using a pre-generated set of replacements."""
    try:
        return template.format(**replacements)
    except (KeyError, IndexError):
        return template


# ═══════════════════════════════════════════════════════════════
# Per-minigame-type generators
# ═══════════════════════════════════════════════════════════════

# Each generator returns a content dict matching the schema the dispatcher expects.

# --- Quick Pick ---
_QP_TEMPLATES = [
    {
        "prompt": "At {time}, {name} asks you to {action} {item} at {location}, {complication}. What do you do?",
        "options": [
            "Do it carefully and properly — safety first",
            "Rush through it to save time",
            "Ask {name} for clarification first",
            "Skip it and handle it later",
        ],
        "correct": "Do it carefully and properly — safety first",
    },
    {
        "prompt": "You notice {item} is damaged at {location}. {name} says to ignore it. Best action?",
        "options": [
            "Report it and fix it properly",
            "Listen to {name} and ignore it",
            "Quietly fix it without telling anyone",
            "Take a photo and post it online",
        ],
        "correct": "Report it and fix it properly",
    },
    {
        "prompt": "It's {time} and {weather}. {person} needs you to {action} {item} {complication}. Your move?",
        "options": [
            "Assess the situation, then act methodically",
            "Panic and freeze up",
            "Improvise with whatever's nearby",
            "Tell them to find someone else",
        ],
        "correct": "Assess the situation, then act methodically",
    },
    {
        "prompt": "{name} drops {item} near {location}. You're the only one who sees it. What do you do?",
        "options": [
            "Pick it up and return it to {name}",
            "Keep it — finders keepers",
            "Kick it under {location} and walk away",
            "Announce it loudly so anyone can claim it",
        ],
        "correct": "Pick it up and return it to {name}",
    },
    {
        "prompt": "You're at {location} when {name} starts doing something unsafe with {item}. Best response?",
        "options": [
            "Stop them and explain the safe procedure",
            "Mind your own business",
            "Join in — looks fun",
            "Film it for later",
        ],
        "correct": "Stop them and explain the safe procedure",
    },
    {
        "prompt": "Emergency at {location}! {person} needs help with {item} {complication}. First action?",
        "options": [
            "Stay calm, assess, then respond appropriately",
            "Scream for help and run",
            "Act immediately without thinking",
            "Call your supervisor and wait",
        ],
        "correct": "Stay calm, assess, then respond appropriately",
    },
    {
        "prompt": "You have {number} {item}s to {action} before {time}, {complication}. Best strategy?",
        "options": [
            "Prioritize by importance and work steadily",
            "Do them all at once — multitasking!",
            "Do the easiest ones first, ignore the rest",
            "Ask for an extension",
        ],
        "correct": "Prioritize by importance and work steadily",
    },
    {
        "prompt": "{name} and {name2} are arguing about how to {action} {item}. You're asked to decide. Best call?",
        "options": [
            "Suggest the safest, most efficient method",
            "Side with {name} — they're more experienced",
            "Side with {name2} — they're newer and eager",
            "Tell them to figure it out themselves",
        ],
        "correct": "Suggest the safest, most efficient method",
    },
]


def _gen_quick_pick(job_id: str) -> dict:
    template = random.choice(_QP_TEMPLATES)
    reps = _make_replacements(job_id)
    prompt = _fill_with(template["prompt"], reps)
    options = [_fill_with(o, reps) for o in template["options"]]
    correct = _fill_with(template["correct"], reps)
    # Shuffle options
    random.shuffle(options)
    return {"prompt": prompt, "options": options, "correct": correct}


# --- Sequence ---
_SEQ_TEMPLATES = [
    ["Assess the situation", "Gather tools/materials", "Prepare the workspace",
     "Execute the main task", "Quality check your work", "Clean up and document"],
    ["Receive the assignment", "Review instructions", "Set up equipment",
     "Perform the task step by step", "Inspect the result", "Report completion"],
    ["Put on safety gear", "Inspect the area", "Identify hazards",
     "Begin the procedure", "Monitor progress", "Secure and sign off"],
    ["Greet the customer", "Assess their needs", "Gather required materials",
     "Perform the service", "Verify satisfaction", "Document the work"],
    ["Check the schedule", "Prepare your tools", "Arrive at {location}",
     "Begin the task", "Handle any complications", "Complete and log it"],
]


def _gen_sequence(job_id: str) -> dict:
    template = random.choice(_SEQ_TEMPLATES)
    items = [_fill_template(t, job_id) if "{" in t else t for t in template]
    order = list(items)  # correct order
    random.shuffle(items)  # shuffle for display
    prompts = [
        "Complete this work task in the correct order:",
        "Your shift task — arrange these steps properly:",
        "Put these work steps in the right sequence:",
        "Order these tasks correctly for your shift:",
    ]
    return {"prompt": random.choice(prompts), "items": items, "order": order}


# --- Sort ---
_SORT_TEMPLATES = [
    {
        "criterion": "by urgency (most urgent first)",
        "items": [
            "Spill in {location} — safety hazard",
            "Restock {item} in {location}",
            "Organize the supply closet",
            "Refill the {item}",
            "Sweep the floor",
        ],
    },
    {
        "criterion": "by priority (highest first)",
        "items": [
            "{name}'s urgent request about {item}",
            "Scheduled maintenance of {item}",
            "Weekly inventory check",
            "Clean {location}",
            "Update the log book",
        ],
    },
    {
        "criterion": "by size (largest first)",
        "items": [
            "{item} — heavy and bulky",
            "{item2} — medium sized",
            "Tool kit — small box",
            "Paperwork — folder",
            "Keys — pocket sized",
        ],
    },
]


def _gen_sort(job_id: str) -> dict:
    template = random.choice(_SORT_TEMPLATES)
    items = [_fill_template(t, job_id) for t in template["items"]]
    order = list(items)
    random.shuffle(items)
    return {
        "prompt": f"Sort these tasks {template['criterion']}:",
        "items": items,
        "order": order,
    }


# --- Memory ---
def _gen_memory(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    count = random.randint(4, 6)
    items = random.sample(flavor["objects"], min(count, len(flavor["objects"])))
    prompts = [
        "Memorize these items — you'll need to recall them:",
        "Quick! Study this list before it disappears:",
        "Remember this sequence for your task:",
        "Flash memorization — don't forget these:",
    ]
    return {"prompt": random.choice(prompts), "sequence": items}


# --- Match Pairs ---
def _gen_match_pairs(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    objs = random.sample(flavor["objects"], min(4, len(flavor["objects"])))
    acts = random.sample(flavor["actions"], min(4, len(flavor["actions"])))
    pairs = list(zip(objs, acts))
    prompts = [
        "Match each item to its correct action:",
        "Connect each object with what you should do with it:",
        "Pair each tool with its proper use:",
    ]
    return {"prompt": random.choice(prompts), "pairs": pairs}


# --- Spot Error ---
def _gen_spot_error(job_id: str) -> dict:
    template = random.choice(_SEQ_TEMPLATES)
    correct = [_fill_template(t, job_id) if "{" in t else t for t in template]
    # Swap two random positions
    presented = list(correct)
    i, j = random.sample(range(len(presented)), 2)
    presented[i], presented[j] = presented[j], presented[i]
    prompts = [
        "Something's out of order — find the error:",
        "One step is wrong here. Spot it!",
        "A coworker left this procedure messed up. Find the mistake:",
    ]
    return {
        "prompt": random.choice(prompts),
        "correct_sequence": correct,
        "presented_sequence": presented,
    }


# --- Pattern ---
_PATTERNS = [
    (["Inspect", "Clean", "Inspect", "Clean", "?"], "Inspect"),
    (["Load", "Secure", "Load", "Secure", "?"], "Load"),
    (["Measure", "Cut", "Measure", "Cut", "?"], "Measure"),
    (["Check", "Adjust", "Check", "Adjust", "?"], "Check"),
    (["Prep", "Execute", "Verify", "Prep", "Execute", "?"], "Verify"),
]


def _gen_pattern(job_id: str) -> dict:
    seq, answer = random.choice(_PATTERNS)
    prompts = [
        "Complete the work pattern — what comes next?",
        "What's the next step in this cycle?",
        "Fill in the missing step:",
    ]
    return {"prompt": random.choice(prompts), "sequence": seq, "answer": answer}


# --- Timing ---
def _gen_timing(job_id: str) -> dict:
    beats = random.randint(1, 4)
    prompts = [
        "Click exactly when the indicator hits the target!",
        "Time your action perfectly — hit the beat!",
        "Wait for the right moment, then click!",
        "Precision timing — click on the mark!",
    ]
    return {"prompt": random.choice(prompts), "beats": beats}


# --- Precision ---
def _gen_precision(job_id: str) -> dict:
    target = random.randint(10, 200)
    tolerance = random.randint(1, 5)
    prompts = [
        f"Stop the counter at exactly {target}!",
        f"Hold steady at {target} — click when you hit it!",
        f"Match the target value of {target}!",
        f"Click when the gauge reaches {target}!",
    ]
    return {"prompt": random.choice(prompts), "target": target, "tolerance": tolerance}


# --- Budget ---
def _gen_budget(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    cats = random.sample(flavor["objects"], 4)
    budget = random.choice([10000, 25000, 50000, 100000, 500000])
    # Create a roughly even split with some variance
    weights = [random.randint(15, 35) for _ in range(4)]
    total = sum(weights)
    optimal = {c: (budget * w // total) for c, w in zip(cats, weights)}
    # Fix rounding to sum to budget
    remainder = budget - sum(optimal.values())
    optimal[cats[0]] += remainder
    prompts = [
        f"Allocate ${budget:,} across these areas:",
        f"Budget ${budget:,} — distribute it wisely:",
        f"Split ${budget:,} between these priorities:",
    ]
    return {"prompt": random.choice(prompts), "categories": cats, "budget": budget, "optimal": optimal}


# --- Fill Blank ---
def _gen_fill_blank(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    action = random.choice(flavor["actions"])
    item = random.choice(flavor["objects"])
    prompts = [
        f"After you {action} {item}, you must always ____ it.",
        f"The first step when handling {item} is to ____ it.",
        f"Before you {action}, make sure to ____ the area.",
        f"When {item} is not in use, you should ____ it.",
    ]
    answers = ["inspect", "clean", "secure", "label", "store", "document"]
    answer = random.choice(answers)
    return {
        "prompt": random.choice(prompts),
        "context": f"It's {random.choice(_TIMES)} and you're at {random.choice(_LOCATIONS)}.",
        "answer": answer,
    }


# --- Math ---
def _gen_math(job_id: str) -> dict:
    a = random.randint(3, 50)
    b = random.randint(2, 20)
    op = random.choice(["+", "-", "*"])
    if op == "+":
        answer = a + b
        formula = f"{a} + {b}"
    elif op == "-":
        answer = a - b
        formula = f"{a} - {b}"
    else:
        answer = a * b
        formula = f"{a} × {b}"
    prompts = [
        f"Calculate: {formula} = ?",
        f"Quick math for your shift: {formula}",
        f"Solve: {formula}",
    ]
    return {"prompt": random.choice(prompts), "formula": formula, "answer": answer}


# --- Typing Race ---
def _gen_typing_race(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    action = random.choice(flavor["actions"])
    item = random.choice(flavor["objects"])
    location = random.choice(_LOCATIONS)
    phrases = [
        f"I need to {action} the {item} at {location} before my shift ends",
        f"The {item} must be handled carefully and stored properly after use",
        f"Always remember to inspect your equipment before starting any task",
        f"Safety first: check your gear then proceed with the job at hand",
        f"The supervisor wants all {item}s organized and logged by closing time",
    ]
    return {"prompt": "Type this phrase as fast and accurately as you can:", "phrase": random.choice(phrases)}


# --- Route Plan ---
def _gen_route_plan(job_id: str) -> dict:
    count = random.randint(4, 5)
    locations = random.sample(_LOCATIONS, count)
    stops = [(locations[0], "Start")]
    for i in range(1, count):
        stops.append((locations[i], locations[i - 1]))
    optimal = locations
    prompts = [
        "Plan the most efficient route — visit each stop in order:",
        "Organize your delivery route for minimum travel:",
        "Sequence your stops for the best route:",
    ]
    return {"prompt": random.choice(prompts), "stops": stops, "optimal": optimal}


# --- Diagnosis ---
def _gen_diagnosis(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    item = random.choice(flavor["objects"])
    options = [
        f"{item} is worn out and needs replacement",
        f"{item} has a minor calibration issue — adjust and retry",
        f"{item} is fine — the problem is elsewhere",
        f"{item} needs a full diagnostic teardown",
    ]
    correct = options[1]
    random.shuffle(options)
    prompts = [
        f"{random.choice(_NAMES)} reports {item} isn't working right. Diagnose the issue:",
        f"{item} is acting up during your shift. What's most likely wrong?",
        f"You inspect {item} and notice slight irregularity. Your diagnosis?",
    ]
    return {
        "prompt": random.choice(prompts),
        "options": options,
        "correct": correct,
        "reasoning": "Minor issues are more common than complete failures. Always try calibration first.",
    }


# --- Negotiation ---
def _gen_negotiation(job_id: str) -> dict:
    name = random.choice(_NAMES)
    options = [
        f"Listen to {name}'s concerns, then propose a win-win compromise",
        f"Stand firm — accept nothing less than your original offer",
        f"Give in to all their demands to keep the peace",
        f"Walk away — it's not worth the hassle",
    ]
    correct = options[0]
    random.shuffle(options)
    prompts = [
        f"{name} is unhappy with the current arrangement and wants to renegotiate. How do you handle it?",
        f"A dispute arises between you and {name} over responsibilities. Best approach?",
        f"{name} pushes back on your proposed plan. Your negotiation strategy?",
    ]
    return {
        "prompt": random.choice(prompts),
        "options": options,
        "correct": correct,
        "explanation": "Active listening + compromise builds long-term working relationships.",
    }


# --- Speed Run ---
def _gen_speed_run(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    count = random.randint(4, 5)
    tasks = random.sample(flavor["actions"], min(count, len(flavor["actions"])))
    prompts = [
        "Complete all tasks as fast as you can!",
        "Speed round — click every task button!",
        "Quick! Handle all these before the timer runs out!",
    ]
    return {"prompt": random.choice(prompts), "tasks": tasks}


# --- Shift Sim ---
def _gen_shift_sim(job_id: str) -> dict:
    situations = [
        f"Emergency: {random.choice(_NAMES)} needs help at {random.choice(_LOCATIONS)}",
        f"Routine: Restock {random.choice(_ITEMS)} at {random.choice(_LOCATIONS)}",
        f"Customer: {random.choice(_NAMES)} is waiting at the front desk",
        f"Maintenance: {random.choice(_ITEMS)} needs attention",
        f"Break: Your lunch break is in 10 minutes",
    ]
    random.shuffle(situations)
    # Optimal = emergency first, then customer, then maintenance, then routine, then break
    optimal = sorted(situations, key=lambda s: 0 if "Emergency" in s else 1 if "Customer" in s else 2 if "Maintenance" in s else 3 if "Routine" in s else 4)
    prompts = [
        "Handle these shift situations in priority order:",
        "Your shift just got busy — prioritize these by urgency:",
        "Multiple things happening at once! Order by priority:",
    ]
    return {"prompt": random.choice(prompts), "situations": situations, "optimal": optimal}


# --- Triage ---
def _gen_triage(job_id: str) -> dict:
    patients = [
        f"Patient with severe bleeding at {random.choice(_LOCATIONS)}",
        f"Patient with minor cut on their finger",
        f"Patient complaining of chest pain",
        f"Patient with a sprained ankle",
        f"Patient here for a routine check-up",
    ]
    random.shuffle(patients)
    optimal = sorted(patients, key=lambda s: 0 if "chest pain" in s else 1 if "severe bleeding" in s else 2 if "sprained" in s else 3 if "minor cut" in s else 4)
    prompts = [
        "Triage these patients by treatment priority:",
        "Who do you treat first? Order by severity:",
        "Emergency triage — prioritize these patients:",
    ]
    return {"prompt": random.choice(prompts), "patients": patients, "optimal": optimal}


# --- Categorize ---
def _gen_categorize(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    items = random.sample(flavor["objects"], min(6, len(flavor["objects"])))
    cats = ["Priority A", "Priority B", "Priority C"]
    prompts = [
        "Classify each item into the right category:",
        "Sort these into their proper categories:",
        "Categorize these items by importance:",
    ]
    return {"prompt": random.choice(prompts), "items": items, "categories": cats}


# --- Combo Lock ---
def _gen_combo_lock(job_id: str) -> dict:
    pins = [random.randint(0, 9) for _ in range(random.randint(3, 4))]
    prompts = [
        "Crack the combination lock to access the equipment:",
        "Enter the correct code to unlock the supply cabinet:",
        "Open the security lock — find the right combination:",
    ]
    return {"prompt": random.choice(prompts), "pins": pins, "max_val": 9}


# --- Assembly ---
def _gen_assembly(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    count = random.randint(4, 6)
    parts = random.sample(flavor["objects"], min(count, len(flavor["objects"])))
    order = list(parts)
    random.shuffle(parts)
    prompts = [
        "Assemble these parts in the correct dependency order:",
        "Put these components together in the right sequence:",
        "Build this — select parts in the correct assembly order:",
    ]
    return {"prompt": random.choice(prompts), "parts": parts, "order": order}


# --- Recipe Build ---
def _gen_recipe_build(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    count = random.randint(5, 6)
    ingredients = random.sample(flavor["objects"], min(count, len(flavor["objects"])))
    order = list(ingredients)
    random.shuffle(ingredients)
    prompts = [
        "Build this in the correct order:",
        "Combine these ingredients in the right sequence:",
        "Prepare this — add components in proper order:",
    ]
    return {"prompt": random.choice(prompts), "ingredients": ingredients, "order": order}


# --- Multi-Stage ---
def _gen_multi_stage(job_id: str) -> dict:
    stages = [
        {
            "type": "quick_pick",
            "prompt": _fill_template(
                "At {time}, {person} asks you to handle {item} at {location}. What's your first step?",
                job_id),
            "options": [
                "Assess the situation before acting",
                "Jump right in and start working",
                "Ask for more details first",
                "Delegate it to someone else",
            ],
            "correct": "Assess the situation before acting",
        },
        {
            "type": "sequence",
            "prompt": "Now complete the task — arrange these steps in order:",
            "items": ["Prepare tools", "Start the main task", "Check quality", "Clean up"],
            "order": ["Prepare tools", "Start the main task", "Check quality", "Clean up"],
        },
        {
            "type": "quick_pick",
            "prompt": _fill_template(
                "Something goes wrong with {item}! {complication}. What do you do?",
                job_id),
            "options": [
                "Stop, assess, and fix the issue safely",
                "Push through and hope for the best",
                "Abandon the task entirely",
                "Blame someone else",
            ],
            "correct": "Stop, assess, and fix the issue safely",
        },
    ]
    return {"prompt": "Multi-stage shift challenge — complete all 3 stages!", "stages": stages}


# ═══════════════════════════════════════════════════════════════
# Dispatcher
# ═══════════════════════════════════════════════════════════════

_GENERATORS = {
    "quick_pick": _gen_quick_pick,
    "sequence": _gen_sequence,
    "sort": _gen_sort,
    "memory": _gen_memory,
    "match_pairs": _gen_match_pairs,
    "spot_error": _gen_spot_error,
    "pattern": _gen_pattern,
    "timing": _gen_timing,
    "precision": _gen_precision,
    "budget": _gen_budget,
    "fill_blank": _gen_fill_blank,
    "math": _gen_math,
    "typing_race": _gen_typing_race,
    "route_plan": _gen_route_plan,
    "diagnosis": _gen_diagnosis,
    "negotiation": _gen_negotiation,
    "speed_run": _gen_speed_run,
    "shift_sim": _gen_shift_sim,
    "triage": _gen_triage,
    "categorize": _gen_categorize,
    "combo_lock": _gen_combo_lock,
    "assembly": _gen_assembly,
    "recipe_build": _gen_recipe_build,
    "multi_stage": _gen_multi_stage,
}


def generate_content(job_id: str, mg_type: str) -> dict | None:
    """Generate procedural minigame content for a job/minigame type.
    
    Returns a content dict, or None if the type isn't supported.
    The content is unique each call thanks to randomized templates.
    """
    gen = _GENERATORS.get(mg_type)
    if gen is None:
        return None
    try:
        return gen(job_id)
    except Exception:
        return None
