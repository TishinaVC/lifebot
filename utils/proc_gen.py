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


def _gerund_to_base(action: str) -> str:
    """Convert gerund to base form: 'busking' -> 'busk', 'washing windows' -> 'wash windows',
    'taking surveys' -> 'take surveys', 'shining shoes' -> 'shine shoes'."""
    words = action.split()
    first = words[0]
    if first.endswith("ing") and len(first) > 4:
        stem = first[:-3]
        dedoubled = False
        # Handle doubled consonants: "shopping" -> "shop", "scrubbing" -> "scrub"
        # But NOT 'll' words like "selling" -> "sell" (already double in base form)
        if (len(stem) >= 3 and stem[-1] == stem[-2] and stem[-1] not in "aeiou"
                and stem[-1] != "l"):
            stem = stem[:-1]
            dedoubled = True
        # Add 'e' back for silent-e verbs: "tak" -> "take", "shin" -> "shine"
        # Pattern: vowel (not 'e') + single consonant at end, preceded by consonant
        if (not dedoubled and len(stem) >= 3
                and stem[-1] not in "aeiouwy"
                and stem[-2] in "aiou"
                and stem[-3] not in "aeiou"):
            stem = stem + "e"
        words[0] = stem
    return " ".join(words)


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
        "action_base": "",  # placeholder, set below
        "person": _pick(flavor["people"]),
        "time": _pick(_TIMES),
        "weather": _pick(_WEATHER),
        "complication": _pick(_COMPLICATIONS),
        "number": str(random.randint(3, 47)),
        "number2": str(random.randint(2, 20)),
        "job_name": job.get("name", job_id).replace("\U0001f3b6 ", "").replace("🎸 ", "").strip(),
    }
    replacements["action_base"] = _gerund_to_base(replacements["action"])

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
        "prompt": "At {time}, {name} asks you to {action_base} {item} at {location}, {complication}. What do you do?",
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
        "prompt": "It's {time} and {weather}. {person} needs you to {action_base} {item} {complication}. Your move?",
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
        "prompt": "You have {number} {item}s to {action_base} before {time}, {complication}. Best strategy?",
        "options": [
            "Prioritize by importance and work steadily",
            "Do them all at once — multitasking!",
            "Do the easiest ones first, ignore the rest",
            "Ask for an extension",
        ],
        "correct": "Prioritize by importance and work steadily",
    },
    {
        "prompt": "{name} and {name2} are arguing about how to {action_base} {item}. You're asked to decide. Best call?",
        "options": [
            "Suggest the safest, most efficient method",
            "Side with {name} — they're more experienced",
            "Side with {name2} — they're newer and eager",
            "Tell them to figure it out themselves",
        ],
        "correct": "Suggest the safest, most efficient method",
    },
    {
        "prompt": "You're about to {action_base} {item} when you notice it's slightly damaged. {complication}. What do you do?",
        "options": [
            "Stop and report the damage before proceeding",
            "Use it anyway — it's probably fine",
            "Quietly swap it with {item2} from the supply room",
            "Fix it yourself without telling anyone",
        ],
        "correct": "Stop and report the damage before proceeding",
    },
    {
        "prompt": "It's the end of your shift and {person} asks you to stay late to {action_base} {item}. {complication}. Best response?",
        "options": [
            "Agree if you can, but check with your supervisor first",
            "Refuse — your shift is over, not your problem",
            "Say yes to everything, cancel your plans",
            "Pretend you didn't hear them and leave",
        ],
        "correct": "Agree if you can, but check with your supervisor first",
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
    ["Greet the {person}", "Set up your {item}", "Begin {action}",
     "Handle {complication}", "Quality check your work", "Pack up your {item2}"],
    ["Review the {action} instructions", "Gather your {item} and {item2}",
     "Prepare the workspace at {location}", "Start {action}",
     "Inspect the result", "Report to your {person}"],
    ["Put on safety gear", "Inspect the {item}", "Identify hazards at {location}",
     "Begin {action}", "Monitor the {item2}", "Secure and sign off"],
    ["Welcome the {person}", "Assess what they need", "Grab your {item}",
     "Perform {action}", "Confirm they're satisfied", "Log the {action} completion"],
    ["Check the schedule with {person}", "Prepare your {item}", "Head to {location}",
     "Start {action}", "Deal with {complication}", "Finish and document it"],
    ["Get the {action} assignment", "Collect your {item}", "Set up at {location}",
     "{action} step by step", "Check quality of the {item2}", "Clean up and report"],
    ["Inspect your {item}", "Prepare your {item2}", "Calibrate at {location}",
     "Execute {action}", "Verify with {person}", "Store equipment safely"],
    ["Brief with {person}", "Gather {item} and {item2}", "Position at {location}",
     "Carry out {action}", "Review for quality", "Submit completion report"],
]


def _gen_sequence(job_id: str) -> dict:
    template = random.choice(_SEQ_TEMPLATES)
    reps = _make_replacements(job_id)
    items = [_fill_with(t, reps) for t in template]
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
    {
        "criterion": "by deadline (soonest first)",
        "items": [
            "{name} needs {item} now — due in 5 min",
            "Restock {item2} — due in 30 min",
            "Weekly report on {action} — due in 2 hours",
            "Clean {location} — due end of shift",
            "Organize {item} storage — due next week",
        ],
    },
    {
        "criterion": "by importance (most important first)",
        "items": [
            "Safety check on {item} — critical",
            "{person} is waiting for {item2} — important",
            "Log your {action} hours — moderate",
            "Restock supplies at {location} — low priority",
            "Update the notice board — optional",
        ],
    },
    {
        "criterion": "by frequency (most frequent first)",
        "items": [
            "{action} — done every hour",
            "Inspect {item} — done every shift",
            "Clean {location} — done daily",
            "Organize {item2} — done weekly",
            "Review procedures — done monthly",
        ],
    },
]


def _gen_sort(job_id: str) -> dict:
    template = random.choice(_SORT_TEMPLATES)
    reps = _make_replacements(job_id)
    items = [_fill_with(t, reps) for t in template["items"]]
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
    # Mix objects and actions for more interesting sequences
    pool = flavor["objects"] + flavor["actions"]
    items = random.sample(pool, min(count, len(pool)))
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
    acts = flavor["actions"]
    # Build meaningful pairs: try to find actions that share a keyword with the object
    def _sensible_action(obj: str) -> str:
        o = obj.lower()
        # Try keyword overlap between object and action
        obj_words = set(o.split())
        for a in acts:
            a_words = set(a.lower().split())
            if obj_words & a_words:
                return a
        # Try semantic matching based on common object types
        if any(k in o for k in ["sign", "flyer", "poster", "banner"]):
            match = [a for a in acts if any(k in a.lower() for k in ["hand", "display", "hold", "wave", "distribut"])]
            if match: return random.choice(match)
        if any(k in o for k in ["jar", "cup", "hat", "bucket", "case", "bowl", "pot", "pan"]):
            match = [a for a in acts if any(k in a.lower() for k in ["fill", "organize", "handle", "manage", "clean", "wash", "store"])]
            if match: return random.choice(match)
        if any(k in o for k in ["cart", "truck", "vehicle", "bike", "delivery"]):
            match = [a for a in acts if any(k in a.lower() for k in ["push", "drive", "load", "deliver", "transport"])]
            if match: return random.choice(match)
        if any(k in o for k in ["tool", "kit", "gear", "equipment", "instrument"]):
            match = [a for a in acts if any(k in a.lower() for k in ["inspect", "prepare", "handle", "organize", "calibrate", "maintain"])]
            if match: return random.choice(match)
        if any(k in o for k in ["knife", "blade", "cutter", "saw", "scissors"]):
            match = [a for a in acts if any(k in a.lower() for k in ["cut", "chop", "slice", "prep"])]
            if match: return random.choice(match)
        if any(k in o for k in ["mop", "broom", "brush", "squeegee", "vacuum"]):
            match = [a for a in acts if any(k in a.lower() for k in ["clean", "sweep", "mop", "scrub", "wash", "dust", "vacuum"])]
            if match: return random.choice(match)
        if any(k in o for k in ["book", "log", "report", "document", "clipboard", "schedule"]):
            match = [a for a in acts if any(k in a.lower() for k in ["review", "log", "file", "organize", "update", "record"])]
            if match: return random.choice(match)
        if any(k in o for k in ["megaphone", "boom", "microphone", "speaker"]):
            match = [a for a in acts if any(k in a.lower() for k in ["use", "handle", "operate", "announce"])]
            if match: return random.choice(match)
        # Fallback: random action (still job-specific, just not semantically linked)
        return random.choice(acts)
    pairs = [(obj, _sensible_action(obj)) for obj in objs]
    prompts = [
        "Match each item to its correct action:",
        "Connect each object with what you should do with it:",
        "Pair each tool with its proper use:",
    ]
    return {"prompt": random.choice(prompts), "pairs": pairs}


# --- Spot Error ---
def _gen_spot_error(job_id: str) -> dict:
    template = random.choice(_SEQ_TEMPLATES)
    reps = _make_replacements(job_id)
    correct = [_fill_with(t, reps) for t in template]
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
def _gen_pattern(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    acts = random.sample(flavor["actions"], min(2, len(flavor["actions"])))
    a, b = acts[0], acts[1] if len(acts) > 1 else "inspect"
    templates = [
        ([a, b, a, b, "?"], a),
        ([b, a, b, a, "?"], b),
        ([a, b, "Verify", a, b, "?"], "Verify"),
        (["Prep", a, "Check", "Prep", a, "?"], "Check"),
    ]
    seq, answer = random.choice(templates)
    prompts = [
        "Complete the work pattern — what comes next?",
        "What's the next step in this cycle?",
        "Fill in the missing step:",
    ]
    return {"prompt": random.choice(prompts), "sequence": seq, "answer": answer}


# --- Timing ---
def _gen_timing(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    action = random.choice(flavor["actions"])
    action_base = _gerund_to_base(action)
    item = random.choice(flavor["objects"])
    beats = random.randint(1, 4)
    prompts = [
        f"Time your {action} perfectly — hit the beat!",
        f"Click exactly when you finish {action} the {item}!",
        f"Wait for the right moment to {action_base}, then click!",
        f"Precision timing for {action} — click on the mark!",
    ]
    return {"prompt": random.choice(prompts), "beats": beats}


# --- Precision ---
def _gen_precision(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    item = random.choice(flavor["objects"])
    target = random.randint(10, 200)
    tolerance = random.randint(1, 5)
    prompts = [
        f"Calibrate the {item} — stop at exactly {target}!",
        f"Set the {item} gauge to {target} — click when you hit it!",
        f"Match the target value of {target} for the {item}!",
        f"Click when the {item} reading reaches {target}!",
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
    action = random.choice(flavor["actions"])
    prompts = [
        f"Allocate ${budget:,} for your {action} operations across these areas:",
        f"Budget ${budget:,} — distribute it wisely for your shift:",
        f"Split ${budget:,} between these {action} priorities:",
        f"Your department has ${budget:,} — allocate it across these needs:",
    ]
    return {"prompt": random.choice(prompts), "categories": cats, "budget": budget, "optimal": optimal}


# --- Fill Blank ---
def _gen_fill_blank(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    item = random.choice(flavor["objects"])
    item2 = random.choice(flavor["objects"])
    while item2 == item:
        item2 = random.choice(flavor["objects"])
    person = random.choice(flavor["people"])
    # Each template has its own coherent answer set
    templates = [
        (f"After handling {item}, you must always ____ it before storing.", ["clean", "inspect", "label", "sanitize"]),
        (f"The first step when working with {item} is to ____ it.", ["inspect", "prepare", "calibrate", "test"]),
        (f"Before leaving for the day, make sure to ____ the {item}.", ["secure", "store", "lock", "cover"]),
        (f"When {item} is not in use, you should ____ it.", ["store", "cover", "secure", "organize"]),
        (f"After {person} finishes with {item}, you need to ____ it.", ["inspect", "clean", "reset", "calibrate"]),
        (f"Something is wrong with {item}. You should ____ it first.", ["inspect", "diagnose", "test", "examine"]),
        (f"To keep {item} in good shape, remember to ____ it regularly.", ["clean", "maintain", "inspect", "service"]),
        (f"You finished using {item} and {item2}. Now ____ them both.", ["clean", "organize", "store", "inspect"]),
    ]
    prompt, answers = random.choice(templates)
    answer = random.choice(answers)
    return {
        "prompt": prompt,
        "context": f"It's {random.choice(_TIMES)} and you're at {random.choice(_LOCATIONS)}.",
        "answer": answer,
    }


# --- Math ---
def _gen_math(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    item = random.choice(flavor["objects"])
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
        f"You have {a} {item}s and get {b} more. Total? ({formula})",
        f"Calculate for inventory: {formula} = ?",
        f"Quick math for your shift: {formula}",
        f"Solve: {formula}",
    ]
    return {"prompt": random.choice(prompts), "formula": formula, "answer": answer}


# --- Typing Race ---
def _gen_typing_race(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    action = random.choice(flavor["actions"])
    action_base = _gerund_to_base(action)
    item = random.choice(flavor["objects"])
    item2 = random.choice(flavor["objects"])
    while item2 == item:
        item2 = random.choice(flavor["objects"])
    person = random.choice(flavor["people"])
    location = random.choice(_LOCATIONS)
    phrases = [
        f"I need to {action_base} the {item} at {location} before my shift ends",
        f"The {item} must be handled carefully and stored properly after use",
        f"Always remember to inspect the {item} before starting any task",
        f"Safety first: check your {item} then proceed with {action}",
        f"The {person} wants all {item}s organized and logged by closing time",
        f"After you {action_base} the {item}, make sure to clean up {location}",
        f"Never leave {item} unattended while you {action_base} the {item2}",
        f"The shift report says to {action_base} first, then inspect the {item2}",
        f"Remember to {action_base} the {item} and return it to {location}",
        f"Before {action}, check that the {item} and {item2} are ready",
    ]
    return {"prompt": "Type this phrase as fast and accurately as you can:", "phrase": random.choice(phrases)}


# --- Route Plan ---
def _gen_route_plan(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    count = random.randint(4, 5)
    objs = random.sample(flavor["objects"], min(count, len(flavor["objects"])))
    acts = random.sample(flavor["actions"], min(count, len(flavor["actions"])))
    locs = random.sample(_LOCATIONS, count)
    stop_verbs = ["Deliver", "Pick up", "Inspect", "Service", "Restock", "Check on"]
    stops_raw = []
    for i in range(count):
        verb = stop_verbs[i % len(stop_verbs)]
        obj = objs[i] if i < len(objs) else random.choice(flavor["objects"])
        loc = locs[i]
        stops_raw.append(f"{verb} {obj} at {loc}")
    optimal = list(stops_raw)
    random.shuffle(stops_raw)
    prompts = [
        "Plan the most efficient route — visit each stop in order:",
        "Organize your delivery route for minimum travel:",
        "Sequence your stops for the best route:",
    ]
    return {"prompt": random.choice(prompts), "stops": stops_raw, "optimal": optimal}


# --- Diagnosis ---
def _gen_diagnosis(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    item = random.choice(flavor["objects"])
    item2 = random.choice(flavor["objects"])
    while item2 == item:
        item2 = random.choice(flavor["objects"])
    action = random.choice(flavor["actions"])
    action_base = _gerund_to_base(action)
    person = random.choice(flavor["people"])
    name = random.choice(_NAMES)
    templates = [
        {
            "options": [
                f"{item} is worn out and needs replacement",
                f"{item} has a minor calibration issue — adjust and retry",
                f"{item} is fine — the problem is with how you {action_base}",
                f"{item} needs a full diagnostic teardown",
            ],
            "correct_idx": 1,
            "reasoning": "Minor issues are more common than complete failures. Always try calibration first.",
        },
        {
            "options": [
                f"{item} is overheating — let it cool down then retry",
                f"{item} is completely broken — order a new one",
                f"{item} just needs a firmware update",
                f"Someone misconfigured {item} — reset to defaults",
            ],
            "correct_idx": 0,
            "reasoning": "Overheating is the most common cause of sudden failure. Let it cool first.",
        },
        {
            "options": [
                f"The {item} is fine — check the {item2} instead",
                f"Replace the {item} entirely",
                f"The {item} has a loose connection — reseat it",
                f"The {item} needs professional repair service",
            ],
            "correct_idx": 2,
            "reasoning": "Loose connections cause most intermittent issues. Always check connections first.",
        },
    ]
    template = random.choice(templates)
    options = template["options"]
    correct = options[template["correct_idx"]]
    random.shuffle(options)
    prompts = [
        f"{name} reports {item} isn't working right during {action}. Diagnose the issue:",
        f"{item} is acting up while you {action_base}. What's most likely wrong?",
        f"A {person} asks you to check {item} — you notice slight irregularity. Your diagnosis?",
        f"{name} says {item} stopped working at {random.choice(_LOCATIONS)}. What's your call?",
    ]
    return {
        "prompt": random.choice(prompts),
        "options": options,
        "correct": correct,
        "reasoning": template["reasoning"],
    }


# --- Negotiation ---
def _gen_negotiation(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    name = random.choice(_NAMES)
    name2 = random.choice(_NAMES)
    while name2 == name:
        name2 = random.choice(_NAMES)
    action = random.choice(flavor["actions"])
    action_base = _gerund_to_base(action)
    item = random.choice(flavor["objects"])
    person = random.choice(flavor["people"])
    templates = [
        {
            "options": [
                f"Listen to {name}'s concerns, then propose a win-win compromise",
                f"Stand firm — accept nothing less than your original offer",
                f"Give in to all their demands to keep the peace",
                f"Walk away — it's not worth the hassle",
            ],
            "correct_idx": 0,
            "explanation": "Active listening + compromise builds long-term working relationships.",
        },
        {
            "options": [
                f"Acknowledge {name}'s point, then redirect to shared goals",
                f"Interrupt and correct {name}'s misunderstanding",
                f"Stay silent and let {name} vent",
                f"Escalate to management immediately",
            ],
            "correct_idx": 0,
            "explanation": "Acknowledging then redirecting keeps conversations productive.",
        },
        {
            "options": [
                f"Offer to {action_base} together to find a solution that works for both",
                f"Insist on doing it your way — you have more experience",
                f"Let {name} handle it entirely",
                f"Refuse to negotiate and file a complaint",
            ],
            "correct_idx": 0,
            "explanation": "Collaborative approaches produce better outcomes than confrontation.",
        },
    ]
    template = random.choice(templates)
    options = template["options"]
    correct = options[template["correct_idx"]]
    random.shuffle(options)
    prompts = [
        f"{name} is unhappy about how you {action_base} the {item} and wants to renegotiate. How do you handle it?",
        f"A dispute arises between you and {name} over {item} responsibilities. Best approach?",
        f"{name} pushes back on your plan to {action_base}. Your negotiation strategy?",
        f"{name} and {name2} disagree about {item}. {person} asks you to mediate. What do you do?",
    ]
    return {
        "prompt": random.choice(prompts),
        "options": options,
        "correct": correct,
        "explanation": template["explanation"],
    }


# --- Speed Run ---
def _gen_speed_run(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    count = random.randint(4, 5)
    acts = random.sample(flavor["actions"], min(count, len(flavor["actions"])))
    objs = random.sample(flavor["objects"], min(count, len(flavor["objects"])))
    # Pair each action with an object for more descriptive task names
    tasks = [f"{a} the {o}" for a, o in zip(acts, objs)]
    prompts = [
        "Complete all tasks as fast as you can!",
        "Speed round — click every task button!",
        "Quick! Handle all these before the timer runs out!",
    ]
    return {"prompt": random.choice(prompts), "tasks": tasks}


# --- Shift Sim ---
def _gen_shift_sim(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    item = random.choice(flavor["objects"])
    item2 = random.choice(flavor["objects"])
    while item2 == item:
        item2 = random.choice(flavor["objects"])
    action = random.choice(flavor["actions"])
    action_base = _gerund_to_base(action)
    person = random.choice(flavor["people"])
    name = random.choice(_NAMES)
    loc = random.choice(_LOCATIONS)
    scenario_sets = [
        [
            f"Emergency: {name} needs help at {loc}",
            f"Customer: {person} is waiting — needs you to {action_base}",
            f"Maintenance: {item} needs attention",
            f"Routine: {action_base} the {item2} at {loc}",
            f"Break: Your lunch break is in 10 minutes",
        ],
        [
            f"Emergency: Fire alarm at {loc} — evacuate needed",
            f"Customer: {person} is upset about {item}",
            f"Maintenance: {item2} broke down mid-shift",
            f"Routine: Restock {item} before closing",
            f"Break: Your lunch break is in 10 minutes",
        ],
        [
            f"Emergency: {name} collapsed at {loc}",
            f"Customer: {person} wants to speak with a manager about {action}",
            f"Maintenance: {item} is making strange noises",
            f"Routine: Log your {action} hours",
            f"Break: Your lunch break is in 10 minutes",
        ],
    ]
    situations = random.choice(scenario_sets)
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
    flavor = _get_flavor(job_id)
    item = random.choice(flavor["objects"])
    item2 = random.choice(flavor["objects"])
    while item2 == item:
        item2 = random.choice(flavor["objects"])
    action = random.choice(flavor["actions"])
    action_base = _gerund_to_base(action)
    person = random.choice(flavor["people"])
    name = random.choice(_NAMES)
    loc = random.choice(_LOCATIONS)
    # Multiple scenario templates for variety
    scenario_sets = [
        [
            f"Urgent: {item} malfunction — someone is injured",
            f"High: A {person} collapsed while you {action_base}",
            f"Medium: Worker tripped over {item} — sprained wrist",
            f"Low: Minor scrape from handling {item}",
            f"Routine: Someone needs directions to {loc}",
        ],
        [
            f"Critical: {name} has a head injury at {loc}",
            f"High: {item2} fell on someone — possible fracture",
            f"Medium: {person} reports back pain from {action}",
            f"Low: Small cut from {item} — needs a bandage",
            f"Routine: Worker feels dizzy but is conscious",
        ],
        [
            f"Urgent: Electrical shock from {item} — not breathing",
            f"High: {name} slipped at {loc} — can't stand up",
            f"Medium: Burn from handling {item2}",
            f"Low: Eye irritation from {action}",
            f"Routine: General fatigue — needs rest",
        ],
    ]
    patients = random.choice(scenario_sets)
    random.shuffle(patients)
    optimal = sorted(patients, key=lambda s: 0 if any(k in s for k in ["Urgent", "Critical"]) else 1 if "High" in s else 2 if "Medium" in s else 3 if "Low" in s else 4)
    prompts = [
        "Triage these patients by treatment priority:",
        "Who do you treat first? Order by severity:",
        "Emergency triage — prioritize these patients:",
    ]
    return {"prompt": random.choice(prompts), "patients": patients, "optimal": optimal}


# --- Categorize ---
def _gen_categorize(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    objs = flavor["objects"]
    acts = flavor["actions"]
    # Map actions to meaningful categories based on keywords
    def _classify(action: str) -> str:
        a = action.lower()
        if any(k in a for k in ["clean", "sanitize", "wash", "sweep", "scrub", "mop", "dust", "polish"]):
            return "Cleaning"
        if any(k in a for k in ["inspect", "check", "test", "examine", "diagnose", "review", "verify"]):
            return "Inspection"
        if any(k in a for k in ["organize", "sort", "arrange", "store", "stock", "label", "file", "log"]):
            return "Organization"
        if any(k in a for k in ["repair", "fix", "maintain", "service", "calibrate", "adjust", "replace"]):
            return "Maintenance"
        if any(k in a for k in ["handle", "manage", "process", "prepare", "complete", "deliver", "serve"]):
            return "Operations"
        return "General"
    # Build items with known categories
    pairs = []
    for a in acts:
        for o in objs:
            cat = _classify(a)
            pairs.append((f"{a} the {o}", cat))
    random.shuffle(pairs)
    # Pick items that span at least 2 categories
    selected = pairs[:min(6, len(pairs))]
    items = [p[0] for p in selected]
    cats = sorted(set(p[1] for p in selected))
    categories = [p[1] for p in selected]
    prompts = [
        "Classify each task by its type:",
        "Sort these tasks into the right categories:",
        "Categorize these by the type of work:",
    ]
    return {"prompt": random.choice(prompts), "items": items, "categories": cats, "item_categories": categories}


# --- Combo Lock ---
def _gen_combo_lock(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    item = random.choice(flavor["objects"])
    pins = [random.randint(0, 9) for _ in range(random.randint(3, 4))]
    prompts = [
        f"Crack the lock to access the {item}:",
        f"Enter the code to unlock the {item} cabinet:",
        f"Open the security lock for the {item} — find the combination:",
    ]
    return {"prompt": random.choice(prompts), "pins": pins, "max_val": 9}


# --- Assembly ---
def _gen_assembly(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    count = random.randint(4, 6)
    parts = random.sample(flavor["objects"], min(count, len(flavor["objects"])))
    order = list(parts)
    random.shuffle(parts)
    action = random.choice(flavor["actions"])
    prompts = [
        f"Assemble these parts in the correct order for {action}:",
        "Put these components together in the right sequence:",
        f"Build this — select parts in the correct assembly order:",
        f"Construct the setup — these parts go in a specific order for {action}:",
    ]
    return {"prompt": random.choice(prompts), "parts": parts, "order": order}


# --- Recipe Build ---
def _gen_recipe_build(job_id: str) -> dict:
    flavor = _get_flavor(job_id)
    count = random.randint(5, 6)
    ingredients = random.sample(flavor["objects"], min(count, len(flavor["objects"])))
    order = list(ingredients)
    random.shuffle(ingredients)
    action = random.choice(flavor["actions"])
    prompts = [
        f"Build this in the correct order for {action}:",
        "Combine these ingredients in the right sequence:",
        f"Prepare this — add components in proper order for {action}:",
        f"Set up your {action} station — these go in a specific order:",
    ]
    return {"prompt": random.choice(prompts), "ingredients": ingredients, "order": order}


# --- Multi-Stage ---
def _gen_multi_stage(job_id: str) -> dict:
    reps = _make_replacements(job_id)
    flavor = _get_flavor(job_id)
    action = random.choice(flavor["actions"])
    item = random.choice(flavor["objects"])
    item2 = random.choice(flavor["objects"])
    while item2 == item:
        item2 = random.choice(flavor["objects"])
    person = random.choice(flavor["people"])
    # Multiple stage configurations for variety
    stage_configs = [
        # Config 1: quick_pick → sequence → quick_pick
        [
            {
                "type": "quick_pick",
                "prompt": _fill_with("At {time}, {person} asks you to handle {item} at {location}. What's your first step?", reps),
                "options": ["Assess the situation before acting", "Jump right in and start working", "Ask for more details first", "Delegate it to someone else"],
                "correct": "Assess the situation before acting",
            },
            {
                "type": "sequence",
                "prompt": "Now complete the task — arrange these steps in order:",
                "items": [f"Prepare your {item}", f"Begin {action}", "Check quality", "Clean up"],
                "order": [f"Prepare your {item}", f"Begin {action}", "Check quality", "Clean up"],
            },
            {
                "type": "quick_pick",
                "prompt": _fill_with("Something goes wrong with {item}! {complication}. What do you do?", reps),
                "options": ["Stop, assess, and fix the issue safely", "Push through and hope for the best", "Abandon the task entirely", "Blame someone else"],
                "correct": "Stop, assess, and fix the issue safely",
            },
        ],
        # Config 2: quick_pick → memory → quick_pick
        [
            {
                "type": "quick_pick",
                "prompt": _fill_with("{name} needs you to {action_base} {item} {complication}. First step?", reps),
                "options": ["Check safety procedures first", "Start immediately to save time", "Ask {name} to do it instead", "Wait for instructions"],
                "correct": "Check safety procedures first",
            },
            {
                "type": "memory",
                "prompt": f"Memorize these items for your {action} task:",
                "sequence": random.sample(flavor["objects"], min(4, len(flavor["objects"]))),
            },
            {
                "type": "quick_pick",
                "prompt": _fill_with("The {person} reviews your work. {complication}. How do you respond?", reps),
                "options": ["Explain your process clearly and accept feedback", "Get defensive about your work", "Blame the tools", "Say nothing and walk away"],
                "correct": "Explain your process clearly and accept feedback",
            },
        ],
        # Config 3: sequence → quick_pick → sequence
        [
            {
                "type": "sequence",
                "prompt": f"Start your shift — arrange these steps in order:",
                "items": [f"Check in with {person}", f"Inspect {item}", f"Begin {action}", "Log your start time"],
                "order": [f"Check in with {person}", f"Inspect {item}", f"Begin {action}", "Log your start time"],
            },
            {
                "type": "quick_pick",
                "prompt": _fill_with("A {person} asks about your progress. {complication}. Best response?", reps),
                "options": ["Give a clear, honest status update", "Say everything's fine when it isn't", "Ignore them and keep working", "Get annoyed at the interruption"],
                "correct": "Give a clear, honest status update",
            },
            {
                "type": "sequence",
                "prompt": f"End your shift — arrange these steps in order:",
                "items": [f"Finish {action}", f"Store the {item}", f"Clean up the {item2}", "Submit your report"],
                "order": [f"Finish {action}", f"Store the {item}", f"Clean up the {item2}", "Submit your report"],
            },
        ],
    ]
    stages = random.choice(stage_configs)
    # Shuffle any sequence stages' items
    for stage in stages:
        if stage["type"] == "sequence" and "items" in stage:
            stage["items"] = list(stage["items"])
            random.shuffle(stage["items"])
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
