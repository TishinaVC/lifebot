"""
Job requirements and minigame assignments for all 200 jobs.
Maps job_id → {minigame_type, stat_reqs, qual_reqs}

Minigame types (30): sequence, match_pairs, quick_pick, stroop, memory, timing,
sort, spot_error, pattern, precision, combo_lock, budget, speed_run, assembly,
typing_race, math, word_scramble, fill_blank, estimate, transcribe,
multi_stage, diagnosis, negotiation, triage, inspection, shift_sim,
categorize, recipe_build, route_plan, schedule
"""
from config.jobs import JOBS

JOB_REQUIREMENTS = {
    # ═══════════════ Entry Level (25) ═══════════════
    "beggar":          {"minigame": "quick_pick",  "stat_reqs": {},                          "qual_reqs": []},
    "busker":          {"minigame": "timing",      "stat_reqs": {},                          "qual_reqs": []},
    "leafleter":       {"minigame": "sort",        "stat_reqs": {},                          "qual_reqs": []},
    "window_washer":   {"minigame": "speed_run",   "stat_reqs": {},                          "qual_reqs": []},
    "dog_walker":      {"minigame": "sequence",    "stat_reqs": {},                          "qual_reqs": []},
    "recycler":        {"minigame": "sort",        "stat_reqs": {},                          "qual_reqs": []},
    "shoe_shiner":     {"minigame": "sequence",    "stat_reqs": {},                          "qual_reqs": []},
    "newspaper":       {"minigame": "route_plan",  "stat_reqs": {},                          "qual_reqs": []},
    "car_wash":        {"minigame": "sequence",    "stat_reqs": {},                          "qual_reqs": []},
    "trolley":         {"minigame": "sort",        "stat_reqs": {},                          "qual_reqs": []},
    "plant_waterer":   {"minigame": "quick_pick",  "stat_reqs": {},                          "qual_reqs": []},
    "litter_picker":   {"minigame": "sort",        "stat_reqs": {},                          "qual_reqs": []},
    "sign_holder":     {"minigame": "timing",      "stat_reqs": {},                          "qual_reqs": []},
    "survey_taker":    {"minigame": "quick_pick",  "stat_reqs": {},                          "qual_reqs": []},
    "moving_helper":   {"minigame": "sequence",    "stat_reqs": {"strength": 12},            "qual_reqs": []},
    "ticket_tearer":   {"minigame": "quick_pick",  "stat_reqs": {},                          "qual_reqs": []},
    "ice_cream":       {"minigame": "quick_pick",  "stat_reqs": {},                          "qual_reqs": []},
    "balloon_seller":  {"minigame": "memory",      "stat_reqs": {},                          "qual_reqs": []},
    "parking_attend":  {"minigame": "quick_pick",  "stat_reqs": {"perception": 12},          "qual_reqs": []},
    "garden_helper":   {"minigame": "sort",        "stat_reqs": {},                          "qual_reqs": []},
    "shelf_stocker":   {"minigame": "sort",        "stat_reqs": {},                          "qual_reqs": []},
    "janitor":         {"minigame": "sequence",    "stat_reqs": {},                          "qual_reqs": []},
    "laundry":         {"minigame": "sort",        "stat_reqs": {},                          "qual_reqs": []},
    "food_sample":     {"minigame": "quick_pick",  "stat_reqs": {"charisma": 12},            "qual_reqs": []},
    "cart_pusher":     {"minigame": "speed_run",   "stat_reqs": {"endurance": 12},           "qual_reqs": []},

    # ═══════════════ Food & Service (25) ═══════════════
    "barista":         {"minigame": "recipe_build",  "stat_reqs": {"dexterity": 15},                "qual_reqs": []},
    "chef":            {"minigame": "sequence",      "stat_reqs": {"dexterity": 20, "focus": 15},   "qual_reqs": ["food_safety_cert"]},
    "waiter":          {"minigame": "memory",        "stat_reqs": {"charisma": 15, "dexterity": 12},"qual_reqs": []},
    "bartender":       {"minigame": "recipe_build",  "stat_reqs": {"dexterity": 18, "charisma": 15},"qual_reqs": ["food_safety_cert"]},
    "fast_food":       {"minigame": "speed_run",     "stat_reqs": {"dexterity": 12},                "qual_reqs": []},
    "sushi_chef":      {"minigame": "sequence",      "stat_reqs": {"dexterity": 30, "focus": 25},   "qual_reqs": ["food_safety_cert"]},
    "pastry_chef":     {"minigame": "sequence",      "stat_reqs": {"dexterity": 25, "focus": 20},   "qual_reqs": ["food_safety_cert"]},
    "sommelier":       {"minigame": "match_pairs",   "stat_reqs": {"perception": 25, "charisma": 20},"qual_reqs": ["food_safety_cert"]},
    "food_truck":      {"minigame": "quick_pick",    "stat_reqs": {"dexterity": 20, "charisma": 15},"qual_reqs": ["food_safety_cert"]},
    "caterer":         {"minigame": "sort",          "stat_reqs": {"dexterity": 18, "endurance": 15},"qual_reqs": ["food_safety_cert"]},
    "butcher":         {"minigame": "sequence",      "stat_reqs": {"strength": 20, "dexterity": 18},"qual_reqs": ["food_safety_cert"]},
    "baker":           {"minigame": "sequence",      "stat_reqs": {"dexterity": 18, "focus": 15},   "qual_reqs": ["food_safety_cert"]},
    "host":            {"minigame": "memory",        "stat_reqs": {"charisma": 18, "perception": 12},"qual_reqs": []},
    "barista_master":  {"minigame": "recipe_build",  "stat_reqs": {"dexterity": 30, "focus": 25},   "qual_reqs": ["food_safety_cert"]},
    "sous_chef":       {"minigame": "multi_stage",   "stat_reqs": {"dexterity": 35, "focus": 30, "charisma": 20}, "qual_reqs": ["food_safety_cert"]},
    "nutritionist":    {"minigame": "quick_pick",    "stat_reqs": {"intelligence": 25, "perception": 20}, "qual_reqs": ["food_safety_cert"]},
    "food_critic":     {"minigame": "spot_error",    "stat_reqs": {"perception": 30, "intelligence": 25, "charisma": 20}, "qual_reqs": ["food_safety_cert"]},
    "hotel_manager":   {"minigame": "shift_sim",     "stat_reqs": {"charisma": 30, "intelligence": 25, "focus": 20}, "qual_reqs": ["food_safety_cert"]},
    "event_planner":   {"minigame": "sort",          "stat_reqs": {"charisma": 25, "intelligence": 20, "dexterity": 18}, "qual_reqs": ["food_safety_cert"]},
    "sommelier_master":{"minigame": "match_pairs",   "stat_reqs": {"perception": 35, "charisma": 30, "focus": 25}, "qual_reqs": ["food_safety_cert"]},
    "mixologist":      {"minigame": "recipe_build",  "stat_reqs": {"dexterity": 30, "charisma": 25, "focus": 20}, "qual_reqs": ["food_safety_cert"]},
    "chocolatier":     {"minigame": "sequence",      "stat_reqs": {"dexterity": 28, "focus": 25, "perception": 20}, "qual_reqs": ["food_safety_cert"]},
    "teasomm":         {"minigame": "match_pairs",   "stat_reqs": {"perception": 25, "charisma": 22, "focus": 18}, "qual_reqs": ["food_safety_cert"]},
    "private_chef":    {"minigame": "multi_stage",   "stat_reqs": {"dexterity": 35, "charisma": 30, "focus": 28}, "qual_reqs": ["food_safety_cert"]},
    "restaurateur":    {"minigame": "shift_sim",     "stat_reqs": {"charisma": 35, "intelligence": 30, "dexterity": 25, "focus": 25}, "qual_reqs": ["food_safety_cert", "business_degree"]},

    # ═══════════════ Trades & Labor (25) ═══════════════
    "mechanic":        {"minigame": "sequence",      "stat_reqs": {"strength": 25, "dexterity": 22, "focus": 18}, "qual_reqs": ["apprenticeship"]},
    "electrician":     {"minigame": "sequence",      "stat_reqs": {"intelligence": 25, "dexterity": 22, "focus": 20}, "qual_reqs": ["electrical_cert"]},
    "plumber":         {"minigame": "sequence",      "stat_reqs": {"strength": 22, "dexterity": 20, "focus": 15}, "qual_reqs": ["apprenticeship"]},
    "carpenter":       {"minigame": "assembly",      "stat_reqs": {"strength": 22, "dexterity": 22, "focus": 18}, "qual_reqs": ["apprenticeship"]},
    "welder":          {"minigame": "sequence",      "stat_reqs": {"strength": 25, "dexterity": 22, "focus": 20}, "qual_reqs": ["welding_cert"]},
    "construction":    {"minigame": "assembly",      "stat_reqs": {"strength": 20, "endurance": 18}, "qual_reqs": []},
    "roofer":          {"minigame": "sequence",      "stat_reqs": {"strength": 20, "endurance": 20, "dexterity": 15}, "qual_reqs": []},
    "painter":         {"minigame": "sort",          "stat_reqs": {"dexterity": 18, "perception": 15}, "qual_reqs": []},
    "mason":           {"minigame": "sequence",      "stat_reqs": {"strength": 22, "dexterity": 18, "focus": 15}, "qual_reqs": ["apprenticeship"]},
    "tiler":           {"minigame": "pattern",       "stat_reqs": {"dexterity": 20, "perception": 18, "focus": 15}, "qual_reqs": []},
    "insulator":       {"minigame": "sequence",      "stat_reqs": {"strength": 18, "endurance": 18}, "qual_reqs": []},
    "glazier":         {"minigame": "precision",     "stat_reqs": {"dexterity": 22, "perception": 20, "focus": 18}, "qual_reqs": ["apprenticeship"]},
    "hvac":            {"minigame": "sequence",      "stat_reqs": {"strength": 20, "intelligence": 22, "dexterity": 18}, "qual_reqs": ["hvac_cert"]},
    "landscaper":      {"minigame": "sort",          "stat_reqs": {"strength": 18, "perception": 15, "endurance": 18}, "qual_reqs": []},
    "foreman":         {"minigame": "shift_sim",     "stat_reqs": {"strength": 25, "intelligence": 25, "charisma": 25, "focus": 20}, "qual_reqs": ["apprenticeship"]},
    "surveyor":        {"minigame": "precision",     "stat_reqs": {"intelligence": 25, "perception": 25, "focus": 22}, "qual_reqs": ["apprenticeship"]},
    "demolition":      {"minigame": "sequence",      "stat_reqs": {"strength": 25, "endurance": 22, "focus": 18}, "qual_reqs": []},
    "scaffolder":      {"minigame": "assembly",      "stat_reqs": {"strength": 22, "dexterity": 20, "endurance": 20}, "qual_reqs": []},
    "floor_layer":     {"minigame": "sequence",      "stat_reqs": {"strength": 20, "dexterity": 20, "focus": 15}, "qual_reqs": []},
    "locksmith":       {"minigame": "combo_lock",    "stat_reqs": {"dexterity": 25, "perception": 22, "focus": 20}, "qual_reqs": ["apprenticeship"]},
    "heavy_equipment": {"minigame": "precision",     "stat_reqs": {"strength": 25, "perception": 22, "focus": 20}, "qual_reqs": ["commercial_license"]},
    "steelworker":     {"minigame": "assembly",      "stat_reqs": {"strength": 28, "dexterity": 22, "endurance": 25, "focus": 20}, "qual_reqs": ["apprenticeship"]},
    "elevator_fix":    {"minigame": "sequence",      "stat_reqs": {"intelligence": 25, "dexterity": 25, "focus": 22}, "qual_reqs": ["electrical_cert"]},
    "solar_installer": {"minigame": "sequence",      "stat_reqs": {"strength": 22, "dexterity": 20, "intelligence": 18}, "qual_reqs": ["electrical_cert"]},
    "contractor":      {"minigame": "shift_sim",     "stat_reqs": {"strength": 30, "intelligence": 30, "charisma": 28, "focus": 25}, "qual_reqs": ["apprenticeship", "business_degree"]},

    # ═══════════════ Medical & Science (25) ═══════════════
    "doctor":          {"minigame": "diagnosis",     "stat_reqs": {"intelligence": 40, "perception": 35, "focus": 30}, "qual_reqs": ["medical_degree"]},
    "nurse":           {"minigame": "triage",        "stat_reqs": {"intelligence": 30, "perception": 25, "endurance": 25}, "qual_reqs": ["nursing_degree"]},
    "paramedic":       {"minigame": "quick_pick",    "stat_reqs": {"intelligence": 28, "perception": 25, "endurance": 28}, "qual_reqs": ["nursing_degree"]},
    "pharmacist":      {"minigame": "match_pairs",   "stat_reqs": {"intelligence": 35, "focus": 30, "perception": 25}, "qual_reqs": ["pharmacy_cert"]},
    "dentist":         {"minigame": "spot_error",    "stat_reqs": {"intelligence": 35, "dexterity": 30, "perception": 28, "focus": 25}, "qual_reqs": ["medical_degree"]},
    "surgeon":         {"minigame": "sequence",      "stat_reqs": {"intelligence": 45, "dexterity": 40, "perception": 35, "focus": 35}, "qual_reqs": ["medical_degree"]},
    "vet":             {"minigame": "diagnosis",     "stat_reqs": {"intelligence": 30, "perception": 28, "dexterity": 22}, "qual_reqs": ["nursing_degree"]},
    "therapist":       {"minigame": "quick_pick",    "stat_reqs": {"intelligence": 30, "charisma": 30, "perception": 25}, "qual_reqs": ["nursing_degree"]},
    "radiologist":     {"minigame": "spot_error",    "stat_reqs": {"intelligence": 35, "perception": 35, "focus": 30}, "qual_reqs": ["medical_degree"]},
    "lab_tech":        {"minigame": "sequence",      "stat_reqs": {"intelligence": 25, "perception": 20, "focus": 22}, "qual_reqs": []},
    "research_sci":    {"minigame": "multi_stage",   "stat_reqs": {"intelligence": 40, "perception": 30, "focus": 35}, "qual_reqs": ["medical_degree"]},
    "biologist":       {"minigame": "categorize",    "stat_reqs": {"intelligence": 35, "perception": 30, "focus": 28}, "qual_reqs": ["medical_degree"]},
    "chemist":         {"minigame": "sequence",      "stat_reqs": {"intelligence": 35, "focus": 30, "dexterity": 25}, "qual_reqs": ["pharmacy_cert"]},
    "physicist":       {"minigame": "math",          "stat_reqs": {"intelligence": 45, "focus": 40, "perception": 30}, "qual_reqs": ["medical_degree"]},
    "astronomer":      {"minigame": "pattern",       "stat_reqs": {"intelligence": 40, "perception": 35, "focus": 35}, "qual_reqs": ["medical_degree"]},
    "geneticist":      {"minigame": "match_pairs",   "stat_reqs": {"intelligence": 42, "perception": 35, "focus": 35}, "qual_reqs": ["medical_degree"]},
    "neurosurgeon":    {"minigame": "sequence",      "stat_reqs": {"intelligence": 50, "dexterity": 45, "perception": 40, "focus": 40}, "qual_reqs": ["medical_degree"]},
    "cardiologist":    {"minigame": "diagnosis",     "stat_reqs": {"intelligence": 45, "perception": 40, "focus": 35}, "qual_reqs": ["medical_degree"]},
    "pediatrician":    {"minigame": "diagnosis",     "stat_reqs": {"intelligence": 38, "perception": 32, "charisma": 30, "focus": 28}, "qual_reqs": ["medical_degree"]},
    "optometrist":     {"minigame": "quick_pick",    "stat_reqs": {"intelligence": 30, "perception": 30, "focus": 25}, "qual_reqs": ["nursing_degree"]},
    "physical_ther":   {"minigame": "sequence",      "stat_reqs": {"strength": 25, "dexterity": 25, "intelligence": 22, "endurance": 22}, "qual_reqs": ["nursing_degree"]},
    "med_researcher":  {"minigame": "multi_stage",   "stat_reqs": {"intelligence": 40, "perception": 32, "focus": 35}, "qual_reqs": ["medical_degree"]},
    "epidemiologist":  {"minigame": "pattern",       "stat_reqs": {"intelligence": 42, "perception": 35, "focus": 35}, "qual_reqs": ["medical_degree"]},
    "toxicologist":    {"minigame": "match_pairs",   "stat_reqs": {"intelligence": 38, "perception": 32, "focus": 32}, "qual_reqs": ["pharmacy_cert"]},
    "astronaut":       {"minigame": "multi_stage",   "stat_reqs": {"intelligence": 45, "perception": 40, "focus": 40, "endurance": 40, "strength": 35}, "qual_reqs": ["medical_degree", "pilot_license"]},

    # ═══════════════ Tech & IT (25) ═══════════════
    "programmer":      {"minigame": "spot_error",    "stat_reqs": {"intelligence": 40, "focus": 35, "dexterity": 20}, "qual_reqs": ["cs_degree"]},
    "it_support":      {"minigame": "quick_pick",    "stat_reqs": {"intelligence": 20, "focus": 15, "charisma": 15}, "qual_reqs": []},
    "web_dev":         {"minigame": "assembly",      "stat_reqs": {"intelligence": 30, "focus": 25, "dexterity": 20}, "qual_reqs": []},
    "data_analyst":    {"minigame": "pattern",       "stat_reqs": {"intelligence": 32, "focus": 28, "perception": 22}, "qual_reqs": []},
    "sysadmin":        {"minigame": "sequence",      "stat_reqs": {"intelligence": 28, "focus": 25, "perception": 20}, "qual_reqs": []},
    "ux_designer":     {"minigame": "sort",          "stat_reqs": {"intelligence": 25, "dexterity": 25, "perception": 22, "charisma": 18}, "qual_reqs": []},
    "game_dev":        {"minigame": "assembly",      "stat_reqs": {"intelligence": 35, "focus": 30, "dexterity": 25}, "qual_reqs": ["cs_degree"]},
    "data_scientist":  {"minigame": "math",          "stat_reqs": {"intelligence": 40, "focus": 35, "perception": 28}, "qual_reqs": ["cs_degree"]},
    "devops":          {"minigame": "sequence",      "stat_reqs": {"intelligence": 35, "focus": 32, "perception": 25}, "qual_reqs": ["cs_degree"]},
    "security_analyst":{"minigame": "spot_error",    "stat_reqs": {"intelligence": 35, "perception": 30, "focus": 30}, "qual_reqs": ["cs_degree"]},
    "mobile_dev":      {"minigame": "assembly",      "stat_reqs": {"intelligence": 32, "focus": 28, "dexterity": 25}, "qual_reqs": []},
    "ai_engineer":     {"minigame": "sequence",      "stat_reqs": {"intelligence": 45, "focus": 40, "perception": 30}, "qual_reqs": ["cs_degree"]},
    "cloud_arch":      {"minigame": "assembly",      "stat_reqs": {"intelligence": 40, "focus": 35, "perception": 28}, "qual_reqs": ["cs_degree"]},
    "blockchain_dev":  {"minigame": "sequence",      "stat_reqs": {"intelligence": 40, "focus": 35, "dexterity": 25}, "qual_reqs": ["cs_degree"]},
    "qa_tester":       {"minigame": "spot_error",    "stat_reqs": {"intelligence": 22, "perception": 22, "focus": 20}, "qual_reqs": []},
    "tech_writer":     {"minigame": "fill_blank",    "stat_reqs": {"intelligence": 25, "charisma": 20, "focus": 22}, "qual_reqs": []},
    "product_manager": {"minigame": "shift_sim",     "stat_reqs": {"intelligence": 35, "charisma": 30, "focus": 28}, "qual_reqs": ["cs_degree"]},
    "db_admin":        {"minigame": "sequence",      "stat_reqs": {"intelligence": 32, "focus": 30, "perception": 25}, "qual_reqs": []},
    "network_eng":     {"minigame": "assembly",      "stat_reqs": {"intelligence": 32, "focus": 28, "perception": 25}, "qual_reqs": []},
    "frontend_dev":    {"minigame": "assembly",      "stat_reqs": {"intelligence": 28, "dexterity": 25, "focus": 22, "perception": 20}, "qual_reqs": []},
    "backend_dev":     {"minigame": "assembly",      "stat_reqs": {"intelligence": 35, "focus": 30, "perception": 25}, "qual_reqs": ["cs_degree"]},
    "pentester":       {"minigame": "sequence",      "stat_reqs": {"intelligence": 40, "perception": 35, "focus": 32}, "qual_reqs": ["cs_degree"]},
    "ml_engineer":     {"minigame": "sequence",      "stat_reqs": {"intelligence": 45, "focus": 40, "perception": 30}, "qual_reqs": ["cs_degree"]},
    "cto":             {"minigame": "shift_sim",     "stat_reqs": {"intelligence": 50, "focus": 40, "charisma": 35, "perception": 30}, "qual_reqs": ["cs_degree", "business_degree"]},
    "hacker":          {"minigame": "combo_lock",    "stat_reqs": {"intelligence": 40, "perception": 35, "focus": 32, "dexterity": 25}, "qual_reqs": ["cs_degree"]},

    # ═══════════════ Business & Finance (25) ═══════════════
    "ceo":             {"minigame": "shift_sim",     "stat_reqs": {"intelligence": 50, "charisma": 50, "focus": 40}, "qual_reqs": ["mba"]},
    "bank_teller":     {"minigame": "quick_pick",    "stat_reqs": {"intelligence": 20, "charisma": 18, "focus": 18}, "qual_reqs": []},
    "accountant":      {"minigame": "math",          "stat_reqs": {"intelligence": 28, "focus": 25, "perception": 22}, "qual_reqs": []},
    "sales_rep":       {"minigame": "negotiation",   "stat_reqs": {"charisma": 25, "intelligence": 20, "perception": 18}, "qual_reqs": []},
    "real_estate":     {"minigame": "quick_pick",    "stat_reqs": {"charisma": 25, "intelligence": 22, "perception": 22}, "qual_reqs": []},
    "stockbroker":     {"minigame": "pattern",       "stat_reqs": {"intelligence": 35, "focus": 30, "perception": 28}, "qual_reqs": ["business_degree"]},
    "financial_adv":   {"minigame": "budget",        "stat_reqs": {"intelligence": 32, "charisma": 28, "focus": 28}, "qual_reqs": ["business_degree"]},
    "manager":         {"minigame": "shift_sim",     "stat_reqs": {"intelligence": 28, "charisma": 28, "focus": 22}, "qual_reqs": []},
    "hr_specialist":   {"minigame": "quick_pick",    "stat_reqs": {"charisma": 25, "intelligence": 22, "perception": 22}, "qual_reqs": []},
    "marketing":       {"minigame": "quick_pick",    "stat_reqs": {"charisma": 25, "intelligence": 22, "perception": 20}, "qual_reqs": []},
    "consultant":      {"minigame": "multi_stage",   "stat_reqs": {"intelligence": 35, "charisma": 30, "focus": 28}, "qual_reqs": ["business_degree"]},
    "auditor":         {"minigame": "spot_error",    "stat_reqs": {"intelligence": 32, "perception": 30, "focus": 28}, "qual_reqs": ["business_degree"]},
    "loan_officer":    {"minigame": "quick_pick",    "stat_reqs": {"intelligence": 25, "charisma": 22, "perception": 22}, "qual_reqs": []},
    "insurance":       {"minigame": "quick_pick",    "stat_reqs": {"charisma": 22, "intelligence": 20, "perception": 20}, "qual_reqs": []},
    "bookkeeper":      {"minigame": "math",          "stat_reqs": {"intelligence": 22, "focus": 22, "perception": 18}, "qual_reqs": []},
    "tax_prep":        {"minigame": "math",          "stat_reqs": {"intelligence": 25, "focus": 25, "perception": 22}, "qual_reqs": []},
    "investment_bank": {"minigame": "negotiation",   "stat_reqs": {"intelligence": 40, "charisma": 35, "focus": 32}, "qual_reqs": ["business_degree"]},
    "venture_cap":     {"minigame": "quick_pick",    "stat_reqs": {"intelligence": 40, "charisma": 35, "perception": 32, "focus": 30}, "qual_reqs": ["business_degree"]},
    "hedge_fund":      {"minigame": "pattern",       "stat_reqs": {"intelligence": 45, "focus": 40, "perception": 35}, "qual_reqs": ["business_degree"]},
    "entrepreneur":    {"minigame": "shift_sim",     "stat_reqs": {"intelligence": 35, "charisma": 32, "focus": 30, "perception": 25}, "qual_reqs": []},
    "cfo":             {"minigame": "budget",        "stat_reqs": {"intelligence": 45, "focus": 40, "charisma": 35}, "qual_reqs": ["mba"]},
    "coo":             {"minigame": "shift_sim",     "stat_reqs": {"intelligence": 42, "charisma": 38, "focus": 35, "endurance": 30}, "qual_reqs": ["business_degree"]},
    "trader":          {"minigame": "pattern",       "stat_reqs": {"intelligence": 35, "focus": 32, "perception": 28, "luck": 20}, "qual_reqs": ["business_degree"]},
    "negotiator":      {"minigame": "negotiation",   "stat_reqs": {"charisma": 35, "intelligence": 30, "perception": 28, "focus": 25}, "qual_reqs": ["business_degree"]},
    "magnate":         {"minigame": "shift_sim",     "stat_reqs": {"intelligence": 55, "charisma": 55, "focus": 45, "perception": 35}, "qual_reqs": ["mba"]},

    # ═══════════════ Creative & Arts (25) ═══════════════
    "artist":          {"minigame": "quick_pick",    "stat_reqs": {"dexterity": 18, "perception": 18}, "qual_reqs": []},
    "musician":        {"minigame": "sequence",      "stat_reqs": {"dexterity": 22, "perception": 20, "charisma": 15}, "qual_reqs": []},
    "writer":          {"minigame": "fill_blank",    "stat_reqs": {"intelligence": 20, "charisma": 18, "focus": 18}, "qual_reqs": []},
    "photographer":    {"minigame": "quick_pick",    "stat_reqs": {"perception": 22, "dexterity": 18, "focus": 18}, "qual_reqs": []},
    "graphic_design":  {"minigame": "sort",          "stat_reqs": {"dexterity": 25, "perception": 22, "intelligence": 18}, "qual_reqs": []},
    "actor":           {"minigame": "memory",        "stat_reqs": {"charisma": 25, "dexterity": 20, "perception": 20}, "qual_reqs": []},
    "filmmaker":       {"minigame": "sequence",      "stat_reqs": {"charisma": 28, "perception": 25, "intelligence": 22, "dexterity": 20}, "qual_reqs": ["art_degree"]},
    "animator":        {"minigame": "sequence",      "stat_reqs": {"dexterity": 28, "perception": 25, "focus": 22}, "qual_reqs": ["art_degree"]},
    "fashion_design":  {"minigame": "sort",          "stat_reqs": {"dexterity": 28, "perception": 25, "charisma": 22}, "qual_reqs": ["art_degree"]},
    "interior_design": {"minigame": "sort",          "stat_reqs": {"dexterity": 22, "perception": 25, "charisma": 20, "intelligence": 18}, "qual_reqs": []},
    "architect":       {"minigame": "assembly",      "stat_reqs": {"intelligence": 32, "dexterity": 28, "perception": 28, "focus": 25}, "qual_reqs": ["art_degree"]},
    "sculptor":        {"minigame": "sequence",      "stat_reqs": {"dexterity": 25, "strength": 20, "perception": 22}, "qual_reqs": []},
    "tattoo_artist":   {"minigame": "precision",     "stat_reqs": {"dexterity": 28, "perception": 22, "focus": 22}, "qual_reqs": ["art_degree"]},
    "makeup_artist":   {"minigame": "quick_pick",    "stat_reqs": {"dexterity": 22, "perception": 20, "charisma": 18}, "qual_reqs": []},
    "dancer":          {"minigame": "sequence",      "stat_reqs": {"dexterity": 22, "endurance": 22, "charisma": 18}, "qual_reqs": []},
    "comedian":        {"minigame": "quick_pick",    "stat_reqs": {"charisma": 25, "perception": 20, "focus": 18}, "qual_reqs": []},
    "dj":              {"minigame": "sequence",      "stat_reqs": {"dexterity": 25, "perception": 22, "charisma": 20}, "qual_reqs": []},
    "producer":        {"minigame": "assembly",      "stat_reqs": {"dexterity": 28, "perception": 25, "intelligence": 22, "focus": 22}, "qual_reqs": ["art_degree"]},
    "director":        {"minigame": "shift_sim",     "stat_reqs": {"charisma": 35, "perception": 30, "intelligence": 28, "focus": 28}, "qual_reqs": ["art_degree"]},
    "novelist":        {"minigame": "fill_blank",    "stat_reqs": {"intelligence": 28, "charisma": 22, "focus": 25}, "qual_reqs": ["art_degree"]},
    "jeweler":         {"minigame": "precision",     "stat_reqs": {"dexterity": 28, "perception": 25, "focus": 22}, "qual_reqs": ["apprenticeship"]},
    "potter":          {"minigame": "sequence",      "stat_reqs": {"dexterity": 18, "perception": 15, "focus": 15}, "qual_reqs": []},
    "stunt_double":    {"minigame": "timing",        "stat_reqs": {"dexterity": 28, "endurance": 25, "strength": 22, "focus": 22}, "qual_reqs": []},
    "voice_actor":     {"minigame": "typing_race",   "stat_reqs": {"charisma": 25, "dexterity": 20, "perception": 20}, "qual_reqs": []},
    "maestro":         {"minigame": "sequence",      "stat_reqs": {"dexterity": 40, "perception": 35, "charisma": 35, "focus": 30}, "qual_reqs": ["art_degree"]},

    # ═══════════════ Transport & Logistics (25) ═══════════════
    "delivery":        {"minigame": "route_plan",    "stat_reqs": {"endurance": 15, "perception": 12}, "qual_reqs": ["drivers_license"]},
    "pilot":           {"minigame": "sequence",      "stat_reqs": {"perception": 40, "focus": 35, "intelligence": 30}, "qual_reqs": ["pilot_license"]},
    "truck_driver":    {"minigame": "route_plan",    "stat_reqs": {"endurance": 22, "perception": 20}, "qual_reqs": ["commercial_license"]},
    "taxi_driver":     {"minigame": "quick_pick",    "stat_reqs": {"perception": 18, "charisma": 15}, "qual_reqs": ["drivers_license"]},
    "bus_driver":      {"minigame": "route_plan",    "stat_reqs": {"perception": 20, "endurance": 20}, "qual_reqs": ["drivers_license"]},
    "train_driver":    {"minigame": "timing",        "stat_reqs": {"perception": 22, "focus": 22, "endurance": 20}, "qual_reqs": ["drivers_license"]},
    "ship_captain":    {"minigame": "multi_stage",   "stat_reqs": {"perception": 35, "focus": 30, "intelligence": 28, "endurance": 25}, "qual_reqs": ["commercial_license"]},
    "forklift":        {"minigame": "precision",     "stat_reqs": {"perception": 18, "dexterity": 18, "focus": 15}, "qual_reqs": ["drivers_license"]},
    "warehouse":       {"minigame": "sort",          "stat_reqs": {"endurance": 15, "perception": 12}, "qual_reqs": []},
    "courier":         {"minigame": "route_plan",    "stat_reqs": {"endurance": 18, "perception": 18}, "qual_reqs": ["drivers_license"]},
    "ambulance_drv":   {"minigame": "quick_pick",    "stat_reqs": {"perception": 22, "endurance": 22, "focus": 20}, "qual_reqs": ["drivers_license"]},
    "fire_truck_drv":  {"minigame": "quick_pick",    "stat_reqs": {"perception": 22, "endurance": 22, "strength": 20}, "qual_reqs": ["drivers_license"]},
    "subway_op":       {"minigame": "timing",        "stat_reqs": {"perception": 20, "focus": 20, "endurance": 18}, "qual_reqs": ["drivers_license"]},
    "tram_driver":     {"minigame": "timing",        "stat_reqs": {"perception": 18, "focus": 18, "endurance": 18}, "qual_reqs": ["drivers_license"]},
    "logistics_mgr":   {"minigame": "shift_sim",     "stat_reqs": {"intelligence": 30, "perception": 25, "charisma": 22, "focus": 25}, "qual_reqs": ["business_degree"]},
    "air_traffic":     {"minigame": "sequence",      "stat_reqs": {"perception": 35, "focus": 35, "intelligence": 28}, "qual_reqs": ["pilot_license"]},
    "harbor_master":   {"minigame": "sequence",      "stat_reqs": {"perception": 30, "focus": 28, "intelligence": 25, "charisma": 22}, "qual_reqs": ["commercial_license"]},
    "cargo_pilot":     {"minigame": "sequence",      "stat_reqs": {"perception": 35, "focus": 32, "endurance": 28}, "qual_reqs": ["pilot_license"]},
    "helicopter_pilot":{"minigame": "sequence",      "stat_reqs": {"perception": 32, "focus": 30, "dexterity": 25}, "qual_reqs": ["pilot_license"]},
    "dispatch":        {"minigame": "sort",          "stat_reqs": {"perception": 22, "focus": 22, "intelligence": 20}, "qual_reqs": ["drivers_license"]},
    "bike_courier":    {"minigame": "route_plan",    "stat_reqs": {"endurance": 18, "perception": 15, "dexterity": 15}, "qual_reqs": []},
    "chauffeur":       {"minigame": "quick_pick",    "stat_reqs": {"perception": 22, "charisma": 22, "dexterity": 18}, "qual_reqs": ["drivers_license"]},
    "tow_truck":       {"minigame": "route_plan",    "stat_reqs": {"strength": 18, "perception": 18, "endurance": 18}, "qual_reqs": ["drivers_license"]},
    "supply_chain":    {"minigame": "budget",        "stat_reqs": {"intelligence": 32, "perception": 28, "focus": 28}, "qual_reqs": ["business_degree"]},
    "test_pilot":      {"minigame": "multi_stage",   "stat_reqs": {"perception": 45, "focus": 40, "dexterity": 35, "endurance": 32}, "qual_reqs": ["pilot_license"]},
}

# ═══════════════════════════════════════════════════════════════
# 3-minigame system — each job gets 3 potential minigames.
# One is randomly selected each shift so players can't anticipate
# which one they'll face. The existing minigame is kept as #1,
# and 2 more are drawn from a category-themed pool.
# ═══════════════════════════════════════════════════════════════

import random as _random
from config.minigame_content import JOB_CONTENT as _JOB_CONTENT

_CATEGORY_MINIGAME_POOL = {
    "entry":     ["quick_pick", "sort", "sequence", "timing", "speed_run", "memory", "route_plan", "match_pairs"],
    "service":   ["recipe_build", "sequence", "memory", "sort", "quick_pick", "match_pairs", "speed_run", "shift_sim", "multi_stage"],
    "trades":    ["sequence", "assembly", "precision", "sort", "pattern", "combo_lock", "shift_sim", "speed_run"],
    "medical":   ["diagnosis", "triage", "sequence", "match_pairs", "spot_error", "multi_stage", "pattern", "categorize", "memory"],
    "tech":      ["spot_error", "assembly", "sequence", "pattern", "math", "combo_lock", "fill_blank", "shift_sim", "precision"],
    "business":  ["math", "budget", "negotiation", "quick_pick", "shift_sim", "pattern", "multi_stage", "match_pairs"],
    "creative":  ["sort", "sequence", "quick_pick", "fill_blank", "precision", "memory", "timing", "typing_race", "match_pairs"],
    "transport": ["route_plan", "timing", "sequence", "sort", "quick_pick", "precision", "multi_stage", "speed_run"],
}

# Subcategory-specific overrides for more thematic variety
_SUBCATEGORY_EXTRA = {
    "kitchen":     ["recipe_build", "sequence", "speed_run", "sort"],
    "beverage":    ["recipe_build", "match_pairs", "precision", "memory"],
    "construction":["assembly", "sequence", "precision", "speed_run"],
    "skilled":     ["sequence", "assembly", "combo_lock", "precision"],
    "clinical":    ["diagnosis", "triage", "sequence", "spot_error"],
    "research":    ["categorize", "pattern", "match_pairs", "multi_stage"],
    "software":    ["spot_error", "assembly", "sequence", "pattern"],
    "data_ai":     ["math", "pattern", "sequence", "categorize"],
    "finance":     ["math", "budget", "pattern", "precision"],
    "performing":  ["memory", "timing", "sequence", "quick_pick"],
    "driving":     ["route_plan", "timing", "quick_pick", "precision"],
    "writing":     ["fill_blank", "typing_race", "quick_pick", "pattern"],
}

for _jid, _req in JOB_REQUIREMENTS.items():
    _job = JOBS.get(_jid, {})
    _cat = _job.get("category", "")
    _sub = _job.get("subcategory", "")
    _primary = _req.get("minigame", "quick_pick")

    # Build pool from category + subcategory extras
    _pool = list(_CATEGORY_MINIGAME_POOL.get(_cat, ["quick_pick", "sort", "sequence"]))
    _sub_extras = _SUBCATEGORY_EXTRA.get(_sub, [])
    if _sub_extras:
        _pool = _sub_extras + [m for m in _pool if m not in _sub_extras]

    # Only pick minigame types that have content available for this job
    _available = set(_JOB_CONTENT.get(_jid, {}).keys())
    _others = [m for m in _pool if m != _primary and m in _available]
    _random.shuffle(_others)
    _picked = _others[:2]

    _req["minigames"] = [_primary] + _picked
    while len(_req["minigames"]) < 3:
        _fallback = [m for m in _pool if m not in _req["minigames"] and m in _available]
        if _fallback:
            _req["minigames"].append(_fallback[0])
        else:
            # Last resort: use any available content type not yet assigned
            _any_left = [m for m in _available if m not in _req["minigames"]]
            if _any_left:
                _req["minigames"].append(_any_left[0])
            else:
                _req["minigames"].append("quick_pick")
                break
