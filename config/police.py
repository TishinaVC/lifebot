# ============================================================
# POLICE CHASE SYSTEM — Heat, tailing hints, chase minigame config
# ============================================================

# Heat gained per crime type
HEAT_PER_CRIME = {
    "pickpocket": 15,
    "rob": 25,
    "heist": 40,
    "hack": 30,
    "rob_user": 20,
}

# Heat thresholds
HEAT_TAILING_THRESHOLD = 50      # police start tailing at this heat
HEAT_WARRANT_THRESHOLD = 80      # warrant issued — guaranteed arrest attempt
HEAT_MAX = 100

# Heat decay
HEAT_DECAY_PER_TICK = 3          # heat lost per survival decay tick
HEAT_DECAY_INTERVAL = 240        # same as DECAY_INTERVAL

# Tailing escalation
TAILING_INTERACTIONS_TO_ESCALATE = 1  # interactions before escalating to next hint
TAILING_CHANCE_BASE = 0.15       # base chance per activity to start tailing when heat >= threshold
TAILING_CHANCE_HEAT_SCALE = 0.005  # additional chance per heat point above threshold

# Fines and jail
FINE_PER_HEAT = 8                # fine = heat * this value
JAIL_COOLDOWN_BASE = 300         # base jail cooldown in seconds
JAIL_COOLDOWN_PER_HEAT = 5       # additional seconds per heat point
JAIL_COOLDOWN_MAX = 1800         # max jail cooldown

# Chase escape calculation
ESCAPE_BASE_CHANCE = 0.30
ESCAPE_ENERGY_BONUS = 0.20       # max bonus from full energy
ESCAPE_HEALTH_BONUS = 0.10       # max bonus from full health
ESCAPE_LEVEL_BONUS = 0.10        # max bonus from level 50+
ESCAPE_HELP_BONUS = 0.15         # per helper
ESCAPE_HELP_MAX = 2              # max helpers counted
ESCAPE_HEAT_PENALTY = 0.01       # per heat point above 50

# Chase energy costs per stage
CHASE_ENERGY_COST_PER_STAGE = 10
CHASE_HEALTH_RISK_BASE = 5
CHASE_HEALTH_RISK_MAX = 25

# ============================================================
# TAILING HINTS — Escalating narrator hints (3 levels)
# ============================================================
# Level 1: Very subtle — environmental clues
# Level 2: Less subtle — obvious police presence
# Level 3: Arrest attempt — officers approach

TAILING_HINTS = {
    1: [
        "You notice a dark sedan parked across the street. It's been there a while.",
        "A man in a jacket seems to be watching you from a distance. Could be nothing.",
        "You catch a glimpse of someone talking into a radio nearby. Probably just a security guard.",
        "Something feels off. The usual crowd seems different today — someone new is lingering.",
        "A car circles the block for the second time. You're not sure, but it feels like it's watching you.",
        "The shopkeeper's smile falters for just a moment as they glance past you. Weird.",
        "You hear a distant siren. It could be heading anywhere. Right?",
        "There's an unmarked van at the end of the street. You've seen it before... or have you?",
    ],
    2: [
        "Two officers in plainclothes are clearly watching you now. They're not even trying to hide it.",
        "The shopkeeper whispers something to a customer and glances at you nervously. People are talking.",
        "A police radio crackles nearby. You hear your description being read out. Time to think fast.",
        "There are definitely more cops on this street than usual. They're positioning themselves around you.",
        "Someone points at you from across the square. A woman pulls her child closer. The mood has shifted.",
        "You see a uniformed officer speaking into a radio, looking your direction. They're closing in.",
        "A patrol car slows as it passes you. The officer inside is studying your face carefully.",
        "The bartender suddenly remembers they need to close early. They're looking at you apologetically. You should go.",
    ],
}

# ============================================================
# ARREST ATTEMPT — Narrator text when police move in
# ============================================================
ARREST_NARRATIVES = [
    "🚨 **Police are moving in!** Two officers step out from a doorway, badges out. \"Stop right there! You're coming with us!\"",
    "🚨 **It's a bust!** A squad car screeches to a halt. Officers pour out, surrounding the area. \"We've been watching you. Hands where we can see them!\"",
    "🚨 **Warrant served!** A detective approaches with paperwork in hand. \"We have a warrant for your arrest. Come quietly and this goes easier.\"",
    "🚨 **Surrounded!** Officers emerge from multiple directions. You're boxed in. \"You've led us on quite the chase. It's over. Surrender.\"",
    "🚨 **Caught in the act!** Plainclothes officers grab your arm. \"Police! You're under arrest for your recent activities. Don't make this harder.\"",
]

# ============================================================
# CHASE STAGES — Multi-stage text adventure
# ============================================================

CHASE_STAGES = {
    1: {
        "title": "🏃 Initial Flight",
        "narratives": [
            "You shove past the officers and sprint down the street! Sirens erupt behind you. Adrenaline floods your veins. Where do you go?",
            "You break free and bolt! Boots pound the pavement behind you. Multiple officers give chase. You need to lose them — fast!",
            "You knock over a display rack and dash for the exit! Police scramble to follow. The chase is on. Which way?",
        ],
        "choices": [
            {
                "label": "🏚️ Alleys",
                "description": "Duck into the back alleys. Tight spaces, lots of corners. Good for losing tails.",
                "escape_mod": 0.10,
                "energy_cost": 12,
                "health_risk": 8,
            },
            {
                "label": "🏢 Rooftops",
                "description": "Scale the fire escape to the rooftops. High risk, but police can't follow easily.",
                "escape_mod": 0.15,
                "energy_cost": 18,
                "health_risk": 15,
            },
            {
                "label": "🧥 Crowd",
                "description": "Blend into the busy market crowd. Low energy, but risky if spotted.",
                "escape_mod": -0.05,
                "energy_cost": 6,
                "health_risk": 3,
            },
            {
                "label": "🚇 Subway",
                "description": "Dash for the underground subway. If a train is there, you're gone.",
                "escape_mod": 0.05,
                "energy_cost": 10,
                "health_risk": 5,
            },
        ],
    },
    2: {
        "title": "🚓 Pursuit",
        "narratives": {
            "alleys": [
                "You weave through narrow passages, knocking over trash cans behind you. But a chain-link fence blocks your path! Officers are closing in.",
                "The alleys twist and turn. You're gaining ground — until you hit a dead end. A fence looms ahead. You hear boots behind you.",
            ],
            "rooftops": [
                "You leap across rooftops, the city sprawling below. But there's a wide gap between buildings ahead! The police are climbing up behind you.",
                "The wind whips your face as you sprint across the rooftop. A helicopter spotlight sweeps toward you. There's a gap ahead — it's big.",
            ],
            "crowd": [
                "You merge into the bustling market crowd, pulling your hood up. But officers are pushing through, showing your photo to people. You need to move.",
                "You duck behind a stall, heart pounding. An officer passes within feet. Another is scanning the crowd from a raised platform. Stay low or run?",
            ],
            "subway": [
                "You sprint down the subway stairs. You hear a train approaching the platform! But officers are right behind you on the escalator.",
                "The subway tunnel echoes with your footsteps. A train's headlights appear in the tunnel. Officers are at the top of the stairs. It's now or never.",
            ],
        },
        "choices": [
            {
                "label": "💪 Push through",
                "description": "Force your way past the obstacle. Costs energy and health, but maximizes escape distance.",
                "escape_mod": 0.12,
                "energy_cost": 15,
                "health_risk": 18,
            },
            {
                "label": "🧠 Outsmart them",
                "description": "Use the environment to your advantage. Lower risk, but gives police time to close in.",
                "escape_mod": 0.03,
                "energy_cost": 8,
                "health_risk": 6,
            },
            {
                "label": "🫥 Hide",
                "description": "Find a hiding spot and wait for them to pass. Risky — if they search thoroughly, you're caught.",
                "escape_mod": -0.08,
                "energy_cost": 4,
                "health_risk": 2,
            },
            {
                "label": "🚨 Create a diversion",
                "description": "Cause chaos to distract the police. Can work brilliantly or backfire.",
                "escape_mod": 0.06,
                "energy_cost": 10,
                "health_risk": 10,
            },
        ],
    },
    3: {
        "title": "⚡ Final Escape",
        "narratives": [
            "You can hear the police coordinator on the radio — they're setting up a perimeter. This is your last chance to break free before they box you in completely!",
            "A helicopter spotlight sweeps the street. Roadblocks ahead. K-9 units barking. This is it — one final push and you're home free, or you're done.",
            "You're exhausted, but freedom is close. One more obstacle stands between you and escape. The police are right on your heels. What's your move?",
        ],
        "choices": [
            {
                "label": "🥊 Fight through",
                "description": "Bull rush the nearest officer and break the line. High risk, high reward.",
                "escape_mod": 0.20,
                "energy_cost": 20,
                "health_risk": 25,
            },
            {
                "label": "🏭 Find a hideout",
                "description": "Slip into an abandoned building. If they don't search it, you're safe.",
                "escape_mod": 0.05,
                "energy_cost": 8,
                "health_risk": 5,
            },
            {
                "label": "🚗 Steal a vehicle",
                "description": "Hotwire the nearest car. Fast escape, but reckless and dangerous.",
                "escape_mod": 0.12,
                "energy_cost": 12,
                "health_risk": 15,
            },
            {
                "label": "🌊 Go to ground",
                "description": "Disappear into the storm drains. Dark, filthy, but police won't follow.",
                "escape_mod": 0.08,
                "energy_cost": 10,
                "health_risk": 8,
            },
        ],
    },
}

# ============================================================
# CHASE OUTCOMES — Narrative for results
# ============================================================

CHASE_OUTCOMES = {
    "escape": [
        "You did it! You lost them in the maze of streets. You lean against a wall, gasping for air, but you're free. For now.",
        "The sirens fade into the distance. You're safe — for the moment. You duck into a safe house and catch your breath. That was close.",
        "You emerge from hiding an hour later. The police have moved on. You're battered, exhausted, but free. They'll think twice before trying that again.",
        "You blend into the night, disappearing like a ghost. The police search for hours but find nothing. You're in the clear. For now.",
    ],
    "caught": [
        "An officer tackles you from behind! You hit the ground hard. Handcuffs click around your wrists. \"Gotcha,\" someone says. The chase is over.",
        "You turn a corner and run straight into a roadblock. Officers surround you. There's nowhere to go. \"Game's up, friend.\"",
        "A K-9 unit catches your scent. The dog drags you down before you can react. Officers are on you in seconds. Busted.",
        "Your legs give out from exhaustion. You stumble and fall. By the time you try to get up, officers are standing over you. It's over.",
    ],
    "injured_escape": [
        "You break free, but not without cost. You limp away, bleeding from a dozen scrapes. You escaped, but you're hurt bad.",
        "You clear the last obstacle but land wrong. Pain shoots through your body. You crawl into the shadows, injured but alive. Free... barely.",
        "You make it out, but just barely. You're going to feel that chase for a week. At least you're not in handcuffs.",
    ],
    "injured_caught": [
        "You almost made it. But the fall was too much. Officers find you lying in an alley, unable to move. \"Call an ambulance,\" someone says. You're going to jail — after the hospital.",
        "You push too hard and your body gives out. You collapse in the street. Officers cuff you as you fade in and out. Worst outcome possible.",
    ],
}

# ============================================================
# HELP SYSTEM — What other players can do
# ============================================================
HELP_ACTIONS = [
    {
        "id": "distraction",
        "label": "🎆 Create Distraction",
        "description": "Cause a scene to draw police attention away from the runner.",
        "escape_bonus": 0.10,
        "helper_risk": 0,
        "helper_reward_xp": 15,
        "helper_reward_rep": 2,
        "narrative": "{helper} sets off fireworks in the square! Officers turn toward the commotion, giving the runner a window!",
    },
    {
        "id": "escape_route",
        "label": "🚗 Provide Escape Route",
        "description": "Pull up in a getaway car and honk the horn. Let's go!",
        "escape_bonus": 0.15,
        "helper_risk": 5,
        "helper_reward_xp": 25,
        "helper_reward_rep": 3,
        "narrative": "{helper} screeches to a halt in a beat-up sedan! \"GET IN!\" The runner dives into the back seat and they peel out!",
    },
    {
        "id": "block",
        "label": "🚧 Block the Path",
        "description": "Stand in the officers' way and slow them down. Risky for you!",
        "escape_bonus": 0.12,
        "helper_risk": 15,
        "helper_reward_xp": 30,
        "helper_reward_rep": 5,
        "narrative": "{helper} knocks over a fruit stand into the officers' path! \"Sorry! So clumsy!\" The runner gains precious seconds.",
    },
]

# ============================================================
# WARRANT NOTICES — Shown when a warrant is active
# ============================================================
WARRANT_NOTICES = [
    "📋 You've heard whispers — the police have a warrant out for you. Keep your head down.",
    "📋 A friend texts you: \"Cops are looking for you. Lay low.\" Maybe you should listen.",
    "📋 You see your face on a community alert poster. That's not good.",
    "📋 The bartender slides you a note: \"There's a warrant with your name on it. Don't stay in one place too long.\"",
]
