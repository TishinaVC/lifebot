# Lifebot Roadmap: Jobs & Minigames Overhaul

## Overview
- 200 jobs across 8 categories (25 each)
- 2 job slots per player
- Every job has a unique themed minigame
- Anti-automation: randomized content, shuffled buttons, time pressure
- Pay based on performance (0.0–1.0 multiplier)
- Deep features: streaks, events, boss shifts, co-op, reputation, grades

---

## Phase 1: DB Schema (DONE ✅)
- [x] `player_jobs` table (user_id, slot 1|2, job_id, job_level, job_xp)
- [x] `database/jobs.py` CRUD: get/set/quit/update_xp/count/reset
- [x] Migration: existing `job` column → slot 1
- [x] `reset_user` cleanup
- [x] `database/__init__.py` export

## Phase 2: Minigame Engine — 30 Mechanic Types

### Button-Based (14 types)
1. **sequence** — Click steps in correct order (shuffled button positions)
2. **match_pairs** — Match related items from a grid (symptom→treatment, tool→task)
3. **quick_pick** — Multiple choice, 4 shuffled answers
4. **stroop** — Pick the COLOR of the text, not the word itself
5. **memory** — Memorize a sequence shown briefly, then reproduce it
6. **timing** — Click a button at the exact right moment (random delay)
7. **sort** — Arrange jumbled items into correct order via buttons
8. **spot_error** — Find the deliberate mistake in displayed content
9. **pattern** — What comes next in the sequence? Pick from 4 options
10. **precision** — Stop a counter at a target number (random target)
11. **combo_lock** — Deduce the right combination from hints
12. **budget** — Distribute limited points across options to hit a target
13. **speed_run** — Complete N mini-tasks as fast as possible
14. **assembly** — Build from parts in the right order (multi-step)

### Modal / Text Input (6 types)
15. **typing_race** — Type a job-specific phrase fast (randomized phrases)
16. **math** — Solve job-specific math (calculate bills, measure materials, doses)
17. **word_scramble** — Unscramble job-specific terms
18. **fill_blank** — Complete a job-specific procedure sentence
19. **estimate** — Estimate a quantity (close enough = good score)
20. **transcribe** — Copy a string exactly, character-for-character

### Multi-Message / Multi-Stage (6 types)
21. **multi_stage** — Chain 3 different tasks across multiple messages
22. **diagnosis** — Narrow down from symptoms through multiple questions
23. **negotiation** — Back-and-forth dialogue with choices to reach a deal
24. **triage** — Prioritize multiple patients/orders by urgency
25. **inspection** — Multi-step quality inspection with pass/fail per step
26. **shift_sim** — Simulate a full work shift with random events and decisions

### Select Dropdown (4 types)
27. **categorize** — Assign items to correct categories via dropdowns
28. **recipe_build** — Select correct ingredients from dropdowns to build a recipe
29. **route_plan** — Select stops in order from a dropdown
30. **schedule** — Build a correct schedule from dropdown options

---

## Phase 3: Job-Specific Themed Content (200 jobs)

Each job gets:
- A `minigame_type` (one of the 30 mechanics above)
- A `content_pool` — arrays of themed questions, sequences, items, scenarios
- 3 rounds per shift, drawn randomly from the pool
- Difficulty scales with job_level (more steps, tighter timers, harder questions)

### Content Examples (by job):

**Chef (sequence):**
- Round content: cooking steps for random dishes (shuffled each play)
- "Cook spaghetti bolognese: [Boil water] [Cook pasta] [Brown meat] [Add sauce] [Plate]"

**Programmer (spot_error):**
- Round content: code snippets with injected bugs
- "```py\ndef add(a, b):\n    return a - b  # BUG: should be +\n```"
- Buttons: [Line 1] [Line 2] [Line 3] [No bug]

**Doctor (triage):**
- Round content: patients with symptoms, prioritize by severity
- "🤕 Patient A: mild headache | 🤮 Patient B: severe bleeding | 😷 Patient C: cough"
- Buttons: [A first] [B first] [C first] [All equal]

**Pilot (sequence + multi_stage):**
- Round 1: Pre-flight checks in order
- Round 2: Respond to weather change
- Round 3: Landing sequence

**Beggar (quick_pick):**
- Round content: pick the best begging spot
- "Where should you beg? [Outside mall] [Empty alley] [Busy subway] [Rich neighborhood]"

**CEO (budget):**
- Round content: allocate $10M across departments
- "Distribute budget: R&D? Marketing? Operations? Bonuses?"
- Buttons with +/- to hit a target allocation

### Content Generation Approach:
- `config/minigame_content.py` — dict keyed by job_id
- Each entry: `{"type": "sequence", "rounds": 3, "content": [...arrays...]}`
- Content arrays have 10-20 variants per round → randomized each play
- Some jobs share a mechanic but have completely different content

---

## Phase 4: Cog Refactor — 2-Slot System

### Commands:
- `/jobs [category]` — Browse jobs (already done, update for 2-slot info)
- `/job view` — Show both job slots with level/XP/progress
- `/job set <category> <job> [slot:1|2]` — Set a job into a slot
- `/job quit <slot:1|2>` — Quit a specific job slot
- `/work [slot:1|2]` — Work a specific job, launches that job's minigame
  - If no slot specified, prompts to pick which job to work

### Work Flow:
1. Player runs `/work 1` or `/work 2`
2. Validate: has job in slot, off cooldown, health/hunger/thirst OK
3. Launch 3-round minigame specific to that job
4. Each round: show themed embed + interactive buttons/modal
5. Score each round 0.0–1.0
6. Average score = performance multiplier
7. Pay = base_pay × job_level_mult × performance × bonuses
8. Apply stat costs, XP, job XP, cooldown
9. Show results embed with grade (S/A/B/C/D/F)

### Cooldowns:
- Per-slot: `work_1` and `work_2` cooldowns
- Each job has its own cooldown from config

---

## Phase 5: Deep Features

### 5a. Streak Combos
- Consecutive correct rounds multiply pay
- 3/3 correct = 1.5× bonus
- Track best streaks per job on profile

### 5b. Random Shift Events
- 15% chance per shift for a random event:
  - "Customer complains!" — extra quick_pick round
  - "Tool breaks!" — performance penalty unless you pass a quick fix
  - "Surprise inspection!" — bonus pay if you score above 0.8
  - "Coworker calls in sick!" — do extra work for bonus XP
  - "Big tip!" — flat bonus coins

### 5c. Boss Shifts
- Weekly high-pay shifts with 5-round minigames
- Harder content, tighter timers
- 3× pay multiplier
- Limited to once per week per job
- Unique achievement for completing

### 5d. Co-op Jobs
- Certain jobs allow `/work @partner`
- Both players do synchronized minigames
- Combined performance = pay split
- Requires both players to have same job

### 5e. Job Reputation
- Hidden reputation per job_id
- Higher rep = easier minigames (more time, fewer rounds)
- Earned by: high performance, streaks, showing up consistently
- Lost by: failing shifts, quitting mid-shift

### 5f. Quality Grade System
- S (100%): 2× pay + bonus items
- A (85%+): 1.5× pay
- B (70%+): 1.2× pay
- C (50%+): 1.0× pay (base)
- D (30%+): 0.5× pay
- F (<30%): 0.1× pay + stat penalty
- Grade shown on profile, tracked per job

### 5g. Progressive Difficulty
- Job level 1-5: 2 rounds, 30s timer, 4 buttons
- Job level 6-15: 3 rounds, 20s timer, 5 buttons
- Job level 16-30: 3 rounds, 15s timer, 6 buttons + harder content
- Job level 31+: 4 rounds, 12s timer, hard content + random events

### 5h. Visual Theming
- Embed colors match job category
- Emoji art per job (food emojis for chefs, tools for mechanics, etc.)
- Code blocks for programmer/hacker jobs
- Tables for business/finance jobs
- ASCII art for creative jobs

---

## Phase 6: Integration & Polish
- [x] Update `/help` text for new job commands
- [x] Update `/balance` to show both job slots
- [x] Update `/profile` to show job grades and streaks
- [ ] Update achievements for new job system
- [ ] Update quest tracking for work across both slots
- [ ] Syntax check all files
- [ ] Test bot startup
- [ ] Test minigame flow end-to-end

---

## Phase 7: RPG Stats System

### 7a. Core Stats (8 stats, 1-100 scale)
1. **Strength (STR)** 💪 — Physical power. Heavy labor, construction, trades.
2. **Intelligence (INT)** 🧠 — Mental capacity. Tech, medical, science, business.
3. **Dexterity (DEX)** 🫰 — Hand-eye coordination. Creative, service, precision jobs.
4. **Perception (PER)** 👁️ — Awareness, observation. Medical diagnosis, driving, security.
5. **Endurance (END)** 🏃 — Stamina, physical resilience. Long shifts, physical jobs.
6. **Charisma (CHA)** 🗣️ — Social skills. Service, business, negotiation, sales.
7. **Luck (LCK)** 🍀 — Random events, rare finds, gambling, tips.
8. **Focus (FOC)** 🎯 — Concentration, minigame performance, accuracy.

### 7b. Stat Growth
- **Base stats:** All start at 10
- **Training:** `/train <stat>` — costs coins + energy, +1-3 stat points, cooldown 1hr
  - Cost scales with current stat level: `cost = 100 * (stat_level / 10)`
  - Energy cost: 20-40 per session
- **Schooling:** `/school <type>` — bigger investment, unlocks qualifications
  - Costs 1000-50000 coins, takes multiple sessions (cooldown 6hr)
  - Grants qualifications (degrees, licenses, certifications)
  - Also grants stat points: +5-10 per course completion
- **Job practice:** Working a job passively increases relevant stats
  - +1 stat point per 10 shifts in a job (tracked per job)
  - Stat raised depends on job's primary stat
- **Activities:** Fishing raises PER, Mining raises STR, Exploring raises END, etc.

### 7c. Qualifications System
- `player_qualifications` table (user_id, qualification_id, earned_at)
- Qualifications are prerequisites for higher-tier jobs
- Earned through schooling (pay coins + time)
- Types:
  - **Licenses:** Driver's License, Commercial License, Pilot License, Medical License
  - **Degrees:** Business Degree, Medical Degree, CS Degree, Engineering Degree, Art Degree
  - **Certifications:** Food Safety Cert, Welding Cert, HVAC Cert, Pharmacy Cert, Security Cert
  - **Training:** Military Training, Police Academy, Fire Academy, Apprenticeship
- Each qualification has: cost, prerequisite stats, prerequisite qualifications, school time

### 7d. Job Requirements
Each job in config gets:
- `stat_reqs`: dict of stat → minimum value (e.g. `{"INT": 40, "PER": 35}`)
- `qual_reqs`: list of qualification IDs needed (e.g. `["medical_degree"]`)
- Some jobs need only stats, some need only quals, some need both
- Entry-level jobs: no requirements (just level)
- Mid-tier jobs: 1-2 stat requirements (20-40 range)
- High-tier jobs: 2-3 stat requirements (40-60) + 1 qualification
- Top-tier jobs: 3+ stat requirements (60-80) + 2+ qualifications

### 7e. Stat Booster Items (temporary)
- New store items that temporarily boost a stat via the buff system
- Duration: 15min – 2hr
- Examples:
  - `protein_shake` → +10 STR for 30min, $150
  - `nootropic` → +15 INT for 1hr, $300
  - `caffeine_pill` → +10 FOC for 45min, $120
  - `energy_drink` → +10 END for 30min, $100 (already exists, add stat buff)
  - `lucky_rabbit_foot` → +15 LCK for 1hr, $500
  - `confidence_potion` → +12 CHA for 30min, $250
  - `eye_drops` → +10 PER for 30min, $80
  - `hand_warmup` → +10 DEX for 20min, $60
- Stack with equipment bonuses for minigame performance

### 7f. Stats in Minigames
- Stat bonuses affect minigame performance:
  - STR: More time on physical minigames
  - INT: Hints shown on puzzle minigames
  - DEX: Slower timer decay on precision minigames
  - PER: Extra info shown on diagnosis/inspection minigames
  - END: Stat drain reduction per shift
  - CHA: Better tips (bonus pay) on service minigames
  - LCK: Chance for random bonus events
  - FOC: Score rounding bonus (0.7 rounds to 0.75)
- Stats checked at job entry AND applied during minigames

### 7g. Commands
- `/stats` — View all 8 stats + qualifications + stat history
- `/train <stat>` — Train a specific stat (costs coins + energy, cooldown)
- `/school` — Browse available schooling/qualifications
- `/school enroll <qualification>` — Start earning a qualification
- `/qualifications` — View earned qualifications
- Booster items used via existing `/use` command (applies buff)

### 7h. DB Schema
- `player_stats` table: user_id, str, int, dex, per, end, cha, lck, foc (all DEFAULT 10)
- `player_qualifications` table: user_id, qualification_id, earned_at
- `player_training` table: user_id, stat_trained, sessions_count (for passive growth tracking)
- Migration: add to init_db, add reset_user cleanup

---

## Implementation Order

1. **Phase 1** — DB: Jobs (DONE ✅)
2. **Phase 7** — DB: Stats + qualifications schema → config/stats.py → database/stats.py (DONE ✅)
3. **Phase 3** — Config: minigame content for all 200 jobs (DONE ✅ — 600 entries across 2 files)
4. **Phase 2** — Minigame engine: 24 mechanic views (DONE ✅)
5. **Phase 4** — Cog refactor: 2-slot system + work flow + stat checks (DONE ✅)
6. **Phase 7c** — Cog: training/schooling/stats commands (DONE ✅)
7. **Phase 5** — Deep features (streaks, events, grades, difficulty) — PENDING
8. **Phase 6** — Integration & polish — PARTIALLY DONE

### File Structure:
- `config/stats.py` — Stat definitions, training costs, qualification definitions
- `config/minigame_content.py` — All 200 jobs' minigame content + stat/qual requirements
- `cogs/minigames.py` — All 30 minigame mechanic views
- `cogs/jobs.py` — Refactored job management + work flow
- `cogs/stats.py` — Training, schooling, stats viewing
- `database/jobs.py` — Player jobs CRUD (DONE)
- `database/stats.py` — Player stats + qualifications CRUD
- `database/connection.py` — Schema (jobs DONE, stats pending)

---

## Progress Tracking
- [x] Phase 1: DB Schema (Jobs)
- [x] Phase 2: Minigame Engine (24 types implemented)
- [x] Phase 3: Job-Specific Themed Content (200 jobs × 3 minigames = 600 content entries)
- [x] Phase 4: Cog Refactor (2-slot system, interactive nav, /work with slots)
- [x] Phase 7: RPG Stats System (8 stats, training, schooling, qualifications, boosters)
- [ ] Phase 5: Deep Features (streaks, events, boss shifts, co-op, reputation, grades, difficulty)
- [ ] Phase 6: Integration & Polish (help/balance/profile updates, achievements, quests, testing)

### Additional Completed Work (Beyond Original Phases):
- [x] Nested Job Categories — 8 categories × 38 subcategories, interactive select-menu navigation
- [x] 3-Minigame Per Job System — Each job gets 3 potential minigames, randomly selected per shift
- [x] Content-Driven Assignment — Minigame types assigned based on available content (no gaps)
- [x] Action Templates — All cogs use get_action_text() for dynamic narrative text
- [x] Living World System — Persistent real-time world simulation (vectors, NPCs, locations, market, weather)
- [x] Economy Cog Refactor — BaseCog inheritance pattern
- [x] All 7 Immersion Systems — Buffs, reputation, NPC interactions, game time, weather, world, narrative
- [x] Procedural Minigame Content Generator — Pure-Python generator (utils/proc_gen.py) with 38 subcategory-specific flavor pools (config/job_flavor.py), all 24 minigame types, infinite variety, zero external dependencies
- [x] Phase 5: Deep Features — Quality grades (S/A/B/C/D/F), streak combos (up to 2x pay), random shift events (8 types), boss shifts (rare 3x pay), progressive difficulty (scales with job level), profile updates
- [x] Phase 5: Visual Theming — Category-themed embed colors, grade-colored result embeds
- [x] Phase 5: Job Reputation — Per-job-category standing system (6 tiers: Novice→Legend), pay/XP/fatigue benefits, /jobrep command, profile & balance integration
- [x] Phase 5: Co-op Jobs — Multiplayer shift system (/coop start/join), team bonuses (up to +40%), co-op events, all-good/fail modifiers, achievement & quest tracking
- [x] Nested Item Categories — STORE_CATALOG with 10 categories × subcategories, interactive button navigation (CategoryView → SubcategoryView → ItemListView → ItemDetailView)
- [x] Phase 6: Integration & Polish — Updated /help, /balance, /profile with all new systems; 9 new achievements (S-grade, streaks, boss wins, co-op, reputation); co-op quest tracking; end-to-end import verification

### Still Pending:
- (None — all systems complete)
