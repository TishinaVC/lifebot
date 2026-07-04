"""Procedural narrative engine — a template-based 'tiny LLM' that runs entirely in-bot.
Generates dynamic event descriptions, NPC encounters, item finds, and story text
without any external API calls or hosting requirements."""

import random
from config import NARRATIVE_TEMPLATES, ITEM_QUALITIES
from config.action_templates import ACTION_TEMPLATES
from utils.quality import (
    roll_quality,
    quality_multiplier,
    quality_value_mult,
    quality_name,
    quality_emoji,
)


def get_action_text(category: str, key: str, **kwargs) -> str:
    """Return a random variant from ACTION_TEMPLATES, formatted with kwargs.
    Falls back to the first variant if the category/key isn't found."""
    cat = ACTION_TEMPLATES.get(category, {})
    templates = cat.get(key)
    if not templates:
        return f"[{category}.{key}]"
    template = random.choice(templates)
    try:
        return template.format(**kwargs)
    except (KeyError, IndexError):
        return template


def generate(category: str, template_key: str, **kwargs) -> str:
    """Generate procedural text from a template category.
    
    Args:
        category: Key in NARRATIVE_TEMPLATES (e.g. 'explore', 'fish', 'mine')
        template_key: Sub-key within the category (e.g. 'intro', 'find_item')
        **kwargs: Variables to fill into templates (e.g. location='a cave')
    
    Returns:
        Generated text string
    """
    cat = NARRATIVE_TEMPLATES.get(category, {})
    templates = cat.get(template_key, [])
    if not templates:
        return ""
    template = random.choice(templates)
    return template.format(**kwargs) if kwargs else template


def generate_explore_intro() -> str:
    """Generate a random exploration intro with location and mood."""
    cat = NARRATIVE_TEMPLATES["explore"]
    location = random.choice(cat["locations"])
    mood = random.choice(cat["moods"])
    return generate("explore", "intro", location=location, mood=mood)


def generate_explore_find(item_name: str) -> str:
    """Generate a find-item description during exploration."""
    return generate("explore", "find_item", item=item_name)


def generate_explore_nothing() -> str:
    """Generate a nothing-found description."""
    return random.choice(NARRATIVE_TEMPLATES["explore"]["find_nothing"])


def generate_npc_encounter() -> tuple:
    """Generate an NPC encounter. Returns (encounter_text, npc_name, outcome_text)."""
    cat = NARRATIVE_TEMPLATES["explore"]
    npc = random.choice(cat["npcs"])
    encounter = random.choice(cat["encounter_npc"]).format(npc=npc)
    outcomes = cat["npc_outcomes"].get(npc, ["does nothing"])
    outcome = random.choice(outcomes)
    return encounter, npc, outcome


def generate_danger(hp_loss: int) -> str:
    """Generate a danger event description."""
    return random.choice(NARRATIVE_TEMPLATES["explore"]["danger"]).format(hp=hp_loss)


def generate_reward(xp_gain: int) -> str:
    """Generate a reward description."""
    return random.choice(NARRATIVE_TEMPLATES["explore"]["reward"]).format(xp=xp_gain)


def generate_fish_cast() -> str:
    """Generate a fishing cast description."""
    spot = random.choice(NARRATIVE_TEMPLATES["fish"]["spots"])
    return generate("fish", "cast", spot=spot)


def generate_fish_catch(fish_name: str) -> str:
    """Generate a fish catch description."""
    return generate("fish", "catch", fish=fish_name)


def generate_fish_nothing() -> str:
    """Generate a fishing nothing-bites description."""
    return random.choice(NARRATIVE_TEMPLATES["fish"]["nothing"])


def generate_mine_swing() -> str:
    """Generate a mining swing description."""
    vein = random.choice(NARRATIVE_TEMPLATES["mine"]["veins"])
    return generate("mine", "swing", vein=vein)


def generate_mine_find(ore_name: str) -> str:
    """Generate a mining find description."""
    return generate("mine", "find", ore=ore_name)


def generate_mine_cave_in() -> str:
    """Generate a cave-in warning."""
    return random.choice(NARRATIVE_TEMPLATES["mine"]["cave_in"])


def roll_random_event() -> dict:
    """Roll a random world event. Returns dict with text and effects.
    
    Returns:
        {"text": str, "coins": int, "xp": int, "hp": int, "energy": int, 
         "hygiene": int, "hunger": int}
    """
    events = NARRATIVE_TEMPLATES["random_event"]["events"]
    total_weight = sum(e.get("weight", 1) for e in events)
    roll = random.randint(1, total_weight)
    cumulative = 0
    event = events[0]
    for e in events:
        cumulative += e.get("weight", 1)
        if roll <= cumulative:
            event = e
            break

    def _roll(val):
        if isinstance(val, tuple):
            return random.randint(val[0], val[1])
        return val

    coins = _roll(event.get("coins", 0))
    xp = _roll(event.get("xp", 0))
    hp = _roll(event.get("hp", 0))
    energy = _roll(event.get("energy", 0))
    hygiene = _roll(event.get("hygiene", 0))
    hunger = _roll(event.get("hunger", 0))

    text = random.choice(event["texts"]).format(
        coins=coins, xp=xp, hp=hp, energy=energy, hygiene=hygiene, hunger=hunger
    )

    return {
        "text": text,
        "coins": coins,
        "xp": xp,
        "hp": hp,
        "energy": energy,
        "hygiene": hygiene,
        "hunger": hunger,
    }


def generate_item_description(item_name: str, quality: str, item_type: str) -> str:
    """Generate a quality-flavored item description."""
    q = ITEM_QUALITIES.get(quality, ITEM_QUALITIES["common"])
    prefixes = {
        "cursed": ["A foul, dark aura surrounds this", "A cursed, twisted", "A warped and unlucky", "A vile, shadow-cloaked", "A wretched, hexed", "A malignant, oozing", "A corrupted, whispering", "A blighted, cold-to-the-touch"],
        "broken": ["A cracked and barely functional", "A damaged, worn-out", "A barely holding together", "A splintered, fragile", "A rusted, groaning", "A chipped and tottering", "A battered, duct-taped", "A sagging, threadbare"],
        "worn": ["A well-used but serviceable", "A scuffed but reliable", "A faded but functional", "A weathered but sturdy", "A chipped but honest", "A dull-edged but proven", "A patched-up but loyal", "A sun-faded but tough"],
        "common": ["A standard", "A plain", "A typical", "A run-of-the-mill", "An ordinary", "An unremarkable", "A basic, no-frills", "A serviceable, everyday"],
        "fine": ["A well-crafted", "A finely made", "A quality", "A carefully forged", "A neatly stitched", "A polished, balanced", "A sturdy, reliable", "A precision-made"],
        "rare": ["An exceptional, gleaming", "A remarkable, polished", "A superior-grade", "An exquisite, flawless", "A gleaming, master-crafted", "A brilliant, razor-sharp", "A pristine, coveted", "An impressive, head-turning"],
        "epic": ["An extraordinary, masterwork", "An awe-inspiring, pristine", "A magnificent, superior", "A breathtaking, flawless", "A legendary-crafted, immaculate", "A resplendent, peerless", "A stunning, world-class", "An opulent, grand"],
        "legendary": ["A legendary, mythic-grade", "An ancient, storied", "A fabled, legendary", "A mythic, world-renowned", "An ageless, revered", "A storied, battle-hardened", "A timeless, celebrated", "An epic, song-worthy"],
        "mythic": ["A godlike, transcendent", "An impossible, reality-bending", "A mythic, world-shaping", "A divine, cosmos-forged", "A supreme, eternal", "A transcendent, universe-altering", "An unfathomable, god-touched", "A reality-warping, supreme"],
    }
    prefix_list = prefixes.get(quality, ["A"])
    prefix = random.choice(prefix_list)
    return f"{prefix} {item_name}. {q['name']} quality — effects multiplied by {q['multiplier']}x."


def maybe_random_event(chance: float = 0.15) -> dict | None:
    """Roll for a random event. Returns event dict or None."""
    if random.random() < chance:
        return roll_random_event()
    return None


def generate_cooking_text(quality: str) -> str:
    """Generate a cooking action description flavored by quality."""
    quality_texts = {
        "cursed": [
            "The food turns black and smokes ominously...",
            "Something went very wrong in the kitchen.",
            "A foul smell rises from the pan. The food hisses at you.",
            "The dish writhes on the plate. You're not sure it's dead.",
            "Shadow leaks from the food like ink. The pot is cold to the touch.",
            "You taste it and your vision goes dark for a moment. Nope.",
            "The ingredients have turned to ash in your mouth. Literally.",
            "Something in the pan is whispering. You decide not to eat it.",
        ],
        "broken": [
            "You burn the food to a crisp. Edible... barely.",
            "The pan catches fire. You salvage what you can.",
            "Smoke fills the kitchen. The fire alarm is screaming.",
            "You forgot about it for ten minutes. The bottom is now carbon.",
            "The food sticks to the pan and tears apart in shreds.",
            "It's technically cooked. If 'cooked' means 'destroyed'.",
            "You scrape the charred remains onto a plate. Bon appetit.",
            "The smoke detector is still beeping. The food is a lost cause.",
        ],
        "worn": [
            "It's a bit overcooked, but it'll do.",
            "Not your best work, but it's food.",
            "The edges are burnt but the center is fine. Mostly.",
            "A little dry, a little chewy, but it fills the belly.",
            "You rushed it. The result is... acceptable.",
            "It won't win any awards, but it's warm and it's yours.",
            "The seasoning is uneven but it's not bad. Not great either.",
            "You plate it and shrug. It is what it is.",
        ],
        "common": [
            "You cook a decent meal.",
            "The food comes out alright. Nothing special.",
            "A solid, unremarkable dish. It does the job.",
            "You follow the recipe and it turns out fine.",
            "Not bad. Not great. Just... food. And that's okay.",
            "The meal is competent. You've made this a hundred times.",
            "It tastes like home. Simple, familiar, adequate.",
            "You cook it the way you always do. It's fine.",
        ],
        "fine": [
            "The aroma is delightful. A solid meal!",
            "You plate it nicely — looks good!",
            "The flavors come together well. A satisfying dish.",
            "You season it just right. Tasty!",
            "The texture is perfect, the seasoning is on point. Well done.",
            "You take a bite and nod. Yeah, that's good cooking.",
            "The kitchen smells wonderful. This is a proper meal.",
            "You garnish it with care. Presentation matters, and this shows.",
        ],
        "rare": [
            "The flavors are exceptional! A truly fine dish.",
            "You instinctively season it perfectly. Wonderful!",
            "The sauce reduces beautifully. This is something special.",
            "Every bite is better than the last. You outdid yourself.",
            "The aroma alone makes your mouth water. Excellent work.",
            "You knife-work is precise, the cook is spot-on. Impressive.",
            "The balance of salt, fat, acid, and heat is masterful.",
            "This is the kind of dish you'd pay good money for. Nice.",
        ],
        "epic": [
            "This is restaurant-quality! Magnificent!",
            "The kitchen smells incredible. A masterpiece!",
            "You've elevated a simple recipe into something extraordinary.",
            "The plating is artful, the flavors are sublime. Bravo.",
            "You taste it and your eyes go wide. This is exceptional.",
            "The sauce is silky, the protein is juicy, the crust is perfect.",
            "This would impress a food critic. Seriously impressive.",
            "Every element sings in harmony. This is what cooking should be.",
        ],
        "legendary": [
            "You've created something extraordinary. A legendary dish!",
            "Every bite is perfection. This is the stuff of legends!",
            "The flavors dance on your tongue. This will be talked about for years.",
            "You've achieved something rare — a dish that transcends skill. This is art.",
            "The aroma fills the entire building. People are knocking on the door.",
            "You take a bite and time stops. This is the best thing you've ever cooked.",
            "The texture, the flavor, the presentation — all flawless. A career-defining dish.",
            "This meal could make a grown man weep. Absolutely legendary.",
        ],
        "mythic": [
            "The food glows with an otherworldly aura. A mythic creation!",
            "You've transcended cooking. This dish is mythical!",
            "The ingredients seem to have transformed into something divine.",
            "Golden light pours from the plate. The aroma is intoxicating.",
            "You've broken the boundaries of cuisine. This is god-tier cooking.",
            "The dish hums with energy. Eating it feels like a spiritual experience.",
            "Reality bends around the plate. This food should not exist. And yet.",
            "You've created a dish that legends will be written about. Mythic.",
        ],
    }
    texts = quality_texts.get(quality, quality_texts["common"])
    return random.choice(texts)


def generate_travel_text(location_name: str) -> str:
    """Generate a travel description for a location."""
    templates = [
        f"You set off toward {location_name}, the road stretching ahead.",
        f"The journey to {location_name} takes you through familiar streets.",
        f"You make your way to {location_name}, watching the scenery change.",
        f"Footsteps carry you closer to {location_name}.",
        f"The path to {location_name} winds through the city.",
        f"You head toward {location_name}, the sounds of the city fading behind you.",
        f"The road to {location_name} is long but the weather is fair.",
        f"You walk with purpose toward {location_name}, anticipation building.",
        f"Streets blur past as you make your way to {location_name}.",
        f"You take the scenic route to {location_name}, enjoying the walk.",
        f"The way to {location_name} is quieter than usual. Peaceful.",
        f"You navigate the alleys and main roads toward {location_name}.",
        f"A cool breeze accompanies you on the walk to {location_name}.",
        f"You can see {location_name} in the distance now. Almost there.",
        f"The streets grow more familiar as you approach {location_name}.",
        f"You pick up the pace as {location_name} comes into view.",
        f"The walk to {location_name} gives you time to think.",
        f"You round the last corner and {location_name} greets you.",
        f"The journey to {location_name} is uneventful but pleasant.",
        f"You arrive at the outskirts of {location_name}, taking it all in.",
    ]
    return random.choice(templates)


def generate_npc_dialogue(personality: str) -> str:
    """Generate personality-flavored NPC dialogue."""
    dialogues = {
        "shrewd": [
            "Everything has a price, friend. Everything.",
            "I didn't get where I am by being careless.",
            "Let's make a deal that benefits us both, yes?",
            "A good merchant reads people like books. And you? You're an open book.",
            "Profit is not greed. Profit is survival. There's a difference.",
            "I've never met a coin I didn't like. Can you blame me?",
            "The secret to wealth? Buy low, sell high, and never trust a stranger's tears.",
            "Every transaction is a negotiation. Even this conversation.",
            "I can tell you're weighing your options. Good. That means you're smart.",
            "There's always a market for someone willing to hustle. Are you?",
            "I don't do charity. I do mutual benefit. There's a difference.",
            "The best deals are the ones where everyone thinks they won.",
        ],
        "wise": [
            "Patience is the angler's greatest tool.",
            "The river teaches you more than any book.",
            "Time flows like water — you can't hold it, but you can ride it.",
            "The oldest fish in the river is the one that never took the bait.",
            "Wisdom isn't knowing all the answers. It's knowing which questions to ask.",
            "A calm mind sees what a busy mind misses.",
            "The water doesn't fight the rock. It flows around it. Remember that.",
            "Youth rushes. Age observes. Both have their place.",
            "Every mistake is a lesson wearing a disguise.",
            "The river doesn't care about your plans. Fish anyway.",
            "Stillness is not laziness. The baited hook is patient, and so must you be.",
            "The wise person learns from the river: it gives without asking, and never stops.",
        ],
        "tough": [
            "Down here, only the strong survive.",
            "I've seen tougher than you. But maybe you'll surprise me.",
            "Rock doesn't care about your feelings. Neither do I. Much.",
            "You want respect? Earn it. The mine doesn't hand out medals.",
            "Pain is just weakness leaving the body. Keep swinging.",
            "I've buried three partners in these tunnels. You won't be the fourth. Probably.",
            "The mountain doesn't move for anyone. You move for it.",
            "Fear is fine. Letting it stop you is not. Keep going.",
            "You think you're tough? The rock will test that. It always does.",
            "I don't do encouragement. I do honesty. And honestly? You might make it.",
            "Every scar down here tells a story. What story will yours tell?",
            "The weak complain. The strong dig. Which are you?",
        ],
        "cheerful": [
            "Oh, how wonderful to see you! Let me fix you something!",
            "Every meal is a chance to make someone smile!",
            "The secret ingredient? It's always love. And butter.",
            "You look hungry! Don't worry, I've got just the thing!",
            "Cooking is my love language, and you're about to be fluently loved!",
            "Life is short — eat dessert first! Or second. Or third!",
            "A warm meal and a warm heart — that's all anyone needs!",
            "The kitchen is the happiest place in the world. Welcome to it!",
            "I had a bad day once. Then I made soup. It fixed everything!",
            "You're not just a customer. You're a guest. There's a difference!",
            "Food made with a frown tastes like a frown. So I always smile!",
            "The world can be cold, but this kitchen is always warm. Come in!",
        ],
        "mysterious": [
            "The veil between worlds is thin today...",
            "I see patterns where others see chaos. You are... interesting.",
            "There are whispers in the wind. Do you hear them?",
            "The crystal shows me many things. Your path is... clouded.",
            "I know what you seek before you speak it. The spirits told me.",
            "Every shadow hides a door. Not all doors should be opened.",
            "You carry a burden you haven't named yet. I can feel its weight.",
            "The stars are restless tonight. Something is coming. Something old.",
            "I speak in riddles because the truth is too sharp for plain words.",
            "Your aura flickers. Doubt? Fear? Or something deeper...",
            "The cards have shown your face before. I wondered when you'd arrive.",
            "There are threads connecting all things. Yours are... tangled.",
        ],
        "friendly": [
            "Always good to chat with a neighbor! How are things?",
            "You're welcome here anytime. The forest is for everyone.",
            "I've got tea brewing if you want to rest a while.",
            "Hey there! Good to see a friendly face on the trail!",
            "No need to rush — sit down, catch your breath. The forest can wait.",
            "You look like you could use a break. I've got water and shade.",
            "The woods are kind to those who walk them gently. You're doing fine.",
            "I always feel better after a chat. Thanks for stopping by!",
            "If you ever need directions or a warm meal, you know where to find me.",
            "The forest provides, and so do I. What can I do for you?",
            "It's a good day when a friend drops by. Even an unexpected one!",
            "You carry the smell of the trail with you. Been walking long?",
        ],
        "gruff": [
            "Don't waste my time. What do you need?",
            "Talk fast. The forge won't tend itself.",
            "Hmph. You again? Fine. What is it?",
            "State your business and make it quick. I'm behind on orders.",
            "I don't do small talk. What do you want forged?",
            "You're blocking my light. Move or make it worth my while.",
            "If you're here to chat, go find the chef. If you're here for work, speak.",
            "The anvil's hot and so am I. What do you need?",
            "I've got iron to shape and no patience for dawdling. Talk.",
            "You want something or you're just loitering? Which is it?",
            "Make it short. I've already spent more words on you than I should.",
            "The forge doesn't pause for pleasantries. Neither do I. Go.",
        ],
        "suspicious": [
            "Keep your voice down. Walls have ears.",
            "You're asking too many questions. Be careful.",
            "I don't know you. And I don't need to. Understood?",
            "Who sent you? No one? That's either a lie or a problem.",
            "If you're here for information, it'll cost you. And not just coin.",
            "Look around. Notice anything? No? Then you're not paying attention.",
            "I don't do trust. I do transactions. There's a difference.",
            "You've got nervous hands. That's either smart or guilty. Which?",
            "The less you know about me, the longer you'll live. Friendly advice.",
            "People who ask questions in this alley don't always get answers. Sometimes they get trouble.",
            "I work in shadows. If you want sunlight, go to the market.",
            "Say what you need and vanish. That's how this works.",
        ],
    }
    texts = dialogues.get(personality, dialogues["friendly"])
    return random.choice(texts)


# ============================================================
# WORLD-AWARE NARRATIVE — text generation that reflects living world state
# ============================================================

async def generate_world_flavored_explore(location_id: str = None) -> str:
    """Generate an exploration intro flavored by the world state of the location."""
    import world as w

    if location_id:
        state = await w.get_location_state(location_id)
        from config import LOCATIONS
        loc_data = LOCATIONS.get(location_id, {})
        loc_name = loc_data.get("name", "the area")
        atmos = state.get("atmosphere", 0.5)
        pop = state.get("population", 0.25)
        danger = state.get("danger", 0.1)

        if atmos < 0.2:
            mood = random.choice([
                f"The air feels heavy and gloomy as you enter {loc_name}.",
                f"A oppressive stillness settles over {loc_name}. Something's not right here.",
                f"The light seems dimmer in {loc_name}. Shadows cling to every corner.",
                f"You step into {loc_name} and immediately feel uneasy. The air is thick.",
            ])
        elif atmos > 0.8:
            mood = random.choice([
                f"The energy in {loc_name} is electric — something exciting is happening!",
                f"{loc_name} is alive with energy. You can feel it in your bones.",
                f"There's a buzz in the air as you enter {loc_name}. Something big is going on.",
                f"The atmosphere in {loc_name} is charged with excitement. You're drawn in.",
            ])
        elif pop < 0.1:
            mood = random.choice([
                f"{loc_name} is eerily deserted. Your footsteps echo.",
                f"Not a soul in sight in {loc_name}. The silence is unsettling.",
                f"{loc_name} is empty — abandoned-looking. You're alone here.",
                f"You wander into {loc_name}. It's a ghost town. Where is everyone?",
            ])
        elif pop > 0.7:
            mood = random.choice([
                f"{loc_name} is bustling with activity. People everywhere.",
                f"The streets of {loc_name} are packed. You weave through the crowd.",
                f"{loc_name} is alive with people — talking, shouting, living. It's chaotic.",
                f"You can barely move in {loc_name}. The crowds are thick and energetic.",
            ])
        elif danger > 0.4:
            mood = random.choice([
                f"You feel a sense of danger as you enter {loc_name}.",
                f"{loc_name} feels threatening. You watch your step and keep your guard up.",
                f"There's tension in the air of {loc_name}. Something bad could happen here.",
                f"You enter {loc_name} cautiously. The place feels risky.",
            ])
        else:
            mood = generate_explore_intro()
        return mood
    else:
        return generate_explore_intro()


async def generate_world_flavored_npc_dialogue(npc_id: str, personality: str) -> str:
    """Generate NPC dialogue flavored by their current mood and tension."""
    import world as w

    state = await w.get_npc_state(npc_id)
    mood = state.get("mood", 0.5)
    tension = state.get("tension", 0.3)

    base = generate_npc_dialogue(personality)

    if mood < 0.25:
        prefix = random.choice([
            "*They scowl at you.* ", "*Their expression is dark.* ",
            "*They seem upset.* ", "*They barely look at you.* ",
            "*They sigh heavily before acknowledging you.* ",
            "*Their jaw tightens as they turn to face you.* ",
            "*They look like they're in a terrible mood.* ",
            "*Their greeting is cold and clipped.* ",
        ])
    elif mood > 0.75:
        prefix = random.choice([
            "*They beam at you warmly.* ", "*Their eyes light up.* ",
            "*They greet you with a big smile.* ", "*They seem genuinely happy to see you.* ",
            "*They wave enthusiastically.* ",
            "*Their whole demeanor brightens when they see you.* ",
            "*They chuckle and clap you on the shoulder.* ",
            "*They look like your arrival just made their day.* ",
        ])
    elif tension > 0.6:
        prefix = random.choice([
            "*They glance around nervously.* ", "*They speak in a tense whisper.* ",
            "*Something seems to be bothering them.* ",
            "*They jump at a noise behind them.* ",
            "*They keep checking over their shoulder.* ",
            "*Their hands shake slightly as they talk.* ",
            "*They look like they haven't slept well.* ",
            "*Their voice is strained and edgy.* ",
        ])
    else:
        prefix = ""

    return prefix + base


async def generate_world_flavored_fish(location_id: str = None) -> str:
    """Generate a fishing cast flavored by location resources and weather intensity."""
    import world as w

    base = generate_fish_cast()

    if location_id:
        state = await w.get_location_state(location_id)
        res = state.get("resources", 0.6)
        if res < 0.2:
            base += random.choice([
                " The waters seem depleted lately.",
                " The fishing spot looks overfished and barren.",
                " You can tell the pickings have been slim here.",
                " Not much life left in these waters.",
            ])
        elif res > 0.8:
            base += random.choice([
                " The waters are teeming with life today!",
                " Fish are practically jumping out of the water!",
                " The spot is rich — you can see movement everywhere.",
                " This place is overflowing with fish. Perfect conditions!",
            ])

    intensity = await w.get_weather_intensity()
    if intensity > 0.7:
        base += random.choice([
            " The weather is fierce, making it hard to focus.",
            " Wind and spray batter your face as you cast.",
            " The rough conditions make every cast a challenge.",
            " You squint against the elements, determined to fish on.",
        ])

    return base


async def generate_world_flavored_mine(location_id: str = None) -> str:
    """Generate a mining swing flavored by location resources and danger."""
    import world as w

    base = generate_mine_swing()

    if location_id:
        state = await w.get_location_state(location_id)
        res = state.get("resources", 0.6)
        danger = state.get("danger", 0.1)
        if res < 0.2:
            base += random.choice([
                " The seams look picked clean.",
                " Not much ore left in this section.",
                " The walls show signs of heavy mining. Depleted.",
                " You can see where others have already taken the best stuff.",
            ])
        elif res > 0.8:
            base += random.choice([
                " Rich veins glint everywhere you look!",
                " The walls are thick with unmined ore. Jackpot.",
                " You can see glittering deposits all around. Rich ground!",
                " This section is practically untouched. Full of potential.",
            ])
        if danger > 0.4:
            base += random.choice([
                " The walls groan ominously.",
                " Dust trickles from the ceiling. This place is unstable.",
                " You hear deep creaking from the rock. Dangerous.",
                " A distant rumble reminds you how deep you are. Stay alert.",
            ])

    return base


async def generate_atmosphere_text(location_id: str) -> str:
    """Generate a short atmospheric description based on location world state."""
    import world as w

    state = await w.get_location_state(location_id)
    atmos = state.get("atmosphere", 0.5)
    pop = state.get("population", 0.25)

    if atmos > 0.75 and pop > 0.6:
        return random.choice([
            "The area buzzes with energy and life.",
            "There's a vibrant, electric feeling in the air.",
            "People are everywhere, and the mood is infectious.",
            "The streets hum with activity and excitement.",
            "You can feel the pulse of the crowd — alive, loud, thriving.",
            "This place is bursting with energy. It's hard not to get caught up in it.",
        ])
    elif atmos < 0.2 and pop < 0.15:
        return random.choice([
            "An oppressive silence hangs over the area.",
            "The place feels abandoned and desolate.",
            "Shadows stretch long in the empty streets.",
            "Not a sound, not a movement. The area is dead quiet.",
            "A chill settles in your chest. The emptiness is unsettling.",
            "You feel like the last person in the world standing here.",
        ])
    elif atmos > 0.6:
        return random.choice([
            "There's a pleasant buzz in the air.",
            "The atmosphere feels warm and welcoming.",
            "A gentle energy pervades the area.",
            "The mood here is upbeat and inviting.",
            "You feel comfortable here. The vibe is good.",
            "A soft hum of contentment fills the area.",
        ])
    elif atmos < 0.35:
        return random.choice([
            "A somber mood settles over the area.",
            "Things feel quiet and subdued here.",
            "The atmosphere is muted, almost melancholic.",
            "A grey feeling permeates the place. Not sad, just... heavy.",
            "The energy here is low. People move slowly, speak softly.",
            "You feel a weight on your shoulders just standing here.",
        ])
    else:
        return random.choice([
            "The area feels calm and unremarkable.",
            "Nothing particularly notable about the atmosphere right now.",
            "It's a typical day in this part of the world.",
            "The mood is neutral — neither good nor bad. Just... fine.",
            "A quiet, ordinary atmosphere. The world goes on.",
            "Everything is as it usually is. Steady, uneventful, normal.",
        ])
