# Lifebot

A full-featured Discord life simulation bot with economy, survival mechanics, housing, crafting, exploration, NPCs, factions, and procedural narrative generation.

## Tech Stack

- **Python 3.11+**
- **discord.py** — Discord bot framework with slash commands
- **aiosqlite** — Async SQLite database driver
- **python-dotenv** — Environment variable loading

No external APIs. All content is generated in-bot via procedural templates.

## Setup

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your `DISCORD_TOKEN`
4. Run: `python main.py`

## Project Structure

```
Lifebot/
├── main.py              # Bot setup, cog loading, /help /ping /profile /reset
├── config/              # All game configuration (modular)
│   ├── core.py          # Bot token, DB path, starting values, max stats, decay
│   ├── items.py         # Store items (food, drinks, medical, boosters, hygiene, collectibles, stat boosters)
│   ├── equipment.py     # Tools, clothing, possessions, raw materials, crafting recipes, item qualities
│   ├── store_catalog.py # Hierarchical store catalog with categories, subcategories, and special deals
│   ├── jobs.py          # Job definitions
│   ├── pets.py          # Pet definitions
│   ├── achievements.py  # Achievement definitions
│   ├── quests.py        # Quest definitions
│   ├── housing.py       # Housing tiers, upgrades, decorations
│   ├── weather.py       # Weather states
│   ├── npcs.py          # NPC definitions
│   ├── locations.py     # Location definitions
│   ├── time_periods.py  # Day/night cycle time periods
│   ├── immersion.py     # Cooking recipes, buff types, factions
│   ├── police.py        # Police heat, tailing, chase config
│   ├── stats.py         # Stat definitions
│   ├── job_requirements.py
│   ├── minigame_content.py
│   ├── narrative_templates.py
│   └── action_templates.py  # Procedural action text templates
├── database/            # SQLite schema + async DB functions (modular)
├── world.py             # Living world simulation engine (vectors, perturbations, tick loop)
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── cogs/                # Discord command cogs (modular feature groups)
│   ├── economy.py       # Balance, deposit, withdraw, pay, leaderboard
│   ├── jobs.py          # Jobs, work
│   ├── gambling.py      # Coinflip, dice, slots, blackjack, roulette
│   ├── store.py         # Interactive shop (Views/Buttons), buy, use, sell, equipment, special deals
│   ├── survival.py      # Status, hospital, heal, sleep, shower, stat decay
│   ├── leveling.py      # Rank, level rewards
│   ├── daily.py         # Daily/weekly rewards
│   ├── crime.py         # Crime, rob
│   ├── social.py        # Marry, divorce, relationship, gift
│   ├── pets.py          # Pet shop, adopt, feed, play, battle
│   ├── achievements.py  # Achievements, stats
│   ├── quests.py        # Daily quests
│   ├── housing.py       # Buy/rent/sell homes, upgrades, decorations, storage, market
│   ├── weather.py       # Weather display + background weather loop
│   ├── activities.py    # Fish, mine, explore, forage, chop, dig, craft, equipment
│   └── immersion.py     # Travel, NPCs, cooking, buffs, reputation, time
├── utils/
│   ├── embeds.py        # Discord embed helpers (success, error, info, money, stat bars)
│   ├── helpers.py       # XP calc, stat modifiers, housing/equipment/combined bonuses
│   └── narrative.py     # Procedural text generation engine
└── lifebot.db           # SQLite database (auto-created on first run)
```

## Key Systems

### Economy & Jobs
- Wallet + bank with capacity upgrades
- 200 jobs across 8 categories (entry, service, trades, medical, tech, business, creative, transport)
- 38 subcategories with interactive select-menu navigation
- 3 minigames per job (randomly selected each shift, category-themed)
- 24 minigame types with job-specific themed content
- 2-slot job system with stat/qual requirements, XP, and cooldowns
- Gambling: coinflip, dice, slots, blackjack, roulette

### Survival Stats
- Health, hunger, thirst, energy, hygiene
- Background decay loop
- Hospital on death (50% wallet penalty)
- Sleep/shower to restore energy/hygiene

### Activities
- Fishing (requires fishing rod), mining (requires pickaxe)
- Exploration, foraging, wood chopping, digging
- Crafting from raw materials (7 recipes)
- All activities roll item quality (9 tiers: cursed → mythic)

### Interactive Store
- Button-driven hierarchical navigation (categories → subcategories → items)
- Supports infinite categories and subcategories (bypasses Discord's 25-choice limit)
- Flash sales (random category discounted every 6 hours)
- Daily deals (one item at 40% off, changes daily)
- Mystery Box (random item, rarity-weighted)
- Lucky Dip (cheap random item)
- Traveler's Pack (guaranteed items + chance at rare bonus items)
- Autocomplete on all buy/use/sell slash commands for quick access
- Pagination for item lists (10 items per page)

### Equipment
- Tools (19), clothing (40), possessions (22) with quality + durability
- Stat bonuses from equipped items
- Equipment damages with use

### Housing (20 tiers)
- Buy or rent homes
- Upgrades (security, garden, workshop, etc.)
- Decorations
- Home storage
- Player-to-player housing market

### World & NPCs
- 10 locations with unique activities, NPCs, danger levels, loot tables
- 8 NPCs with personalities, dialogue, trades, and quests
- Travel between locations (energy cost, random encounters)

### Day/Night Cycle
- 7 time periods (dawn → midnight)
- Each affects work pay, fish luck, crime success, encounter rates
- Game time advances 1 hour every 30 minutes real time

### Weather
- 8 weather states with gameplay effects
- Affects energy/hygiene decay, work pay, crime, fishing, rare finds
- Changes every 30 minutes

### Cooking & Buffs
- 8 cooking recipes using raw ingredients
- Cooked food grants temporary buffs (regen, work pay, luck, etc.)
- Buffs auto-expire and integrate with all gameplay systems

### Reputation & Factions
- 6 factions: merchants, fishers, miners, explorers, chefs, underworld
- Reputation gained through related activities
- Tiered benefits at 10/25/50 reputation thresholds

### Quests & Achievements
- Daily quests with progress tracking
- NPC quests (deliver, catch, mine, explore, crime)
- Achievement system with coin/XP rewards

### Procedural Narrative
- Template-based text generation for all activities
- Quality-flavored item descriptions
- NPC dialogue by personality type
- Random events with weighted outcomes

## Configuration

All game balance and content is defined in modular config files under `config/`:
- `items.py`: `STORE_ITEMS` (food, drinks, medical, boosters, stat boosters, hygiene, collectibles)
- `equipment.py`: `TOOLS`, `CLOTHING`, `POSSESSIONS`, `RAW_MATERIALS`, `CRAFTING_RECIPES`, `ITEM_QUALITIES`
- `store_catalog.py`: `STORE_CATALOG`, `MYSTERY_BOX`, `DAILY_DEAL`, `FLASH_SALE`, `LUCKY_DIP`, `TRAVELER_PACK`
- `jobs.py`, `pets.py`, `achievements.py`, `quests.py`
- `housing.py`: `HOUSING_TIERS`, `HOME_UPGRADES`, `HOME_DECORATIONS`
- `weather.py`: `WEATHER_STATES`
- `npcs.py`, `locations.py`, `time_periods.py`
- `immersion.py`: `COOKING_RECIPES`, `BUFF_TYPES`, `FACTIONS`
- `police.py`: Heat thresholds, chase stages, tailing config
- `narrative_templates.py`, `action_templates.py`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DISCORD_TOKEN` | Bot token from Discord Developer Portal | Required |
| `DB_PATH` | SQLite database file path | `lifebot.db` |
| `PREFIX` | Legacy command prefix (unused with slash commands) | `!` |

## Roadmap

### Completed
- [x] Interactive store with button navigation (infinite categories/subcategories)
- [x] Special deals: Mystery Box, Daily Deal, Flash Sale, Lucky Dip, Traveler's Pack
- [x] Autocomplete on all buy/use/sell commands
- [x] Expanded item catalog (130+ store items, 19 tools, 40 clothing, 22 possessions)
- [x] 200 jobs across 8 categories, 38 subcategories, nested select-menu navigation
- [x] 3 minigames per job (randomly selected each shift, category-themed pools)
- [x] 24 minigame types with job-specific themed content
- [x] 2-slot job system with stat/qual requirements, XP, cooldowns
- [x] Living world simulation (NPC moods, location dynamics, market demand)
- [x] Police evasion minigame (heat system, tailing, multi-stage chase)
- [x] Weather-triggered debuffs (Soaked, Frostbite, Heatstroke, etc.)
- [x] Housing bonuses for sleep/shower
- [x] Procedural narrative templates for all actions
- [x] 7 immersion systems (NPC, locations, day/night, cooking, buffs, narrative, reputation)

### Planned — Job Expansion

#### New Job Categories (12+ new categories)
- [ ] **Education** — Teachers, professors, tutors, librarians, coaches
  - Subcategories: Primary (substitute, TA, tutor), Secondary (teacher, counselor, librarian), Higher Ed (professor, dean, researcher), Specialty (music teacher, art teacher, PE coach)
- [ ] **Law & Government** — Lawyers, judges, clerks, politicians
  - Subcategories: Legal (paralegal, lawyer, defense attorney, prosecutor, judge), Civil Service (clerk, notary, social worker, case worker), Government (mayor, governor, senator, diplomat)
- [ ] **Law Enforcement** — Police, detectives, security
  - Subcategories: Patrol (security guard, cop, sheriff, state trooper), Investigation (detective, forensic analyst, PI, FBI agent), Federal (DEA, ATF, US Marshal, secret service)
- [ ] **Agriculture & Farming** — Farmers, ranchers, gardeners
  - Subcategories: Crops (farmhand, farmer, agronomist, harvest manager), Livestock (ranch hand, rancher, vet tech, dairy manager), Specialty (beekeeper, vintner, orchardist, horticulturist)
- [ ] **Media & Journalism** — Reporters, editors, broadcasters
  - Subcategories: Print (reporter, editor, columnist, editor-in-chief), Broadcast (news anchor, weather presenter, field reporter), Digital (podcaster, blogger, content creator, social media manager)
- [ ] **Sports & Fitness** — Athletes, trainers, coaches
  - Subcategories: Athletics (gym trainer, personal trainer, yoga instructor, crossfit coach), Competitive (amateur athlete, pro athlete, coach, sports manager), Specialty (physio, sports medic, referee, commentator)
- [ ] **Military** — Soldiers, officers, specialists
  - Subcategories: Enlisted (recruit, infantry, medic, engineer), Officer (lieutenant, captain, major, general), Specialty (pilot, sniper, intelligence officer, special forces)
- [ ] **Religion & Spiritual** — Priests, monks, fortune tellers
  - Subcategories: Clergy (acolyte, priest, bishop, pastor), Mystical (fortune teller, tarot reader, medium, oracle), Wellness (meditation guide, retreat leader, spiritual counselor)
- [ ] **Hospitality & Tourism** — Tour guides, hotel staff, cruise staff
  - Subcategories: Accommodation (bellhop, concierge, housekeeping, resort manager), Tourism (tour guide, travel agent, cruise director, expedition leader), Entertainment (casino dealer, event host, theme park worker, cruise performer)
- [ ] **Fashion & Beauty** — Models, stylists, barbers
  - Subcategories: Hair & Beauty (barber, hairstylist, nail tech, esthetician), Fashion (model, stylist, personal shopper, fashion consultant), Wellness (spa therapist, massage therapist, makeup artist)
- [ ] **Engineering** — Civil, mechanical, aerospace engineers
  - Subcategories: Civil (junior engineer, civil engineer, structural engineer, chief engineer), Mechanical (mechanical engineer, robotics engineer, automotive engineer), Aerospace (aerospace engineer, propulsion engineer, flight test engineer)
- [ ] **Emergency Services** — Firefighters, rescue, disaster response
  - Subcategories: Fire (probationary firefighter, firefighter, fire captain, fire chief), Rescue (lifeguard, search & rescue, mountain rescue, swiftwater rescue), Medical (EMT, paramedic supervisor, flight medic, disaster coordinator)

#### New Minigame Types (job-specific, "feel like doing the job")
- [ ] **code_review** — Spot bugs in code snippets (programmer, QA, web dev)
- [ ] **diagnose_car** — Match symptoms to car problems (mechanic)
- [ ] **mix_chemicals** — Combine reagents in correct order (chemist, pharmacist)
- [ ] **interrogate** — Choose questions to ask a suspect (detective, lawyer)
- [ ] **lesson_plan** — Arrange topics in teaching order (teacher, professor, tutor)
- [ ] **court_case** — Present evidence in the right order (lawyer, prosecutor)
- [ ] **workout_routine** — Sequence exercises by muscle group (trainer, athlete)
- [ ] **farm_harvest** — Time-based crop harvesting mini-game (farmer, rancher)
- [ ] **broadcast** — Read news script with timing precision (anchor, reporter)
- [ ] **surgery_sim** — Precision-based surgical cuts at exact points (surgeon, neurosurgeon)
- [ ] **negotiate_deal** — Back-and-forth offer/counteroffer (negotiator, real estate, sales)
- [ ] **tune_engine** — Adjust sliders to hit target performance values (mechanic, engineer)
- [ ] **wire_circuit** — Connect components to complete a circuit (electrician, engineer)
- [ ] **recipe_taste** — Identify ingredients from taste test descriptions (chef, sommelier, food critic)
- [ ] **patrol_route** — Plan patrol through dangerous areas avoiding threats (cop, security, military)
- [ ] **translate** — Match phrases between languages (diplomat, translator, interpreter)
- [ ] **debug_trace** — Follow execution path to find the bug (programmer, devops, backend dev)
- [ ] **balance_books** — Accounting puzzle: match debits to credits (accountant, bookkeeper, auditor)
- [ ] **decorate_room** — Place items to match a design brief (interior designer, event planner)
- [ ] **triage_emergency** — Sort patients by severity under time pressure (nurse, EMT, paramedic)
- [ ] **flight_plan** — Plot course avoiding weather and traffic (pilot, air traffic controller)
- [ ] **crop_rotation** — Plan seasonal planting for maximum yield (farmer, agronomist)
- [ ] **intercept_signal** — Tune radio frequency to intercept message (military intel, dispatcher)
- [ ] **spa_treatment** — Sequence spa steps for client satisfaction (massage therapist, esthetician)
- [ ] **fitness_assessment** — Evaluate client and recommend workout plan (personal trainer, physio)
- [ ] **sermon** — Arrange sermon/wisdom points in compelling order (priest, pastor, counselor)
- [ ] **tour_narration** — Deliver tour facts in engaging order (tour guide, cruise director)
- [ ] **evidence_board** — Connect clues to solve a case (detective, forensic analyst, PI)

#### More Minigame Content for Existing Jobs
- [ ] Write job-specific content for all 3 minigame types per job (currently many fall back to GENERIC for games #2 and #3)
- [ ] Add difficulty scaling — minigames get harder at higher job levels (more steps, tighter timing, more options)
- [ ] Add combo/streak bonuses — consecutive correct actions multiply rewards
- [ ] Add visual polish — progress bars, color-coded feedback, animated reactions

### Planned — Feature Depth & Interwiring

#### Job ↔ Equipment Interwiring
- [ ] Job-specific equipment requirements (mechanic needs wrench, chef needs knife, doctor needs stethoscope)
- [ ] Equipment quality boosts minigame performance (better tools = wider timing windows, fewer options, hints)
- [ ] Equipment durability degrades from job use (not just activities)
- [ ] Job-specific tools sold in store (new store category: "Professional Equipment")
- [ ] Crafting recipes for job-specific tools (sharpen knife, calibrate instruments)

#### Job ↔ Stats Interwiring
- [ ] Job level increases relevant stats passively (chef gains dexterity, programmer gains intelligence)
- [ ] Stat thresholds unlock higher-tier jobs within a career path
- [ ] Minigame performance affected by current stats (low energy = slower timing, low focus = more options)

#### Job ↔ Store/Economy Interwiring
- [ ] Job-specific consumables in store (energy drinks for physical jobs, coffee for office jobs, medical supplies for medical jobs)
- [ ] Salary deposits — passive income based on job level (small trickle between active work shifts)
- [ ] Job-specific discounts in store (chef gets cooking supplies cheaper, mechanic gets parts cheaper)
- [ ] Dynamic pricing: store prices influenced by living world market demand vector

#### Job ↔ Weather/Time Interwiring
- [ ] Weather affects outdoor jobs (construction slower in rain, farming boosted by good weather, delivery harder in snow)
- [ ] Time-of-day pay modifiers (night shift premium for medical/transport, daytime bonus for service/creative)
- [ ] Seasonal job availability (agriculture jobs change with seasons, retail spikes during holidays)

#### Job ↔ Police/Crime Interwiring
- [ ] Law enforcement jobs reduce heat over time (cop, detective passively lower heat)
- [ ] High heat blocks law enforcement and government jobs (can't be a cop with a warrant)
- [ ] Crime jobs (hacker, lockpick) have higher pay but add heat each shift
- [ ] Underworld faction reputation unlocks crime-adjacent jobs (fence, smuggler, fixer)

#### Job ↔ Housing Interwiring
- [ ] Home office boosts work-from-home jobs (programmer, writer, trader, consultant)
- [ ] Workshop upgrade boosts trade jobs (carpenter, welder, mechanic)
- [ ] Kitchen upgrade boosts cooking jobs (chef, baker, caterer)
- [ ] Commute time: living far from "work district" costs extra energy per shift
- [ ] Home storage for job-specific materials and tools

#### Job ↔ NPC/Reputation Interwiring
- [ ] NPC relationships unlock exclusive job offers (high reputation with merchant NPC unlocks trader jobs)
- [ ] Faction reputation gates certain job categories (underworld rep for crime jobs, merchant rep for business jobs)
- [ ] NPC mentors: high relationship with specific NPC gives passive XP boost to related job category
- [ ] NPC quests tied to job progression (deliver X items as delivery driver, cook Y meals as chef)

#### Job ↔ Pet Interwiring
- [ ] Pet companions boost specific job types (dog boosts outdoor jobs, cat boosts creative jobs, bird boosts music jobs)
- [ ] Pet mood affected by job (pet gets lonely if you work long shifts)
- [ ] Working pets: certain pets can "help" on jobs (guard dog for security, horse for ranch work)

#### Job ↔ Buffs/Cooking Interwiring
- [ ] Food buffs enhance minigame performance (coffee = faster timing, energy drink = longer speed runs, meal = better memory)
- [ ] Cooking quality affects buff strength (better cooked food = stronger job buffs)
- [ ] Job-specific buff recommendations (chef gets cooking buff, athlete gets protein buff)
- [ ] Buff expiry timed to shift cooldowns (buff lasts exactly one work shift)

#### Job ↔ Achievements/Quests Interwiring
- [ ] Job milestone achievements (work 100 shifts, reach level 10 in a job, try 5 different job categories)
- [ ] Daily quests tied to current job (work 3 shifts, earn X from job, get perfect minigame score)
- [ ] Career achievement chains (entry → service → chef → sous chef → restaurateur path)
- [ ] "Renaissance" achievement for reaching level 5 in 5 different categories

#### Job ↔ Living World Interwiring
- [ ] Market demand vector influences job pay (high demand = bonus pay for related jobs)
- [ ] Location danger vector affects outdoor job risk (high danger = chance of injury on shift)
- [ ] NPC mood affects job availability (grumpy NPC won't offer quests or job referrals)
- [ ] World events create temporary job surges (festival needs caterers, disaster needs medics)

### Planned — Other Feature Expansions

#### NPC System Depth
- [ ] NPC schedules (time/location availability — mystic only at midnight, merchant only during market hours)
- [ ] NPC relationship levels (affinity 0-100, unlock dialogue tiers, better trades, exclusive quests)
- [ ] NPC gift system (give items to NPCs to increase relationship)
- [ ] NPC mood affects interaction quality (happy NPC gives better trades, angry NPC refuses)
- [ ] NPC rivalry system (befriending one NPC may lower another's opinion)

#### Dynamic Economy
- [ ] Store prices fluctuate based on living world market demand vector
- [ ] Time-of-day pricing (lunch rush increases food prices, late night increases drink prices)
- [ ] Weather affects product availability (storm blocks shipping = shortage = price spike)
- [ ] Player-driven market (selling lots of X item depresses its sell price)

#### Location System Depth
- [ ] Location-specific random events (danger-scaled loot, encounters, discoveries)
- [ ] Player homes in locations (buy property in different areas with location-specific bonuses)
- [ ] Location-based activities unlock (beach = surfing, mountains = skiing, ruins = archaeology)
- [ ] Location danger affects activity risk/reward (higher danger = rarer finds but injury chance)

#### Crafting System Expansion
- [ ] Crafting with buffs (temporary weapon sharpening, armor coating, tool calibration)
- [ ] Location-specific crafting recipes (beach glass art, mountain forge, forest woodworking)
- [ ] Rare ingredient drops from exploration (used in high-tier crafting recipes)
- [ ] Crafted items can be sold to NPCs for reputation + coins

#### Seasonal/Event System
- [ ] Seasonal events (holiday-themed content, seasonal weather patterns)
- [ ] Limited-time jobs (harvest festival workers, holiday gift wrapper, summer lifeguard)
- [ ] Seasonal store items (pumpkin spice latte in autumn, hot cocoa in winter)
- [ ] Annual competitions (fishing tournament, cooking contest, minigame olympics)

#### Social System Expansion
- [ ] Gang/faction wars (competing factions, weekly events, territory control)
- [ ] Group activities (co-op fishing, team heists, group exploration)
- [ ] Player-run businesses (open your own shop, hire other players, set prices)
- [ ] Marriage bonuses (spouse shares housing bonus, combined income for power couples)

#### Buff System Depth
- [ ] Buff stacking rules (limit concurrent buffs, buff interactions/conflicts)
- [ ] Negative buffs from poor self-care (no sleep = exhaustion debuff, no shower = social penalty)
- [ ] Environmental buffs (well-decorated home = creativity buff, garden = relaxation buff)
- [ ] Buff tooltips showing exact stat modifications and timers

#### Store Expansion
- [ ] More store categories and items (infinite expansion via catalog system)
- [ ] Sub-subcategories for items (food → prepared → meals → breakfast)
- [ ] Player marketplace (list items for sale to other players)
- [ ] Auction house (rare items bid on by players)
- [ ] Subscription model (monthly delivery of consumables at a discount)

#### Minigame System Expansion
- [ ] Difficulty scaling based on job level (higher level = harder minigames = better pay)
- [ ] Perfect-run bonuses (complete minigame with no mistakes for bonus coins + XP)
- [ ] Minigame leaderboards (fastest times, highest scores per minigame type)
- [ ] Daily minigame challenge (one special minigame per day with unique rewards)
- [ ] Minigame tutorial mode (practice without pay before trying for real)
- [ ] Multiplayer minigames (compete against other players in real-time)

#### Quality of Life
- [ ] /profile redesign with job history, career path, and stats breakdown
- [ ] Job recommendation system (suggests jobs based on current stats and level)
- [ ] Career path visualization (shows progression from current job to top-tier jobs)
- [ ] Notification system (alerts when cooldowns expire, when deals refresh, when events start)
- [ ] Tutorial/onboarding flow for new players
