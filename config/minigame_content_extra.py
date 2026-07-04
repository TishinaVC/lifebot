"""
Extra minigame content for the 3-minigame system.
Contains the 2 additional minigame types per job that were added
when expanding from 1 to 3 minigames per job.
Each entry is themed to feel like doing the actual job.
"""

EXTRA_CONTENT = {

    # ═══════════════════════════════════════════════════════════════
    # ENTRY LEVEL — 25 jobs
    # ═══════════════════════════════════════════════════════════════

    "beggar": {
        "timing": {
            "prompt": "Time your ask perfectly! Click when a passerby makes eye contact to ask for change.",
            "beats": 4,
        },
        "match_pairs": {
            "prompt": "Match each begging spot to its best time of day:",
            "pairs": [("Restaurant exit", "After dinner"), ("ATM", "Payday Friday"), ("Subway entrance", "Morning rush"), ("Church steps", "Sunday morning")],
        },
    },
    "busker": {
        "sequence": {
            "prompt": "Set up your busking spot in the right order:",
            "items": ["Scout the location", "Set out instrument case", "Tune guitar", "Test acoustics", "Start playing", "Engage passersby"],
            "order": ["Scout the location", "Set out instrument case", "Tune guitar", "Test acoustics", "Start playing", "Engage passersby"],
        },
        "quick_pick": {
            "prompt": "A crowd is gathering but someone puts in a request you don't know. Best response?",
            "options": ["Refuse politely", "Play it anyway and improvise", "Offer a similar song you know", "Pack up and leave"],
            "correct": "Offer a similar song you know",
        },
    },
    "leafleter": {
        "memory": {
            "prompt": "Remember which streets you've already covered: Main St, Oak Ave, Park Rd, Elm St, Main St again",
            "sequence": ["Main St", "Oak Ave", "Park Rd", "Elm St", "Main St again"],
        },
        "quick_pick": {
            "prompt": "A pedestrian looks annoyed and waves you off. Best approach?",
            "options": ["Shove flyer at them", "Smile and move on", "Follow them", "Stop handing out flyers"],
            "correct": "Smile and move on",
        },
    },
    "window_washer": {
        "memory": {
            "prompt": "Remember which windows the boss wants done first: 2nd floor corner, 1st floor entrance, 3rd floor office, Ground floor display",
            "sequence": ["2nd floor corner", "1st floor entrance", "3rd floor office", "Ground floor display"],
        },
        "timing": {
            "prompt": "Squeegee in rhythm! Click each time the squeegee reaches the bottom of the stroke.",
            "beats": 5,
        },
    },
    "dog_walker": {
        "sort": {
            "prompt": "Sort the dogs by their walking needs — energetic first, slow last:",
            "items": ["Rex (pulls hard, needs long run)", "Bella (senior, short stroll)", "Max (medium energy)", "Luna (puppy, frequent stops)"],
            "order": ["Rex (pulls hard, needs long run)", "Max (medium energy)", "Luna (puppy, frequent stops)", "Bella (senior, short stroll)"],
        },
        "route_plan": {
            "prompt": "Plan the dog walking route — park first for exercise, then residential for calm:",
            "stops": ["House", "Park entrance", "Park trail", "Water fountain", "Residential loop", "House"],
            "optimal": ["House", "Park entrance", "Park trail", "Water fountain", "Residential loop", "House"],
        },
    },
    "recycler": {
        "speed_run": {
            "prompt": "Collect all the cans and bottles before the truck comes! Click each pile to collect.",
            "tasks": ["Pile by bench", "Pile in bushes", "Pile near fountain", "Pile by trash can", "Pile in gutter"],
        },
        "timing": {
            "prompt": "Time your crush! Click when the can is centered under the compactor.",
            "beats": 4,
        },
    },
    "shoe_shiner": {
        "timing": {
            "prompt": "Buff in rhythm! Click each time your brush completes a full circle.",
            "beats": 5,
        },
        "memory": {
            "prompt": "Remember the customer's shoe preferences: Brown leather oxfords, extra shine, no conditioner, quick service",
            "sequence": ["Brown leather oxfords", "Extra shine", "No conditioner", "Quick service"],
        },
    },
    "newspaper": {
        "quick_pick": {
            "prompt": "A customer complains they didn't get their paper. What's the best response?",
            "options": ["Blame the weather", "Deliver a replacement immediately", "Tell them to call the office", "Skip their house tomorrow"],
            "correct": "Deliver a replacement immediately",
        },
        "memory": {
            "prompt": "Remember your delivery list in order: 12 Maple, 45 Oak, 8 Pine, 23 Cedar, 67 Birch",
            "sequence": ["12 Maple", "45 Oak", "8 Pine", "23 Cedar", "67 Birch"],
        },
    },
    "car_wash": {
        "speed_run": {
            "prompt": "The queue is building up! Wash each car section before the timer runs out.",
            "tasks": ["Roof", "Hood", "Windshield", "Doors (left)", "Doors (right)", "Trunk", "Wheels"],
        },
        "memory": {
            "prompt": "Remember the customer's special requests: No wax, extra tire shine, air freshener vanilla, clean floor mats",
            "sequence": ["No wax", "Extra tire shine", "Air freshener vanilla", "Clean floor mats"],
        },
    },
    "trolley": {
        "sequence": {
            "prompt": "Collect trolleys in the correct order — farthest first, work back to store:",
            "items": ["Garden section trolleys", "Far lot trolleys", "Entrance trolleys", "Cart corral trolleys", "Store returns"],
            "order": ["Garden section trolleys", "Far lot trolleys", "Cart corral trolleys", "Entrance trolleys", "Store returns"],
        },
        "timing": {
            "prompt": "Push the trolley train through the lot! Click to steer when the path clears.",
            "beats": 4,
        },
    },
    "plant_waterer": {
        "sort": {
            "prompt": "Sort plants by watering needs — thirsty first, drought-tolerant last:",
            "items": ["Fern (needs lots of water)", "Orchid (moderate water)", "Succulent (rarely watered)", "Cactus (almost never)", "Ivy (regular water)"],
            "order": ["Fern (needs lots of water)", "Ivy (regular water)", "Orchid (moderate water)", "Succulent (rarely watered)", "Cactus (almost never)"],
        },
        "speed_run": {
            "prompt": "Water all the office plants before the meeting starts! Click each plant to water it.",
            "tasks": ["Reception desk plant", "Conference room fern", "Break room ivy", "CEO office orchid", "Hallway succulents", "Lobby palm"],
        },
    },
    "litter_picker": {
        "memory": {
            "prompt": "Remember which bins you've emptied: North bin, East bin, South bin, West bin, North bin (overflowing again)",
            "sequence": ["North bin", "East bin", "South bin", "West bin", "North bin (overflowing again)"],
        },
        "sequence": {
            "prompt": "Clean the park in the correct order — high-traffic areas first:",
            "items": ["Playground area", "Picnic tables", "Walking paths", "Park benches", "Parking lot", "Entrance"],
            "order": ["Playground area", "Picnic tables", "Park benches", "Walking paths", "Parking lot", "Entrance"],
        },
    },
    "sign_holder": {
        "sequence": {
            "prompt": "Set up your sign-holding station in the right order:",
            "items": ["Check the sign for damage", "Find a visible corner", "Position for traffic flow", "Start waving sign", "Rotate to face new traffic", "Take micro-breaks"],
            "order": ["Check the sign for damage", "Find a visible corner", "Position for traffic flow", "Start waving sign", "Rotate to face new traffic", "Take micro-breaks"],
        },
        "sort": {
            "prompt": "Sort the signs by which direction they should face:",
            "items": ["Sale sign (face oncoming traffic)", "Open sign (face pedestrians)", "Direction sign (face intersection)", "Parking sign (face lot entrance)"],
            "categories": ["Traffic", "Pedestrian", "Intersection", "Parking"],
        },
    },
    "survey_taker": {
        "timing": {
            "prompt": "Approach people at the right moment! Click when someone looks approachable (not rushing).",
            "beats": 4,
        },
        "speed_run": {
            "prompt": "Complete your survey quota before the deadline! Click each person to survey them.",
            "tasks": ["Person on bench", "Person at bus stop", "Person leaving store", "Person on phone (wait)", "Person with coffee"],
        },
    },
    "moving_helper": {
        "sort": {
            "prompt": "Sort items by loading priority — heaviest and most durable first:",
            "items": ["Refrigerator (heavy, durable)", "Sofa (heavy, durable)", "TV (fragile, medium)", "Dishes (fragile, light)", "Lamp (fragile, light)"],
            "categories": ["Load first (heavy)", "Load first (heavy)", "Load last (fragile)", "Load last (fragile)", "Load last (fragile)"],
        },
        "quick_pick": {
            "prompt": "The client asks where to put the heavy dresser. Best answer?",
            "options": ["Against any wall", "Against a load-bearing wall", "In the middle of the room", "Near the window"],
            "correct": "Against a load-bearing wall",
        },
    },
    "ticket_tearer": {
        "sequence": {
            "prompt": "Process a large group in the correct order:",
            "items": ["Greet group", "Count tickets", "Tear stubs", "Hand back stubs", "Direct to seats", "Thank them"],
            "order": ["Greet group", "Count tickets", "Tear stubs", "Hand back stubs", "Direct to seats", "Thank them"],
        },
        "match_pairs": {
            "prompt": "Match each ticket type to its correct entrance:",
            "pairs": [("VIP pass", "VIP entrance"), ("General admission", "Main doors"), ("Student ticket", "Side entrance"), ("Press badge", "Back stage door")],
        },
    },
    "ice_cream": {
        "match_pairs": {
            "prompt": "Match each customer's request to the correct flavor:",
            "pairs": [("Kid wants something sweet", "Bubblegum"), ("Adult wants something rich", "Chocolate fudge"), ("Health-conscious customer", "Mango sorbet"), ("Classic customer", "Vanilla bean")],
        },
        "timing": {
            "prompt": "Scoop in rhythm! Click each time the scoop completes a full turn in the tub.",
            "beats": 4,
        },
    },
    "balloon_seller": {
        "quick_pick": {
            "prompt": "A kid wants a balloon animal. Which one can you make fastest?",
            "options": ["A dog (3 twists)", "A sword (1 twist)", "A flower (5 twists)", "A hat (4 twists)"],
            "correct": "A sword (1 twist)",
        },
        "sort": {
            "prompt": "Sort balloons by inflation order — largest first for stability:",
            "items": ["Giant balloon (needs 3 breaths)", "Large balloon (2 breaths)", "Medium balloon (1 breath)", "Small balloon (half breath)"],
            "order": ["Giant balloon (needs 3 breaths)", "Large balloon (2 breaths)", "Medium balloon (1 breath)", "Small balloon (half breath)"],
        },
    },
    "parking_attend": {
        "memory": {
            "prompt": "Remember the license plates of cars in the lot: ABC-123, XYZ-789, DEF-456, GHI-012",
            "sequence": ["ABC-123", "XYZ-789", "DEF-456", "GHI-012"],
        },
        "timing": {
            "prompt": "Raise the barrier at the right moment! Click when the car reaches the gate.",
            "beats": 3,
        },
    },
    "garden_helper": {
        "match_pairs": {
            "prompt": "Match each plant to its correct care instruction:",
            "pairs": [("Tomato", "Stake and prune"), ("Lettuce", "Keep shaded and moist"), ("Rose bush", "Deadhead blooms"), ("Lawn", "Mow and edge")],
        },
        "sequence": {
            "prompt": "Prepare a garden bed in the correct order:",
            "items": ["Clear weeds", "Turn soil", "Add compost", "Rake smooth", "Mark rows", "Plant seeds", "Water gently"],
            "order": ["Clear weeds", "Turn soil", "Add compost", "Rake smooth", "Mark rows", "Plant seeds", "Water gently"],
        },
    },
    "shelf_stocker": {
        "sequence": {
            "prompt": "Stock a new shipment in the correct order — back stock first, then front:",
            "items": ["Unload pallet", "Check inventory list", "Rotate old stock forward", "Stock back shelves", "Stock front shelves", "Face products", "Remove empty boxes"],
            "order": ["Unload pallet", "Check inventory list", "Rotate old stock forward", "Stock back shelves", "Stock front shelves", "Face products", "Remove empty boxes"],
        },
        "match_pairs": {
            "prompt": "Match each product to its correct shelf section:",
            "pairs": [("Cereal", "Aisle 1 — Breakfast"), ("Pasta", "Aisle 2 — Italian"), ("Dairy", "Aisle 3 — Refrigerated"), ("Frozen pizza", "Aisle 5 — Frozen")],
        },
    },
    "janitor": {
        "memory": {
            "prompt": "Remember the cleaning schedule: Bathrooms at 9am, Lobby at 10am, Offices at 11am, Bathrooms again at 2pm",
            "sequence": ["Bathrooms at 9am", "Lobby at 10am", "Offices at 11am", "Bathrooms again at 2pm"],
        },
        "route_plan": {
            "prompt": "Plan the most efficient cleaning route through the building:",
            "stops": ["Supply closet", "3rd floor offices", "2nd floor bathrooms", "1st floor lobby", "Basement storage", "Supply closet"],
            "optimal": ["Supply closet", "3rd floor offices", "2nd floor bathrooms", "1st floor lobby", "Basement storage", "Supply closet"],
        },
    },
    "laundry": {
        "memory": {
            "prompt": "Remember the customer's special instructions: Whites hot, Colors cold, Delicates hand wash, Towels separate",
            "sequence": ["Whites hot", "Colors cold", "Delicates hand wash", "Towels separate"],
        },
        "timing": {
            "prompt": "Fold sheets in rhythm! Click each time you complete a fold.",
            "beats": 4,
        },
    },
    "food_sample": {
        "memory": {
            "prompt": "Remember which samples each customer tried: Spicy wing, Sweet dessert, Mild dip, Savory snack",
            "sequence": ["Spicy wing", "Sweet dessert", "Mild dip", "Savory snack"],
        },
        "timing": {
            "prompt": "Time your pitch! Click when a shopper slows down near your sample station.",
            "beats": 4,
        },
    },
    "cart_pusher": {
        "quick_pick": {
            "prompt": "A customer needs help reaching their car with heavy bags. Best response?",
            "options": ["Direct them to customer service", "Help them immediately", "Get a coworker", "Suggest a cart"],
            "correct": "Help them immediately",
        },
        "sort": {
            "prompt": "Sort the carts by which corral they belong in:",
            "items": ["Small cart (corral A)", "Large cart (corral B)", "Flatbed (corral C)", "Small cart (corral A)", "Large cart (corral B)"],
            "categories": ["Corral A", "Corral B", "Corral C", "Corral A", "Corral B"],
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # SERVICE LEVEL — 25 jobs
    # ═══════════════════════════════════════════════════════════════

    "barista": {
        "shift_sim": {
            "prompt": "Manage the morning rush — handle in priority order:",
            "situations": ["Espresso machine down (critical)", "Long queue forming (high)", "Milk running low (medium)", "Restock cups (medium)", "Wipe tables (low)"],
            "optimal": ["Espresso machine down (critical)", "Long queue forming (high)", "Milk running low (medium)", "Restock cups (medium)", "Wipe tables (low)"],
        },
        "match_pairs": {
            "prompt": "Match each coffee drink to its correct ingredient ratio:",
            "pairs": [("Espresso", "1 shot, no milk"), ("Latte", "1 shot, 3/4 steamed milk"), ("Cappuccino", "1 shot, 1/3 foam"), ("Americano", "1 shot, 3/4 hot water")],
        },
    },
    "chef": {
        "quick_pick": {
            "prompt": "A VIP guest has a nut allergy. Which appetizer is safe?",
            "options": ["Pesto pasta (pine nuts)", "Almond-crusted salmon", "Caprese salad", "Satay chicken skewers"],
            "correct": "Caprese salad",
        },
        "speed_run": {
            "prompt": "Fire all the tickets! Complete each dish before the timer runs out.",
            "tasks": ["Seared scallops", "Beef Wellington", "Caesar salad", "Lobster bisque", "Chocolate fondant"],
        },
    },
    "waiter": {
        "match_pairs": {
            "prompt": "Match each menu item to its correct allergen warning:",
            "pairs": [("Shrimp pasta", "Shellfish"), ("Caesar salad", "Eggs/anchovy"), ("Peanut sauce chicken", "Peanuts"), ("Wheat bread", "Gluten")],
        },
        "shift_sim": {
            "prompt": "Manage your section during dinner rush — prioritize:",
            "situations": ["Table 3 food is cold (critical)", "Table 5 waiting to order (high)", "Table 1 needs water refills (low)", "Table 7 wants the check (medium)", "Table 2 spilled wine (high)"],
            "optimal": ["Table 2 spilled wine (high)", "Table 3 food is cold (critical)", "Table 5 waiting to order (high)", "Table 7 wants the check (medium)", "Table 1 needs water refills (low)"],
        },
    },
    "bartender": {
        "match_pairs": {
            "prompt": "Match each cocktail to its base spirit:",
            "pairs": [("Margarita", "Tequila"), ("Old Fashioned", "Bourbon"), ("Martini", "Gin"), ("Mojito", "White rum")],
        },
        "sequence": {
            "prompt": "Open and close the bar in the correct order:",
            "items": ["Check ID stock", "Cut garnishes", "Ice wells", "Stock bottles", "Wipe bar", "Check taps", "Open doors"],
            "order": ["Check ID stock", "Cut garnishes", "Ice wells", "Stock bottles", "Wipe bar", "Check taps", "Open doors"],
        },
    },
    "fast_food": {
        "multi_stage": {
            "prompt": "Handle the lunch rush across 3 stations:",
            "stages": [
                {"type": "quick_pick", "prompt": "Drive-thru timer is at 3 minutes. Priority?", "options": ["Take next order", "Finish current order", "Ask for help", "Skip to window 2"], "correct": "Finish current order"},
                {"type": "sequence", "prompt": "Build a burger in the correct order:", "items": ["Bottom bun", "Patty", "Cheese", "Lettuce", "Tomato", "Top bun"], "order": ["Bottom bun", "Patty", "Cheese", "Lettuce", "Tomato", "Top bun"]},
                {"type": "quick_pick", "prompt": "Customer complains their fries are cold. Response?", "options": ["Argue", "Replace immediately", "Offer refund", "Ignore them"], "correct": "Replace immediately"},
            ],
        },
        "sort": {
            "prompt": "Sort orders by preparation time — quickest first to maximize throughput:",
            "items": ["Ice cream cone (30 sec)", "Coffee (1 min)", "Burger combo (3 min)", "Chicken meal (5 min)", "Custom order (7 min)"],
            "order": ["Ice cream cone (30 sec)", "Coffee (1 min)", "Burger combo (3 min)", "Chicken meal (5 min)", "Custom order (7 min)"],
        },
    },
    "sushi_chef": {
        "speed_run": {
            "prompt": "Roll all the orders before the fish warms up! Click each roll to complete it.",
            "tasks": ["California roll", "Spicy tuna roll", "Dragon roll", "Rainbow roll", "Tempura roll", "Nigiri platter"],
        },
        "multi_stage": {
            "prompt": "Prepare an omakase course across 3 stages:",
            "stages": [
                {"type": "sequence", "prompt": "Prepare the rice in order:", "items": ["Wash rice", "Cook rice", "Season with vinegar", "Cool to body temp", "Cover with cloth"], "order": ["Wash rice", "Cook rice", "Season with vinegar", "Cool to body temp", "Cover with cloth"]},
                {"type": "quick_pick", "prompt": "Which fish for the first course?", "options": ["Fatty tuna (rich start)", "Eel (heavy)", "Mackerel (strong)", "Egg (sweet)"], "correct": "Fatty tuna (rich start)"},
                {"type": "sequence", "prompt": "Plate the final course in order:", "items": ["Tamago", "Eel roll", "Miso soup", "Tea", "Dessert"], "order": ["Tamago", "Eel roll", "Miso soup", "Tea", "Dessert"]},
            ],
        },
    },
    "pastry_chef": {
        "quick_pick": {
            "prompt": "A customer wants a gluten-free dessert. Which option is safe?",
            "options": ["Croissant (wheat)", "Flourless chocolate cake", "Puff pastry tart", "Bread pudding"],
            "correct": "Flourless chocolate cake",
        },
        "match_pairs": {
            "prompt": "Match each pastry to its key technique:",
            "pairs": [("Croissant", "Lamination"), ("Macaron", "Macaronage"), ("Eclair", "Pâte à choux"), ("Tart", "Blind baking")],
        },
    },
    "sommelier": {
        "speed_run": {
            "prompt": "Serve wine to all tables before the tasting event starts! Click each table to serve.",
            "tasks": ["Table 1: Pinot Noir", "Table 2: Chardonnay", "Table 3: Champagne", "Table 4: Bordeaux", "Table 5: Riesling"],
        },
        "recipe_build": {
            "prompt": "Build the perfect wine flight — select in serving order (lightest to fullest):",
            "ingredients": ["Prosecco (sparkling)", "Pinot Grigio (light white)", "Sauvignon Blanc (medium white)", "Pinot Noir (light red)", "Cabernet Sauvignon (full red)"],
            "order": ["Prosecco (sparkling)", "Pinot Grigio (light white)", "Sauvignon Blanc (medium white)", "Pinot Noir (light red)", "Cabernet Sauvignon (full red)"],
        },
    },
    "food_truck": {
        "sort": {
            "prompt": "Sort the prep tasks by what needs to start first:",
            "items": ["Marinate chicken (2 hrs)", "Cook rice (20 min)", "Chop vegetables (10 min)", "Heat grill (5 min)", "Set up serving station (2 min)"],
            "order": ["Marinate chicken (2 hrs)", "Cook rice (20 min)", "Chop vegetables (10 min)", "Heat grill (5 min)", "Set up serving station (2 min)"],
        },
        "multi_stage": {
            "prompt": "Run the food truck lunch service across 3 stages:",
            "stages": [
                {"type": "quick_pick", "prompt": "First customer wants 'the usual.' What is it?", "options": ["Taco combo", "Burger special", "Veggie bowl", "Just a drink"], "correct": "Taco combo"},
                {"type": "sequence", "prompt": "Cook the taco combo in order:", "items": ["Grill tortilla", "Add protein", "Add salsa", "Add garnish", "Wrap and serve"], "order": ["Grill tortilla", "Add protein", "Add salsa", "Add garnish", "Wrap and serve"]},
                {"type": "quick_pick", "prompt": "Propane is running low. Action?", "options": ["Keep cooking", "Switch to backup tank", "Close early", "Use electric stove"], "correct": "Switch to backup tank"},
            ],
        },
    },
    "caterer": {
        "sequence": {
            "prompt": "Set up a catering event in the correct order:",
            "items": ["Arrive and assess venue", "Set up tables and linens", "Arrange buffet stations", "Plate appetizers", "Set up beverage station", "Final quality check", "Greet guests"],
            "order": ["Arrive and assess venue", "Set up tables and linens", "Arrange buffet stations", "Plate appetizers", "Set up beverage station", "Final quality check", "Greet guests"],
        },
        "quick_pick": {
            "prompt": "At a wedding, the bride is vegetarian but the menu is set. Best response?",
            "options": ["Tell her to pick around it", "Prepare a special vegetarian plate", "Apologize and offer salad", "Change the entire menu"],
            "correct": "Prepare a special vegetarian plate",
        },
    },
    "butcher": {
        "recipe_build": {
            "prompt": "Prepare a sausage — assemble ingredients in the correct order:",
            "ingredients": ["Grind meat", "Add fat ratio", "Mix spices", "Add ice water", "Stuff casings", "Link sausages", "Hang to dry"],
            "order": ["Grind meat", "Add fat ratio", "Mix spices", "Add ice water", "Stuff casings", "Link sausages", "Hang to dry"],
        },
        "memory": {
            "prompt": "Remember the customer orders: 2lb ground beef, 1 ribeye steak, 3 pork chops, 1 whole chicken, 1lb bacon",
            "sequence": ["2lb ground beef", "1 ribeye steak", "3 pork chops", "1 whole chicken", "1lb bacon"],
        },
    },
    "baker": {
        "multi_stage": {
            "prompt": "Run the morning bake across 3 stages:",
            "stages": [
                {"type": "sequence", "prompt": "Prepare sourdough in order:", "items": ["Feed starter", "Mix autolyse", "Bulk ferment", "Shape loaves", "Proof overnight"], "order": ["Feed starter", "Mix autolyse", "Bulk ferment", "Shape loaves", "Proof overnight"]},
                {"type": "quick_pick", "prompt": "Oven temp is off by 25°F. Action?", "options": ["Bake anyway", "Adjust thermostat", "Call repair", "Use different oven"], "correct": "Adjust thermostat"},
                {"type": "sequence", "prompt": "Fill the display case in order:", "items": ["Sourdough loaves", "Baguettes", "Croissants", "Muffins", "Cookies", "Cakes"], "order": ["Sourdough loaves", "Baguettes", "Croissants", "Muffins", "Cookies", "Cakes"]},
            ],
        },
        "sort": {
            "prompt": "Sort the breads by bake temperature — hottest first:",
            "items": ["Artisan sourdough (450°F)", "Baguettes (425°F)", "Brioche (375°F)", "Muffins (350°F)", "Cheesecake (325°F)"],
            "order": ["Artisan sourdough (450°F)", "Baguettes (425°F)", "Brioche (375°F)", "Muffins (350°F)", "Cheesecake (325°F)"],
        },
    },
    "host": {
        "sequence": {
            "prompt": "Seat a large party in the correct order:",
            "items": ["Greet at door", "Check reservation", "Assess table availability", "Grab menus", "Walk to table", "Introduce server", "Offer water"],
            "order": ["Greet at door", "Check reservation", "Assess table availability", "Grab menus", "Walk to table", "Introduce server", "Offer water"],
        },
        "match_pairs": {
            "prompt": "Match each party size to the best table arrangement:",
            "pairs": [("Party of 2", "Window table"), ("Party of 4", "Center booth"), ("Party of 6", "Pushed tables"), ("Party of 8+", "Private room")],
        },
    },
    "barista_master": {
        "speed_run": {
            "prompt": "Complete all the latte art orders for the competition! Click each cup to finish.",
            "tasks": ["Heart latte", "Rosetta latte", "Tulip latte", "Swan latte", "Dragon latte", "Portrait latte"],
        },
        "sequence": {
            "prompt": "Dial in a new espresso blend — calibrate in the correct order:",
            "items": ["Weigh beans (18g)", "Grind at setting 3", "Distribute grounds", "Tamp level", "Extract 25 sec", "Taste shot", "Adjust grind", "Re-extract"],
            "order": ["Weigh beans (18g)", "Grind at setting 3", "Distribute grounds", "Tamp level", "Extract 25 sec", "Taste shot", "Adjust grind", "Re-extract"],
        },
    },
    "sous_chef": {
        "sort": {
            "prompt": "Sort the prep tasks by kitchen station priority:",
            "items": ["Butcher proteins (cold first)", "Prep sauces (stove next)", "Chop vegetables (anytime)", "Bake breads (oven last)", "Plate garnishes (last minute)"],
            "order": ["Butcher proteins (cold first)", "Prep sauces (stove next)", "Chop vegetables (anytime)", "Bake breads (oven last)", "Plate garnishes (last minute)"],
        },
        "match_pairs": {
            "prompt": "Match each sauce to its correct mother sauce base:",
            "pairs": [("Béarnaise", "Hollandaise"), ("Mornay", "Béchamel"), ("Bourguignonne", "Espagnole"), ("Vin blanc", "Velouté")],
        },
    },
    "nutritionist": {
        "match_pairs": {
            "prompt": "Match each nutrient to its primary food source:",
            "pairs": [("Vitamin C", "Citrus fruits"), ("Calcium", "Dairy products"), ("Iron", "Red meat/spinach"), ("Omega-3", "Fatty fish")],
        },
        "multi_stage": {
            "prompt": "Create a meal plan for a client across 3 stages:",
            "stages": [
                {"type": "quick_pick", "prompt": "Client wants to lose weight. First priority?", "options": ["Cut all carbs", "Create caloric deficit", "Increase protein only", "Fasting only"], "correct": "Create caloric deficit"},
                {"type": "sequence", "prompt": "Build a balanced day in order:", "items": ["Breakfast: protein + fiber", "Snack: fruit + nuts", "Lunch: lean protein + veg", "Snack: yogurt", "Dinner: fish + salad + complex carb"], "order": ["Breakfast: protein + fiber", "Snack: fruit + nuts", "Lunch: lean protein + veg", "Snack: yogurt", "Dinner: fish + salad + complex carb"]},
                {"type": "quick_pick", "prompt": "Client lost 5lb in week 1. Adjust?", "options": ["No change needed", "Reduce calories more", "Increase calories", "Add cheat day"], "correct": "No change needed"},
            ],
        },
    },
    "food_critic": {
        "recipe_build": {
            "prompt": "Construct the perfect review — assemble elements in the correct order:",
            "ingredients": ["Ambiance description", "Service assessment", "Appetizer critique", "Main course analysis", "Dessert evaluation", "Overall verdict", "Star rating"],
            "order": ["Ambiance description", "Service assessment", "Appetizer critique", "Main course analysis", "Dessert evaluation", "Overall verdict", "Star rating"],
        },
        "match_pairs": {
            "prompt": "Match each cooking technique to its description:",
            "pairs": [("Sous vide", "Vacuum-sealed water bath"), ("Confit", "Cooking in fat at low temp"), ("Braise", "Sear then slow-cook in liquid"), ("Flambé", "Alcohol-ignited finishing")],
        },
    },
    "hotel_manager": {
        "memory": {
            "prompt": "Remember today's VIP check-ins: Suite 1200 (3pm), Penthouse (5pm), Suite 800 (6pm), Presidential (8pm)",
            "sequence": ["Suite 1200 (3pm)", "Penthouse (5pm)", "Suite 800 (6pm)", "Presidential (8pm)"],
        },
        "match_pairs": {
            "prompt": "Match each guest complaint to the correct response:",
            "pairs": [("Room not clean", "Upgrade + housekeeping ASAP"), ("Noise next door", "Move rooms + comp breakfast"), ("AC not working", "Engineer + fan delivered"), ("Wrong room type", "Upgrade to booked type")],
        },
    },
    "event_planner": {
        "memory": {
            "prompt": "Remember the wedding timeline: Ceremony 2pm, Cocktails 3pm, Dinner 5pm, Toasts 6pm, Dancing 8pm",
            "sequence": ["Ceremony 2pm", "Cocktails 3pm", "Dinner 5pm", "Toasts 6pm", "Dancing 8pm"],
        },
        "match_pairs": {
            "prompt": "Match each event type to its typical venue requirement:",
            "pairs": [("Corporate conference", "A/V equipped hall"), ("Wedding", "Ceremony + reception spaces"), ("Birthday party", "Private dining room"), ("Trade show", "Open floor exhibition hall")],
        },
    },
    "sommelier_master": {
        "recipe_build": {
            "prompt": "Build a vertical tasting flight — select vintages in order (oldest to youngest):",
            "ingredients": ["2010 Bordeaux", "2012 Bordeaux", "2015 Bordeaux", "2018 Bordeaux", "2020 Bordeaux"],
            "order": ["2010 Bordeaux", "2012 Bordeaux", "2015 Bordeaux", "2018 Bordeaux", "2020 Bordeaux"],
        },
        "memory": {
            "prompt": "Remember the cellar inventory: 12 Cabernet, 8 Pinot Noir, 5 Chardonnay, 3 Champagne, 7 Riesling",
            "sequence": ["12 Cabernet", "8 Pinot Noir", "5 Chardonnay", "3 Champagne", "7 Riesling"],
        },
    },
    "mixologist": {
        "match_pairs": {
            "prompt": "Match each cocktail to its correct glassware:",
            "pairs": [("Martini", "V-shaped coupe"), ("Old Fashioned", "Rocks glass"), ("Mojito", "Highball glass"), ("Champagne cocktail", "Flute")],
        },
        "sort": {
            "prompt": "Sort the cocktail ingredients by addition order — spirits first, garnish last:",
            "items": ["Vodka (base spirit)", "Triple sec (liqueur)", "Lime juice (acid)", "Cranberry (mixer)", "Ice (dilution)", "Lime wheel (garnish)"],
            "order": ["Vodka (base spirit)", "Triple sec (liqueur)", "Lime juice (acid)", "Cranberry (mixer)", "Ice (dilution)", "Lime wheel (garnish)"],
        },
    },
    "chocolatier": {
        "speed_run": {
            "prompt": "Dip all the truffles before the chocolate seizes! Click each truffle to dip it.",
            "tasks": ["Dark chocolate truffle", "Milk chocolate truffle", "White chocolate truffle", "Caramel center", "Raspberry truffle", "Pistachio truffle"],
        },
        "shift_sim": {
            "prompt": "Manage the chocolate shop — prioritize:",
            "situations": ["Temper machine overheating (critical)", "Valentine's Day orders (high)", "Display case restocking (medium)", "Packaging supplies (low)", "Tasting samples (low)"],
            "optimal": ["Temper machine overheating (critical)", "Valentine's Day orders (high)", "Display case restocking (medium)", "Packaging supplies (low)", "Tasting samples (low)"],
        },
    },
    "teasomm": {
        "sequence": {
            "prompt": "Perform a traditional gongfu tea ceremony in the correct order:",
            "items": ["Warm the teapot", "Rinse tea leaves", "First infusion (10 sec)", "Pour to fairness cup", "Serve guests", "Second infusion (15 sec)", "Third infusion (20 sec)"],
            "order": ["Warm the teapot", "Rinse tea leaves", "First infusion (10 sec)", "Pour to fairness cup", "Serve guests", "Second infusion (15 sec)", "Third infusion (20 sec)"],
        },
        "speed_run": {
            "prompt": "Brew all the tea orders for the afternoon tea service! Click each pot to brew.",
            "tasks": ["Earl Grey pot", "Jasmine green tea", "Darjeeling first flush", "Pu-erh aged", "Chamomile blend", "Oolong roasted"],
        },
    },
    "private_chef": {
        "sort": {
            "prompt": "Sort the market list by which store to visit first (perishables last):",
            "items": ["Dry goods (pantry store)", "Spices (specialty shop)", "Wine (bottle shop)", "Vegetables (farmer's market)", "Fish (seamarket — last)"],
            "order": ["Dry goods (pantry store)", "Spices (specialty shop)", "Wine (bottle shop)", "Vegetables (farmer's market)", "Fish (seamarket — last)"],
        },
        "shift_sim": {
            "prompt": "Manage a private dinner party — prioritize:",
            "situations": ["Guest arrives early (high)", "Sauce is splitting (critical)", "Wine needs decanting (medium)", "Table setting incomplete (medium)", "Music selection (low)"],
            "optimal": ["Sauce is splitting (critical)", "Guest arrives early (high)", "Table setting incomplete (medium)", "Wine needs decanting (medium)", "Music selection (low)"],
        },
    },
    "restaurateur": {
        "match_pairs": {
            "prompt": "Match each restaurant problem to its correct solution:",
            "pairs": [("Food cost too high", "Renegotiate supplier contracts"), ("Staff turnover rising", "Review compensation and culture"), ("Negative Yelp reviews", "Respond professionally + fix issues"), ("Declining weekend covers", "Refresh menu + marketing push")],
        },
        "sequence": {
            "prompt": "Open a new restaurant location in the correct order:",
            "items": ["Market research", "Secure lease", "Design layout", "Obtain permits", "Hire and train staff", "Soft opening", "Grand opening"],
            "order": ["Market research", "Secure lease", "Design layout", "Obtain permits", "Hire and train staff", "Soft opening", "Grand opening"],
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # TRADES & LABOR — 25 jobs
    # ═══════════════════════════════════════════════════════════════

    "mechanic": {
        "pattern": {
            "prompt": "Spark plug firing order for a V8: 1, 8, 4, 3, 6, 5, 7, 2. What comes after 1, 8, 4, 3?",
            "sequence": ["1", "8", "4", "3", "?"],
            "answer": "6",
        },
        "precision": {
            "prompt": "Torque the lug nut to exactly 100 ft-lbs. Click when the wrench gauge hits 100!",
            "target": 100,
            "tolerance": 3,
        },
    },
    "electrician": {
        "pattern": {
            "prompt": "Wire gauge pattern: 14 AWG (15A), 12 AWG (20A), 10 AWG (30A), 8 AWG (?A)",
            "sequence": ["15A", "20A", "30A", "?"],
            "answer": "40A",
        },
        "combo_lock": {
            "prompt": "Set the breaker combination — find the correct 3-switch sequence:",
            "pins": [2, 5, 1],
            "max_val": 6,
        },
    },
    "plumber": {
        "speed_run": {
            "prompt": "Fix all the leaks before the homeowner gets home! Click each leak to repair it.",
            "tasks": ["Kitchen sink leak", "Bathroom pipe joint", "Toilet supply line", "Water heater valve", "Outdoor hose bib"],
        },
        "combo_lock": {
            "prompt": "Open the locked shutoff valve — find the correct 3-position combination:",
            "pins": [4, 2, 7],
            "max_val": 9,
        },
    },
    "carpenter": {
        "combo_lock": {
            "prompt": "Set the router depth — find the correct 3-dial combination for a 3/4\" cut:",
            "pins": [7, 5, 4],
            "max_val": 9,
        },
        "precision": {
            "prompt": "Cut the board to exactly 48 inches. Click when the tape measure hits 48!",
            "target": 48,
            "tolerance": 0.5,
        },
    },
    "welder": {
        "shift_sim": {
            "prompt": "Manage the welding shop — prioritize job orders:",
            "situations": ["Structural beam repair (critical)", "Custom gate fabrication (high)", "Tool rack welding (medium)", "Touch-up work (low)", "Shop cleanup (low)"],
            "optimal": ["Structural beam repair (critical)", "Custom gate fabrication (high)", "Tool rack welding (medium)", "Touch-up work (low)", "Shop cleanup (low)"],
        },
        "precision": {
            "prompt": "Set the wire feed speed to exactly 250 IPM. Click when the dial hits 250!",
            "target": 250,
            "tolerance": 10,
        },
    },
    "construction": {
        "speed_run": {
            "prompt": "Complete all site prep tasks before the inspector arrives! Click each task to finish it.",
            "tasks": ["Mark utility lines", "Set up safety barriers", "Grade the site", "Dig foundation trench", "Set form boards", "Pour concrete"],
        },
        "shift_sim": {
            "prompt": "Manage the construction site shift — prioritize:",
            "situations": ["Crane safety check (critical)", "Material delivery delay (high)", "Crew break schedule (medium)", "Tool inventory (low)", "Site cleanup (low)"],
            "optimal": ["Crane safety check (critical)", "Material delivery delay (high)", "Crew break schedule (medium)", "Tool inventory (low)", "Site cleanup (low)"],
        },
    },
    "roofer": {
        "sort": {
            "prompt": "Sort roofing materials by installation order:",
            "items": ["Drip edge (first)", "Underlayment (second)", "Starter strip (third)", "Shingles (fourth)", "Flashing (fifth)", "Ridge cap (last)"],
            "order": ["Drip edge (first)", "Underlayment (second)", "Starter strip (third)", "Shingles (fourth)", "Flashing (fifth)", "Ridge cap (last)"],
        },
        "pattern": {
            "prompt": "Shingle exposure pattern: 5\", 5\", 5\", 5\", ? (standard 3-tab)",
            "sequence": ["5\"", "5\"", "5\"", "5\"", "?"],
            "answer": "5\"",
        },
    },
    "painter": {
        "precision": {
            "prompt": "Cut in the edge to exactly 2mm from the ceiling line. Click when the brush is at 2mm!",
            "target": 2,
            "tolerance": 1,
        },
        "assembly": {
            "prompt": "Prep a room for painting — assemble steps in the correct order:",
            "parts": [("Move furniture", "Base"), ("Cover floors", "Move furniture"), ("Remove hardware", "Cover floors"), ("Patch holes", "Remove hardware"), ("Sand smooth", "Patch holes"), ("Tape edges", "Sand smooth")],
        },
    },
    "mason": {
        "shift_sim": {
            "prompt": "Manage the masonry job site — prioritize:",
            "situations": ["Mortar mixing wrong ratio (critical)", "Wall plumb check (high)", "Material delivery (medium)", "Tool maintenance (low)", "Site cleanup (low)"],
            "optimal": ["Mortar mixing wrong ratio (critical)", "Wall plumb check (high)", "Material delivery (medium)", "Tool maintenance (low)", "Site cleanup (low)"],
        },
        "precision": {
            "prompt": "Set the mortar joint to exactly 10mm thickness. Click when the gauge hits 10!",
            "target": 10,
            "tolerance": 1,
        },
    },
    "tiler": {
        "sequence": {
            "prompt": "Install floor tile in the correct order:",
            "items": ["Measure room center", "Snap chalk lines", "Mix thinset", "Comb mortar", "Lay first tile", "Continue outward", "Spacers between", "Grout joints", "Seal grout"],
            "order": ["Measure room center", "Snap chalk lines", "Mix thinset", "Comb mortar", "Lay first tile", "Continue outward", "Spacers between", "Grout joints", "Seal grout"],
        },
        "speed_run": {
            "prompt": "Lay all the tiles before the thinset dries! Click each section to tile it.",
            "tasks": ["Section A (entrance)", "Section B (center)", "Section C (left wall)", "Section D (right wall)", "Section E (back wall)"],
        },
    },
    "insulator": {
        "shift_sim": {
            "prompt": "Manage the insulation crew — prioritize:",
            "situations": ["Vapor barrier tear (critical)", "Cavity measurement (high)", "Material staging (medium)", "Tool check (low)", "Break schedule (low)"],
            "optimal": ["Vapor barrier tear (critical)", "Cavity measurement (high)", "Material staging (medium)", "Tool check (low)", "Break schedule (low)"],
        },
        "speed_run": {
            "prompt": "Insulate all the wall cavities before the drywall crew arrives! Click each cavity to fill it.",
            "tasks": ["Cavity 1 (living room)", "Cavity 2 (kitchen)", "Cavity 3 (bedroom)", "Cavity 4 (bathroom)", "Cavity 5 (hallway)"],
        },
    },
    "glazier": {
        "sequence": {
            "prompt": "Install a large window — follow the steps in order:",
            "items": ["Measure opening", "Order glass to size", "Remove old putty", "Clean frame", "Set glazing points", "Place glass", "Press into points", "Apply glazing compound", "Smooth and cure"],
            "order": ["Measure opening", "Order glass to size", "Remove old putty", "Clean frame", "Set glazing points", "Place glass", "Press into points", "Apply glazing compound", "Smooth and cure"],
        },
        "sort": {
            "prompt": "Sort glass panels by thickness for the project:",
            "items": ["3mm (interior partitions)", "6mm (standard windows)", "10mm (doors)", "12mm (storefront)", "19mm (safety barriers)"],
            "order": ["3mm (interior partitions)", "6mm (standard windows)", "10mm (doors)", "12mm (storefront)", "19mm (safety barriers)"],
        },
    },
    "hvac": {
        "speed_run": {
            "prompt": "Complete all service calls before end of shift! Click each call to finish it.",
            "tasks": ["AC not cooling (residential)", "Furnace no heat (commercial)", "Refrigerant recharge", "Duct cleaning", "Thermostat install", "Filter replacement"],
        },
        "precision": {
            "prompt": "Charge the system to exactly 75 PSI on the low side. Click when the gauge hits 75!",
            "target": 75,
            "tolerance": 2,
        },
    },
    "landscaper": {
        "shift_sim": {
            "prompt": "Manage the landscaping crew — prioritize:",
            "situations": ["Irrigation pipe burst (critical)", "Client walkthrough (high)", "Mulch delivery (medium)", "Tool sharpening (low)", "Truck refueling (low)"],
            "optimal": ["Irrigation pipe burst (critical)", "Client walkthrough (high)", "Mulch delivery (medium)", "Tool sharpening (low)", "Truck refueling (low)"],
        },
        "pattern": {
            "prompt": "Plant spacing pattern for a hedge: 3ft, 3ft, 3ft, 3ft, ?",
            "sequence": ["3ft", "3ft", "3ft", "3ft", "?"],
            "answer": "3ft",
        },
    },
    "foreman": {
        "assembly": {
            "prompt": "Organize the construction project — assemble phases in order:",
            "parts": [("Site prep", "Base"), ("Foundation", "Site prep"), ("Framing", "Foundation"), ("Roofing", "Framing"), ("Exterior", "Roofing"), ("Interior finish", "Exterior")],
        },
        "pattern": {
            "prompt": "Rebar spacing pattern: 16\", 16\", 16\", 16\", ? (standard grid)",
            "sequence": ["16\"", "16\"", "16\"", "16\"", "?"],
            "answer": "16\"",
        },
    },
    "surveyor": {
        "speed_run": {
            "prompt": "Complete all survey markers before the crew needs them! Click each point to survey it.",
            "tasks": ["Corner pin A", "Corner pin B", "Property line midpoint", "Elevation benchmark", "Setback marker"],
        },
        "sequence": {
            "prompt": "Conduct a property survey in the correct order:",
            "items": ["Research deed", "Locate existing monuments", "Set up total station", "Measure baseline", "Shoot property corners", "Calculate area", "Mark boundaries", "File survey plat"],
            "order": ["Research deed", "Locate existing monuments", "Set up total station", "Measure baseline", "Shoot property corners", "Calculate area", "Mark boundaries", "File survey plat"],
        },
    },
    "demolition": {
        "speed_run": {
            "prompt": "Clear all debris before the dump truck leaves! Click each pile to load it.",
            "tasks": ["Drywall pile", "Wood framing pile", "Concrete chunks", "Metal scraps", "Fixture pile", "Insulation pile"],
        },
        "precision": {
            "prompt": "Position the wrecking ball for a controlled swing. Click when the angle hits 45 degrees!",
            "target": 45,
            "tolerance": 3,
        },
    },
    "scaffolder": {
        "sort": {
            "prompt": "Sort scaffolding components by assembly order:",
            "items": ["Base plates (first)", "Standards (uprights)", "Ledgers (horizontal)", "Transoms (cross)", "Decking planks", "Guardrails (last)"],
            "order": ["Base plates (first)", "Standards (uprights)", "Ledgers (horizontal)", "Transoms (cross)", "Decking planks", "Guardrails (last)"],
        },
        "shift_sim": {
            "prompt": "Manage the scaffolding crew — prioritize:",
            "situations": ["Guardrail missing on level 3 (critical)", "Material hoist needed (high)", "Weather check (medium)", "Tool inventory (low)", "Break schedule (low)"],
            "optimal": ["Guardrail missing on level 3 (critical)", "Material hoist needed (high)", "Weather check (medium)", "Tool inventory (low)", "Break schedule (low)"],
        },
    },
    "floor_layer": {
        "sort": {
            "prompt": "Sort flooring materials by installation order:",
            "items": ["Underlayment (first)", "Vapor barrier (second)", "First row (third)", "Continue boards (fourth)", "Transition strips (fifth)", "Baseboards (last)"],
            "order": ["Underlayment (first)", "Vapor barrier (second)", "First row (third)", "Continue boards (fourth)", "Transition strips (fifth)", "Baseboards (last)"],
        },
        "assembly": {
            "prompt": "Install laminate flooring — assemble layers in the correct order:",
            "parts": [("Subfloor prep", "Base"), ("Underlayment", "Subfloor prep"), ("First plank row", "Underlayment"), ("Click-lock boards", "First plank row"), ("Transition pieces", "Click-lock boards"), ("Base shoe molding", "Transition pieces")],
        },
    },
    "locksmith": {
        "sort": {
            "prompt": "Sort the key blanks by type for the day's orders:",
            "items": ["House key (KW1)", "Car key (chip)", "Padlock key (1093)", "Safe key (double-bitted)", "Mailbox key (M1)"],
            "categories": ["Residential", "Automotive", "Commercial", "Security", "Residential"],
        },
        "shift_sim": {
            "prompt": "Manage the locksmith shop — prioritize calls:",
            "situations": ["Locked out of house — child inside (critical)", "Business lock change (high)", "Car key duplication (medium)", "Safe combination reset (medium)", "Mailbox lock (low)"],
            "optimal": ["Locked out of house — child inside (critical)", "Business lock change (high)", "Car key duplication (medium)", "Safe combination reset (medium)", "Mailbox lock (low)"],
        },
    },
    "heavy_equipment": {
        "sort": {
            "prompt": "Sort the equipment by job site need — heaviest earthmoving first:",
            "items": ["Bulldozer (rough grading)", "Excavator (trenching)", "Grader (fine leveling)", "Roller (compaction)", "Skid steer (finishing)"],
            "order": ["Bulldozer (rough grading)", "Excavator (trenching)", "Grader (fine leveling)", "Roller (compaction)", "Skid steer (finishing)"],
        },
        "pattern": {
            "prompt": "Bulldozer pass pattern: N→S, S→N, N→S, S→N, ?",
            "sequence": ["N→S", "S→N", "N→S", "S→N", "?"],
            "answer": "N→S",
        },
    },
    "steelworker": {
        "precision": {
            "prompt": "Align the steel beam to exactly 0 degrees plumb. Click when the level hits 0!",
            "target": 0,
            "tolerance": 1,
        },
        "speed_run": {
            "prompt": "Bolt all the beam connections before the crane moves! Click each connection to bolt it.",
            "tasks": ["Connection A-1", "Connection A-2", "Connection B-1", "Connection B-2", "Connection C-1", "Connection C-2"],
        },
    },
    "elevator_fix": {
        "pattern": {
            "prompt": "Floor call pattern: 1, 3, 5, 3, 1, 3, 5, ?",
            "sequence": ["1", "3", "5", "3", "1", "3", "5", "?"],
            "answer": "3",
        },
        "assembly": {
            "prompt": "Assemble the elevator system — install components in order:",
            "parts": [("Guide rails", "Shaft"), ("Car frame", "Guide rails"), ("Suspension cables", "Car frame"), ("Counterweight", "Suspension cables"), ("Drive motor", "Counterweight"), ("Control panel", "Drive motor")],
        },
    },
    "solar_installer": {
        "speed_run": {
            "prompt": "Install all the panels before sunset! Click each panel to mount it.",
            "tasks": ["Panel 1 (top left)", "Panel 2 (top right)", "Panel 3 (middle left)", "Panel 4 (middle right)", "Panel 5 (bottom left)", "Panel 6 (bottom right)"],
        },
        "combo_lock": {
            "prompt": "Set the inverter DIP switches — find the correct 3-switch combination:",
            "pins": [1, 0, 1],
            "max_val": 1,
        },
    },
    "contractor": {
        "speed_run": {
            "prompt": "Complete all project milestones before the deadline! Click each task to finish it.",
            "tasks": ["Permit approval", "Foundation inspection", "Framing inspection", "Rough-in plumbing", "Electrical rough-in", "Drywall install"],
        },
        "sequence": {
            "prompt": "Manage a construction project from start to finish:",
            "items": ["Design and plans", "Permits and approvals", "Site preparation", "Foundation", "Framing", "Roofing", "MEP rough-in", "Insulation and drywall", "Interior finish", "Final inspection"],
            "order": ["Design and plans", "Permits and approvals", "Site preparation", "Foundation", "Framing", "Roofing", "MEP rough-in", "Insulation and drywall", "Interior finish", "Final inspection"],
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # MEDICAL & SCIENCE — 25 jobs
    # ═══════════════════════════════════════════════════════════════

    "doctor": {
        "match_pairs": {
            "prompt": "Match each symptom cluster to its likely diagnosis:",
            "pairs": [("Chest pain + left arm", "Cardiac event"), ("Sudden weakness + slurred speech", "Stroke"), ("Abdominal RLQ pain + fever", "Appendicitis"), ("Thirst + frequent urination", "Diabetes")],
        },
        "categorize": {
            "prompt": "Categorize each medication by its drug class:",
            "items": ["Lisinopril (blood pressure)", "Metformin (diabetes)", "Atorvastatin (cholesterol)", "Sertraline (antidepressant)", "Amoxicillin (antibiotic)"],
            "categories": ["ACE inhibitor", "Biguanide", "Statin", "SSRI", "Penicillin"],
        },
    },
    "nurse": {
        "diagnosis": {
            "prompt": "Patient: sudden onset fever, chills, productive cough, rapid breathing. Most likely?",
            "options": ["Common cold", "Pneumonia", "Bronchitis", "Asthma flare"],
            "correct": "Pneumonia",
            "reasoning": "Fever + productive cough + rapid breathing suggests pneumonia over simple bronchitis.",
        },
        "spot_error": {
            "prompt": "Find the error in this medication administration record:",
            "correct_sequence": ["Verify patient ID", "Check allergies", "Confirm dose", "Administer medication", "Document time", "Monitor for reaction"],
            "presented_sequence": ["Verify patient ID", "Confirm dose", "Check allergies", "Administer medication", "Document time", "Monitor for reaction"],
        },
    },
    "paramedic": {
        "sequence": {
            "prompt": "Follow the trauma assessment sequence in order:",
            "items": ["Scene safety", "Primary survey (ABC)", "C-spine stabilization", "Secondary survey", "Package for transport", "Load and go"],
            "order": ["Scene safety", "Primary survey (ABC)", "C-spine stabilization", "Secondary survey", "Package for transport", "Load and go"],
        },
        "spot_error": {
            "prompt": "Find the error in this CPR sequence:",
            "correct_sequence": ["Check responsiveness", "Call 911", "Open airway", "Give 30 compressions", "Give 2 breaths", "Continue cycles"],
            "presented_sequence": ["Check responsiveness", "Open airway", "Call 911", "Give 30 compressions", "Give 2 breaths", "Continue cycles"],
        },
    },
    "pharmacist": {
        "triage": {
            "prompt": "Triage these pharmacy patients — assign priority (1=most urgent):",
            "patients": ["Patient with severe allergic reaction", "Patient picking up refills", "Patient asking about side effects", "Patient with new prescription", "Patient browsing vitamins"],
            "optimal": ["Patient with severe allergic reaction", "Patient with new prescription", "Patient asking about side effects", "Patient picking up refills", "Patient browsing vitamins"],
        },
        "categorize": {
            "prompt": "Categorize each medication by its schedule:",
            "items": ["Morphine (Schedule II)", "Codeine (Schedule III)", "Xanax (Schedule IV)", "Cough syrup w/ codeine (Schedule V)", "Ibuprofen (OTC)"],
            "categories": ["Schedule II", "Schedule III", "Schedule IV", "Schedule V", "OTC"],
        },
    },
    "dentist": {
        "match_pairs": {
            "prompt": "Match each dental procedure to its correct instrument:",
            "pairs": [("Cavity filling", "Composite resin + curing light"), ("Root canal", "Endodontic files"), ("Tooth extraction", "Forceps + elevator"), ("Cleaning", "Ultrasonic scaler")],
        },
        "categorize": {
            "prompt": "Categorize each dental issue by urgency:",
            "items": ["Avulsed tooth (knocked out)", "Lost filling", "Routine cleaning", "Mild sensitivity", "Abscess with swelling"],
            "categories": ["Emergency", "Semi-urgent", "Routine", "Non-urgent", "Emergency"],
        },
    },
    "surgeon": {
        "spot_error": {
            "prompt": "Find the error in this pre-op checklist:",
            "correct_sequence": ["Verify patient identity", "Confirm procedure", "Mark surgical site", "Consent signed", "Anesthesia check", "Time out", "Incision"],
            "presented_sequence": ["Verify patient identity", "Confirm procedure", "Consent signed", "Mark surgical site", "Anesthesia check", "Time out", "Incision"],
        },
        "memory": {
            "prompt": "Remember the instrument count: 4 forceps, 6 clamps, 3 scissors, 2 needle holders, 8 retractors",
            "sequence": ["4 forceps", "6 clamps", "3 scissors", "2 needle holders", "8 retractors"],
        },
    },
    "vet": {
        "match_pairs": {
            "prompt": "Match each animal species to its common health screening:",
            "pairs": [("Dog", "Heartworm test"), ("Cat", "FIV/FeLV test"), ("Horse", "Coggins test"), ("Bird", "Psittacosis test")],
        },
        "spot_error": {
            "prompt": "Find the error in this vaccination schedule for a puppy:",
            "correct_sequence": ["6-8 weeks: DHPP", "10-12 weeks: DHPP", "14-16 weeks: DHPP + Rabies", "12 months: Boosters"],
            "presented_sequence": ["6-8 weeks: DHPP", "14-16 weeks: DHPP + Rabies", "10-12 weeks: DHPP", "12 months: Boosters"],
        },
    },
    "therapist": {
        "memory": {
            "prompt": "Remember the client's key issues: Anxiety, work stress, relationship conflict, sleep problems",
            "sequence": ["Anxiety", "Work stress", "Relationship conflict", "Sleep problems"],
        },
        "match_pairs": {
            "prompt": "Match each therapeutic approach to its primary technique:",
            "pairs": [("CBT", "Cognitive restructuring"), ("Psychodynamic", "Free association"), ("DBT", "Mindfulness + distress tolerance"), ("EMDR", "Bilateral stimulation")],
        },
    },
    "radiologist": {
        "triage": {
            "prompt": "Triage these imaging requests — assign priority (1=most urgent):",
            "patients": ["CT head — suspected stroke", "MRI knee — chronic pain", "X-ray chest — routine", "Ultrasound — pregnancy scan", "Mammogram — screening"],
            "optimal": ["CT head — suspected stroke", "Ultrasound — pregnancy scan", "X-ray chest — routine", "MRI knee — chronic pain", "Mammogram — screening"],
        },
        "diagnosis": {
            "prompt": "X-ray shows: irregular mass in right upper lobe, spiculated margins. Most likely?",
            "options": ["Pneumonia", "Lung cancer", "Tuberculosis", "Benign nodule"],
            "correct": "Lung cancer",
            "reasoning": "Spiculated mass in upper lobe is highly suspicious for malignancy.",
        },
    },
    "lab_tech": {
        "pattern": {
            "prompt": "Dilution series: 1:2, 1:4, 1:8, 1:16, ?",
            "sequence": ["1:2", "1:4", "1:8", "1:16", "?"],
            "answer": "1:32",
        },
        "multi_stage": {
            "prompt": "Process a blood sample across 3 lab stages:",
            "stages": [
                {"type": "quick_pick", "prompt": "Tube has lavender top. What test?", "options": ["CBC (EDTA tube)", "Chemistry (green top)", "Coagulation (blue top)", "Blood bank (yellow top)"], "correct": "CBC (EDTA tube)"},
                {"type": "sequence", "prompt": "Run the analyzer in order:", "items": ["Load sample", "Select test panel", "Calibrate", "Run analysis", "Review results", "Flag abnormals"], "order": ["Load sample", "Select test panel", "Calibrate", "Run analysis", "Review results", "Flag abnormals"]},
                {"type": "quick_pick", "prompt": "Hemoglobin reads 7.2 g/dL. Flag?", "options": ["Normal", "Critical low", "Borderline", "Retest needed"], "correct": "Critical low"},
            ],
        },
    },
    "research_sci": {
        "match_pairs": {
            "prompt": "Match each lab equipment to its function:",
            "pairs": [("Centrifuge", "Separate by density"), ("Spectrophotometer", "Measure absorbance"), ("PCR machine", "Amplify DNA"), ("Electrophoresis", "Separate by size")],
        },
        "triage": {
            "prompt": "Triage these experiments — assign priority (1=most urgent):",
            "patients": ["Time-sensitive cell culture", "Equipment calibration", "Literature review", "Grant deadline experiment", "Routine maintenance"],
            "optimal": ["Time-sensitive cell culture", "Grant deadline experiment", "Equipment calibration", "Literature review", "Routine maintenance"],
        },
    },
    "biologist": {
        "pattern": {
            "prompt": "Cell division stages: Prophase, Metaphase, Anaphase, Telophase, ?",
            "sequence": ["Prophase", "Metaphase", "Anaphase", "Telophase", "?"],
            "answer": "Cytokinesis",
        },
        "spot_error": {
            "prompt": "Find the error in this DNA replication sequence:",
            "correct_sequence": ["Unzip double helix", "RNA primer binds", "DNA polymerase adds bases", "Leading strand continuous", "Lagging strand fragments", "Ligase seals gaps"],
            "presented_sequence": ["Unzip double helix", "DNA polymerase adds bases", "RNA primer binds", "Leading strand continuous", "Lagging strand fragments", "Ligase seals gaps"],
        },
    },
    "chemist": {
        "spot_error": {
            "prompt": "Find the error in this titration procedure:",
            "correct_sequence": ["Fill burette", "Add indicator to analyte", "Slowly add titrant", "Swirl flask", "Color change at endpoint", "Record volume"],
            "presented_sequence": ["Fill burette", "Add indicator to analyte", "Swirl flask", "Slowly add titrant", "Color change at endpoint", "Record volume"],
        },
        "match_pairs": {
            "prompt": "Match each element to its atomic number:",
            "pairs": [("Hydrogen", "1"), ("Carbon", "6"), ("Oxygen", "8"), ("Gold", "79")],
        },
    },
    "physicist": {
        "spot_error": {
            "prompt": "Find the error in this physics calculation chain:",
            "correct_sequence": ["Given: v₀ = 0, a = 9.8 m/s², t = 3s", "v = v₀ + at = 0 + 9.8(3) = 29.4 m/s", "d = ½at² = ½(9.8)(9) = 44.1 m", "KE = ½mv² = ½(2)(29.4²) = 864.4 J"],
            "presented_sequence": ["Given: v₀ = 0, a = 9.8 m/s², t = 3s", "v = v₀ + at = 0 + 9.8(3) = 29.4 m/s", "d = ½at² = ½(9.8)(9) = 44.1 m", "KE = ½mv² = ½(2)(29.4) = 29.4 J"],
        },
        "pattern": {
            "prompt": "Quantum energy levels: E₁, E₂=4E₁, E₃=9E₁, E₄=16E₁, E₅=?",
            "sequence": ["E₁", "4E₁", "9E₁", "16E₁", "?"],
            "answer": "25E₁",
        },
    },
    "astronomer": {
        "sequence": {
            "prompt": "Conduct an observation session in the correct order:",
            "items": ["Calibrate telescope", "Find reference star", "Align tracking", "Locate target", "Take exposures", "Stack images", "Analyze data"],
            "order": ["Calibrate telescope", "Find reference star", "Align tracking", "Locate target", "Take exposures", "Stack images", "Analyze data"],
        },
        "memory": {
            "prompt": "Remember the Messier objects observed tonight: M31 (Andromeda), M42 (Orion Nebula), M45 (Pleiades), M51 (Whirlpool)",
            "sequence": ["M31 (Andromeda)", "M42 (Orion Nebula)", "M45 (Pleiades)", "M51 (Whirlpool)"],
        },
    },
    "geneticist": {
        "spot_error": {
            "prompt": "Find the error in this PCR protocol:",
            "correct_sequence": ["Initial denaturation 95°C", "Denature 95°C 30s", "Anneal 55°C 30s", "Extend 72°C 60s", "Final extension 72°C", "Hold 4°C"],
            "presented_sequence": ["Initial denaturation 95°C", "Anneal 55°C 30s", "Denature 95°C 30s", "Extend 72°C 60s", "Final extension 72°C", "Hold 4°C"],
        },
        "memory": {
            "prompt": "Remember the DNA bases in your sample sequence: ATCG, GCTA, CGAT, TAGC",
            "sequence": ["ATCG", "GCTA", "CGAT", "TAGC"],
        },
    },
    "neurosurgeon": {
        "match_pairs": {
            "prompt": "Match each brain region to its primary function:",
            "pairs": [("Frontal lobe", "Decision making"), ("Temporal lobe", "Memory and hearing"), ("Occipital lobe", "Vision"), ("Cerebellum", "Motor coordination")],
        },
        "memory": {
            "prompt": "Remember the surgical plan: Expose dura, Map motor cortex, Resect tumor, Preserve vessels, Close in layers",
            "sequence": ["Expose dura", "Map motor cortex", "Resect tumor", "Preserve vessels", "Close in layers"],
        },
    },
    "cardiologist": {
        "match_pairs": {
            "prompt": "Match each ECG finding to its diagnosis:",
            "pairs": [("ST elevation", "Myocardial infarction"), ("Wide QRS", "Bundle branch block"), ("Flat T waves", "Hypokalemia"), ("A-fib", "Irregular rhythm")],
        },
        "pattern": {
            "prompt": "Blood pressure pattern: 120/80, 130/85, 140/90, 150/95, ?",
            "sequence": ["120/80", "130/85", "140/90", "150/95", "?"],
            "answer": "160/100",
        },
    },
    "pediatrician": {
        "spot_error": {
            "prompt": "Find the error in this immunization schedule:",
            "correct_sequence": ["Birth: HepB", "2 months: DTaP+IPV+Hib+PCV", "6 months: DTaP+IPV+Hib+PCV+Flu", "12 months: MMR+Varicella"],
            "presented_sequence": ["Birth: HepB", "6 months: DTaP+IPV+Hib+PCV", "2 months: DTaP+IPV+Hib+PCV", "12 months: MMR+Varicella"],
        },
        "triage": {
            "prompt": "Triage these pediatric patients — assign priority (1=most urgent):",
            "patients": ["Infant with 104°F fever", "Toddler with scraped knee", "Child for wellness check", "Child with persistent cough", "Teen with sports physical"],
            "optimal": ["Infant with 104°F fever", "Child with persistent cough", "Toddler with scraped knee", "Child for wellness check", "Teen with sports physical"],
        },
    },
    "optometrist": {
        "triage": {
            "prompt": "Triage these eye patients — assign priority (1=most urgent):",
            "patients": ["Sudden vision loss (emergency)", "Eye pain and redness", "Routine eye exam", "New glasses fitting", "Contact lens follow-up"],
            "optimal": ["Sudden vision loss (emergency)", "Eye pain and redness", "Routine eye exam", "Contact lens follow-up", "New glasses fitting"],
        },
        "memory": {
            "prompt": "Remember the lens prescriptions: Patient A -2.50, Patient B -1.00, Patient C +2.00 reading, Patient D -4.25 astigmatism",
            "sequence": ["-2.50", "-1.00", "+2.00 reading", "-4.25 astigmatism"],
        },
    },
    "physical_ther": {
        "categorize": {
            "prompt": "Categorize each exercise by its rehabilitation phase:",
            "items": ["Ice therapy (acute)", "Range of motion (early)", "Strengthening (mid)", "Balance training (mid)", "Sport-specific (late)"],
            "categories": ["Acute phase", "Early phase", "Mid phase", "Mid phase", "Late phase"],
        },
        "memory": {
            "prompt": "Remember today's patient schedule: 9am knee rehab, 10am post-surgery shoulder, 11am stroke patient, 2am back pain, 3am ankle sprain",
            "sequence": ["9am knee rehab", "10am post-surgery shoulder", "11am stroke patient", "2am back pain", "3am ankle sprain"],
        },
    },
    "med_researcher": {
        "memory": {
            "prompt": "Remember the trial data points: Group A 42% response, Group B 38% response, Group C 51% response, Control 12% response",
            "sequence": ["Group A 42%", "Group B 38%", "Group C 51%", "Control 12%"],
        },
        "triage": {
            "prompt": "Triage these research tasks — assign priority (1=most urgent):",
            "patients": ["IRB deadline tomorrow", "Lab reagent ordering", "Data analysis", "Conference abstract", "Literature review"],
            "optimal": ["IRB deadline tomorrow", "Data analysis", "Lab reagent ordering", "Conference abstract", "Literature review"],
        },
    },
    "epidemiologist": {
        "memory": {
            "prompt": "Remember the outbreak data: City A 45 cases, City B 12 cases, City C 89 cases, City D 3 cases",
            "sequence": ["City A 45 cases", "City B 12 cases", "City C 89 cases", "City D 3 cases"],
        },
        "match_pairs": {
            "prompt": "Match each disease to its transmission route:",
            "pairs": [("Cholera", "Waterborne"), ("Tuberculosis", "Airborne"), ("Malaria", "Vector-borne"), ("Hepatitis A", "Fecal-oral")],
        },
    },
    "toxicologist": {
        "diagnosis": {
            "prompt": "Patient presents with: pinpoint pupils, respiratory depression, altered consciousness. Diagnosis?",
            "options": ["Opioid overdose", "Alcohol poisoning", "Carbon monoxide", "Organophosphate"],
            "correct": "Opioid overdose",
            "reasoning": "Pinpoint pupils + respiratory depression is classic opioid toxicity (CNS depression triad).",
        },
        "sequence": {
            "prompt": "Conduct a toxicology screening in the correct order:",
            "items": ["Collect blood sample", "Collect urine sample", "Run immunoassay screen", "Confirm with GC-MS", "Quantify levels", "Interpret results", "Report findings"],
            "order": ["Collect blood sample", "Collect urine sample", "Run immunoassay screen", "Confirm with GC-MS", "Quantify levels", "Interpret results", "Report findings"],
        },
    },
    "astronaut": {
        "sequence": {
            "prompt": "Conduct a spacewalk (EVA) in the correct order:",
            "items": ["Pre-breathe oxygen", "Suit pressure check", "Depressurize airlock", "Open hatch", "Exit station", "Translate to worksite", "Complete task", "Return to airlock", "Repressurize"],
            "order": ["Pre-breathe oxygen", "Suit pressure check", "Depressurize airlock", "Open hatch", "Exit station", "Translate to worksite", "Complete task", "Return to airlock", "Repressurize"],
        },
        "match_pairs": {
            "prompt": "Match each space station module to its function:",
            "pairs": [("Destiny", "US laboratory"), ("Columbus", "European lab"), ("Kibo", "Japanese lab"), ("Zvezda", "Russian service module")],
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # TECH & IT — 25 jobs
    # ═══════════════════════════════════════════════════════════════

    "programmer": {
        "assembly": {
            "prompt": "Build a Python application — assemble components in order:",
            "parts": [("Virtual environment", "Base"), ("Requirements file", "Virtual environment"), ("Core modules", "Requirements file"), ("API layer", "Core modules"), ("Tests", "API layer"), ("CI/CD", "Tests")],
        },
        "fill_blank": {
            "prompt": "Complete the code: 'def reverse(s): return s[__:] + s[:__]'",
            "answer": "-1, -1",
            "context": "s[-1:] gets last char, s[:-1] gets everything before it — but for full reverse use slicing s[::-1].",
        },
    },
    "it_support": {
        "sequence": {
            "prompt": "Troubleshoot a network issue — follow the steps in order:",
            "items": ["Check physical connection", "Verify IP address", "Ping gateway", "Check DNS resolution", "Test external connectivity", "Document resolution"],
            "order": ["Check physical connection", "Verify IP address", "Ping gateway", "Check DNS resolution", "Test external connectivity", "Document resolution"],
        },
        "fill_blank": {
            "prompt": "Complete the command: 'ipconfig /____' to release and renew DHCP lease",
            "answer": "renew",
            "context": "ipconfig /release then ipconfig /renew refreshes the DHCP lease.",
        },
    },
    "web_dev": {
        "spot_error": {
            "prompt": "Find the bug in this HTML:",
            "correct_code": "<div class=\"container\">\n  <ul>\n    <li>Item 1</li>\n    <li>Item 2</li>\n  </ul>\n</div>",
            "buggy_code": "<div class=\"container\">\n  <ul>\n    <li>Item 1\n    <li>Item 2</li>\n  </ul>\n</div>",
        },
        "pattern": {
            "prompt": "CSS specificity: inline=1000, ID=100, class=10, element=1. What is #nav .item a?",
            "sequence": ["1000", "100", "10", "1"],
            "answer": "111",
        },
    },
    "data_analyst": {
        "fill_blank": {
            "prompt": "Complete the SQL: 'SELECT COUNT(*) FROM users WHERE created_at >= ____' for users this month",
            "answer": "DATE('now', 'start of month')",
            "context": "SQLite syntax for first day of current month.",
        },
        "math": {
            "prompt": "Calculate the median of: 12, 18, 25, 30, 45, 50, 60",
            "answer": 30,
            "formula": "Middle value of 7 sorted numbers = 4th value = 30",
        },
    },
    "sysadmin": {
        "fill_blank": {
            "prompt": "Complete the command: 'systemctl ____ nginx' to restart the web server",
            "answer": "restart",
            "context": "systemctl restart nginx restarts the nginx service.",
        },
        "shift_sim": {
            "prompt": "Manage the server room — prioritize alerts:",
            "situations": ["Production database down (critical)", "Disk space 90% on web server (high)", "SSL cert expiring in 3 days (medium)", "Update test environment (low)", "Organize cable closet (low)"],
            "optimal": ["Production database down (critical)", "Disk space 90% on web server (high)", "SSL cert expiring in 3 days (medium)", "Update test environment (low)", "Organize cable closet (low)"],
        },
    },
    "ux_designer": {
        "fill_blank": {
            "prompt": "Complete the principle: 'Don't make me ____' — Steve Krug's usability rule",
            "answer": "think",
            "context": "Users should be able to understand a page immediately without thinking.",
        },
        "pattern": {
            "prompt": "Fitts's Law: target acquisition time depends on distance and __?",
            "sequence": ["Distance", "Size", "?"],
            "answer": "Size",
        },
    },
    "game_dev": {
        "fill_blank": {
            "prompt": "Complete the Unity code: 'void Update() { if (Input.GetKey(KeyCode.__)) Jump(); }'",
            "answer": "Space",
            "context": "KeyCode.Space is the standard jump key in Unity.",
        },
        "pattern": {
            "prompt": "Game loop stages: Input → Update → __ → Render → Display",
            "sequence": ["Input", "Update", "?", "Render", "Display"],
            "answer": "Physics",
        },
    },
    "data_scientist": {
        "fill_blank": {
            "prompt": "Complete the pandas code: 'df.____()' to drop rows with missing values",
            "answer": "dropna",
            "context": "df.dropna() removes rows containing NaN values.",
        },
        "pattern": {
            "prompt": "Overfitting indicators: Train acc 99%, Val acc 65%, Train loss 0.01, Val loss 2.5. Diagnosis?",
            "sequence": ["99%", "65%", "0.01", "2.5"],
            "answer": "Overfitting",
        },
    },
    "devops": {
        "fill_blank": {
            "prompt": "Complete the Docker command: 'docker ____ -d --name web -p 80:80 nginx'",
            "answer": "run",
            "context": "docker run starts a container from an image.",
        },
        "combo_lock": {
            "prompt": "Set the Kubernetes deployment config — find the correct 3-value replica/limit/ratio:",
            "pins": [3, 2, 1],
            "max_val": 5,
        },
    },
    "security_analyst": {
        "fill_blank": {
            "prompt": "Complete the command: 'nmap -s____ target.com' for a SYN stealth scan",
            "answer": "S",
            "context": "nmap -sS performs a SYN scan (half-open scan).",
        },
        "pattern": {
            "prompt": "Attack pattern: Recon → Scan → Exploit → __ → Cover tracks",
            "sequence": ["Recon", "Scan", "Exploit", "?", "Cover tracks"],
            "answer": "Maintain access",
        },
    },
    "mobile_dev": {
        "fill_blank": {
            "prompt": "Complete the Swift code: 'let label = UILabel(); label.____ = \"Hello\"'",
            "answer": "text",
            "context": "UILabel.text sets the displayed string.",
        },
        "pattern": {
            "prompt": "App lifecycle: Launching → Active → Inactive → __ → Terminated",
            "sequence": ["Launching", "Active", "Inactive", "?", "Terminated"],
            "answer": "Background",
        },
    },
    "ai_engineer": {
        "fill_blank": {
            "prompt": "Complete the PyTorch code: 'optimizer.____()' to clear gradients before backward pass",
            "answer": "zero_grad",
            "context": "optimizer.zero_grad() clears accumulated gradients.",
        },
        "math": {
            "prompt": "Neural network layer: 784 inputs, 128 hidden, 10 outputs. Total parameters (with biases)?",
            "answer": 101770,
            "formula": "(784×128 + 128) + (128×10 + 10) = 100352 + 128 + 1280 + 10 = 101770",
        },
    },
    "cloud_arch": {
        "fill_blank": {
            "prompt": "Complete the Terraform: 'resource \"aws_s3_bucket\" \"____\" { bucket = \"my-app-data\" }'",
            "answer": "data",
            "context": "The resource name is an identifier within Terraform.",
        },
        "shift_sim": {
            "prompt": "Manage cloud infrastructure — prioritize alerts:",
            "situations": ["Production RDS failover needed (critical)", "Auto-scaling not triggering (high)", "CDN cache miss rate high (medium)", "Dev environment cleanup (low)", "Documentation update (low)"],
            "optimal": ["Production RDS failover needed (critical)", "Auto-scaling not triggering (high)", "CDN cache miss rate high (medium)", "Dev environment cleanup (low)", "Documentation update (low)"],
        },
    },
    "blockchain_dev": {
        "fill_blank": {
            "prompt": "Complete the Solidity: 'function transfer(address to, uint amount) public returns (____)'",
            "answer": "bool",
            "context": "ERC-20 transfer returns a boolean success value.",
        },
        "math": {
            "prompt": "Gas calculation: 21,000 base gas × 20 Gwei gas price = ? Gwei",
            "answer": 420000,
            "formula": "21000 × 20 = 420,000 Gwei = 0.00042 ETH",
        },
    },
    "qa_tester": {
        "fill_blank": {
            "prompt": "Complete the test: 'assertEqual(add(2, 3), __)' for an addition function",
            "answer": "5",
            "context": "2 + 3 = 5, the expected result.",
        },
        "pattern": {
            "prompt": "Test pyramid: many __ tests, fewer integration, fewest E2E",
            "sequence": ["Many", "Fewer", "Fewest"],
            "answer": "Unit",
        },
    },
    "tech_writer": {
        "fill_blank": {
            "prompt": "Complete the API doc: 'GET /api/users — Returns a ____ of all users'",
            "answer": "list",
            "context": "A GET request to /users typically returns a JSON array (list).",
        },
        "pattern": {
            "prompt": "Documentation structure: Overview → Quick Start → __ → API Reference → FAQ",
            "sequence": ["Overview", "Quick Start", "?", "API Reference", "FAQ"],
            "answer": "Guides",
        },
    },
    "product_manager": {
        "fill_blank": {
            "prompt": "Complete the user story: 'As a ___, I want to ___, so that ___'",
            "answer": "user, action, benefit",
            "context": "Standard user story format: persona, action, value.",
        },
        "pattern": {
            "prompt": "Sprint velocity: 34, 38, 42, 40, 44, ? (trending up ±2)",
            "sequence": ["34", "38", "42", "40", "44", "?"],
            "answer": "43",
        },
    },
    "db_admin": {
        "fill_blank": {
            "prompt": "Complete the SQL: 'CREATE INDEX idx_name ON users (____)' to index the email column",
            "answer": "email",
            "context": "CREATE INDEX idx_name ON users (email) creates an index on the email column.",
        },
        "combo_lock": {
            "prompt": "Set the database config — find the correct 3-pool setting (max_conn/buffer/cache):",
            "pins": [100, 256, 64],
            "max_val": 9,
        },
    },
    "network_eng": {
        "fill_blank": {
            "prompt": "Complete the command: 'ping -____ 5 8.8.8.8' to send exactly 5 ping packets",
            "answer": "c",
            "context": "ping -c 5 sends 5 packets then stops.",
        },
        "pattern": {
            "prompt": "OSI model layers: Physical, Data Link, Network, Transport, Session, __, Application",
            "sequence": ["Physical", "Data Link", "Network", "Transport", "Session", "?", "Application"],
            "answer": "Presentation",
        },
    },
    "frontend_dev": {
        "fill_blank": {
            "prompt": "Complete the React code: 'const [count, setCount] = ____(0)'",
            "answer": "useState",
            "context": "useState(0) initializes state with value 0.",
        },
        "pattern": {
            "prompt": "React lifecycle: Mount → Update → __ → Unmount",
            "sequence": ["Mount", "Update", "?", "Unmount"],
            "answer": "Re-render",
        },
    },
    "backend_dev": {
        "fill_blank": {
            "prompt": "Complete the Express code: 'app.____('/api/users', userRouter)'",
            "answer": "use",
            "context": "app.use('/api/users', userRouter) mounts middleware at the path.",
        },
        "pattern": {
            "prompt": "HTTP status pattern: 2xx=success, 3xx=redirect, 4xx=__, 5xx=server error",
            "sequence": ["2xx", "3xx", "4xx", "5xx"],
            "answer": "Client error",
        },
    },
    "pentester": {
        "fill_blank": {
            "prompt": "Complete the Metasploit command: 'use exploit/windows/smb/____'",
            "answer": "ms17_010_eternalblue",
            "context": "MS17-010 is the EternalBlue exploit targeting SMBv1.",
        },
        "combo_lock": {
            "prompt": "Crack the WPA2 handshake — find the correct 3-octet key prefix:",
            "pins": [8, 4, 2],
            "max_val": 9,
        },
    },
    "ml_engineer": {
        "fill_blank": {
            "prompt": "Complete the sklearn code: 'from sklearn.model_selection import ____'",
            "answer": "train_test_split",
            "context": "train_test_split splits data into training and testing sets.",
        },
        "math": {
            "prompt": "Model precision: TP=85, FP=15. Precision = TP / (TP + FP) = ?",
            "answer": 0.85,
            "formula": "85 / (85 + 15) = 85/100 = 0.85",
        },
    },
    "cto": {
        "fill_blank": {
            "prompt": "Complete: ' Conway's Law: organizations which design systems are constrained to produce designs which are copies of their ____ structures'",
            "answer": "communication",
            "context": "Conway's Law states system design mirrors org communication structure.",
        },
        "pattern": {
            "prompt": "Tech debt pattern: Sprint 1 (0 debt), Sprint 5 (low), Sprint 10 (medium), Sprint 15 (high), Sprint 20 (?)",
            "sequence": ["0", "low", "medium", "high", "?"],
            "answer": "Critical",
        },
    },
    "hacker": {
        "fill_blank": {
            "prompt": "Complete the SQL injection: 'admin' --' OR 1=1 --____",
            "answer": "",
            "context": "The -- comments out the rest of the query. The injection is: ' OR 1=1 --",
        },
        "pattern": {
            "prompt": "Privilege escalation: user → sudo → root → ____ (kernel exploit)",
            "sequence": ["user", "sudo", "root", "?"],
            "answer": "kernel",
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # BUSINESS & FINANCE — 25 jobs
    # ═══════════════════════════════════════════════════════════════

    "ceo": {
        "quick_pick": {
            "prompt": "Board wants 20% growth but market is contracting. Best strategy?",
            "options": ["Cut R&D to boost margins", "Acquire competitor in adjacent market", "Lay off 30% of staff", "Ignore the board"],
            "correct": "Acquire competitor in adjacent market",
        },
        "match_pairs": {
            "prompt": "Match each business metric to its correct category:",
            "pairs": [("EBITDA", "Profitability"), ("Customer Acquisition Cost", "Growth"), ("Net Promoter Score", "Customer satisfaction"), ("Employee Turnover", "HR")],
        },
    },
    "bank_teller": {
        "match_pairs": {
            "prompt": "Match each transaction type to its correct process:",
            "pairs": [("Cash deposit", "Count + credit account"), ("Check cashing", "Verify ID + clear check"), ("Wire transfer", "Verify + SWIFT routing"), ("Currency exchange", "Rate + spread calculation")],
        },
        "sequence": {
            "prompt": "Process a large cash withdrawal in the correct order:",
            "items": ["Verify customer ID", "Check account balance", "Count cash", "Record transaction", "Get signature", "Dispense cash", "Thank customer"],
            "order": ["Verify customer ID", "Check account balance", "Record transaction", "Get signature", "Count cash", "Dispense cash", "Thank customer"],
        },
    },
    "accountant": {
        "spot_error": {
            "prompt": "Find the error in this balance sheet:",
            "correct_sequence": ["Assets: $1,200,000", "Liabilities: $800,000", "Equity: $400,000", "Check: A = L + E → 1,200,000 = 800,000 + 400,000 ✓"],
            "presented_sequence": ["Assets: $1,200,000", "Liabilities: $750,000", "Equity: $400,000", "Check: A = L + E → 1,200,000 = 750,000 + 400,000 ✓"],
        },
        "pattern": {
            "prompt": "Depreciation pattern (straight-line): Year 1 $10k, Year 2 $10k, Year 3 $10k, Year 4 ?",
            "sequence": ["$10k", "$10k", "$10k", "?"],
            "answer": "$10k",
        },
    },
    "sales_rep": {
        "shift_sim": {
            "prompt": "Manage your sales pipeline — prioritize in order:",
            "situations": ["Hot lead ready to sign (critical)", "Demo call with prospect (high)", "Follow-up emails (medium)", "Update CRM (low)", "Team meeting prep (low)"],
            "optimal": ["Hot lead ready to sign (critical)", "Demo call with prospect (high)", "Follow-up emails (medium)", "Update CRM (low)", "Team meeting prep (low)"],
        },
        "quick_pick": {
            "prompt": "Client says 'I need to think about it.' Best response?",
            "options": ["Push harder for the sale", "Ask what concerns they have", "Give them a deadline", "Say 'no problem' and leave"],
            "correct": "Ask what concerns they have",
        },
    },
    "real_estate": {
        "match_pairs": {
            "prompt": "Match each property type to its typical financing method:",
            "pairs": [("Single family home", "Conventional mortgage"), ("Commercial building", "Commercial loan"), ("Apartment complex", "Multifamily loan"), ("Raw land", "Land loan")],
        },
        "shift_sim": {
            "prompt": "Manage your real estate day — prioritize:",
            "situations": ["Closing in 2 hours — docs not ready (critical)", "New listing photoshoot (high)", "Open house setup (medium)", "MLS listing update (low)", "Desk organization (low)"],
            "optimal": ["Closing in 2 hours — docs not ready (critical)", "New listing photoshoot (high)", "Open house setup (medium)", "MLS listing update (low)", "Desk organization (low)"],
        },
    },
    "stockbroker": {
        "quick_pick": {
            "prompt": "Client wants to go all-in on one stock. Best advice?",
            "options": ["Go for it", "Recommend diversification", "Refuse the trade", "Suggest index funds instead"],
            "correct": "Recommend diversification",
        },
        "match_pairs": {
            "prompt": "Match each order type to its execution behavior:",
            "pairs": [("Market order", "Execute immediately at best price"), ("Limit order", "Execute only at specified price or better"), ("Stop order", "Trigger at specified price, then market"), ("Stop-limit", "Trigger at price, then limit order")],
        },
    },
    "financial_adv": {
        "quick_pick": {
            "prompt": "Client is 65, retiring in 1 year, has $500k saved. Priority?",
            "options": ["Aggressive growth stocks", "Preserve capital + income", "Crypto investment", "Real estate speculation"],
            "correct": "Preserve capital + income",
        },
        "pattern": {
            "prompt": "Rule of 72: 72 / 6% return = ? years to double",
            "sequence": ["72", "6%", "?"],
            "answer": "12",
        },
    },
    "manager": {
        "quick_pick": {
            "prompt": "Two team members are in conflict. First step?",
            "options": ["Fire one of them", "Meet each privately", "Team meeting to air it out", "Ignore it"],
            "correct": "Meet each privately",
        },
        "match_pairs": {
            "prompt": "Match each management style to its best scenario:",
            "pairs": [("Autocratic", "Crisis/emergency"), ("Democratic", "Creative projects"), ("Laissez-faire", "Expert teams"), ("Coaching", "Developing talent")],
        },
    },
    "hr_specialist": {
        "match_pairs": {
            "prompt": "Match each interview question type to its purpose:",
            "pairs": [("Tell me about yourself", "Ice breaker + overview"), ("Describe a challenge you overcame", "Behavioral assessment"), ("What's your salary expectation?", "Alignment check"), ("Do you have questions?", "Engagement + interest")],
        },
        "sequence": {
            "prompt": "Conduct a new hire onboarding in the correct order:",
            "items": ["Welcome and tour", "HR paperwork", "IT setup", "Team introductions", "Training plan", "First assignment", "30-day check-in"],
            "order": ["Welcome and tour", "HR paperwork", "IT setup", "Team introductions", "Training plan", "First assignment", "30-day check-in"],
        },
    },
    "marketing": {
        "shift_sim": {
            "prompt": "Manage the marketing campaign launch — prioritize:",
            "situations": ["Campaign deadline tomorrow (critical)", "A/B test results needed (high)", "Influencer contract negotiation (medium)", "Social media calendar (medium)", "Brand guideline update (low)"],
            "optimal": ["Campaign deadline tomorrow (critical)", "A/B test results needed (high)", "Influencer contract negotiation (medium)", "Social media calendar (medium)", "Brand guideline update (low)"],
        },
        "pattern": {
            "prompt": "Conversion funnel: 10,000 impressions → 1,000 clicks → 100 leads → ? customers (1% close rate)",
            "sequence": ["10,000", "1,000", "100", "?"],
            "answer": "1",
        },
    },
    "consultant": {
        "quick_pick": {
            "prompt": "Client asks for a recommendation you're not sure about. Best response?",
            "options": ["Give confident answer anyway", "Say you'll research and follow up", "Admit you don't know", "Redirect to another topic"],
            "correct": "Say you'll research and follow up",
        },
        "match_pairs": {
            "prompt": "Match each consulting framework to its use case:",
            "pairs": [("SWOT analysis", "Strategic positioning"), ("Porter's 5 Forces", "Industry analysis"), ("BCG Matrix", "Product portfolio"), ("McKinsey 7S", "Organizational alignment")],
        },
    },
    "auditor": {
        "sequence": {
            "prompt": "Conduct a financial audit in the correct order:",
            "items": ["Plan the audit", "Assess internal controls", "Test transactions", "Verify account balances", "Review disclosures", "Issue audit opinion"],
            "order": ["Plan the audit", "Assess internal controls", "Test transactions", "Verify account balances", "Review disclosures", "Issue audit opinion"],
        },
        "match_pairs": {
            "prompt": "Match each audit opinion to its meaning:",
            "pairs": [("Unqualified", "Clean opinion — no issues"), ("Qualified", "One exception noted"), ("Adverse", "Material misstatements found"), ("Disclaimer", "Unable to form opinion")],
        },
    },
    "loan_officer": {
        "match_pairs": {
            "prompt": "Match each loan type to its typical term:",
            "pairs": [("Mortgage", "15-30 years"), ("Auto loan", "3-7 years"), ("Personal loan", "1-5 years"), ("Business line of credit", "Revolving")],
        },
        "sequence": {
            "prompt": "Process a loan application in the correct order:",
            "items": ["Collect application", "Pull credit report", "Verify income", "Assess collateral", "Calculate DTI ratio", "Underwriting decision", "Close loan"],
            "order": ["Collect application", "Pull credit report", "Verify income", "Assess collateral", "Calculate DTI ratio", "Underwriting decision", "Close loan"],
        },
    },
    "insurance": {
        "match_pairs": {
            "prompt": "Match each insurance type to its coverage:",
            "pairs": [("Term life", "Death benefit for set period"), ("Whole life", "Lifetime + cash value"), ("Disability", "Income replacement"), ("Liability", "Legal protection")],
        },
        "quick_pick": {
            "prompt": "Client asks if they need umbrella insurance. They have $1M net worth. Best advice?",
            "options": ["Not necessary", "Yes, strongly recommended", "Only if they own a business", "Only for high-risk professions"],
            "correct": "Yes, strongly recommended",
        },
    },
    "bookkeeper": {
        "pattern": {
            "prompt": "Journal entry pattern: Debit ___, Credit ___ (double-entry rule)",
            "sequence": ["Debit", "Credit"],
            "answer": "Equal",
        },
        "spot_error": {
            "prompt": "Find the error in this journal entry:",
            "correct_sequence": ["Debit: Cash $5,000", "Credit: Revenue $5,000", "Balanced: Yes"],
            "presented_sequence": ["Debit: Cash $5,000", "Credit: Revenue $4,500", "Balanced: Yes"],
        },
    },
    "tax_prep": {
        "spot_error": {
            "prompt": "Find the error in this tax return preparation:",
            "correct_sequence": ["Gather W-2s and 1099s", "Calculate gross income", "Apply deductions", "Apply credits", "Calculate tax liability", "File return"],
            "presented_sequence": ["Gather W-2s and 1099s", "Apply deductions", "Calculate gross income", "Apply credits", "Calculate tax liability", "File return"],
        },
        "match_pairs": {
            "prompt": "Match each tax form to its purpose:",
            "pairs": [("W-2", "Wage and tax statement"), ("1099-NEC", "Independent contractor income"), ("Schedule C", "Business profit/loss"), ("Form 1040", "Individual tax return")],
        },
    },
    "investment_bank": {
        "shift_sim": {
            "prompt": "Manage the M&A deal — prioritize:",
            "situations": ["Due diligence deadline missed (critical)", "Valuation model revision (high)", "Client board presentation (high)", "Regulatory filing (medium)", "Team dinner (low)"],
            "optimal": ["Due diligence deadline missed (critical)", "Client board presentation (high)", "Valuation model revision (high)", "Regulatory filing (medium)", "Team dinner (low)"],
        },
        "quick_pick": {
            "prompt": "IPO pricing: demand is 3x oversubscribed. Best pricing action?",
            "options": ["Price at low end", "Price at high end", "Withdraw the IPO", "Price at midpoint"],
            "correct": "Price at high end",
        },
    },
    "venture_cap": {
        "shift_sim": {
            "prompt": "Manage your portfolio — prioritize:",
            "situations": ["Portfolio company running out of cash (critical)", "New deal screening (high)", "Board meeting prep (medium)", "LP update (medium)", "Industry event (low)"],
            "optimal": ["Portfolio company running out of cash (critical)", "New deal screening (high)", "Board meeting prep (medium)", "LP update (medium)", "Industry event (low)"],
        },
        "match_pairs": {
            "prompt": "Match each funding round to its typical stage:",
            "pairs": [("Seed", "Idea/validation"), ("Series A", "Product-market fit"), ("Series B", "Scaling"), ("Series C+", "Expansion/pre-IPO")],
        },
    },
    "hedge_fund": {
        "quick_pick": {
            "prompt": "Market crashes 15% in a day. Your fund is long-only. Best immediate action?",
            "options": ["Panic sell everything", "Assess fundamentals + rebalance", "Go all-in on shorts", "Do nothing"],
            "correct": "Assess fundamentals + rebalance",
        },
        "match_pairs": {
            "prompt": "Match each hedge fund strategy to its approach:",
            "pairs": [("Long/short equity", "Buy winners, short losers"), ("Global macro", "Bet on economic trends"), ("Merger arbitrage", "Profit from M&A spreads"), ("Distressed debt", "Buy troubled debt at discount")],
        },
    },
    "entrepreneur": {
        "quick_pick": {
            "prompt": "Your startup has 3 months of runway. Priority?",
            "options": ["Hire more staff", "Raise capital or cut burn", "Launch new features", "Pivot the business"],
            "correct": "Raise capital or cut burn",
        },
        "match_pairs": {
            "prompt": "Match each startup metric to its meaning:",
            "pairs": [("MRR", "Monthly Recurring Revenue"), ("CAC", "Customer Acquisition Cost"), ("LTV", "Lifetime Value"), ("Churn rate", "Customer loss rate")],
        },
    },
    "cfo": {
        "quick_pick": {
            "prompt": "Company is profitable but cash flow is negative. Most likely cause?",
            "options": ["Accounting error", "High accounts receivable", "Too many employees", "Low prices"],
            "correct": "High accounts receivable",
        },
        "match_pairs": {
            "prompt": "Match each financial statement to its purpose:",
            "pairs": [("Income statement", "Revenue and expenses"), ("Balance sheet", "Assets and liabilities"), ("Cash flow statement", "Cash movements"), ("Statement of equity", "Owner's equity changes")],
        },
    },
    "coo": {
        "quick_pick": {
            "prompt": "Production line is at 60% capacity. Best action?",
            "options": ["Hire more workers", "Identify bottleneck and optimize", "Buy more machines", "Reduce shifts"],
            "correct": "Identify bottleneck and optimize",
        },
        "match_pairs": {
            "prompt": "Match each operations metric to its formula:",
            "pairs": [("OEE", "Availability × Performance × Quality"), ("Cycle time", "Total time / units produced"), ("Throughput", "Units per time period"), ("Utilization", "Actual / capacity")],
        },
    },
    "trader": {
        "quick_pick": {
            "prompt": "Your algorithm signals a buy but news just broke negative. Action?",
            "options": ["Follow the algorithm", "Override and hold", "Sell instead", "Wait 5 minutes then decide"],
            "correct": "Override and hold",
        },
        "match_pairs": {
            "prompt": "Match each trading order to its purpose:",
            "pairs": [("Iceberg order", "Hide large order size"), ("VWAP order", "Execute near volume-weighted average"), ("TWAP order", "Spread execution evenly over time"), ("Implementation shortfall", "Minimize total execution cost")],
        },
    },
    "negotiator": {
        "quick_pick": {
            "prompt": "Counterparty makes an aggressive first offer. Best response?",
            "options": ["Match their aggression", "Ask clarifying questions", "Walk away", "Accept immediately"],
            "correct": "Ask clarifying questions",
        },
        "match_pairs": {
            "prompt": "Match each negotiation tactic to its counter:",
            "pairs": [("Anchoring", "Reframe with your own anchor"), ("Silence tactic", "Wait them out"), ("Good cop/bad cop", "Address the decision-maker"), ("Nibbling", "Address all terms upfront")],
        },
    },
    "magnate": {
        "quick_pick": {
            "prompt": "A subsidiary is underperforming but has strategic value. Best action?",
            "options": ["Sell immediately", "Restructure leadership", "Merge with another subsidiary", "Shut it down"],
            "correct": "Restructure leadership",
        },
        "match_pairs": {
            "prompt": "Match each business empire risk to its mitigation:",
            "pairs": [("Regulatory risk", "Compliance team + lobbying"), ("Succession risk", "Groom next-gen leaders"), ("Concentration risk", "Diversify holdings"), ("Reputation risk", "PR team + crisis plan")],
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # CREATIVE & ARTS — 25 jobs
    # ═══════════════════════════════════════════════════════════════

    "graphic_design": {
        "match_pairs": {
            "prompt": "Match each design principle to its description:",
            "pairs": [("Contrast", "Make different elements stand out"), ("Alignment", "Create visual connection"), ("Repetition", "Unify the design"), ("Proximity", "Group related items")],
        },
        "fill_blank": {
            "prompt": "Complete the color theory: Red + Blue + Yellow are ____ colors",
            "answer": "primary",
            "context": "Red, blue, and yellow are the three primary colors in traditional color theory.",
        },
    },
    "photographer": {
        "sequence": {
            "prompt": "Set up a studio photoshoot in the correct order:",
            "items": ["Choose backdrop", "Set up key light", "Add fill light", "Position hair light", "Set camera settings", "Position subject", "Test shots", "Begin shooting"],
            "order": ["Choose backdrop", "Set up key light", "Add fill light", "Position hair light", "Set camera settings", "Position subject", "Test shots", "Begin shooting"],
        },
        "precision": {
            "prompt": "Set the shutter speed to exactly 1/250 second. Click when the dial hits 250!",
            "target": 250,
            "tolerance": 5,
        },
    },
    "filmmaker": {
        "sequence": {
            "prompt": "Edit a video project in the correct order:",
            "items": ["Import footage", "Organize clips", "Rough cut", "Fine cut", "Color correction", "Audio mix", "Add titles/graphics", "Export final"],
            "order": ["Import footage", "Organize clips", "Rough cut", "Fine cut", "Color correction", "Audio mix", "Add titles/graphics", "Export final"],
        },
        "fill_blank": {
            "prompt": "Complete: '180-degree rule — keep camera on the same side of the ____ line'",
            "answer": "action",
            "context": "The 180-degree rule keeps camera positions on one side of an imaginary action line.",
        },
    },
    "animator": {
        "pattern": {
            "prompt": "Animation timing: ease-in, ease-out, ease-in, ease-out, ?",
            "sequence": ["ease-in", "ease-out", "ease-in", "ease-out", "?"],
            "answer": "ease-in",
        },
        "fill_blank": {
            "prompt": "Complete: '24 frames per second means each frame is held for ____ milliseconds'",
            "answer": "41.67",
            "context": "1000ms / 24fps ≈ 41.67ms per frame.",
        },
    },
    "musician": {
        "pattern": {
            "prompt": "Chord progression: I, V, vi, IV, I, V, vi, ?",
            "sequence": ["I", "V", "vi", "IV", "I", "V", "vi", "?"],
            "answer": "IV",
        },
        "timing": {
            "prompt": "Play the note on beat 3 of a 4/4 measure! Click when the metronome hits beat 3.",
            "beats": 4,
        },
    },
    "writer": {
        "fill_blank": {
            "prompt": "Complete: 'Show, don't ____' — the golden rule of creative writing",
            "answer": "tell",
            "context": "Show don't tell — use sensory details and actions instead of exposition.",
        },
        "sequence": {
            "prompt": "Follow the writing process in the correct order:",
            "items": ["Brainstorm ideas", "Outline structure", "Write first draft", "Set aside", "Revise for content", "Edit for style", "Proofread", "Submit"],
            "order": ["Brainstorm ideas", "Outline structure", "Write first draft", "Set aside", "Revise for content", "Edit for style", "Proofread", "Submit"],
        },
    },
    "journalist": {
        "sequence": {
            "prompt": "Write a news article — follow the process in order:",
            "items": ["Get assignment", "Research topic", "Conduct interviews", "Verify facts", "Write lead paragraph", "Write body", "Get editor review", "Publish"],
            "order": ["Get assignment", "Research topic", "Conduct interviews", "Verify facts", "Write lead paragraph", "Write body", "Get editor review", "Publish"],
        },
        "fill_blank": {
            "prompt": "Complete: 'The 5 Ws: Who, What, When, Where, and ____'",
            "answer": "Why",
            "context": "Every news story should answer the 5 Ws: Who, What, When, Where, Why.",
        },
    },
    "painter": {
        "match_pairs": {
            "prompt": "Match each painting medium to its characteristic:",
            "pairs": [("Oil paint", "Slow drying, blendable"), ("Watercolor", "Transparent, fluid"), ("Acrylic", "Fast drying, versatile"), ("Gouache", "Opaque, matte finish")],
        },
        "precision": {
            "prompt": "Mix the paint to exactly 50% saturation. Click when the gauge hits 50!",
            "target": 50,
            "tolerance": 3,
        },
    },
    "sculptor": {
        "sequence": {
            "prompt": "Create a clay sculpture in the correct order:",
            "items": ["Build armature", "Add base clay", "Rough form", "Refine shapes", "Add details", "Smooth surface", "Hollow for firing", "Fire in kiln"],
            "order": ["Build armature", "Add base clay", "Rough form", "Refine shapes", "Add details", "Smooth surface", "Hollow for firing", "Fire in kiln"],
        },
        "fill_blank": {
            "prompt": "Complete: 'Bronze casting uses the ____ méthode'",
            "answer": "lost wax",
            "context": "Lost wax casting (cire perdue) is the traditional bronze sculpture method.",
        },
    },
    "fashion_design": {
        "sequence": {
            "prompt": "Create a fashion collection in the correct order:",
            "items": ["Mood board", "Sketch designs", "Select fabrics", "Create patterns", "Make toile/muslin", "Fit on model", "Final garment", "Style for show"],
            "order": ["Mood board", "Sketch designs", "Select fabrics", "Create patterns", "Make toile/muslin", "Fit on model", "Final garment", "Style for show"],
        },
        "match_pairs": {
            "prompt": "Match each fabric type to its best use:",
            "pairs": [("Silk", "Evening wear"), ("Denim", "Casual durability"), ("Wool", "Winter warmth"), ("Linen", "Summer breathability")],
        },
    },
    "interior_design": {
        "match_pairs": {
            "prompt": "Match each design style to its key characteristic:",
            "pairs": [("Minimalist", "Clean lines, less is more"), ("Industrial", "Exposed materials, raw texture"), ("Scandinavian", "Light, functional, cozy"), ("Bohemian", "Eclectic, layered, artistic")],
        },
        "fill_blank": {
            "prompt": "Complete: 'The 60-30-10 rule: 60% dominant color, 30% secondary, 10% ____'",
            "answer": "accent",
            "context": "The 60-30-10 color rule uses 10% for accent color.",
        },
    },
    "architect": {
        "sequence": {
            "prompt": "Design a building project in the correct order:",
            "items": ["Client brief", "Site analysis", "Concept design", "Schematic design", "Design development", "Construction documents", "Bidding", "Construction admin"],
            "order": ["Client brief", "Site analysis", "Concept design", "Schematic design", "Design development", "Construction documents", "Bidding", "Construction admin"],
        },
        "fill_blank": {
            "prompt": "Complete: 'Form follows ____' — Louis Sullivan's design principle",
            "answer": "function",
            "context": "Louis Sullivan coined 'form follows function' — a cornerstone of modern architecture.",
        },
    },
    "actor": {
        "sequence": {
            "prompt": "Prepare for a stage performance in the correct order:",
            "items": ["Read script", "Character analysis", "Memorize lines", "Rehearse blocking", "Dress rehearsal", "Notes from director", "Final rehearsal", "Performance"],
            "order": ["Read script", "Character analysis", "Memorize lines", "Rehearse blocking", "Dress rehearsal", "Notes from director", "Final rehearsal", "Performance"],
        },
        "fill_blank": {
            "prompt": "Complete: 'Stanislavski said: Love the art in yourself, not ____ in the art'",
            "answer": "yourself",
            "context": "Stanislavski: 'Love the art in yourself, not yourself in the art.'",
        },
    },
    "dancer": {
        "timing": {
            "prompt": "Hit the count on beat 5 of an 8-count phrase! Click when the beat hits 5.",
            "beats": 8,
        },
        "pattern": {
            "prompt": "Waltz box step: Forward, Side, Close, Back, Side, Close, Forward, ?",
            "sequence": ["Forward", "Side", "Close", "Back", "Side", "Close", "Forward", "?"],
            "answer": "Side",
        },
    },
    "comedian": {
        "quick_pick": {
            "prompt": "A joke bombs. Best recovery?",
            "options": ["Apologize profusely", "Acknowledge it with a callback", "Move on silently", "Blame the audience"],
            "correct": "Acknowledge it with a callback",
        },
        "fill_blank": {
            "prompt": "Complete: 'Comedy is tragedy plus ____' — Mark Twain",
            "answer": "time",
            "context": "Mark Twain: 'Comedy is tragedy plus time.'",
        },
    },
    "director": {
        "shift_sim": {
            "prompt": "Manage the film set — prioritize:",
            "situations": ["Lead actor not on set (critical)", "Lighting setup behind schedule (high)", "Script revision needed (medium)", "Catering delay (low)", "Set decoration tweak (low)"],
            "optimal": ["Lead actor not on set (critical)", "Lighting setup behind schedule (high)", "Script revision needed (medium)", "Catering delay (low)", "Set decoration tweak (low)"],
        },
        "sequence": {
            "prompt": "Shoot a film scene in the correct order:",
            "items": ["Block the scene", "Rehearse with actors", "Set lighting", "Set camera positions", "Sound check", "Roll camera", "Action", "Cut", "Move to next setup"],
            "order": ["Block the scene", "Rehearse with actors", "Set lighting", "Set camera positions", "Sound check", "Roll camera", "Action", "Cut", "Move to next setup"],
        },
    },
    "producer": {
        "shift_sim": {
            "prompt": "Manage the production schedule — prioritize:",
            "situations": ["Budget overrun on day 3 (critical)", "Permit expiring tomorrow (high)", "Cast scheduling conflict (medium)", "Equipment rental return (low)", "Craft services menu (low)"],
            "optimal": ["Budget overrun on day 3 (critical)", "Permit expiring tomorrow (high)", "Cast scheduling conflict (medium)", "Equipment rental return (low)", "Craft services menu (low)"],
        },
        "match_pairs": {
            "prompt": "Match each production role to its responsibility:",
            "pairs": [("Line producer", "Daily budget and schedule"), ("UPM", "Below-the-line crew"), ("First AD", "Set logistics and timing"), ("Production coordinator", "Office and paperwork")],
        },
    },
    "novelist": {
        "spot_error": {
            "prompt": "Find the error in this manuscript edit:",
            "correct_sequence": ["Read full draft", "Check structure", "Fix plot holes", "Line edit for prose", "Copy edit for grammar", "Proofread"],
            "presented_sequence": ["Read full draft", "Line edit for prose", "Check structure", "Fix plot holes", "Copy edit for grammar", "Proofread"],
        },
        "fill_blank": {
            "prompt": "Complete: 'Kill your ____' — Stephen King's editing advice",
            "answer": "darlings",
            "context": "Stephen King: 'Kill your darlings, kill your darlings, even when it breaks your egocentric little scribbler's heart.'",
        },
    },
    "tattoo_artist": {
        "sequence": {
            "prompt": "Complete a tattoo session in the correct order:",
            "items": ["Consult design", "Prepare stencil", "Set up station", "Clean and shave skin", "Apply stencil", "Outline", "Shading", "Color", "Clean and wrap"],
            "order": ["Consult design", "Prepare stencil", "Set up station", "Clean and shave skin", "Apply stencil", "Outline", "Shading", "Color", "Clean and wrap"],
        },
        "precision": {
            "prompt": "Set the needle depth to exactly 1.5mm for lining. Click when the gauge hits 1.5!",
            "target": 1.5,
            "tolerance": 0.2,
        },
    },
    "makeup_artist": {
        "match_pairs": {
            "prompt": "Match each makeup technique to its purpose:",
            "pairs": [("Contouring", "Define bone structure"), ("Highlighting", "Bring forward features"), ("Strobing", "Dewy glow"), ("Cut crease", "Define eye socket")],
        },
        "sequence": {
            "prompt": "Apply bridal makeup in the correct order:",
            "items": ["Cleanse face", "Primer", "Foundation", "Concealer", "Set with powder", "Eyes (shadow, liner, mascara)", "Brows", "Blush and bronzer", "Lips", "Setting spray"],
            "order": ["Cleanse face", "Primer", "Foundation", "Concealer", "Set with powder", "Eyes (shadow, liner, mascara)", "Brows", "Blush and bronzer", "Lips", "Setting spray"],
        },
    },
    "potter": {
        "sequence": {
            "prompt": "Throw a pot on the wheel in the correct order:",
            "items": ["Center clay", "Open center", "Pull walls", "Shape form", "Trim foot", "Remove from wheel", "Dry to leather-hard", "Bisque fire", "Glaze", "Glaze fire"],
            "order": ["Center clay", "Open center", "Pull walls", "Shape form", "Trim foot", "Remove from wheel", "Dry to leather-hard", "Bisque fire", "Glaze", "Glaze fire"],
        },
        "precision": {
            "prompt": "Center the clay to exactly 0mm wobble. Click when the gauge hits 0!",
            "target": 0,
            "tolerance": 1,
        },
    },
    "artist": {
        "fill_blank": {
            "prompt": "Complete: 'In perspective drawing, the ____ line is at the viewer's eye level'",
            "answer": "horizon",
            "context": "The horizon line represents eye level and is where vanishing points sit.",
        },
        "match_pairs": {
            "prompt": "Match each illustration style to its key feature:",
            "pairs": [("Line art", "Pure strokes, no fill"), ("Flat design", "Solid colors, no shading"), ("Crosshatching", "Layered lines for shading"), ("Stippling", "Dots for tone")],
        },
    },
    "game_artist": {
        "fill_blank": {
            "prompt": "Complete: 'A ____ map wraps a 2D image onto a 3D model surface'",
            "answer": "texture",
            "context": "Texture mapping applies a 2D image to a 3D model's UV coordinates.",
        },
        "match_pairs": {
            "prompt": "Match each game art asset to its purpose:",
            "pairs": [("Concept art", "Visual direction guide"), ("Sprite sheet", "2D animation frames"), ("Normal map", "Fake surface detail"), ("Rig", "Skeleton for animation")],
        },
    },
    "voice_actor": {
        "timing": {
            "prompt": "Hit your line on the downbeat! Click when the cue light flashes.",
            "beats": 4,
        },
        "fill_blank": {
            "prompt": "Complete: 'In voice acting, ____ is the key to believable delivery'",
            "answer": "breath",
            "context": "Breath control is essential for pacing, emotion, and stamina in voice acting.",
        },
    },
    "maestro": {
        "timing": {
            "prompt": "Play the note exactly on beat 2 of a 4/4 measure! Click when the metronome hits 2.",
            "beats": 4,
        },
        "pattern": {
            "prompt": "Drum fill pattern: Kick, Snare, Kick-kick, Snare, Kick, Snare, Kick, ?",
            "sequence": ["Kick", "Snare", "Kick-kick", "Snare", "Kick", "Snare", "Kick", "?"],
            "answer": "Snare",
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # TRANSPORT & LOGISTICS — 25 jobs
    # ═══════════════════════════════════════════════════════════════

    "truck_driver": {
        "route_plan": {
            "prompt": "Plan the most efficient delivery route — order these stops:",
            "stops": [("Warehouse (start)", "Depot"), ("Stop A (north side)", "Warehouse (start)"), ("Stop B (east side)", "Stop A (north side)"), ("Stop C (downtown)", "Stop B (east side)"), ("Stop D (south side)", "Stop C (downtown)"), ("Return to warehouse", "Stop D (south side)")],
        },
        "fill_blank": {
            "prompt": "Complete: 'CDL stands for Commercial Driver's ____'",
            "answer": "License",
            "context": "CDL = Commercial Driver's License, required for large commercial vehicles.",
        },
    },
    "delivery": {
        "route_plan": {
            "prompt": "Optimize your delivery route — order stops by efficiency:",
            "stops": [("Distribution center", "Start"), ("House on Elm St", "Distribution center"), ("Apartment on Oak Ave", "House on Elm St"), ("Business on Main St", "Apartment on Oak Ave"), ("Return to center", "Business on Main St")],
        },
        "speed_run": {
            "prompt": "Complete all deliveries before your shift ends! Click each stop to deliver.",
            "tasks": ["Stop 1 (Elm St)", "Stop 2 (Oak Ave)", "Stop 3 (Main St)", "Stop 4 (Pine Rd)", "Stop 5 (Cedar Ln)"],
        },
    },
    "bus_driver": {
        "route_plan": {
            "prompt": "Plan the bus route — order stops by sequence:",
            "stops": [("First stop (transit center)", "Start"), ("Stop 2 (mall)", "First stop (transit center)"), ("Stop 3 (hospital)", "Stop 2 (mall)"), ("Stop 4 (university)", "Stop 3 (hospital)"), ("Stop 5 (suburb)", "Stop 4 (university)"), ("Last stop (transit center)", "Stop 5 (suburb)")],
        },
        "timing": {
            "prompt": "Depart the stop exactly on schedule! Click when the clock hits the departure time.",
            "beats": 4,
        },
    },
    "taxi_driver": {
        "route_plan": {
            "prompt": "Pick the fastest route to the airport — order these segments:",
            "stops": [("Current location (downtown)", "Start"), ("Take Main St north", "Current location (downtown)"), ("Merge onto Highway 9", "Take Main St north"), ("Exit at Airport Blvd", "Merge onto Highway 9"), ("Arrive at terminal", "Exit at Airport Blvd")],
        },
        "quick_pick": {
            "prompt": "Passenger is in a hurry but the fastest route has heavy traffic. Best action?",
            "options": ["Take the highway anyway", "Use surface streets", "Ask passenger's preference", "Cancel the ride"],
            "correct": "Ask passenger's preference",
        },
    },
    "pilot": {
        "sequence": {
            "prompt": "Conduct a pre-flight checklist in the correct order:",
            "items": ["Review weather", "Check fuel", "Inspect exterior", "Test controls", "Verify instruments", "Start engine", "Taxi to runway", "Takeoff clearance", "Takeoff"],
            "order": ["Review weather", "Check fuel", "Inspect exterior", "Test controls", "Verify instruments", "Start engine", "Taxi to runway", "Takeoff clearance", "Takeoff"],
        },
        "fill_blank": {
            "prompt": "Complete: 'V1 is the speed at which takeoff can no longer be safely ____'",
            "answer": "aborted",
            "context": "V1 is the decision speed — after V1, the takeoff must continue.",
        },
    },
    "ship_captain": {
        "sequence": {
            "prompt": "Prepare for departure — follow the correct order:",
            "items": ["Check weather forecast", "Verify cargo secure", "Brief crew", "Test navigation systems", "Start engines", "Untie mooring lines", "Depart port", "Set course"],
            "order": ["Check weather forecast", "Verify cargo secure", "Brief crew", "Test navigation systems", "Start engines", "Untie mooring lines", "Depart port", "Set course"],
        },
        "fill_blank": {
            "prompt": "Complete: 'Port means ____, starboard means ____'",
            "answer": "left, right",
            "context": "Port = left side, starboard = right side of a vessel.",
        },
    },
    "train_driver": {
        "sequence": {
            "prompt": "Conduct a train departure in the correct order:",
            "items": ["Check signals", "Verify track clearance", "Test brakes", "Sound horn", "Release brakes", "Apply power", "Monitor speed", "Depart station"],
            "order": ["Check signals", "Verify track clearance", "Test brakes", "Sound horn", "Release brakes", "Apply power", "Monitor speed", "Depart station"],
        },
        "fill_blank": {
            "prompt": "Complete: 'A ____ signal means proceed with caution'",
            "answer": "yellow",
            "context": "Green = clear, yellow = caution, red = stop.",
        },
    },
    "air_traffic": {
        "shift_sim": {
            "prompt": "Manage arriving and departing traffic — prioritize:",
            "situations": ["Emergency landing — fuel critical (critical)", "Departure queue backing up (high)", "Approaching weather change (medium)", "Frequency congestion (medium)", "Paperwork (low)"],
            "optimal": ["Emergency landing — fuel critical (critical)", "Departure queue backing up (high)", "Approaching weather change (medium)", "Frequency congestion (medium)", "Paperwork (low)"],
        },
        "fill_blank": {
            "prompt": "Complete: 'ATC clearance: 'Cleared to land runway ____' — acknowledge with callsign'",
            "answer": "27R",
            "context": "Pilots must read back runway assignments and clearances.",
        },
    },
    "forklift": {
        "sequence": {
            "prompt": "Safely move a pallet — follow the steps in order:",
            "items": ["Inspect forklift", "Approach pallet", "Level forks", "Insert forks fully", "Lift slightly", "Tilt mast back", "Raise to travel height", "Reverse safely", "Lower at destination"],
            "order": ["Inspect forklift", "Approach pallet", "Level forks", "Insert forks fully", "Lift slightly", "Tilt mast back", "Raise to travel height", "Reverse safely", "Lower at destination"],
        },
        "precision": {
            "prompt": "Position the forks at exactly 12 inches height. Click when the gauge hits 12!",
            "target": 12,
            "tolerance": 1,
        },
    },
    "warehouse": {
        "sort": {
            "prompt": "Sort incoming packages by destination zone:",
            "items": ["Zone A (northeast)", "Zone B (southeast)", "Zone C (midwest)", "Zone D (west coast)", "Zone E (international)"],
            "order": ["Zone A (northeast)", "Zone B (southeast)", "Zone C (midwest)", "Zone D (west coast)", "Zone E (international)"],
        },
        "speed_run": {
            "prompt": "Pick all orders before the truck leaves! Click each order to pick it.",
            "tasks": ["Order #1001 (Aisle 3)", "Order #1002 (Aisle 7)", "Order #1003 (Aisle 1)", "Order #1004 (Aisle 5)", "Order #1005 (Aisle 9)"],
        },
    },
    "logistics_mgr": {
        "route_plan": {
            "prompt": "Optimize the supply chain route — order these distribution points:",
            "stops": [("Factory (origin)", "Start"), ("Regional hub", "Factory (origin)"), ("Cross-dock facility", "Regional hub"), ("Local distribution center", "Cross-dock facility"), ("Retail store", "Local distribution center")],
        },
        "shift_sim": {
            "prompt": "Manage the logistics operations — prioritize:",
            "situations": ["Shipment stuck at customs (critical)", "Truck breakdown on highway (high)", "Warehouse capacity at 95% (medium)", "Supplier delay notification (medium)", "Route optimization study (low)"],
            "optimal": ["Shipment stuck at customs (critical)", "Truck breakdown on highway (high)", "Warehouse capacity at 95% (medium)", "Supplier delay notification (medium)", "Route optimization study (low)"],
        },
    },
    "dispatch": {
        "shift_sim": {
            "prompt": "Manage the dispatch board — prioritize:",
            "situations": ["Driver reported accident (critical)", "Urgent pickup request (high)", "Route reassignment needed (medium)", "Driver check-in calls (medium)", "Log filing (low)"],
            "optimal": ["Driver reported accident (critical)", "Urgent pickup request (high)", "Route reassignment needed (medium)", "Driver check-in calls (medium)", "Log filing (low)"],
        },
        "fill_blank": {
            "prompt": "Complete: 'ETA stands for Estimated Time of ____'",
            "answer": "Arrival",
            "context": "ETA = Estimated Time of Arrival.",
        },
    },
    "courier": {
        "route_plan": {
            "prompt": "Plan your courier route — order stops by efficiency:",
            "stops": [("Office (pickup)", "Start"), ("Law firm (delivery 1)", "Office (pickup)"), ("Bank (delivery 2)", "Law firm (delivery 1)"), ("Hospital (delivery 3)", "Bank (delivery 2)"), ("Return to office", "Hospital (delivery 3)")],
        },
        "speed_run": {
            "prompt": "Deliver all packages before the 5 PM deadline! Click each to deliver.",
            "tasks": ["Package 1 (law firm)", "Package 2 (bank)", "Package 3 (hospital)", "Package 4 (city hall)", "Package 5 (university)"],
        },
    },
    "moving_company": {
        "sequence": {
            "prompt": "Execute a residential move in the correct order:",
            "items": ["Arrive and assess", "Protect floors/walls", "Disassemble furniture", "Load boxes first", "Load furniture", "Secure load", "Drive to new location", "Unload furniture first", "Reassemble furniture", "Final walkthrough"],
            "order": ["Arrive and assess", "Protect floors/walls", "Disassemble furniture", "Load boxes first", "Load furniture", "Secure load", "Drive to new location", "Unload furniture first", "Reassemble furniture", "Final walkthrough"],
        },
        "shift_sim": {
            "prompt": "Manage the moving job — prioritize:",
            "situations": ["Sofa won't fit through door (critical)", ("Customer wants items rearranged (high)"), ("Truck parking expiring (medium)"), ("Lunch break scheduling (low)"), ("Equipment cleanup (low)")],
            "optimal": ["Sofa won't fit through door (critical)", "Customer wants items rearranged (high)", "Truck parking expiring (medium)", "Lunch break scheduling (low)", "Equipment cleanup (low)"],
        },
    },
    "ambulance_drv": {
        "sequence": {
            "prompt": "Respond to an emergency call in the correct order:",
            "items": ["Receive dispatch", "Navigate to scene", "Assess scene safety", "Position ambulance", "Assist medics with patient", "Load patient", "Transport to hospital", "Report to ER", "Clean rig", "Return to station"],
            "order": ["Receive dispatch", "Navigate to scene", "Assess scene safety", "Position ambulance", "Assist medics with patient", "Load patient", "Transport to hospital", "Report to ER", "Clean rig", "Return to station"],
        },
        "speed_run": {
            "prompt": "Navigate through traffic — complete each maneuver quickly! Click each to proceed.",
            "tasks": ["Clear intersection 1", "Take alternate route", "Clear intersection 2", "Merge onto highway", "Exit at hospital"],
        },
    },
    "fire_truck_drv": {
        "sequence": {
            "prompt": "Respond to a structure fire in the correct order:",
            "items": ["Receive alarm", "Don gear", "Board apparatus", "Respond to scene", "Size up situation", "Establish water supply", "Advance hose line", "Enter structure", "Locate and extinguish fire", "Overhaul and ventilate"],
            "order": ["Receive alarm", "Don gear", "Board apparatus", "Respond to scene", "Size up situation", "Establish water supply", "Advance hose line", "Enter structure", "Locate and extinguish fire", "Overhaul and ventilate"],
        },
        "shift_sim": {
            "prompt": "Manage the fireground — prioritize:",
            "situations": ["Trapped victim on 2nd floor (critical)", "Fire spreading to exposure (high)", ("Roof ventilation needed (medium)"), ("Rehab rotation for crew (medium)"), ("Salvage operations (low)")],
            "optimal": ["Trapped victim on 2nd floor (critical)", "Fire spreading to exposure (high)", "Roof ventilation needed (medium)", "Rehab rotation for crew (medium)", "Salvage operations (low)"],
        },
    },
    "police_officer": {
        "sequence": {
            "prompt": "Respond to a domestic disturbance call in the correct order:",
            "items": ["Receive dispatch", "Approach cautiously", "Assess situation", "Separate parties", "Interview each party", "Determine if crime occurred", "Take appropriate action", "Document incident", "File report"],
            "order": ["Receive dispatch", "Approach cautiously", "Assess situation", "Separate parties", "Interview each party", "Determine if crime occurred", "Take appropriate action", "Document incident", "File report"],
        },
        "quick_pick": {
            "prompt": "You pull over a driver who is clearly distressed and crying. Best approach?",
            "options": ["Immediately issue citation", "Ask if they're okay", "Call for backup", "Let them go with warning"],
            "correct": "Ask if they're okay",
        },
    },
    "ems": {
        "triage": {
            "prompt": "Triage these mass casualty patients — assign priority (1=most urgent):",
            "patients": ["Unconscious, not breathing", "Broken leg, conscious", "Minor cuts, walking", "Chest pain, conscious", "Head wound, confused"],
            "optimal": ["Unconscious, not breathing", "Chest pain, conscious", "Head wound, confused", "Broken leg, conscious", "Minor cuts, walking"],
        },
        "fill_blank": {
            "prompt": "Complete: 'ABC stands for Airway, ____, Circulation'",
            "answer": "Breathing",
            "context": "ABC = Airway, Breathing, Circulation — the primary survey sequence.",
        },
    },
    "garbage_collector": {
        "route_plan": {
            "prompt": "Optimize the collection route — order stops by efficiency:",
            "stops": [("Depot (start)", "Start"), ("Maple St (north route)", "Depot (start)"), ("Oak Ave (east route)", "Maple St (north route)"), ("Pine Rd (south route)", "Oak Ave (east route)"), ("Transfer station (end)", "Pine Rd (south route)")],
        },
        "speed_run": {
            "prompt": "Complete all collections before the route deadline! Click each stop to collect.",
            "tasks": ["Maple St", "Oak Ave", "Pine Rd", "Cedar Ln", "Birch Dr"],
        },
    },
    "street_sweeper": {
        "route_plan": {
            "prompt": "Plan the sweeping route — order streets by sequence:",
            "stops": [("Start (depot)", "Start"), ("Main St (downtown)", "Start (depot)"), ("1st Ave (east)", "Main St (downtown)"), ("2nd Ave (west)", "1st Ave (east)"), ("Return to depot", "2nd Ave (west)")],
        },
        "precision": {
            "prompt": "Set the broom height to exactly 2 inches. Click when the gauge hits 2!",
            "target": 2,
            "tolerance": 0.5,
        },
    },
    "snow_plow": {
        "route_plan": {
            "prompt": "Plan the snow plow route — prioritize roads by traffic level:",
            "stops": [("Highway (priority 1)", "Start"), ("Main arterial (priority 2)", "Highway (priority 1)"), ("School zone (priority 3)", "Main arterial (priority 2)"), ("Residential (priority 4)", "School zone (priority 3)"), ("Return to depot", "Residential (priority 4)")],
        },
        "speed_run": {
            "prompt": "Clear all roads before rush hour! Click each road to plow it.",
            "tasks": ["Highway 9", "Main Street", "School Road", "Oak Avenue", "Pine Lane"],
        },
    },
    "chauffeur": {
        "sequence": {
            "prompt": "Execute a VIP pickup in the correct order:",
            "items": ["Inspect vehicle", "Plan route", "Arrive 10 min early", "Park and wait", "Greet client", "Open door", "Confirm destination", "Drive safely", "Arrive and open door", "Thank client"],
            "order": ["Inspect vehicle", "Plan route", "Arrive 10 min early", "Park and wait", "Greet client", "Open door", "Confirm destination", "Drive safely", "Arrive and open door", "Thank client"],
        },
        "fill_blank": {
            "prompt": "Complete: 'A professional chauffeur always maintains client ____'",
            "answer": "confidentiality",
            "context": "Chauffeurs must never disclose client information or destinations.",
        },
    },
    "transit_manager": {
        "shift_sim": {
            "prompt": "Manage the transit system — prioritize:",
            "situations": ["Bus breakdown on main route (critical)", ("Driver shortage for rush hour (high)"), ("Schedule adjustment needed (medium)"), ("Fare collection report (medium)"), ("Fleet maintenance log (low)")],
            "optimal": ["Bus breakdown on main route (critical)", "Driver shortage for rush hour (high)", "Schedule adjustment needed (medium)", "Fare collection report (medium)", "Fleet maintenance log (low)"],
        },
        "match_pairs": {
            "prompt": "Match each transit metric to its meaning:",
            "pairs": [("On-time performance", "% of trips on schedule"), ("Load factor", "Average passengers per trip"), ("Headway", "Time between vehicles"), ("Dwell time", "Time stopped at stations")],
        },
    },
    "harbor_master": {
        "shift_sim": {
            "prompt": "Manage the harbor — prioritize:",
            "situations": ["Cargo ship in distress (critical)", ("Ferry schedule behind (high)"), ("Recreational traffic congestion (medium)"), ("Fuel dock restocking (low)"), ("Office paperwork (low)")],
            "optimal": ["Cargo ship in distress (critical)", "Ferry schedule behind (high)", "Recreational traffic congestion (medium)", "Fuel dock restocking (low)", "Office paperwork (low)"],
        },
        "fill_blank": {
            "prompt": "Complete: 'A ship's ____ is its weight when loaded to the waterline'",
            "answer": "displacement",
            "context": "Displacement tonnage = weight of water displaced by the vessel.",
        },
    },
    "cargo_handler": {
        "sort": {
            "prompt": "Sort cargo by handling priority:",
            "items": ["Perishables (refrigerated)", ("Live animals"), ("Standard freight"), ("Hazardous materials"), ("Oversized cargo")],
            "order": ["Perishables (refrigerated)", "Live animals", "Hazardous materials", "Standard freight", "Oversized cargo"],
        },
        "speed_run": {
            "prompt": "Load all cargo containers before the ship departs! Click each to load.",
            "tasks": ["Container A-1", "Container A-2", "Container B-1", "Container B-2", "Container C-1"],
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # QUICK_PICK FILLS — 27 jobs missing their 3rd minigame content
    # ═══════════════════════════════════════════════════════════════

    "tech_writer": {
        "quick_pick": {
            "variants": [
                {"prompt": "A user guide is too technical for beginners. Best approach?", "options": ["Add more jargon", "Rewrite with simpler language + diagrams", "Keep as-is", "Delete technical sections"], "correct": "Rewrite with simpler language + diagrams"},
                {"prompt": "The API docs have a broken endpoint example. What do you do?", "options": ["Leave it — devs will figure it out", "Fix the example + add a test case", "Remove the example entirely", "Add a TODO comment"], "correct": "Fix the example + add a test case"},
                {"prompt": "Stakeholders want release notes for a technical patch. Best format?", "options": ["Raw git log dump", "Plain-language summary with impact bullets", "Full architecture diagram", "Nothing — skip release notes"], "correct": "Plain-language summary with impact bullets"},
                {"prompt": "Your docs site has 404s after a migration. First action?", "options": ["Ignore them", "Set up redirects + fix internal links", "Delete the broken pages", "Wait for user reports"], "correct": "Set up redirects + fix internal links"},
            ],
        },
    },
    "writer": {
        "quick_pick": {
            "variants": [
                {"prompt": "Your protagonist has no motivation. Which fix works best?", "options": ["Add a tragic backstory", "Give them a clear goal + stakes", "Kill them off", "Make them passive"], "correct": "Give them a clear goal + stakes"},
                {"prompt": "Your middle chapter is dragging. Best solution?", "options": ["Cut it entirely", "Add a subplot complication", "Skip to the ending", "Add more description"], "correct": "Add a subplot complication"},
                {"prompt": "Beta readers say the ending feels rushed. Best fix?", "options": ["Add an epilogue", "Expand the climax with more stakes", "Leave it — they're wrong", "Add a twist villain"], "correct": "Expand the climax with more stakes"},
                {"prompt": "Your dialogue all sounds the same. Best approach?", "options": ["Give each character a speech pattern", "Remove all dialogue", "Make everyone formal", "Add more narration instead"], "correct": "Give each character a speech pattern"},
            ],
        },
    },
    "filmmaker": {
        "quick_pick": {
            "variants": [
                {"prompt": "Your indie film is over budget on day 5. Best action?", "options": ["Shut down production", "Cut 2 scenes + negotiate rates", "Ask crew to work free", "Max out credit cards"], "correct": "Cut 2 scenes + negotiate rates"},
                {"prompt": "The lead actor keeps breaking character. Best approach?", "options": ["Fire them on the spot", "Take a 10-min break + reset", "Yell at them", "Rewrite their lines"], "correct": "Take a 10-min break + reset"},
                {"prompt": "Your only camera battery dies mid-take. Best action?", "options": ["Cancel the shoot day", "Switch to phone B-cam for coverage", "Wait 4 hours to recharge", "Steal power from a nearby shop"], "correct": "Switch to phone B-cam for coverage"},
                {"prompt": "Post-production color grading looks off. Best fix?", "options": ["Release it as-is", "Re-grade with LUT + match shots", "Make it black and white", "Add Instagram filters"], "correct": "Re-grade with LUT + match shots"},
            ],
        },
    },
    "sculptor": {
        "quick_pick": {
            "variants": [
                {"prompt": "The gallery wants a centerpiece but your clay is too wet. Best solution?", "options": ["Use it anyway", "Switch to plaster for a quick cast", "Cancel the show", "Soak it longer"], "correct": "Switch to plaster for a quick cast"},
                {"prompt": "Your bronze cast has air bubbles on the surface. Best fix?", "options": ["Sell it as 'textured'", "Grind + re-weld the bubbles", "Melt and recast", "Paint over them"], "correct": "Grind + re-weld the bubbles"},
                {"prompt": "A client wants a life-size statue in 2 weeks. Best response?", "options": ["Agree and rush it", "Propose a maquette first + negotiate timeline", "Decline entirely", "Hire 5 assistants overnight"], "correct": "Propose a maquette first + negotiate timeline"},
            ],
        },
    },
    "tattoo_artist": {
        "quick_pick": {
            "variants": [
                {"prompt": "Client wants a face tattoo but it's their first. Best response?", "options": ["Refuse and suggest a different placement", "Do it no questions asked", "Charge triple", "Ask for a deposit first"], "correct": "Refuse and suggest a different placement"},
                {"prompt": "The ink keeps spitting during lining. Most likely cause?", "options": ["Bad ink consistency", "Needle too far out of tube", "Client moving", "Machine running too slow"], "correct": "Needle too far out of tube"},
                {"prompt": "Client wants to cover an ex's name with a butterfly. Best approach?", "options": ["Just tattoo over it", "Laser consult first + design with heavy coverage", "Refuse — too risky", "Use white ink first"], "correct": "Laser consult first + design with heavy coverage"},
            ],
        },
    },
    "dj": {
        "quick_pick": {
            "variants": [
                {"prompt": "The dance floor clears after your track. What do you play next?", "options": ["Slower track to chill", "Familiar crowd-pleaser to bring them back", "Same genre louder", "Take a break"], "correct": "Familiar crowd-pleaser to bring them back"},
                {"prompt": "Your laptop freezes mid-set. Best action?", "options": ["Panic", "Switch to USB backup + keep the vibe going", "Silence", "Restart in front of everyone"], "correct": "Switch to USB backup + keep the vibe going"},
                {"prompt": "The crowd requests a song that kills the mood. Best response?", "options": ["Play it anyway", "Tease it briefly then transition out", "Refuse rudely", "Play it at the end"], "correct": "Tease it briefly then transition out"},
            ],
        },
    },
    "director": {
        "quick_pick": {
            "variants": [
                {"prompt": "Two lead actors hate each other and won't rehearse together. Best action?", "options": ["Fire one actor", "Rehearse separately + block scenes together on set", "Cancel the film", "Let them fight it out"], "correct": "Rehearse separately + block scenes together on set"},
                {"prompt": "The weather ruins your exterior shoot day. Best decision?", "options": ["Send everyone home", "Move to interior scenes on the schedule", "Shoot in the rain anyway", "Cancel the production"], "correct": "Move to interior scenes on the schedule"},
                {"prompt": "Your editor's first cut is 4 hours long. Best action?", "options": ["Release as a director's cut", "Kill your darlings — cut to 2hr", "Split into two films", "Add an intermission"], "correct": "Kill your darlings — cut to 2hr"},
            ],
        },
    },
    "novelist": {
        "quick_pick": {
            "variants": [
                {"prompt": "Your publisher wants a sequel but you've run out of ideas. Best strategy?", "options": ["Write a prequel instead", "Force a sequel with new conflict", "Decline the contract", "Copy the first book's plot"], "correct": "Write a prequel instead"},
                {"prompt": "Writer's block hits at chapter 7. Best approach?", "options": ["Wait for inspiration", "Skip ahead to a scene you're excited about", "Force words out", "Abandon the project"], "correct": "Skip ahead to a scene you're excited about"},
                {"prompt": "Your villain is too one-dimensional. Best fix?", "options": ["Make them purely evil", "Give them a relatable motivation", "Remove the villain", "Add a twist villain above them"], "correct": "Give them a relatable motivation"},
            ],
        },
    },
    "jeweler": {
        "quick_pick": {
            "variants": [
                {"prompt": "A customer brings in a ring that's too thin and bending. Best recommendation?", "options": ["Resize it smaller", "Re-shank with thicker metal", "Glue the bend", "Sell them a new ring only"], "correct": "Re-shank with thicker metal"},
                {"prompt": "A diamond looks cloudy under loupe. Most likely issue?", "options": ["Normal for this grade", "Inclusion cloud or treatment", "Dirty stone", "Lighting issue"], "correct": "Inclusion cloud or treatment"},
                {"prompt": "Client wants a custom pendant in 3 days. Best response?", "options": ["Rush it and risk errors", "Explain the process + offer 2-week timeline", "Decline", "3D print a rough version first"], "correct": "Explain the process + offer 2-week timeline"},
            ],
        },
    },
    "potter": {
        "quick_pick": {
            "variants": [
                {"prompt": "Your glaze came out blotchy after firing. Most likely cause?", "options": ["Kiln too hot", "Uneven glaze application", "Clay too dry", "Wrong clay type"], "correct": "Uneven glaze application"},
                {"prompt": "A pot cracked during bisque firing. What went wrong?", "options": ["Kiln ramped too fast", "Pot was too thick", "Air bubbles trapped", "All of the above are possible"], "correct": "All of the above are possible"},
                {"prompt": "Customer wants matching mugs but your clay body is different. Best action?", "options": ["Use the old clay anyway", "Make test tiles + adjust glaze to match", "Refuse the order", "Paint them to match"], "correct": "Make test tiles + adjust glaze to match"},
            ],
        },
    },
    "stunt_double": {
        "quick_pick": {
            "variants": [
                {"prompt": "The lead actor wants to do their own fall. Stunt coordinator says no. Best action?", "options": ["Let the actor do it", "Explain the risk + perform the stunt yourself", "Walk off set", "Let the director decide"], "correct": "Explain the risk + perform the stunt yourself"},
                {"prompt": "Your landing mat has a soft spot. Best action before the stunt?", "options": ["Jump around it", "Replace or reposition the mat", "Do the stunt anyway", "Stack pads on top"], "correct": "Replace or reposition the mat"},
                {"prompt": "Fire gag goes wrong — extra fuel on your sleeve. Best reaction?", "options": ["Keep performing", "Stop, drop, roll, signal safety team", "Run to water", "Take off the jacket while running"], "correct": "Stop, drop, roll, signal safety team"},
            ],
        },
    },
    "delivery": {
        "quick_pick": {
            "variants": [
                {"prompt": "A package is marked fragile but the route is all bumpy back roads. Best action?", "options": ["Drive fast to get it over with", "Take the longer highway route", "Refuse the delivery", "Repackage with extra padding"], "correct": "Take the longer highway route"},
                {"prompt": "Customer isn't home and the package needs a signature. Best action?", "options": ["Leave it at the door", "Leave a notice + attempt redelivery tomorrow", "Open it to check contents", "Take it back and mark undeliverable"], "correct": "Leave a notice + attempt redelivery tomorrow"},
                {"prompt": "You have 12 packages but only 20 minutes left on your shift. Best strategy?", "options": ["Rush and risk errors", "Prioritize by deadline + notify dispatch about overflow", "Skip the furthest ones", "Abandon the route"], "correct": "Prioritize by deadline + notify dispatch about overflow"},
            ],
        },
    },
    "pilot": {
        "quick_pick": {
            "variants": [
                {"prompt": "ATC reports wind shear on final approach. Best action?", "options": ["Continue approach", "Go around and hold", "Land faster", "Switch runways without clearance"], "correct": "Go around and hold"},
                {"prompt": "Engine failure at 500ft after takeoff. Best action?", "options": ["Turn back to the airport", "Fly straight ahead + land ahead", "Climb on remaining engine", "Declare emergency and circle"], "correct": "Fly straight ahead + land ahead"},
                {"prompt": "Passenger has a medical emergency mid-flight. Best action?", "options": ["Continue to destination", "Divert to nearest suitable airport + request medics", "Land immediately anywhere", "Ask if there's a doctor on board only"], "correct": "Divert to nearest suitable airport + request medics"},
            ],
        },
    },
    "truck_driver": {
        "quick_pick": {
            "variants": [
                {"prompt": "Your trailer starts jackknifing on ice. Best corrective action?", "options": ["Brake hard", "Steer into the skid + ease off throttle", "Accelerate", "Steer away sharply"], "correct": "Steer into the skid + ease off throttle"},
                {"prompt": "You've been driving 10 hours and feel drowsy. Best action?", "options": ["Push through it", "Pull over and take a 30-min nap", "Drink energy drinks", "Open the window"], "correct": "Pull over and take a 30-min nap"},
                {"prompt": "Tire blowout on the rear trailer axle. Best action?", "options": ["Brake hard", "Keep steering straight + ease off gas + pull over", "Swerve to the shoulder fast", "Accelerate to maintain control"], "correct": "Keep steering straight + ease off gas + pull over"},
            ],
        },
    },
    "bus_driver": {
        "quick_pick": {
            "variants": [
                {"prompt": "A wheelchair passenger needs to board but the ramp is stuck. Best action?", "options": ["Tell them to take another bus", "Call dispatch for a replacement vehicle", "Lift them manually", "Skip the stop"], "correct": "Call dispatch for a replacement vehicle"},
                {"prompt": "A fight breaks out between passengers. Best action?", "options": ["Ignore it", "Pull over safely + call dispatch + ask them to stop", "Physically intervene", "Kick everyone off"], "correct": "Pull over safely + call dispatch + ask them to stop"},
                {"prompt": "Heavy fog reduces visibility to 50ft on your route. Best action?", "options": ["Continue at normal speed", "Slow down + use hazards + use fog lights", "Stop in the middle of the road", "Take a different route without checking"], "correct": "Slow down + use hazards + use fog lights"},
            ],
        },
    },
    "forklift": {
        "quick_pick": {
            "variants": [
                {"prompt": "A pallet is stacked unevenly and tilting. Best action before lifting?", "options": ["Lift it fast before it falls", "Restack the pallet first", "Drag it instead", "Get a bigger forklift"], "correct": "Restack the pallet first"},
                {"prompt": "Your view is blocked by a tall load. Best driving technique?", "options": ["Honk and go fast", "Drive in reverse or use a spotter", "Guess the path", "Stack it lower on the forks"], "correct": "Drive in reverse or use a spotter"},
                {"prompt": "The forklift tips slightly on a ramp with a load. Best correction?", "options": ["Jump off", "Lower the load + lean into the tilt + reverse slowly", "Brake hard", "Accelerate up the ramp"], "correct": "Lower the load + lean into the tilt + reverse slowly"},
            ],
        },
    },
    "warehouse": {
        "quick_pick": {
            "variants": [
                {"prompt": "You find a damaged chemical drum leaking in aisle 7. First action?", "options": ["Clean it with a mop", "Evacuate the area + call hazmat", "Move it outside", "Ignore it — not your job"], "correct": "Evacuate the area + call hazmat"},
                {"prompt": "The WMS shows 200 units but you count 180. Best action?", "options": ["Trust the system", "Report the discrepancy + recount", "Adjust the system yourself", "Ignore the difference"], "correct": "Report the discrepancy + recount"},
                {"prompt": "A co-worker is not wearing their safety harness in the high bay. Best action?", "options": ["Mind your own business", "Remind them + report if they refuse", "Join them", "Take a photo for laughs"], "correct": "Remind them + report if they refuse"},
            ],
        },
    },
    "courier": {
        "quick_pick": {
            "prompt": "Recipient refuses delivery and the package is perishable. Best action?",
            "options": ["Leave it at the door", "Return to depot + notify sender", "Throw it away", "Open it yourself"],
            "correct": "Return to depot + notify sender",
        },
    },
    "subway_op": {
        "quick_pick": {
            "prompt": "Someone is on the tracks ahead of your train. Best action?",
            "options": ["Honk and continue", "Emergency brake + call control", "Switch tracks", "Slow down slightly"],
            "correct": "Emergency brake + call control",
        },
    },
    "tram_driver": {
        "quick_pick": {
            "prompt": "A car is blocking the tram tracks at an intersection. Best action?",
            "options": ["Push through the car", "Stop and call traffic control", "Go around on the wrong track", "Honk until they move"],
            "correct": "Stop and call traffic control",
        },
    },
    "logistics_mgr": {
        "quick_pick": {
            "prompt": "A key supplier just went bankrupt mid-contract. Best immediate action?",
            "options": ["Panic", "Activate backup supplier + reroute shipments", "Wait and see", "Sue the supplier"],
            "correct": "Activate backup supplier + reroute shipments",
        },
    },
    "cargo_pilot": {
        "quick_pick": {
            "prompt": "Cargo shift alarm goes off mid-flight. Best action?",
            "options": ["Ignore it", "Slow down + level wings + return to departure", "Open cargo door", "Continue to destination"],
            "correct": "Slow down + level wings + return to departure",
        },
    },
    "helicopter_pilot": {
        "quick_pick": {
            "prompt": "Engine RPM drops suddenly during a mountain rescue. Best action?",
            "options": ["Climb harder", "Enter autorotation + mayday", "Land on the mountain", "Restart engine in flight"],
            "correct": "Enter autorotation + mayday",
        },
    },
    "bike_courier": {
        "quick_pick": {
            "prompt": "A car door opens in your path during a delivery sprint. Best evasive action?",
            "options": ["Swerve into traffic", "Brake hard + brace", "Hop the curb", "Lean into the door"],
            "correct": "Hop the curb",
        },
    },
    "tow_truck": {
        "quick_pick": {
            "prompt": "The car you're towing has a damaged transmission. Best towing method?",
            "options": ["Flatbed tow", "Hook and chain", "Wheel lift", "Drag it"],
            "correct": "Flatbed tow",
        },
    },
    "supply_chain": {
        "quick_pick": {
            "prompt": "Tariffs just doubled on your primary import source. Best strategy?",
            "options": ["Absorb the cost", "Diversify suppliers to tariff-free regions", "Raise prices 100%", "Stop importing"],
            "correct": "Diversify suppliers to tariff-free regions",
        },
    },
    "test_pilot": {
        "quick_pick": {
            "prompt": "At 15,000ft the test aircraft's fly-by-wire system fails. Best action?",
            "options": ["Continue the test envelope", "Switch to backup analog controls + land", "Eject immediately", "Reboot the system in flight"],
            "correct": "Switch to backup analog controls + land",
        },
    },

}

# ═══════════════════════════════════════════════════════════════
# 3RD DISTINCT MINIGAME — 30 jobs that had duplicate quick_pick
# Each gets a unique minigame type that fits the job thematically
# Stored in separate dict to avoid key collision with EXTRA_CONTENT
# ═══════════════════════════════════════════════════════════════

THIRD_CONTENT = {
    # ─── Creative jobs: add spot_error, pattern, memory, timing, match_pairs, sequence ───

    "tech_writer": {
        "spot_error": {
            "prompt": "Find the error in this API documentation:",
            "correct_sequence": ["Endpoint URL", "HTTP method", "Parameters", "Request body", "Response codes", "Example"],
            "presented_sequence": ["Endpoint URL", "HTTP method", "Response codes", "Parameters", "Request body", "Example"],
        },
    },
    "writer": {
        "pattern": {
            "prompt": "Story beat pattern: Setup, Inciting incident, Rising action, Midpoint, ?, Climax, Resolution",
            "sequence": ["Setup", "Inciting incident", "Rising action", "Midpoint", "?", "Climax", "Resolution"],
            "answer": "All is lost",
        },
    },
    "filmmaker": {
        "match_pairs": {
            "prompt": "Match each shot type to its purpose:",
            "pairs": [("Extreme close-up", "Show intense emotion"), ("Wide shot", "Establish location"), ("Over-the-shoulder", "Dialogue intimacy"), ("Tracking shot", "Follow action")],
        },
    },
    "sculptor": {
        "pattern": {
            "prompt": "Sculpture process pattern: Sketch, Maquette, Armature, Base clay, Refine, ?, Fire, Finish",
            "sequence": ["Sketch", "Maquette", "Armature", "Base clay", "Refine", "?", "Fire", "Finish"],
            "answer": "Dry slowly",
        },
    },
    "tattoo_artist": {
        "memory": {
            "prompt": "Memorize the stencil placement sequence for a sleeve tattoo:",
            "items": ["Wrist anchor", "Forearm center", "Inner elbow transition", "Bicep main", "Shoulder cap"],
        },
    },
    "comedian": {
        "timing": {
            "prompt": "Hit the punchline on the beat! Click when the spotlight flashes.",
            "beats": 3,
        },
    },
    "dj": {
        "match_pairs": {
            "prompt": "Match each BPM range to its genre:",
            "pairs": [("60-90 BPM", "Hip-hop"), ("120-130 BPM", "House"), ("140-150 BPM", "Dubstep"), ("174 BPM", "Drum & bass")],
        },
    },
    "director": {
        "multi_stage": {
            "prompt": "Run a full production day:",
            "stages": [
                {"type": "quick_pick", "prompt": "6am call sheet: crew short 2 grips. Action?", "options": ["Cancel the day", "Redistribute crew + start late 30min", "Hire day-players", "Shoot without grips"], "correct": "Redistribute crew + start late 30min"},
                {"type": "sequence", "prompt": "Block the scene in order:", "items": ["Set marks", "Rehearse actors", "Light the set", "Final hair/makeup", "Roll camera"], "order": ["Set marks", "Rehearse actors", "Light the set", "Final hair/makeup", "Roll camera"]},
                {"type": "quick_pick", "prompt": "Actor refuses to do a stunt. Best action?", "options": ["Force them", "Use stunt double", "Cut the stunt", "Rewrite the scene"], "correct": "Use stunt double"},
            ],
        },
    },
    "novelist": {
        "sequence": {
            "prompt": "Outline your novel in the correct narrative order:",
            "items": ["Ordinary world", "Inciting incident", "Refusal of call", "Meeting mentor", "Crossing threshold", "Tests & allies", "Ordeal", "Reward", "The road back", "Resurrection", "Return with elixir"],
            "order": ["Ordinary world", "Inciting incident", "Refusal of call", "Meeting mentor", "Crossing threshold", "Tests & allies", "Ordeal", "Reward", "The road back", "Resurrection", "Return with elixir"],
        },
    },
    "jeweler": {
        "pattern": {
            "prompt": "Prong setting pattern: Measure, Cut seat, File, Seat stone, Bend prong 1, ?, Bend prong 3, Bend prong 4, Polish",
            "sequence": ["Measure", "Cut seat", "File", "Seat stone", "Bend prong 1", "?", "Bend prong 3", "Bend prong 4", "Polish"],
            "answer": "Bend prong 2",
        },
    },
    "potter": {
        "match_pairs": {
            "prompt": "Match each glaze type to its firing temperature:",
            "pairs": [("Raku", "1800°F (fast cool)"), ("Earthenware", "1900°F"), ("Stoneware", "2200°F"), ("Porcelain", "2400°F")],
        },
    },
    "stunt_double": {
        "pattern": {
            "prompt": "Fight choreography pattern: Jab, Cross, Hook, Dodge, Uppercut, Roll, ?, Reset stance",
            "sequence": ["Jab", "Cross", "Hook", "Dodge", "Uppercut", "Roll", "?", "Reset stance"],
            "answer": "Sweep kick",
        },
    },

    # ─── Transport jobs: add sort, timing, sequence, precision, budget, route_plan ───

    "delivery": {
        "sort": {
            "prompt": "Sort packages by delivery priority:",
            "items": ["Overnight (before 10am)", "Express (before noon)", "Standard (by 5pm)", "Economy (by 8pm)", "Pickup (hold for customer)"],
            "order": ["Overnight (before 10am)", "Express (before noon)", "Standard (by 5pm)", "Economy (by 8pm)", "Pickup (hold for customer)"],
        },
    },
    "pilot": {
        "timing": {
            "prompt": "Rotate at Vr — click exactly when the airspeed indicator hits the rotation speed!",
            "beats": 1,
        },
    },
    "truck_driver": {
        "sort": {
            "prompt": "Sort cargo by unloading order (last stop first):",
            "items": ["Stop D (furthest)", "Stop C", "Stop B", "Stop A (nearest)"],
            "order": ["Stop D (furthest)", "Stop C", "Stop B", "Stop A (nearest)"],
        },
    },
    "taxi_driver": {
        "sort": {
            "prompt": "Sort pickups by proximity for maximum efficiency:",
            "items": ["Pickup 1 (2 blocks north)", "Pickup 2 (5 blocks east)", "Pickup 3 (8 blocks south)", "Pickup 4 (12 blocks west)"],
            "order": ["Pickup 1 (2 blocks north)", "Pickup 2 (5 blocks east)", "Pickup 3 (8 blocks south)", "Pickup 4 (12 blocks west)"],
        },
    },
    "bus_driver": {
        "sort": {
            "prompt": "Sort passenger requests by stop order on Route 7:",
            "items": ["Stop 23 (downtown)", "Stop 15 (midtown)", "Stop 8 (university)", "Stop 3 (suburbs)"],
            "order": ["Stop 3 (suburbs)", "Stop 8 (university)", "Stop 15 (midtown)", "Stop 23 (downtown)"],
        },
    },
    "forklift": {
        "sort": {
            "prompt": "Sort pallets by warehouse zone before storing:",
            "items": ["Zone A (cold storage)", "Zone B (hazardous)", "Zone C (bulk goods)", "Zone D (high-value)"],
            "order": ["Zone B (hazardous)", "Zone A (cold storage)", "Zone D (high-value)", "Zone C (bulk goods)"],
        },
    },
    "warehouse": {
        "sequence": {
            "prompt": "Process an inbound shipment in the correct order:",
            "items": ["Verify BOL", "Inspect for damage", "Count pallets", "Scan into WMS", "Assign putaway location", "Move with forklift", "Confirm placement", "Close receipt"],
            "order": ["Verify BOL", "Inspect for damage", "Count pallets", "Scan into WMS", "Assign putaway location", "Move with forklift", "Confirm placement", "Close receipt"],
        },
    },
    "courier": {
        "sort": {
            "prompt": "Sort deliveries by deadline urgency:",
            "items": ["Legal docs (court in 1hr)", "Medical samples (lab in 2hr)", "Parts order (factory in 3hr)", "Retail package (anytime today)"],
            "order": ["Legal docs (court in 1hr)", "Medical samples (lab in 2hr)", "Parts order (factory in 3hr)", "Retail package (anytime today)"],
        },
    },
    "subway_op": {
        "sequence": {
            "prompt": "Execute the morning start-up sequence for a subway train:",
            "items": ["Pre-trip inspection", "Power up cab", "Test brakes", "Check signal lights", "Test doors", "Announce service", "Depart on schedule"],
            "order": ["Pre-trip inspection", "Power up cab", "Test brakes", "Check signal lights", "Test doors", "Announce service", "Depart on schedule"],
        },
    },
    "tram_driver": {
        "sequence": {
            "prompt": "Follow the tram route sequence — stops in order:",
            "items": ["Terminal A", "Market Square", "City Hall", "University", "Hospital", "Park View", "Terminal B"],
            "order": ["Terminal A", "Market Square", "City Hall", "University", "Hospital", "Park View", "Terminal B"],
        },
    },
    "logistics_mgr": {
        "budget": {
            "prompt": "Allocate $500K across transport modes to minimize total delivery time:",
            "options": ["Air freight (fast, expensive)", "Trucking (balanced)", "Rail (slow, cheap)", "Last-mile delivery"],
            "target": {"Air freight": 30, "Trucking": 40, "Rail": 15, "Last-mile delivery": 15},
        },
    },
    "cargo_pilot": {
        "precision": {
            "prompt": "Balance the cargo load to exactly 45% aft CG. Click when the gauge hits 45!",
            "target": 45,
            "tolerance": 2,
        },
    },
    "helicopter_pilot": {
        "precision": {
            "prompt": "Hold the helicopter at exactly 200ft hover altitude. Click when the altimeter hits 200!",
            "target": 200,
            "tolerance": 5,
        },
    },
    "bike_courier": {
        "timing": {
            "prompt": "Beat the traffic light cycle — click exactly when the green flashes!",
            "beats": 2,
        },
    },
    "tow_truck": {
        "sequence": {
            "prompt": "Hook up a vehicle for towing in the correct order:",
            "items": ["Assess vehicle damage", "Position truck", "Lower wheel lift", "Secure front wheels", "Attach safety chains", "Check lights", "Raise lift", "Drive away"],
            "order": ["Assess vehicle damage", "Position truck", "Lower wheel lift", "Secure front wheels", "Attach safety chains", "Check lights", "Raise lift", "Drive away"],
        },
    },
    "supply_chain": {
        "route_plan": {
            "prompt": "Plan the most cost-effective supply route — order these nodes:",
            "stops": [("Factory (origin)", "Start"), ("Port (ocean freight)", "Factory (origin)"), ("Distribution center", "Port (ocean freight)"), ("Regional warehouse", "Distribution center"), ("Retail stores", "Regional warehouse")],
        },
    },
    "test_pilot": {
        "precision": {
            "prompt": "Hold the test aircraft at exactly 3.0 Gs during the pull-up maneuver. Click when the G-meter hits 3.0!",
            "target": 30,
            "tolerance": 1,
        },
    },

    # ─── Business job: add budget ───

    "insurance": {
        "budget": {
            "prompt": "Allocate $100K across policy types to maximize portfolio balance:",
            "options": ["Auto (high volume)", "Home (stable)", "Life (long-term)", "Commercial (high margin)"],
            "target": {"Auto (high volume)": 25, "Home (stable)": 25, "Life (long-term)": 25, "Commercial (high margin)": 25},
        },
    },
}
