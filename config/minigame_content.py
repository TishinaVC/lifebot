"""
Job-specific minigame content pools for all 200 jobs.
Each job_id maps to themed content for its assigned minigame type.
This provides the actual words, sequences, patterns, etc. that make
each minigame feel unique and themed to the job.
"""

from config.minigame_content_extra import EXTRA_CONTENT

# ─── Generic fallback content ───
GENERIC = {
    "sequence": ["Step 1", "Step 2", "Step 3", "Step 4"],
    "sort": ["Item A", "Item B", "Item C", "Item D"],
    "quick_pick": ["Option A", "Option B", "Option C", "Option D"],
    "memory": ["Red", "Blue", "Green", "Yellow"],
    "match_pairs": [("A", "1"), ("B", "2"), ("C", "3")],
    "timing": [],
    "spot_error": ["The correct sequence"],
    "pattern": [1, 2, 3, 4, 5],
    "precision": [],
    "combo_lock": [3, 5, 2],
    "budget": [],
    "speed_run": ["Task 1", "Task 2", "Task 3"],
    "assembly": [("Part A", "Base"), ("Part B", "Part A"), ("Part C", "Part B")],
    "typing_race": ["Type this phrase carefully and quickly"],
    "math": [],
    "fill_blank": ["The ___ is the most important part."],
    "multi_stage": [],
    "diagnosis": [],
    "negotiation": [],
    "triage": [],
    "shift_sim": [],
    "categorize": [],
    "recipe_build": [],
    "route_plan": [],
}

# ─── Entry Level ───
JOB_CONTENT = {
    "beggar": {
        "quick_pick": {
            "prompt": "Choose the best spot to beg for maximum sympathy:",
            "options": ["Outside a fancy restaurant", "Near a bus stop", "By the ATM", "In front of the church"],
            "correct": "Outside a fancy restaurant",
        },
    },
    "busker": {
        "timing": {
            "prompt": "Play your guitar in rhythm! Click when the note aligns with the beat marker.",
            "beats": 5,
        },
    },
    "leafleter": {
        "sort": {
            "prompt": "Sort the flyers by neighborhood before distributing:",
            "items": ["Downtown flyer", "Suburb flyer", "Mall flyer", "Park flyer", "School flyer"],
            "order": ["Downtown flyer", "Mall flyer", "School flyer", "Park flyer", "Suburb flyer"],
        },
    },
    "window_washer": {
        "speed_run": {
            "prompt": "Wash all the windows before the boss arrives! Click each window to clean it.",
            "tasks": ["Window 1", "Window 2", "Window 3", "Window 4", "Window 5", "Window 6"],
        },
    },
    "dog_walker": {
        "sequence": {
            "prompt": "Walk the dogs in the correct order based on their needs:",
            "items": ["Walk Rex (energetic)", "Walk Bella (slow)", "Walk Max (quick)", "Walk Luna (long route)"],
            "order": ["Walk Rex (energetic)", "Walk Max (quick)", "Walk Luna (long route)", "Walk Bella (slow)"],
        },
    },
    "recycler": {
        "sort": {
            "prompt": "Sort items into the correct recycling bins:",
            "items": ["Plastic bottle", "Aluminum can", "Glass jar", "Paper cup", "Banana peel", "Cardboard box"],
            "categories": ["Plastic", "Metal", "Glass", "Paper", "Organic", "Paper"],
        },
    },
    "shoe_shiner": {
        "sequence": {
            "prompt": "Shine the shoes in the correct order of steps:",
            "items": ["Apply polish", "Brush off dust", "Buff with cloth", "Wipe clean", "Apply conditioner"],
            "order": ["Wipe clean", "Apply conditioner", "Apply polish", "Brush off dust", "Buff with cloth"],
        },
    },
    "newspaper": {
        "route_plan": {
            "prompt": "Plan the most efficient newspaper delivery route:",
            "stops": ["Maple St #12", "Oak Ave #45", "Pine Rd #8", "Cedar Ln #23", "Birch Dr #67"],
            "optimal": ["Pine Rd #8", "Maple St #12", "Cedar Ln #23", "Oak Ave #45", "Birch Dr #67"],
        },
    },
    "car_wash": {
        "sequence": {
            "prompt": "Wash the car in the correct order:",
            "items": ["Rinse", "Soap", "Scrub wheels", "Rinse again", "Dry", "Wax"],
            "order": ["Rinse", "Soap", "Scrub wheels", "Rinse again", "Dry", "Wax"],
        },
    },
    "trolley": {
        "sort": {
            "prompt": "Sort the trolleys by store:",
            "items": ["Green trolley (Grocery)", "Red trolley (Hardware)", "Blue trolley (Pharmacy)", "Yellow trolley (Toy store)"],
            "order": ["Blue trolley (Pharmacy)", "Green trolley (Grocery)", "Red trolley (Hardware)", "Yellow trolley (Toy store)"],
        },
    },
    "plant_waterer": {
        "quick_pick": {
            "prompt": "Which plants need watering? Pick the drooping ones:",
            "options": ["Healthy fern", "Drooping orchid", "Vibrant cactus", "Wilted lily", "Fresh succulent"],
            "correct": "Drooping orchid",
        },
    },
    "litter_picker": {
        "sort": {
            "prompt": "Sort the litter into the right bins:",
            "items": ["Candy wrapper", "Apple core", "Soda can", "Plastic bag", "Cigarette butt", "Newspaper"],
            "categories": ["General", "Organic", "Metal", "Plastic", "General", "Paper"],
        },
    },
    "sign_holder": {
        "timing": {
            "prompt": "Switch the sign to match passing traffic! Click when the arrow aligns.",
            "beats": 4,
        },
    },
    "survey_taker": {
        "quick_pick": {
            "prompt": "Ask the right survey question based on the person's demographic:",
            "options": ["Ask teen about gaming", "Ask senior about healthcare", "Ask parent about schools", "Ask worker about commute"],
            "correct": "Ask teen about gaming",
        },
    },
    "moving_helper": {
        "sequence": {
            "prompt": "Load the moving truck in the right order (heavy to light, bottom to top):",
            "items": ["Refrigerator", "Sofa", "Boxes", "Lamp", "Fragile vase"],
            "order": ["Refrigerator", "Sofa", "Boxes", "Lamp", "Fragile vase"],
        },
    },
    "ticket_tearer": {
        "quick_pick": {
            "prompt": "Validate each ticket — which one is expired?",
            "options": ["Ticket A: 7:30 PM", "Ticket B: 5:00 PM (expired)", "Ticket C: 8:00 PM", "Ticket D: 9:15 PM"],
            "correct": "Ticket B: 5:00 PM (expired)",
        },
    },
    "ice_cream": {
        "quick_pick": {
            "prompt": "The customer wants strawberry with sprinkles. Which scoop is correct?",
            "options": ["Vanilla with chocolate", "Strawberry with sprinkles", "Chocolate with nuts", "Mint with whip"],
            "correct": "Strawberry with sprinkles",
        },
    },
    "balloon_seller": {
        "memory": {
            "prompt": "Remember the balloon order from the kid: Red, Blue, Green, Yellow, Red",
            "sequence": ["Red", "Blue", "Green", "Yellow", "Red"],
        },
    },
    "parking_attend": {
        "quick_pick": {
            "prompt": "Direct the car to the correct parking zone:",
            "options": ["Zone A (Compact)", "Zone B (SUV)", "Zone C (Motorcycle)", "Zone D (Disabled)"],
            "correct": "Zone B (SUV)",
        },
    },
    "garden_helper": {
        "sort": {
            "prompt": "Sort the plants by sun/shade preference:",
            "items": ["Tomato (full sun)", "Fern (shade)", "Cactus (full sun)", "Hosta (shade)", "Basil (partial sun)"],
            "order": ["Tomato (full sun)", "Cactus (full sun)", "Basil (partial sun)", "Fern (shade)", "Hosta (shade)"],
        },
    },
    "shelf_stocker": {
        "sort": {
            "prompt": "Stock items in the correct aisle order:",
            "items": ["Cereal (Aisle 1)", "Dairy (Aisle 3)", "Bread (Aisle 2)", "Frozen (Aisle 5)", "Produce (Aisle 4)"],
            "order": ["Cereal (Aisle 1)", "Bread (Aisle 2)", "Dairy (Aisle 3)", "Produce (Aisle 4)", "Frozen (Aisle 5)"],
        },
    },
    "janitor": {
        "sequence": {
            "prompt": "Clean the building in the correct order (top to bottom):",
            "items": ["3rd floor offices", "2nd floor bathrooms", "1st floor lobby", "Basement storage"],
            "order": ["3rd floor offices", "2nd floor bathrooms", "1st floor lobby", "Basement storage"],
        },
    },
    "laundry": {
        "sort": {
            "prompt": "Sort clothes by wash temperature:",
            "items": ["White cotton (hot)", "Red shirt (cold)", "Dark jeans (cold)", "Towels (hot)", "Delicate silk (cold)"],
            "categories": ["Hot", "Cold", "Cold", "Hot", "Cold"],
        },
    },
    "food_sample": {
        "quick_pick": {
            "prompt": "Offer the right sample to the right customer type:",
            "options": ["Spicy sample for kids", "Sweet sample for adults", "Mild sample for elderly", "Sour sample for everyone"],
            "correct": "Mild sample for elderly",
        },
    },
    "cart_pusher": {
        "speed_run": {
            "prompt": "Collect all the stray carts before the manager sees!",
            "tasks": ["Cart in lot A", "Cart in lot B", "Cart in lot C", "Cart by entrance", "Cart in garden section"],
        },
    },

    # ─── Food & Service ───
    "barista": {
        "recipe_build": {
            "prompt": "Build a Latte: select ingredients in the correct order:",
            "ingredients": ["Espresso shot", "Steamed milk", "Milk foam", "Cinnamon sprinkle"],
            "order": ["Espresso shot", "Steamed milk", "Milk foam", "Cinnamon sprinkle"],
        },
    },
    "chef": {
        "sequence": {
            "prompt": "Cook Beef Wellington — follow the recipe steps in order:",
            "items": ["Sear the beef", "Wrap in mushroom duxelles", "Wrap in prosciutto", "Encase in puff pastry", "Bake at 200°C"],
            "order": ["Sear the beef", "Wrap in mushroom duxelles", "Wrap in prosciutto", "Encase in puff pastry", "Bake at 200°C"],
        },
    },
    "waiter": {
        "memory": {
            "prompt": "Remember table 5's order: Steak medium, Salad no croutons, Water no ice, Coffee with cream",
            "sequence": ["Steak medium", "Salad no croutons", "Water no ice", "Coffee with cream"],
        },
    },
    "bartender": {
        "recipe_build": {
            "prompt": "Build a Mojito: select ingredients in the correct order:",
            "ingredients": ["Muddle mint", "Add lime juice", "Add rum", "Top with soda", "Garnish with mint"],
            "order": ["Muddle mint", "Add lime juice", "Add rum", "Top with soda", "Garnish with mint"],
        },
    },
    "fast_food": {
        "speed_run": {
            "prompt": "Complete all drive-thru orders before the timer runs out!",
            "tasks": ["Burger combo", "Chicken meal", "Fries only", "Milkshake", "Ice cream cone", "Coffee"],
        },
    },
    "sushi_chef": {
        "sequence": {
            "prompt": "Make a Dragon Roll — assemble in the correct order:",
            "items": ["Prepare rice", "Cut avocado", "Slice eel", "Wrap nori", "Layer eel on top", "Torch the eel", "Drizzle sauce"],
            "order": ["Prepare rice", "Wrap nori", "Cut avocado", "Slice eel", "Layer eel on top", "Torch the eel", "Drizzle sauce"],
        },
    },
    "pastry_chef": {
        "sequence": {
            "prompt": "Bake a croissant — follow the lamination steps in order:",
            "items": ["Mix dough", "Fold in butter", "Roll and fold #1", "Roll and fold #2", "Roll and fold #3", "Shape crescents", "Bake"],
            "order": ["Mix dough", "Fold in butter", "Roll and fold #1", "Roll and fold #2", "Roll and fold #3", "Shape crescents", "Bake"],
        },
    },
    "sommelier": {
        "match_pairs": {
            "prompt": "Match each wine to its ideal food pairing:",
            "pairs": [("Cabernet Sauvignon", "Steak"), ("Chardonnay", "Salmon"), ("Pinot Noir", "Duck"), ("Riesling", "Spicy Thai")],
        },
    },
    "food_truck": {
        "quick_pick": {
            "prompt": "Three orders at once! Which one has been waiting longest?",
            "options": ["Order #1: Taco (2 min ago)", "Order #2: Burger (5 min ago)", "Order #3: Fries (1 min ago)"],
            "correct": "Order #2: Burger (5 min ago)",
        },
    },
    "caterer": {
        "sort": {
            "prompt": "Organize the catering supplies by event priority:",
            "items": ["Appetizers (urgent)", "Main course (next)", "Dessert (later)", "Drinks (urgent)", "Tableware (setup)"],
            "order": ["Tableware (setup)", "Appetizers (urgent)", "Drinks (urgent)", "Main course (next)", "Dessert (later)"],
        },
    },
    "butcher": {
        "sequence": {
            "prompt": "Break down a side of beef in the correct cutting order:",
            "items": ["Remove tenderloin", "Cut rib section", "Separate short loin", "Trim sirloin", "Cut round", "Process chuck"],
            "order": ["Remove tenderloin", "Cut rib section", "Separate short loin", "Trim sirloin", "Cut round", "Process chuck"],
        },
    },
    "baker": {
        "sequence": {
            "prompt": "Bake sourdough bread — follow the steps in order:",
            "items": ["Feed starter", "Mix autolyse", "Add salt", "Stretch & fold", "Bulk ferment", "Shape", "Proof", "Bake"],
            "order": ["Feed starter", "Mix autolyse", "Add salt", "Stretch & fold", "Bulk ferment", "Shape", "Proof", "Bake"],
        },
    },
    "host": {
        "memory": {
            "prompt": "Remember the reservation list: Party of 4 at 7pm (Smith), Party of 2 at 7:30 (Chen), Party of 6 at 8pm (Garcia)",
            "sequence": ["Party of 4 at 7pm (Smith)", "Party of 2 at 7:30 (Chen)", "Party of 6 at 8pm (Garcia)"],
        },
    },
    "barista_master": {
        "recipe_build": {
            "prompt": "Build a Caramel Macchiato: select ingredients in the correct order:",
            "ingredients": ["Vanilla syrup", "Steamed milk", "Espresso shot", "Caramel drizzle", "Milk foam"],
            "order": ["Vanilla syrup", "Steamed milk", "Milk foam", "Espresso shot", "Caramel drizzle"],
        },
    },
    "sous_chef": {
        "multi_stage": {
            "prompt": "Assist the head chef across 3 stations:",
            "stages": [
                {"type": "quick_pick", "prompt": "Which sauce goes with the fish?", "options": ["Bechamel", "Hollandaise", "Beurre blanc", "Marinara"], "correct": "Beurre blanc"},
                {"type": "sequence", "prompt": "Plate the dish in order:", "items": ["Sauce base", "Protein", "Vegetable garnish", "Microgreens"], "order": ["Sauce base", "Protein", "Vegetable garnish", "Microgreens"]},
                {"type": "quick_pick", "prompt": "Fire alarm! Which station?", "options": ["Grill station", "Dessert station", "Prep area", "Walk-in fridge"], "correct": "Grill station"},
            ],
        },
    },
    "nutritionist": {
        "quick_pick": {
            "prompt": "A diabetic client needs a low-GI meal plan. Which option is best?",
            "options": ["White rice with chicken", "Quinoa with grilled salmon", "Pasta with garlic bread", "Cereal with banana"],
            "correct": "Quinoa with grilled salmon",
        },
    },
    "food_critic": {
        "spot_error": {
            "prompt": "Find the error in this restaurant's tasting menu sequence:",
            "correct_sequence": ["Amuse-bouche", "Appetizer", "Soup", "Sorbet palate cleanser", "Main course", "Cheese plate", "Dessert"],
            "presented_sequence": ["Amuse-bouche", "Appetizer", "Main course", "Sorbet palate cleanser", "Soup", "Cheese plate", "Dessert"],
        },
    },
    "hotel_manager": {
        "shift_sim": {
            "prompt": "Manage the hotel shift — handle situations in priority order:",
            "situations": ["VIP check-in (high priority)", "Room service backlog (medium)", "Pool maintenance (low)", "Front desk queue (high)", "Staff break schedule (low)"],
            "optimal": ["VIP check-in (high priority)", "Front desk queue (high)", "Room service backlog (medium)", "Pool maintenance (low)", "Staff break schedule (low)"],
        },
    },
    "event_planner": {
        "sort": {
            "prompt": "Organize wedding tasks by deadline urgency:",
            "items": ["Confirm caterer (3 days)", "Order flowers (1 week)", "Book DJ (2 weeks)", "Send invites (1 month)", "Buy decorations (2 days)"],
            "order": ["Buy decorations (2 days)", "Confirm caterer (3 days)", "Order flowers (1 week)", "Book DJ (2 weeks)", "Send invites (1 month)"],
        },
    },
    "sommelier_master": {
        "match_pairs": {
            "prompt": "Match vintage wines to their optimal drinking years:",
            "pairs": [("1982 Bordeaux", "Now-2030"), ("1990 Burgundy", "Now-2025"), ("1997 Napa Cab", "Now-2028"), ("2000 Champagne", "Now-2035")],
        },
    },
    "mixologist": {
        "recipe_build": {
            "prompt": "Create a signature cocktail: build in the correct order:",
            "ingredients": ["Muddle berries", "Add gin", "Splash elderflower", "Add ice", "Shake", "Strain", "Top with prosecco"],
            "order": ["Muddle berries", "Add gin", "Splash elderflower", "Add ice", "Shake", "Strain", "Top with prosecco"],
        },
    },
    "chocolatier": {
        "sequence": {
            "prompt": "Craft a chocolate truffle — follow the steps in order:",
            "items": ["Temper dark chocolate", "Pour into molds", "Let set", "Make ganache filling", "Fill shells", "Cap with chocolate", "Demold", "Dust with cocoa"],
            "order": ["Temper dark chocolate", "Pour into molds", "Let set", "Make ganache filling", "Fill shells", "Cap with chocolate", "Demold", "Dust with cocoa"],
        },
    },
    "teasomm": {
        "match_pairs": {
            "prompt": "Match each tea to its ideal food pairing:",
            "pairs": [("Sencha", "Sushi"), ("Earl Grey", "Scones"), ("Pu-erh", "Dim sum"), ("Chamomile", "Shortbread")],
        },
    },
    "private_chef": {
        "multi_stage": {
            "prompt": "Prepare a 3-course meal for your VIP client:",
            "stages": [
                {"type": "quick_pick", "prompt": "Client is allergic to nuts. Which appetizer?", "options": ["Pesto bruschetta", "Caprese skewers", "Almond-crusted brie", "Peanut satay"], "correct": "Caprese skewers"},
                {"type": "sequence", "prompt": "Cook the main course in order:", "items": ["Sear scallops", "Make beurre blanc", "Plate puree", "Add scallops", "Garnish"], "order": ["Sear scallops", "Make beurre blanc", "Plate puree", "Add scallops", "Garnish"]},
                {"type": "quick_pick", "prompt": "Which dessert wine pairs with the chocolate fondant?", "options": ["Chardonnay", "Port", "Sauvignon Blanc", "Prosecco"], "correct": "Port"},
            ],
        },
    },
    "restaurateur": {
        "shift_sim": {
            "prompt": "Run Friday night service — handle issues in priority order:",
            "situations": ["Kitchen fire alarm (critical)", "VIP table arrival (high)", "Negative review threat (high)", "Supply shortage (medium)", "Staff scheduling (low)", "Social media post (low)"],
            "optimal": ["Kitchen fire alarm (critical)", "VIP table arrival (high)", "Negative review threat (high)", "Supply shortage (medium)", "Staff scheduling (low)", "Social media post (low)"],
        },
    },

    # ─── Trades & Labor ───
    "mechanic": {
        "sequence": {
            "prompt": "Replace brake pads — follow the correct repair order:",
            "items": ["Loosen lug nuts", "Jack up car", "Remove wheel", "Remove caliper", "Replace pads", "Reassemble", "Torque wheels"],
            "order": ["Loosen lug nuts", "Jack up car", "Remove wheel", "Remove caliper", "Replace pads", "Reassemble", "Torque wheels"],
        },
    },
    "electrician": {
        "sequence": {
            "prompt": "Wire a new outlet — follow safety steps in order:",
            "items": ["Turn off breaker", "Test for voltage", "Strip wires", "Connect ground", "Connect neutral", "Connect hot", "Secure outlet", "Test outlet"],
            "order": ["Turn off breaker", "Test for voltage", "Strip wires", "Connect ground", "Connect neutral", "Connect hot", "Secure outlet", "Test outlet"],
        },
    },
    "plumber": {
        "sequence": {
            "prompt": "Fix a leaky pipe under the sink — correct order:",
            "items": ["Shut off water valve", "Place bucket", "Disconnect trap", "Replace washer", "Reconnect trap", "Turn on water", "Check for leaks"],
            "order": ["Shut off water valve", "Place bucket", "Disconnect trap", "Replace washer", "Reconnect trap", "Turn on water", "Check for leaks"],
        },
    },
    "carpenter": {
        "assembly": {
            "prompt": "Build a bookshelf — assemble parts in the correct order:",
            "parts": [("Side panels", "Base"), ("Shelves", "Side panels"), ("Back panel", "Shelves"), ("Top", "Back panel"), ("Trim", "Top")],
        },
    },
    "welder": {
        "sequence": {
            "prompt": "Weld a steel joint — follow the procedure in order:",
            "items": ["Clean metal surface", "Set amperage", "Tack weld corners", "Run root pass", "Clean slag", "Run cap pass", "Inspect weld"],
            "order": ["Clean metal surface", "Set amperage", "Tack weld corners", "Run root pass", "Clean slag", "Run cap pass", "Inspect weld"],
        },
    },
    "construction": {
        "assembly": {
            "prompt": "Assemble a wall frame — put components together in order:",
            "parts": [("Bottom plate", "Foundation"), ("Studs", "Bottom plate"), ("Top plate", "Studs"), ("Header", "Top plate"), ("Sheathing", "Header")],
        },
    },
    "roofer": {
        "sequence": {
            "prompt": "Install asphalt shingles — correct order:",
            "items": ["Lay underlayment", "Install drip edge", "Apply starter strip", "Lay shingles bottom-up", "Install flashing", "Ridge cap"],
            "order": ["Install drip edge", "Lay underlayment", "Apply starter strip", "Lay shingles bottom-up", "Install flashing", "Ridge cap"],
        },
    },
    "painter": {
        "sort": {
            "prompt": "Sort paint cans by finish type for the job:",
            "items": ["Matte (ceiling)", "Eggshell (walls)", "Semi-gloss (trim)", "Gloss (doors)", "Primer (first coat)"],
            "order": ["Primer (first coat)", "Matte (ceiling)", "Eggshell (walls)", "Semi-gloss (trim)", "Gloss (doors)"],
        },
    },
    "mason": {
        "sequence": {
            "prompt": "Build a brick wall — follow the masonry steps in order:",
            "items": ["Lay mortar bed", "Place first brick", "Butter next brick", "Level and tap", "Lay course", "Check plumb", "Tool joints", "Clean excess"],
            "order": ["Lay mortar bed", "Place first brick", "Butter next brick", "Level and tap", "Lay course", "Check plumb", "Tool joints", "Clean excess"],
        },
    },
    "tiler": {
        "pattern": {
            "prompt": "Complete the tile pattern — what comes next in the sequence?",
            "sequence": ["White", "Black", "White", "Black", "White", "?"],
            "answer": "Black",
        },
    },
    "insulator": {
        "sequence": {
            "prompt": "Install wall insulation — correct order:",
            "items": ["Measure cavity", "Cut batt", "Place vapor barrier", "Insert insulation", "Seal gaps", "Install drywall"],
            "order": ["Measure cavity", "Cut batt", "Place vapor barrier", "Insert insulation", "Seal gaps", "Install drywall"],
        },
    },
    "glazier": {
        "precision": {
            "prompt": "Cut the glass to exactly 45cm. Click when the measurement hits 45!",
            "target": 45,
            "tolerance": 2,
        },
    },
    "hvac": {
        "sequence": {
            "prompt": "Install a split AC system — correct order:",
            "items": ["Mount indoor unit", "Drill wall hole", "Run refrigerant lines", "Mount outdoor unit", "Connect lines", "Vacuum system", "Release refrigerant", "Test"],
            "order": ["Mount indoor unit", "Drill wall hole", "Run refrigerant lines", "Mount outdoor unit", "Connect lines", "Vacuum system", "Release refrigerant", "Test"],
        },
    },
    "landscaper": {
        "sort": {
            "prompt": "Arrange plants by sunlight needs for the garden design:",
            "items": ["Sunflowers (full sun)", "Hostas (full shade)", "Tomatoes (full sun)", "Ferns (partial shade)", "Lavender (full sun)"],
            "categories": ["Full Sun", "Full Shade", "Full Sun", "Partial Shade", "Full Sun"],
        },
    },
    "foreman": {
        "shift_sim": {
            "prompt": "Manage the construction site — handle in priority order:",
            "situations": ["Crane safety check (critical)", "Material delivery (high)", "Crew break schedule (medium)", "Inspection prep (high)", "Tool inventory (low)"],
            "optimal": ["Crane safety check (critical)", "Inspection prep (high)", "Material delivery (high)", "Crew break schedule (medium)", "Tool inventory (low)"],
        },
    },
    "surveyor": {
        "precision": {
            "prompt": "Measure the property line to exactly 32.5m. Click when the laser hits the target!",
            "target": 32.5,
            "tolerance": 0.5,
        },
    },
    "demolition": {
        "sequence": {
            "prompt": "Demolish a wall safely — follow the correct order:",
            "items": ["Check for utilities", "Seal area", "Wear PPE", "Remove fixtures", "Start from top", "Work downward", "Clear debris"],
            "order": ["Check for utilities", "Seal area", "Wear PPE", "Remove fixtures", "Start from top", "Work downward", "Clear debris"],
        },
    },
    "scaffolder": {
        "assembly": {
            "prompt": "Build scaffolding — assemble in the correct order:",
            "parts": [("Base plates", "Ground"), ("Standards", "Base plates"), ("Ledgers", "Standards"), ("Transoms", "Ledgers"), ("Decking", "Transoms"), ("Guardrails", "Standards")],
        },
    },
    "floor_layer": {
        "sequence": {
            "prompt": "Install hardwood flooring — correct order:",
            "items": ["Acclimate wood", "Clean subfloor", "Lay underlayment", "Snap chalk line", "Lay first row", "Continue boards", "Cut door frames", "Install trim"],
            "order": ["Acclimate wood", "Clean subfloor", "Lay underlayment", "Snap chalk line", "Lay first row", "Continue boards", "Cut door frames", "Install trim"],
        },
    },
    "locksmith": {
        "combo_lock": {
            "prompt": "Pick the lock — find the correct 3-pin combination:",
            "pins": [3, 7, 5],
            "max_val": 9,
        },
    },
    "heavy_equipment": {
        "precision": {
            "prompt": "Lower the crane hook to exactly 12m. Click when the depth gauge hits 12!",
            "target": 12,
            "tolerance": 1,
        },
    },
    "steelworker": {
        "assembly": {
            "prompt": "Assemble a steel beam structure — connect in order:",
            "parts": [("Base columns", "Foundation"), ("Cross beams", "Base columns"), ("Vertical supports", "Cross beams"), ("Top beams", "Vertical supports"), ("Weld points", "Top beams")],
        },
    },
    "elevator_fix": {
        "sequence": {
            "prompt": "Repair an elevator — follow the safety procedure:",
            "items": ["Lock out power", "Open hoistway", "Inspect cables", "Replace worn sheave", "Check governor", "Test brakes", "Restore power", "Run test cycle"],
            "order": ["Lock out power", "Open hoistway", "Inspect cables", "Replace worn sheave", "Check governor", "Test brakes", "Restore power", "Run test cycle"],
        },
    },
    "solar_installer": {
        "sequence": {
            "prompt": "Install solar panels — correct order:",
            "items": ["Inspect roof", "Install mounting rails", "Attach panels", "Wire in series", "Connect inverter", "Install battery", "Connect to grid", "Test system"],
            "order": ["Inspect roof", "Install mounting rails", "Attach panels", "Wire in series", "Connect inverter", "Install battery", "Connect to grid", "Test system"],
        },
    },
    "contractor": {
        "shift_sim": {
            "prompt": "Manage the entire construction project — prioritize tasks:",
            "situations": ["Permit renewal (critical)", "Foundation pour (high)", "Supply delivery (high)", "Crew scheduling (medium)", "Client meeting (medium)", "Site cleanup (low)"],
            "optimal": ["Permit renewal (critical)", "Foundation pour (high)", "Supply delivery (high)", "Client meeting (medium)", "Crew scheduling (medium)", "Site cleanup (low)"],
        },
    },

    # ─── Medical & Science ───
    "doctor": {
        "diagnosis": {
            "prompt": "Patient presents with: fever, cough, fatigue. What's the most likely diagnosis?",
            "options": ["Common cold", "Influenza", "Pneumonia", "COVID-19"],
            "correct": "Influenza",
            "reasoning": "Fever + cough + fatigue without shortness of breath suggests influenza over pneumonia or COVID-19.",
        },
    },
    "nurse": {
        "triage": {
            "prompt": "Triage these patients — assign priority (1=most urgent):",
            "patients": ["Chest pain patient", "Broken arm patient", "Sprained ankle", "Routine checkup", "Minor cut"],
            "optimal": ["Chest pain patient", "Broken arm patient", "Minor cut", "Sprained ankle", "Routine checkup"],
        },
    },
    "paramedic": {
        "quick_pick": {
            "prompt": "Arrived at accident scene — what's your first action?",
            "options": ["Check airway", "Stop bleeding", "Call hospital", "Move patient"],
            "correct": "Check airway",
        },
    },
    "pharmacist": {
        "match_pairs": {
            "prompt": "Match each medication to its correct use:",
            "pairs": [("Amoxicillin", "Bacterial infection"), ("Ibuprofen", "Inflammation"), ("Metformin", "Diabetes"), ("Lisinopril", "Hypertension")],
        },
    },
    "dentist": {
        "spot_error": {
            "prompt": "Find the error in this dental procedure sequence:",
            "correct_sequence": ["Num area", "Isolate tooth", "Remove decay", "Etch enamel", "Apply bonding", "Place filling", "Cure", "Polish"],
            "presented_sequence": ["Num area", "Isolate tooth", "Etch enamel", "Remove decay", "Apply bonding", "Place filling", "Cure", "Polish"],
        },
    },
    "surgeon": {
        "sequence": {
            "prompt": "Perform an appendectomy — follow the surgical steps in order:",
            "items": ["Prep and drape", "Make incision", "Locate appendix", "Clamp mesoappendix", "Ligate appendix", "Remove appendix", "Irrigate cavity", "Close incision"],
            "order": ["Prep and drape", "Make incision", "Locate appendix", "Clamp mesoappendix", "Ligate appendix", "Remove appendix", "Irrigate cavity", "Close incision"],
        },
    },
    "vet": {
        "diagnosis": {
            "prompt": "Dog presents with: limping, swollen joint, reluctance to move. Diagnosis?",
            "options": ["Sprain", "Arthritis", "Hip dysplasia", "Bone fracture"],
            "correct": "Hip dysplasia",
            "reasoning": "Swollen joint + reluctance to move in a dog suggests hip dysplasia over a simple sprain.",
        },
    },
    "therapist": {
        "quick_pick": {
            "prompt": "Client with anxiety asks for coping strategies. Which approach first?",
            "options": ["Prescribe medication", "Teach breathing exercises", "Refer to psychiatrist", "Discuss childhood"],
            "correct": "Teach breathing exercises",
        },
    },
    "radiologist": {
        "spot_error": {
            "prompt": "Compare these two X-rays. Find the abnormality in the second one:",
            "normal": "Clear lung fields, no opacity",
            "abnormal": "Right lower lobe opacity — likely pneumonia",
        },
    },
    "lab_tech": {
        "sequence": {
            "prompt": "Run a blood test — follow the lab procedure in order:",
            "items": ["Label sample", "Centrifuge blood", "Load into analyzer", "Calibrate machine", "Run test", "Record results", "Clean equipment"],
            "order": ["Label sample", "Centrifuge blood", "Calibrate machine", "Load into analyzer", "Run test", "Record results", "Clean equipment"],
        },
    },
    "research_sci": {
        "multi_stage": {
            "prompt": "Conduct a research experiment across 3 stages:",
            "stages": [
                {"type": "quick_pick", "prompt": "Which control group is needed?", "options": ["Positive control", "Negative control", "Both", "Neither"], "correct": "Both"},
                {"type": "sequence", "prompt": "Set up the experiment in order:", "items": ["Prepare samples", "Add reagent", "Incubate", "Measure absorbance", "Record data"], "order": ["Prepare samples", "Add reagent", "Incubate", "Measure absorbance", "Record data"]},
                {"type": "quick_pick", "prompt": "Results show p=0.04. Significant?", "options": ["Yes (p<0.05)", "No (p>0.05)", "Inconclusive", "Need more data"], "correct": "Yes (p<0.05)"},
            ],
        },
    },
    "biologist": {
        "categorize": {
            "prompt": "Classify these organisms into the correct kingdoms:",
            "items": ["Mushroom", "Oak tree", "E. coli", "Amoeba", "Moss"],
            "categories": ["Fungi", "Plantae", "Bacteria", "Protista", "Plantae"],
        },
    },
    "chemist": {
        "sequence": {
            "prompt": "Synthesize aspirin — follow the reaction steps in order:",
            "items": ["Weigh salicylic acid", "Add acetic anhydride", "Add catalyst (H2SO4)", "Heat gently", "Cool in ice bath", "Filter crystals", "Recrystallize", "Dry product"],
            "order": ["Weigh salicylic acid", "Add acetic anhydride", "Add catalyst (H2SO4)", "Heat gently", "Cool in ice bath", "Filter crystals", "Recrystallize", "Dry product"],
        },
    },
    "physicist": {
        "math": {
            "prompt": "Calculate the force: A 5kg object accelerates at 12 m/s². F = ?",
            "answer": 60,
            "formula": "F = m × a = 5 × 12 = 60 N",
        },
    },
    "astronomer": {
        "pattern": {
            "prompt": "Complete the stellar classification sequence: O, B, A, F, G, K, ?",
            "sequence": ["O", "B", "A", "F", "G", "K", "?"],
            "answer": "M",
        },
    },
    "geneticist": {
        "match_pairs": {
            "prompt": "Match each gene to its associated trait:",
            "pairs": [("BRCA1", "Breast cancer risk"), ("CFTR", "Cystic fibrosis"), ("HBB", "Sickle cell"), ("DMD", "Muscular dystrophy")],
        },
    },
    "neurosurgeon": {
        "sequence": {
            "prompt": "Perform a craniotomy — follow the surgical steps precisely:",
            "items": ["Prep and shave", "Mark incision", "Open scalp", "Drill burr holes", "Remove bone flap", "Open dura", "Operate", "Close dura", "Replace flap", "Close scalp"],
            "order": ["Prep and shave", "Mark incision", "Open scalp", "Drill burr holes", "Remove bone flap", "Open dura", "Operate", "Close dura", "Replace flap", "Close scalp"],
        },
    },
    "cardiologist": {
        "diagnosis": {
            "prompt": "Patient: 58yo male, chest pain, radiates to left arm, diaphoretic. Diagnosis?",
            "options": ["GERD", "Myocardial infarction", "Anxiety attack", "Muscle strain"],
            "correct": "Myocardial infarction",
            "reasoning": "Chest pain radiating to left arm + diaphoresis = classic MI presentation.",
        },
    },
    "pediatrician": {
        "diagnosis": {
            "prompt": "3-year-old with: rash, fever, runny nose. What's the diagnosis?",
            "options": ["Chickenpox", "Measles", "Hand-foot-mouth", "Roseola"],
            "correct": "Measles",
            "reasoning": "Rash + fever + runny nose in a toddler is classic measles presentation.",
        },
    },
    "optometrist": {
        "quick_pick": {
            "prompt": "Patient reads line at 20/40. What's the correct prescription action?",
            "options": ["No prescription needed", "Prescribe -1.00 diopters", "Refer to ophthalmologist", "Prescribe reading glasses"],
            "correct": "Prescribe -1.00 diopters",
        },
    },
    "physical_ther": {
        "sequence": {
            "prompt": "Guide a patient through knee rehab — correct exercise order:",
            "items": ["Ice therapy", "Range of motion", "Strengthening", "Balance training", "Functional training", "Sport-specific drills"],
            "order": ["Ice therapy", "Range of motion", "Strengthening", "Balance training", "Functional training", "Sport-specific drills"],
        },
    },
    "med_researcher": {
        "multi_stage": {
            "prompt": "Develop a new treatment across 3 research phases:",
            "stages": [
                {"type": "quick_pick", "prompt": "Which model organism for initial testing?", "options": ["E. coli", "C. elegans", "Mouse", "Human volunteers"], "correct": "Mouse"},
                {"type": "sequence", "prompt": "Design the clinical trial in order:", "items": ["Phase 1 (safety)", "Phase 2 (efficacy)", "Phase 3 (large scale)", "FDA approval", "Phase 4 (monitoring)"], "order": ["Phase 1 (safety)", "Phase 2 (efficacy)", "Phase 3 (large scale)", "FDA approval", "Phase 4 (monitoring)"]},
                {"type": "quick_pick", "prompt": "Trial shows 30% efficacy. Publish?", "options": ["Yes, significant", "No, too low", "Need larger sample", "Abandon project"], "correct": "Need larger sample"},
            ],
        },
    },
    "epidemiologist": {
        "pattern": {
            "prompt": "Track the outbreak: Day 1: 2 cases, Day 2: 4, Day 3: 8, Day 4: 16, Day 5: ?",
            "sequence": ["2", "4", "8", "16", "?"],
            "answer": "32",
        },
    },
    "toxicologist": {
        "match_pairs": {
            "prompt": "Match each toxin to its antidote:",
            "pairs": [("Arsenic", "Dimercaprol"), ("Cyanide", "Hydroxocobalamin"), ("Acetaminophen", "N-acetylcysteine"), ("Lead", "EDTA")],
        },
    },
    "astronaut": {
        "multi_stage": {
            "prompt": "Complete the space station mission across 3 critical stages:",
            "stages": [
                {"type": "sequence", "prompt": "Pre-launch checklist in order:", "items": ["Suit up", "Strap in", "Comm check", "Engine ignition", "Liftoff"], "order": ["Suit up", "Strap in", "Comm check", "Engine ignition", "Liftoff"]},
                {"type": "quick_pick", "prompt": "Docking approach — when to fire thrusters?", "options": ["At 100m", "At 10m", "At contact", "Never"], "correct": "At 10m"},
                {"type": "sequence", "prompt": "EVA repair steps in order:", "items": ["Depressurize airlock", "Exit station", "Reach repair site", "Fix antenna", "Return to airlock", "Repressurize"], "order": ["Depressurize airlock", "Exit station", "Reach repair site", "Fix antenna", "Return to airlock", "Repressurize"]},
            ],
        },
    },

    # ─── Tech & IT ───
    "programmer": {
        "spot_error": {
            "prompt": "Find the bug in this Python code:",
            "correct_code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
            "buggy_code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n)",
        },
    },
    "it_support": {
        "quick_pick": {
            "prompt": "User says 'my computer won't turn on.' First troubleshooting step?",
            "options": ["Reinstall Windows", "Check power cable", "Replace motherboard", "Update drivers"],
            "correct": "Check power cable",
        },
    },
    "web_dev": {
        "assembly": {
            "prompt": "Build a web page — assemble components in the correct order:",
            "parts": [("HTML structure", "Base"), ("CSS styling", "HTML structure"), ("JavaScript logic", "CSS styling"), ("API integration", "JavaScript logic"), ("Deploy", "API integration")],
        },
    },
    "data_analyst": {
        "pattern": {
            "prompt": "Sales data: Jan 100, Feb 120, Mar 144, Apr 172. What's the growth pattern?",
            "sequence": ["100", "120", "144", "172", "?"],
            "answer": "206",
        },
    },
    "sysadmin": {
        "sequence": {
            "prompt": "Configure a new server — follow the setup steps in order:",
            "items": ["Install OS", "Update packages", "Configure firewall", "Create users", "Set up SSH keys", "Install services", "Configure backups", "Monitor"],
            "order": ["Install OS", "Update packages", "Configure firewall", "Create users", "Set up SSH keys", "Install services", "Configure backups", "Monitor"],
        },
    },
    "ux_designer": {
        "sort": {
            "prompt": "Arrange design elements by user flow priority:",
            "items": ["Login screen (first)", "Dashboard (second)", "Settings (third)", "Profile (fourth)", "Help (last)"],
            "order": ["Login screen (first)", "Dashboard (second)", "Settings (third)", "Profile (fourth)", "Help (last)"],
        },
    },
    "game_dev": {
        "assembly": {
            "prompt": "Build a game — assemble systems in the correct order:",
            "parts": [("Engine setup", "Base"), ("Physics system", "Engine setup"), ("Rendering pipeline", "Physics system"), ("Game logic", "Rendering pipeline"), ("UI system", "Game logic"), ("Audio", "UI system")],
        },
    },
    "data_scientist": {
        "math": {
            "prompt": "Calculate accuracy: 85 correct predictions out of 100 total. Accuracy = ?%",
            "answer": 85,
            "formula": "Accuracy = correct / total × 100 = 85/100 × 100 = 85%",
        },
    },
    "devops": {
        "sequence": {
            "prompt": "Deploy a microservice — follow the CI/CD pipeline in order:",
            "items": ["Push code", "Run tests", "Build Docker image", "Push to registry", "Deploy to staging", "Run e2e tests", "Deploy to production", "Monitor logs"],
            "order": ["Push code", "Run tests", "Build Docker image", "Push to registry", "Deploy to staging", "Run e2e tests", "Deploy to production", "Monitor logs"],
        },
    },
    "security_analyst": {
        "spot_error": {
            "prompt": "Find the vulnerability in this authentication code:",
            "correct_code": "if hash(password) == stored_hash:\n    grant_access()",
            "buggy_code": "if password == stored_password:\n    grant_access()",
        },
    },
    "mobile_dev": {
        "assembly": {
            "prompt": "Build a mobile app — assemble layers in order:",
            "parts": [("Project setup", "Base"), ("UI components", "Project setup"), ("State management", "UI components"), ("API layer", "State management"), ("Push notifications", "API layer"), ("Publish to store", "Push notifications")],
        },
    },
    "ai_engineer": {
        "sequence": {
            "prompt": "Build and train a neural network — correct order:",
            "items": ["Prepare dataset", "Define model architecture", "Compile model", "Set hyperparameters", "Train model", "Validate", "Tune hyperparameters", "Deploy model"],
            "order": ["Prepare dataset", "Define model architecture", "Compile model", "Set hyperparameters", "Train model", "Validate", "Tune hyperparameters", "Deploy model"],
        },
    },
    "cloud_arch": {
        "assembly": {
            "prompt": "Design cloud infrastructure — assemble in order:",
            "parts": [("VPC network", "Base"), ("Subnets", "VPC network"), ("Load balancer", "Subnets"), ("Auto-scaling group", "Load balancer"), ("Database cluster", "Auto-scaling group"), ("CDN", "Database cluster")],
        },
    },
    "blockchain_dev": {
        "sequence": {
            "prompt": "Deploy a smart contract — follow the steps in order:",
            "items": ["Write contract", "Test locally", "Audit code", "Compile to bytecode", "Deploy to testnet", "Verify on testnet", "Deploy to mainnet", "Verify on Etherscan"],
            "order": ["Write contract", "Test locally", "Audit code", "Compile to bytecode", "Deploy to testnet", "Verify on testnet", "Deploy to mainnet", "Verify on Etherscan"],
        },
    },
    "qa_tester": {
        "spot_error": {
            "prompt": "Find the bug in this test output:",
            "expected": "Test login_valid: PASSED\nTest login_empty: PASSED\nTest login_wrong_pass: FAILED\nTest login_sql_injection: PASSED",
            "actual": "Test login_valid: PASSED\nTest login_empty: PASSED\nTest login_wrong_pass: PASSED\nTest login_sql_injection: PASSED",
        },
    },
    "tech_writer": {
        "fill_blank": {
            "prompt": "Complete the documentation: 'To install the package, run ___ in your terminal.'",
            "answer": "npm install",
            "context": "The missing command is the standard npm install command.",
        },
    },
    "product_manager": {
        "shift_sim": {
            "prompt": "Manage product development sprint — prioritize in order:",
            "situations": ["Critical bug (critical)", "Sprint planning (high)", "User feedback review (medium)", "Stakeholder update (medium)", "Competitor analysis (low)", "Team lunch (low)"],
            "optimal": ["Critical bug (critical)", "Sprint planning (high)", "User feedback review (medium)", "Stakeholder update (medium)", "Competitor analysis (low)", "Team lunch (low)"],
        },
    },
    "db_admin": {
        "sequence": {
            "prompt": "Optimize a database — follow the maintenance steps in order:",
            "items": ["Backup database", "Analyze slow queries", "Add indexes", "Update statistics", "Rebuild fragmented indexes", "Test performance", "Schedule regular maintenance"],
            "order": ["Backup database", "Analyze slow queries", "Add indexes", "Update statistics", "Rebuild fragmented indexes", "Test performance", "Schedule regular maintenance"],
        },
    },
    "network_eng": {
        "assembly": {
            "prompt": "Build a network infrastructure — assemble in order:",
            "parts": [("Router config", "Base"), ("Switch setup", "Router config"), ("VLANs", "Switch setup"), ("Firewall rules", "VLANs"), ("VPN tunnel", "Firewall rules"), ("Monitoring", "VPN tunnel")],
        },
    },
    "frontend_dev": {
        "assembly": {
            "prompt": "Build a React app — assemble in order:",
            "parts": [("HTML template", "Base"), ("React components", "HTML template"), ("State hooks", "React components"), ("API calls", "State hooks"), ("Styling", "API calls"), ("Testing", "Styling")],
        },
    },
    "backend_dev": {
        "assembly": {
            "prompt": "Build a REST API — assemble in order:",
            "parts": [("Express server", "Base"), ("Routes", "Express server"), ("Controllers", "Routes"), ("Models", "Controllers"), ("Middleware", "Models"), ("Database connection", "Middleware")],
        },
    },
    "pentester": {
        "sequence": {
            "prompt": "Conduct a penetration test — follow the methodology in order:",
            "items": ["Reconnaissance", "Scanning", "Vulnerability assessment", "Exploitation", "Post-exploitation", "Cover tracks", "Write report"],
            "order": ["Reconnaissance", "Scanning", "Vulnerability assessment", "Exploitation", "Post-exploitation", "Cover tracks", "Write report"],
        },
    },
    "ml_engineer": {
        "sequence": {
            "prompt": "Deploy an ML model to production — correct order:",
            "items": ["Export trained model", "Create inference API", "Set up monitoring", "A/B test setup", "Canary deployment", "Full rollout", "Monitor drift", "Retrain schedule"],
            "order": ["Export trained model", "Create inference API", "Set up monitoring", "A/B test setup", "Canary deployment", "Full rollout", "Monitor drift", "Retrain schedule"],
        },
    },
    "cto": {
        "shift_sim": {
            "prompt": "Manage the entire tech organization — prioritize:",
            "situations": ["Security breach (critical)", "Production outage (critical)", "Hiring decisions (high)", "Architecture review (high)", "Team training (medium)", "Tech blog post (low)"],
            "optimal": ["Security breach (critical)", "Production outage (critical)", "Architecture review (high)", "Hiring decisions (high)", "Team training (medium)", "Tech blog post (low)"],
        },
    },
    "hacker": {
        "combo_lock": {
            "prompt": "Crack the security system — find the correct 4-digit access code:",
            "pins": [7, 3, 9, 1],
            "max_val": 9,
        },
    },

    # ─── Business & Finance ───
    "ceo": {
        "shift_sim": {
            "prompt": "Run the company — handle board priorities in order:",
            "situations": ["Quarterly earnings miss (critical)", "Merger opportunity (high)", "Key executive resignation (high)", "Office relocation (medium)", "Charity event (low)", "Golf with investor (low)"],
            "optimal": ["Quarterly earnings miss (critical)", "Key executive resignation (high)", "Merger opportunity (high)", "Office relocation (medium)", "Charity event (low)", "Golf with investor (low)"],
        },
    },
    "bank_teller": {
        "quick_pick": {
            "prompt": "Customer wants to deposit $500 and withdraw $200. What's the net transaction?",
            "options": ["+$300 to account", "-$300 from account", "+$700 to account", "-$700 from account"],
            "correct": "+$300 to account",
        },
    },
    "accountant": {
        "math": {
            "prompt": "Balance the books: Revenue $45,000 - Expenses $12,500 - Taxes $8,750 = ?",
            "answer": 23750,
            "formula": "45000 - 12500 - 8750 = 23750",
        },
    },
    "sales_rep": {
        "negotiation": {
            "prompt": "The client wants a 20% discount. Your target is 10%. How do you respond?",
            "options": ["Accept 20% immediately", "Offer 10% with added value", "Refuse any discount", "Offer 15% with conditions"],
            "correct": "Offer 10% with added value",
            "explanation": "Anchoring with added value preserves margin while showing flexibility.",
        },
    },
    "real_estate": {
        "quick_pick": {
            "prompt": "Which property has the best ROI potential for your client?",
            "options": ["$300k house in declining area", "$250k condo near new transit", "$500k mansion in rural area", "$200k fixer-upper with foundation issues"],
            "correct": "$250k condo near new transit",
        },
    },
    "stockbroker": {
        "pattern": {
            "prompt": "Stock pattern: Up 3%, Down 1%, Up 3%, Down 1%, Up 3%, ?",
            "sequence": ["+3%", "-1%", "+3%", "-1%", "+3%", "?"],
            "answer": "-1%",
        },
    },
    "financial_adv": {
        "budget": {
            "prompt": "Allocate $10,000 for a moderate-risk client:",
            "categories": ["Stocks", "Bonds", "Real Estate", "Cash Reserve"],
            "budget": 10000,
            "optimal": {"Stocks": 5000, "Bonds": 3000, "Real Estate": 1500, "Cash Reserve": 500},
        },
    },
    "manager": {
        "shift_sim": {
            "prompt": "Manage your team's shift — handle in priority order:",
            "situations": ["Employee conflict (high)", "Deadline approaching (high)", "Performance review (medium)", "Training request (medium)", "Office supplies (low)"],
            "optimal": ["Deadline approaching (high)", "Employee conflict (high)", "Performance review (medium)", "Training request (medium)", "Office supplies (low)"],
        },
    },
    "hr_specialist": {
        "quick_pick": {
            "prompt": "Two candidates: one with 10 years experience but no degree, one with a degree but 2 years experience. Who for a senior role?",
            "options": ["Experienced candidate", "Degreed candidate", "Both for interview", "Neither — repost"],
            "correct": "Both for interview",
        },
    },
    "marketing": {
        "quick_pick": {
            "prompt": "Which campaign has the best ROI for a Gen Z audience?",
            "options": ["TV commercial", "TikTok influencer", "Newspaper ad", "Radio spot"],
            "correct": "TikTok influencer",
        },
    },
    "consultant": {
        "multi_stage": {
            "prompt": "Advise a client across 3 strategic areas:",
            "stages": [
                {"type": "quick_pick", "prompt": "Client revenue is declining. First analysis?", "options": ["Cut costs", "Analyze market trends", "Fire staff", "Raise prices"], "correct": "Analyze market trends"},
                {"type": "sequence", "prompt": "Implement changes in order:", "items": ["Stabilize cash flow", "Optimize operations", "Launch new product", "Expand market"], "order": ["Stabilize cash flow", "Optimize operations", "Launch new product", "Expand market"]},
                {"type": "quick_pick", "prompt": "Results: 15% growth in 6 months. Next?", "options": ["Scale up", "Maintain course", "Sell company", "Change strategy"], "correct": "Scale up"},
            ],
        },
    },
    "auditor": {
        "spot_error": {
            "prompt": "Find the discrepancy in this financial report:",
            "expected": "Revenue: $1,200,000\nExpenses: $800,000\nNet Profit: $400,000",
            "actual": "Revenue: $1,200,000\nExpenses: $800,000\nNet Profit: $500,000",
        },
    },
    "loan_officer": {
        "quick_pick": {
            "prompt": "Applicant: credit score 720, income $75k, debt ratio 35%. Approve $300k mortgage?",
            "options": ["Approve", "Deny", "Approve with conditions", "Counter-offer $250k"],
            "correct": "Approve with conditions",
        },
    },
    "insurance": {
        "quick_pick": {
            "prompt": "Client: 25yo, healthy, no dependents. Which policy to recommend?",
            "options": ["Whole life $500k", "Term life $250k (20yr)", "Universal life $1M", "No insurance needed"],
            "correct": "Term life $250k (20yr)",
        },
    },
    "bookkeeper": {
        "math": {
            "prompt": "Record transactions: +$1,200, -$350, +$890, -$1,100, +$450. Net = ?",
            "answer": 1090,
            "formula": "1200 - 350 + 890 - 1100 + 450 = 1090",
        },
    },
    "tax_prep": {
        "math": {
            "prompt": "Calculate tax: Income $65,000, deductions $12,000, tax rate 22%. Tax owed = ?",
            "answer": 11660,
            "formula": "(65000 - 12000) × 0.22 = 53000 × 0.22 = 11660",
        },
    },
    "investment_bank": {
        "negotiation": {
            "prompt": "Company A offers $45/share. Company B wants $52/share. Your client wants $50. What's your opening?",
            "options": ["Accept $45", "Counter at $50", "Demand $52", "Walk away"],
            "correct": "Counter at $50",
            "explanation": "Opening at your client's target leaves room for negotiation.",
        },
    },
    "venture_cap": {
        "quick_pick": {
            "prompt": "Startup: $2M ARR, 150% YoY growth, 20% margins. Invest at $20M valuation?",
            "options": ["Yes — strong growth", "No — overvalued", "Counter at $15M", "Need more data"],
            "correct": "Counter at $15M",
        },
    },
    "hedge_fund": {
        "pattern": {
            "prompt": "Market pattern: Bull, Bull, Bear, Bull, Bull, Bear, Bull, Bull, ?",
            "sequence": ["Bull", "Bull", "Bear", "Bull", "Bull", "Bear", "Bull", "Bull", "?"],
            "answer": "Bear",
        },
    },
    "entrepreneur": {
        "shift_sim": {
            "prompt": "Build your startup — prioritize tasks in order:",
            "situations": ["Product launch (critical)", "Investor pitch (high)", "Hire first engineer (high)", "Office setup (medium)", "Brand design (medium)", "Team retreat (low)"],
            "optimal": ["Product launch (critical)", "Investor pitch (high)", "Hire first engineer (high)", "Brand design (medium)", "Office setup (medium)", "Team retreat (low)"],
        },
    },
    "cfo": {
        "budget": {
            "prompt": "Allocate $1,000,000 corporate budget across departments:",
            "categories": ["R&D", "Marketing", "Operations", "HR", "Reserve"],
            "budget": 1000000,
            "optimal": {"R&D": 350000, "Marketing": 200000, "Operations": 250000, "HR": 100000, "Reserve": 100000},
        },
    },
    "coo": {
        "shift_sim": {
            "prompt": "Manage daily operations — handle in priority order:",
            "situations": ["Supply chain disruption (critical)", "Quality issue (high)", "Facility maintenance (medium)", "Vendor renewal (medium)", "Team building (low)"],
            "optimal": ["Supply chain disruption (critical)", "Quality issue (high)", "Vendor renewal (medium)", "Facility maintenance (medium)", "Team building (low)"],
        },
    },
    "trader": {
        "pattern": {
            "prompt": "Candlestick pattern: Green, Green, Red, Green, Green, Green, ?",
            "sequence": ["Green", "Green", "Red", "Green", "Green", "Green", "?"],
            "answer": "Red",
        },
    },
    "negotiator": {
        "negotiation": {
            "prompt": "Union demands 15% raise. Company offers 5%. Your job is to settle at 8%. Opening?",
            "options": ["Accept 15%", "Offer 5%", "Propose 8%", "Offer 7% with benefits"],
            "correct": "Offer 7% with benefits",
            "explanation": "Slightly below target with added value creates room for compromise at 8%.",
        },
    },
    "magnate": {
        "shift_sim": {
            "prompt": "Manage your business empire — prioritize across industries:",
            "situations": ["Hostile takeover attempt (critical)", "Regulatory investigation (critical)", "New acquisition (high)", "Board meeting (high)", "Philanthropy gala (medium)", "Personal brand (low)"],
            "optimal": ["Hostile takeover attempt (critical)", "Regulatory investigation (critical)", "New acquisition (high)", "Board meeting (high)", "Philanthropy gala (medium)", "Personal brand (low)"],
        },
    },

    # ─── Creative & Arts ───
    "artist": {
        "quick_pick": {
            "prompt": "Which color scheme creates the most dramatic contrast?",
            "options": ["Blue and green", "Red and green (complementary)", "Yellow and orange", "Purple and blue"],
            "correct": "Red and green (complementary)",
        },
    },
    "musician": {
        "sequence": {
            "prompt": "Play the C major scale in order:",
            "items": ["C", "D", "E", "F", "G", "A", "B", "C"],
            "order": ["C", "D", "E", "F", "G", "A", "B", "C"],
        },
    },
    "writer": {
        "fill_blank": {
            "prompt": "Complete the opening line: 'The old lighthouse stood ___ against the storm.'",
            "answer": "resolute",
            "context": "The word should convey strength and determination against adversity.",
        },
    },
    "photographer": {
        "quick_pick": {
            "prompt": "Golden hour portrait — which camera setting is best?",
            "options": ["f/16, 1/100s, ISO 800", "f/2.8, 1/200s, ISO 100", "f/8, 1/1000s, ISO 400", "f/1.4, 1/50s, ISO 3200"],
            "correct": "f/2.8, 1/200s, ISO 100",
        },
    },
    "graphic_design": {
        "sort": {
            "prompt": "Arrange design elements by visual hierarchy:",
            "items": ["Headline (largest)", "Subheadline", "Body text", "Image caption", "Footer (smallest)"],
            "order": ["Headline (largest)", "Subheadline", "Body text", "Image caption", "Footer (smallest)"],
        },
    },
    "actor": {
        "memory": {
            "prompt": "Memorize your lines: 'To be or not to be, that is the question. Whether tis nobler in the mind to suffer.'",
            "sequence": ["To be or not to be", "that is the question", "Whether tis nobler", "in the mind to suffer"],
        },
    },
    "filmmaker": {
        "sequence": {
            "prompt": "Shoot a scene — follow the production order:",
            "items": ["Set up lights", "Block actors", "Rehearse", "Roll camera", "Action", "Cut", "Reset for next take"],
            "order": ["Set up lights", "Block actors", "Rehearse", "Roll camera", "Action", "Cut", "Reset for next take"],
        },
    },
    "animator": {
        "sequence": {
            "prompt": "Create an animation — follow the production pipeline in order:",
            "items": ["Storyboard", "Key frames", "In-betweens", "Clean up", "Color", "Backgrounds", "Composite", "Render"],
            "order": ["Storyboard", "Key frames", "In-betweens", "Clean up", "Color", "Backgrounds", "Composite", "Render"],
        },
    },
    "fashion_design": {
        "sort": {
            "prompt": "Organize the fashion show lineup by collection flow:",
            "items": ["Opening statement piece", "Daywear collection", "Transitional pieces", "Evening wear", "Finale gown"],
            "order": ["Opening statement piece", "Daywear collection", "Transitional pieces", "Evening wear", "Finale gown"],
        },
    },
    "interior_design": {
        "sort": {
            "prompt": "Arrange furniture by room flow (entrance to focal point):",
            "items": ["Entry console", "Seating area", "Coffee table", "Bookshelf", "Window accent", "Focal art piece"],
            "order": ["Entry console", "Seating area", "Coffee table", "Bookshelf", "Window accent", "Focal art piece"],
        },
    },
    "architect": {
        "assembly": {
            "prompt": "Design a building — assemble design phases in order:",
            "parts": [("Site analysis", "Base"), ("Concept design", "Site analysis"), ("Schematic design", "Concept design"), ("Design development", "Schematic design"), ("Construction docs", "Design development"), ("Permits", "Construction docs")],
        },
    },
    "sculptor": {
        "sequence": {
            "prompt": "Sculpt from marble — follow the process in order:",
            "items": ["Select stone", "Create maquette", "Rough out form", "Refine shapes", "Detail work", "Smooth surface", "Polish", "Mount base"],
            "order": ["Select stone", "Create maquette", "Rough out form", "Refine shapes", "Detail work", "Smooth surface", "Polish", "Mount base"],
        },
    },
    "tattoo_artist": {
        "precision": {
            "prompt": "Guide the needle to exactly 3mm depth. Click when the gauge hits 3!",
            "target": 3,
            "tolerance": 0.5,
        },
    },
    "makeup_artist": {
        "quick_pick": {
            "prompt": "For a natural daytime look, which foundation finish is best?",
            "options": ["Full coverage matte", "Sheer dewy", "Heavy contour", "Glossy"],
            "correct": "Sheer dewy",
        },
    },
    "dancer": {
        "sequence": {
            "prompt": "Perform the waltz basic step sequence:",
            "items": ["Step back (1)", "Step side (2)", "Close (3)", "Step forward (1)", "Step side (2)", "Close (3)"],
            "order": ["Step back (1)", "Step side (2)", "Close (3)", "Step forward (1)", "Step side (2)", "Close (3)"],
        },
    },
    "comedian": {
        "quick_pick": {
            "prompt": "The crowd is quiet. Which joke type works best to warm them up?",
            "options": ["Dark humor", "Self-deprecating", "Political satire", "Observational"],
            "correct": "Self-deprecating",
        },
    },
    "dj": {
        "sequence": {
            "prompt": "Mix a seamless transition — follow the steps in order:",
            "items": ["Match BPM", "Find compatible key", "Set cue point", "Start track in headphones", "Adjust EQ", "Crossfade", "Exit old track"],
            "order": ["Match BPM", "Find compatible key", "Set cue point", "Start track in headphones", "Adjust EQ", "Crossfade", "Exit old track"],
        },
    },
    "producer": {
        "assembly": {
            "prompt": "Build a track — assemble layers in the correct order:",
            "parts": [("Drum beat", "Base"), ("Bass line", "Drum beat"), ("Chord progression", "Bass line"), ("Melody", "Chord progression"), ("Vocals", "Melody"), ("Mix & master", "Vocals")],
        },
    },
    "director": {
        "shift_sim": {
            "prompt": "Direct a film shoot day — prioritize in order:",
            "situations": ["Lead actor is late (critical)", "Light setup needs adjustment (high)", "Script revision needed (high)", "Catering delay (medium)", "Wardrobe fitting (medium)", "Behind-the-scenes photo (low)"],
            "optimal": ["Lead actor is late (critical)", "Script revision needed (high)", "Light setup needs adjustment (high)", "Wardrobe fitting (medium)", "Catering delay (medium)", "Behind-the-scenes photo (low)"],
        },
    },
    "novelist": {
        "fill_blank": {
            "prompt": "Complete the chapter ending: 'She opened the door and found ___, standing right there.'",
            "answer": "exactly what she feared",
            "context": "The ending should create tension and emotional resonance.",
        },
    },
    "jeweler": {
        "precision": {
            "prompt": "Set the diamond at exactly 2.5mm depth. Click when the gauge is precise!",
            "target": 2.5,
            "tolerance": 0.3,
        },
    },
    "potter": {
        "sequence": {
            "prompt": "Throw a clay pot on the wheel — correct order:",
            "items": ["Center clay", "Open center", "Pull walls", "Shape body", "Form rim", "Trim base", "Remove from wheel", "Fire in kiln"],
            "order": ["Center clay", "Open center", "Pull walls", "Shape body", "Form rim", "Trim base", "Remove from wheel", "Fire in kiln"],
        },
    },
    "stunt_double": {
        "timing": {
            "prompt": "Time your jump perfectly! Click when the countdown reaches zero.",
            "beats": 3,
        },
    },
    "voice_actor": {
        "typing_race": {
            "prompt": "Read and type the line exactly as shown:",
            "phrase": "In a world where silence speaks louder than words, one voice will rise.",
        },
    },
    "maestro": {
        "sequence": {
            "prompt": "Conduct the symphony — cue sections in the correct order:",
            "items": ["Strings (opening)", "Woodwinds (theme)", "Brass (climax)", "Timpani (transition)", "Full orchestra (finale)", "Silence (resolution)"],
            "order": ["Strings (opening)", "Woodwinds (theme)", "Brass (climax)", "Timpani (transition)", "Full orchestra (finale)", "Silence (resolution)"],
        },
    },

    # ─── Transport & Logistics ───
    "delivery": {
        "route_plan": {
            "prompt": "Plan the most efficient delivery route:",
            "stops": ["Warehouse", "Northside #12", "Eastend #45", "Downtown #8", "Southpark #23"],
            "optimal": ["Warehouse", "Northside #12", "Eastend #45", "Downtown #8", "Southpark #23"],
        },
    },
    "pilot": {
        "sequence": {
            "prompt": "Complete the pre-flight checklist in order:",
            "items": ["Inspect exterior", "Check fuel levels", "Test controls", "Set instruments", "Contact tower", "Taxi to runway", "Takeoff clearance", "Rotate"],
            "order": ["Inspect exterior", "Check fuel levels", "Test controls", "Set instruments", "Contact tower", "Taxi to runway", "Takeoff clearance", "Rotate"],
        },
    },
    "truck_driver": {
        "route_plan": {
            "prompt": "Plan the most fuel-efficient trucking route:",
            "stops": ["Depot", "Highway 5 exit 12", "Highway 5 exit 23", "Highway 5 exit 31", "Warehouse B"],
            "optimal": ["Depot", "Highway 5 exit 12", "Highway 5 exit 23", "Highway 5 exit 31", "Warehouse B"],
        },
    },
    "taxi_driver": {
        "quick_pick": {
            "prompt": "Passenger needs to reach the airport in 20 minutes. Which route?",
            "options": ["Highway (15 min, $25)", "City streets (25 min, $15)", "Back roads (30 min, $18)", "Toll road (12 min, $35)"],
            "correct": "Toll road (12 min, $35)",
        },
    },
    "bus_driver": {
        "route_plan": {
            "prompt": "Follow the bus route in the correct stop order:",
            "stops": ["Main Station", "First St", "Third Ave", "Park Blvd", "School", "Shopping Center", "Main Station"],
            "optimal": ["Main Station", "First St", "Third Ave", "Park Blvd", "School", "Shopping Center", "Main Station"],
        },
    },
    "train_driver": {
        "timing": {
            "prompt": "Maintain the schedule! Click to depart at each station when the timer aligns.",
            "beats": 4,
        },
    },
    "ship_captain": {
        "multi_stage": {
            "prompt": "Navigate the cargo ship through 3 critical stages:",
            "stages": [
                {"type": "sequence", "prompt": "Pre-departure checks in order:", "items": ["Inspect hull", "Check cargo secure", "Test navigation", "Brief crew", "Get port clearance", "Depart"], "order": ["Inspect hull", "Check cargo secure", "Test navigation", "Brief crew", "Get port clearance", "Depart"]},
                {"type": "quick_pick", "prompt": "Storm approaching. Action?", "options": ["Continue course", "Reduce speed", "Reroute", "Drop anchor"], "correct": "Reroute"},
                {"type": "sequence", "prompt": "Dock procedure in order:", "items": ["Contact port", "Reduce speed", "Approach dock", "Deploy lines", "Secure vessel", "Offload cargo"], "order": ["Contact port", "Reduce speed", "Approach dock", "Deploy lines", "Secure vessel", "Offload cargo"]},
            ],
        },
    },
    "forklift": {
        "precision": {
            "prompt": "Lower the pallet to exactly 150cm. Click when the height gauge hits 150!",
            "target": 150,
            "tolerance": 5,
        },
    },
    "warehouse": {
        "sort": {
            "prompt": "Sort incoming packages by destination zone:",
            "items": ["Box A → Zone 1", "Box B → Zone 3", "Box C → Zone 1", "Box D → Zone 2", "Box E → Zone 3"],
            "categories": ["Zone 1", "Zone 3", "Zone 1", "Zone 2", "Zone 3"],
        },
    },
    "courier": {
        "route_plan": {
            "prompt": "Plan the fastest courier route for urgent deliveries:",
            "stops": ["Office", "Bank Tower", "Court House", "City Hall", "Law Firm"],
            "optimal": ["Office", "Bank Tower", "Law Firm", "Court House", "City Hall"],
        },
    },
    "ambulance_drv": {
        "quick_pick": {
            "prompt": "Patient critical — which route gets to the hospital fastest?",
            "options": ["Main Blvd (8 min, heavy traffic)", "Side streets (6 min, clear)", "Highway (10 min, accident)", "Bridge road (7 min, toll)"],
            "correct": "Side streets (6 min, clear)",
        },
    },
    "fire_truck_drv": {
        "quick_pick": {
            "prompt": "Fire reported on 5th Avenue. Best approach route?",
            "options": ["5th Ave direct (blocked by fire)", "6th Ave parallel (clear)", "Through park (narrow)", "Highway exit (long way)"],
            "correct": "6th Ave parallel (clear)",
        },
    },
    "subway_op": {
        "timing": {
            "prompt": "Time the doors perfectly! Click to close doors when the timer aligns at each station.",
            "beats": 3,
        },
    },
    "tram_driver": {
        "timing": {
            "prompt": "Maintain the tram schedule! Click to depart at each stop when the timer aligns.",
            "beats": 3,
        },
    },
    "logistics_mgr": {
        "shift_sim": {
            "prompt": "Manage the logistics center — prioritize in order:",
            "situations": ["Truck breakdown on highway (critical)", "Customs delay at port (high)", "Warehouse staffing (medium)", "Route optimization (medium)", "Fleet maintenance (low)"],
            "optimal": ["Truck breakdown on highway (critical)", "Customs delay at port (high)", "Warehouse staffing (medium)", "Route optimization (medium)", "Fleet maintenance (low)"],
        },
    },
    "air_traffic": {
        "sequence": {
            "prompt": "Guide 3 planes to landing — sequence them correctly:",
            "items": ["Flight 101 (10 miles out, low fuel)", "Flight 202 (15 miles out, normal)", "Flight 303 (20 miles out, normal)"],
            "order": ["Flight 101 (10 miles out, low fuel)", "Flight 202 (15 miles out, normal)", "Flight 303 (20 miles out, normal)"],
        },
    },
    "harbor_master": {
        "sequence": {
            "prompt": "Sequence ship arrivals into port — correct order:",
            "items": ["Tanker (deep draft, needs tide)", "Container ship (scheduled)", "Ferry (priority passenger)", "Fishing fleet (local)"],
            "order": ["Ferry (priority passenger)", "Tanker (deep draft, needs tide)", "Container ship (scheduled)", "Fishing fleet (local)"],
        },
    },
    "cargo_pilot": {
        "sequence": {
            "prompt": "Complete the overnight cargo flight checklist in order:",
            "items": ["Load cargo", "Weight distribution check", "Pre-flight inspection", "File flight plan", "Start engines", "Taxi", "Takeoff", "Cruise altitude"],
            "order": ["Load cargo", "Weight distribution check", "Pre-flight inspection", "File flight plan", "Start engines", "Taxi", "Takeoff", "Cruise altitude"],
        },
    },
    "helicopter_pilot": {
        "sequence": {
            "prompt": "Complete the pre-flight checklist for a rescue mission:",
            "items": ["Check rotor system", "Verify fuel", "Test navigation", "Brief rescue crew", "Start engine", "Engage rotors", "Liftoff", "Set heading"],
            "order": ["Check rotor system", "Verify fuel", "Test navigation", "Brief rescue crew", "Start engine", "Engage rotors", "Liftoff", "Set heading"],
        },
    },
    "dispatch": {
        "sort": {
            "prompt": "Sort dispatch calls by priority:",
            "items": ["Armed robbery in progress", "Noise complaint", "Domestic dispute", "Traffic accident with injuries", "Lost dog report"],
            "order": ["Armed robbery in progress", "Traffic accident with injuries", "Domestic dispute", "Noise complaint", "Lost dog report"],
        },
    },
    "bike_courier": {
        "route_plan": {
            "prompt": "Plan the fastest bike route through the city:",
            "stops": ["Pickup: Cafe", "Drop 1: Office Tower", "Drop 2: Law Firm", "Drop 3: Bank", "Return: Cafe"],
            "optimal": ["Pickup: Cafe", "Drop 1: Office Tower", "Drop 2: Law Firm", "Drop 3: Bank", "Return: Cafe"],
        },
    },
    "chauffeur": {
        "quick_pick": {
            "prompt": "VIP client wants a smooth, scenic route. Which option?",
            "options": ["Highway (fast but bumpy)", "Coastal road (smooth, scenic)", "City center (scenic but traffic)", "Industrial route (smooth but ugly)"],
            "correct": "Coastal road (smooth, scenic)",
        },
    },
    "tow_truck": {
        "route_plan": {
            "prompt": "Plan the tow truck route to reach 3 stranded vehicles:",
            "stops": ["Garage", "Highway Mile 12", "Highway Mile 8", "Parking Lot B"],
            "optimal": ["Garage", "Highway Mile 8", "Highway Mile 12", "Parking Lot B"],
        },
    },
    "supply_chain": {
        "budget": {
            "prompt": "Allocate $500,000 supply chain budget:",
            "categories": ["Manufacturing", "Shipping", "Warehousing", "Last-mile delivery"],
            "budget": 500000,
            "optimal": {"Manufacturing": 200000, "Shipping": 120000, "Warehousing": 100000, "Last-mile delivery": 80000},
        },
    },
    "test_pilot": {
        "multi_stage": {
            "prompt": "Test the experimental aircraft across 3 critical phases:",
            "stages": [
                {"type": "sequence", "prompt": "Pre-flight test sequence:", "items": ["Systems check", "Engine start", "Taxi test", "Runway acceleration", "Rotation", "Climb out"], "order": ["Systems check", "Engine start", "Taxi test", "Runway acceleration", "Rotation", "Climb out"]},
                {"type": "quick_pick", "prompt": "At 10,000ft, vibration detected. Action?", "options": ["Continue test", "Reduce speed", "Return to base", "Eject"], "correct": "Return to base"},
                {"type": "sequence", "prompt": "Emergency landing sequence:", "items": ["Declare emergency", "Dump fuel", "Align runway", "Lower gear", "Touchdown", "Full brakes", "Stop"], "order": ["Declare emergency", "Dump fuel", "Align runway", "Lower gear", "Touchdown", "Full brakes", "Stop"]},
            ],
        },
    },
}

# Merge in the extra content (2 additional minigame types per job)
# Deep merge: add new minigame types to each job without overwriting existing ones
for _job_id, _mg_dict in EXTRA_CONTENT.items():
    if _job_id in JOB_CONTENT:
        JOB_CONTENT[_job_id].update(_mg_dict)
    else:
        JOB_CONTENT[_job_id] = _mg_dict

# Merge in the 3rd distinct minigame types (for jobs that had duplicate quick_pick)
from config.minigame_content_extra import THIRD_CONTENT
for _job_id, _mg_dict in THIRD_CONTENT.items():
    if _job_id in JOB_CONTENT:
        JOB_CONTENT[_job_id].update(_mg_dict)
    else:
        JOB_CONTENT[_job_id] = _mg_dict
