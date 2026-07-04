"""
Per-subcategory flavor pools for procedural minigame generation.
38 subcategories with unique objects, actions, and people.
Management subcategories are prefixed with their category for disambiguation:
  svc_management, trades_management, trans_management, biz_management
"""

SUBCATEGORY_FLAVOR = {
    "street": {
        "objects": ["cardboard sign", "tip jar", "guitar case", "megaphone", "flyer stack", "spare change cup", "shopping cart", "boom box", "hat", "bucket"],
        "actions": ["busking", "begging", "handing out flyers", "shining shoes", "holding a sign", "selling newspapers", "taking surveys", "blowing balloons", "pushing a cart", "waving at cars"],
        "people": ["tourist", "businessman", "commuter", "shopper", "street vendor", "police officer", "pedestrian", "jogger", "dog owner", "teenager"],
    },
    "cleaning": {
        "objects": ["mop bucket", "squeegee", "spray bottle", "trash bag", "broom", "vacuum", "duster", "gloves", "pressure washer", "scrub brush"],
        "actions": ["mopping", "sweeping", "scrubbing", "washing windows", "emptying trash", "vacuuming", "dusting", "polishing", "disinfecting", "wiping down"],
        "people": ["building manager", "tenant", "office worker", "custodian", "supervisor", "delivery person", "security guard", "maintenance worker", "guest", "inspector"],
    },
    "helper": {
        "objects": ["price tag", "shopping cart", "box cutter", "tape dispenser", "hand truck", "shelf label", "inventory clipboard", "cash register", "shopping basket", "stock cart"],
        "actions": ["stocking shelves", "helping customers", "carrying boxes", "organizing products", "restocking", "packing orders", "directing traffic", "setting up displays", "fetching items", "wrapping gifts"],
        "people": ["customer", "store manager", "shopper", "delivery driver", "cashier", "stock boy", "supervisor", "vendor", "regular customer", "tourist"],
    },
    "kitchen": {
        "objects": ["chef knife", "cutting board", "saucepan", "stock pot", "mixing bowl", "whisk", "spatula", "oven mitt", "meat thermometer", "rolling pin"],
        "actions": ["chopping vegetables", "grilling steak", "plating dishes", "kneading dough", "frying tempura", "simmering sauce", "baking bread", "garnishing", "filleting fish", "caramelizing onions"],
        "people": ["head chef", "sous chef", "line cook", "dishwasher", "food critic", "health inspector", "waiter", "pastry chef", "prep cook", "restaurant owner"],
    },
    "beverage": {
        "objects": ["espresso machine", "cocktail shaker", "wine glass", "coffee grinder", "milk frother", "bar spoon", "strainer", "ice scoop", "tamper", "portafilter"],
        "actions": ["pulling espresso", "shaking cocktails", "pouring wine", "frothing milk", "brewing coffee", "mixing drinks", "garnishing cocktails", "tasting wine", "steeping tea", "layering shots"],
        "people": ["barista", "bartender", "sommelier", "regular customer", "bar patron", "cafe owner", "wine critic", "mixologist", "waitress", "bar back"],
    },
    "front": {
        "objects": ["menu", "order pad", "tray", "plate stand", "reservation book", "POS terminal", "uniform apron", "name tag", "check presenter", "serving cart"],
        "actions": ["greeting guests", "taking orders", "serving food", "clearing tables", "processing payments", "making reservations", "recommending dishes", "handling complaints", "seating customers", "rolling silverware"],
        "people": ["diner", "host", "manager", "food critic", "regular customer", "tourist", "business luncher", "family", "couple", "solo diner"],
    },
    "specialty": {
        "objects": ["chocolate tempering machine", "candy thermometer", "mold set", "nutrition chart", "tasting notebook", "confectionery tool", "sugar thermometer", "dipping fork", "piping bag", "flavor extract"],
        "actions": ["tempering chocolate", "tasting dishes", "plating desserts", "analyzing nutrition", "crafting confections", "reviewing restaurants", "creating recipes", "caramelizing sugar", "infusing flavors", "scoring food"],
        "people": ["chocolatier", "food critic", "nutritionist", "pastry chef", "customer", "food blogger", "health inspector", "supplier", "restaurant owner", "VIP guest"],
    },
    "svc_management": {
        "objects": ["booking system", "event timeline", "staff schedule", "budget spreadsheet", "floor plan", "reservation book", "catering contract", "guest list", "inventory report", "POS dashboard"],
        "actions": ["coordinating staff", "planning events", "managing reservations", "overseeing service", "handling complaints", "scheduling shifts", "ordering supplies", "reviewing budgets", "training employees", "inspecting rooms"],
        "people": ["hotel guest", "event client", "staff member", "VIP guest", "caterer", "supplier", "inspector", "conference organizer", "wedding planner", "corporate client"],
    },
    "construction": {
        "objects": ["hammer", "nail gun", "safety harness", "hard hat", "screwdriver", "level", "tape measure", "power drill", "sawhorse", "caulk gun"],
        "actions": ["hammering nails", "laying bricks", "painting walls", "installing drywall", "roofing", "tiling floors", "scaffolding", "insulating", "pouring concrete", "framing walls"],
        "people": ["foreman", "architect", "site inspector", "subcontractor", "laborer", "client", "building official", "engineer", "apprentice", "supplier"],
    },
    "skilled": {
        "objects": ["wrench set", "multimeter", "pipe wrench", "wire stripper", "soldering iron", "voltmeter", "pipe cutter", "threading tool", "conduit bender", "diagnostic scanner"],
        "actions": ["wiring circuits", "fixing pipes", "welding metal", "tuning engines", "picking locks", "installing fixtures", "cutting glass", "repairing HVAC", "soldering wires", "diagnosing faults"],
        "people": ["mechanic", "electrician", "plumber", "carpenter", "welder", "locksmith", "glazier", "HVAC tech", "customer", "apprentice"],
    },
    "heavy": {
        "objects": ["excavator", "crane", "forklift", "bulldozer", "jackhammer", "welding torch", "steel beam", "scissor lift", "concrete mixer", "demolition ball"],
        "actions": ["operating crane", "demolishing walls", "welding steel", "installing elevators", "laying solar panels", "digging trenches", "lifting beams", "driving bulldozer", "pouring foundation", "rigging loads"],
        "people": ["site boss", "crane operator", "steelworker", "safety officer", "engineer", "inspector", "teamster", "apprentice", "project manager", "OSHA inspector"],
    },
    "outdoor": {
        "objects": ["lawn mower", "hedge trimmer", "leaf blower", "pruning shears", "wheelbarrow", "rake", "shovel", "chainsaw", "garden hose", "mulch bag"],
        "actions": ["mowing lawns", "trimming hedges", "planting flowers", "pruning trees", "raking leaves", "laying mulch", "watering plants", "edging walkways", "removing stumps", "spreading soil"],
        "people": ["homeowner", "gardener", "landscape architect", "property manager", "client", "nursery worker", "groundskeeper", "neighbor", "HOA member", "city inspector"],
    },
    "trades_management": {
        "objects": ["blueprint", "survey transit", "project timeline", "cost estimate", "safety plan", "permit document", "work order", "material order", "inspection checklist", "Gantt chart"],
        "actions": ["surveying land", "estimating costs", "managing crew", "inspecting work", "filing permits", "ordering materials", "reviewing blueprints", "scheduling subcontractors", "checking safety", "coordinating deliveries"],
        "people": ["client", "architect", "subcontractor", "inspector", "supplier", "crew member", "engineer", "city planner", "investor", "safety officer"],
    },
    "clinical": {
        "objects": ["stethoscope", "syringe", "IV drip", "surgical scalpel", "patient chart", "X-ray machine", "blood pressure cuff", "defibrillator", "surgical clamp", "medical tray"],
        "actions": ["examining patient", "performing surgery", "taking vitals", "administering medication", "reading X-rays", "stitching wounds", "diagnosing illness", "intubating", "drawing blood", "checking reflexes"],
        "people": ["patient", "surgeon", "nurse", "doctor", "anesthesiologist", "medical student", "hospital admin", "specialist", "EMT", "family member"],
    },
    "care": {
        "objects": ["pill bottle", "prescription pad", "therapy couch", "eye chart", "rehabilitation equipment", "vaccine vial", "blood sample", "crutches", "medication cart", "pharmacy inventory"],
        "actions": ["dispensing medication", "conducting therapy", "examining eyes", "guiding rehab", "vaccinating", "compounding prescriptions", "examining pet", "adjusting braces", "reading lab results", "counseling patient"],
        "people": ["patient", "pharmacist", "therapist", "veterinarian", "optometrist", "physical therapist", "radiologist", "pet owner", "caregiver", "medical rep"],
    },
    "research": {
        "objects": ["microscope", "petri dish", "test tube", "centrifuge", "lab notebook", "Bunsen burner", "pipette", "specimen jar", "telescope", "data terminal"],
        "actions": ["analyzing samples", "running experiments", "culturing bacteria", "operating centrifuge", "recording data", "testing chemicals", "observing cells", "calibrating equipment", "gene sequencing", "stargazing"],
        "people": ["lead scientist", "lab assistant", "research director", "grad student", "funding officer", "peer reviewer", "collaborator", "test subject", "journal editor", "safety officer"],
    },
    "software": {
        "objects": ["keyboard", "monitor", "IDE window", "git branch", "bug report", "code review", "API doc", "test suite", "deploy script", "coffee cup"],
        "actions": ["writing code", "debugging", "running tests", "deploying app", "reviewing PRs", "fixing bugs", "refactoring", "pair programming", "writing docs", "optimizing queries"],
        "people": ["product manager", "QA tester", "tech lead", "junior dev", "client", "user", "designer", "DevOps engineer", "scrum master", "CTO"],
    },
    "data_ai": {
        "objects": ["dataset", "model weights", "GPU cluster", "training curve", "feature matrix", "neural network", "data pipeline", "Jupyter notebook", "confusion matrix", "loss graph"],
        "actions": ["training model", "cleaning data", "tuning hyperparameters", "running inference", "analyzing results", "building pipeline", "labeling data", "evaluating metrics", "deploying model", "visualizing data"],
        "people": ["data scientist", "ML engineer", "research lead", "data engineer", "business analyst", "stakeholder", "domain expert", "annotator", "investor", "academic peer"],
    },
    "infra": {
        "objects": ["server rack", "router", "load balancer", "Docker container", "Kubernetes pod", "firewall rule", "SSH terminal", "backup drive", "network cable", "monitoring dashboard"],
        "actions": ["configuring server", "deploying container", "scaling cluster", "fixing outage", "running migration", "setting up VPN", "monitoring traffic", "patching system", "troubleshooting network", "automating deploy"],
        "people": ["sysadmin", "DevOps engineer", "cloud architect", "network engineer", "IT support ticket", "developer", "security team", "vendor", "CIO", "end user"],
    },
    "security": {
        "objects": ["penetration report", "vulnerability scanner", "firewall log", "exploit kit", "encryption key", "SIEM dashboard", "phishing template", "access token", "password hash", "network packet"],
        "actions": ["scanning ports", "exploiting vulnerability", "analyzing malware", "hardening system", "running pentest", "reviewing logs", "intercepting traffic", "cracking hash", "patching CVE", "writing report"],
        "people": ["security analyst", "pentester", "CISO", "IT manager", "attacker", "client", "compliance officer", "forensics expert", "developer", "auditor"],
    },
    "design_lead": {
        "objects": ["wireframe", "design system", "user journey map", "product roadmap", "Figma file", "stakeholder deck", "KPI dashboard", "user persona", "A/B test result", "sprint board"],
        "actions": ["designing wireframes", "running user research", "planning roadmap", "reviewing designs", "presenting to stakeholders", "analyzing metrics", "prioritizing backlog", "conducting interviews", "prototyping", "defining KPIs"],
        "people": ["UX designer", "product manager", "CTO", "CEO", "developer", "user", "stakeholder", "design researcher", "marketing lead", "investor"],
    },
    "finance": {
        "objects": ["ledger", "spreadsheet", "tax form", "bank statement", "calculator", "audit report", "financial plan", "loan document", "trading terminal", "receipt"],
        "actions": ["balancing books", "filing taxes", "auditing accounts", "approving loans", "advising clients", "processing transactions", "reconciling statements", "forecasting budget", "calculating interest", "reviewing expenses"],
        "people": ["client", "accountant", "auditor", "bank manager", "tax official", "investor", "loan applicant", "business owner", "financial advisor", "regulator"],
    },
    "biz_management": {
        "objects": ["HR handbook", "marketing plan", "org chart", "performance review", "strategy deck", "meeting agenda", "consulting report", "sales pipeline", "employee survey", "project brief"],
        "actions": ["hiring staff", "reviewing performance", "planning campaign", "advising clients", "managing team", "optimizing process", "presenting strategy", "conducting interview", "analyzing market", "training employees"],
        "people": ["employee", "manager", "CEO", "client", "candidate", "HR director", "marketing team", "consultant", "stakeholder", "vendor"],
    },
    "executive": {
        "objects": ["quarterly report", "board resolution", "stock option", "acquisition offer", "mission statement", "investor pitch", "executive summary", "company valuation", "strategic plan", "annual budget"],
        "actions": ["pitching investors", "negotiating deal", "reviewing financials", "leading board meeting", "setting strategy", "approving acquisition", "managing crisis", "expanding business", "hiring executive", "presenting keynote"],
        "people": ["board member", "investor", "CEO", "CFO", "COO", "venture capitalist", "shareholder", "journalist", "regulator", "rival CEO"],
    },
    "investing": {
        "objects": ["stock chart", "portfolio", "term sheet", "risk model", "trading algorithm", "market report", "investment memo", "cap table", "bond certificate", "commodity index"],
        "actions": ["analyzing market", "trading stock", "evaluating startup", "managing portfolio", "hedging risk", "pitching fund", "reading candlestick", "shorting position", "pricing option", "rebalancing assets"],
        "people": ["trader", "analyst", "fund manager", "VC partner", "LP investor", "startup founder", "broker", "risk officer", "market maker", "regulator"],
    },
    "services": {
        "objects": ["property listing", "insurance policy", "contract draft", "negotiation term sheet", "client file", "premium calculator", "deed", "inspection report", "commission chart", "settlement statement"],
        "actions": ["showing property", "writing policy", "negotiating deal", "assessing risk", "closing sale", "appraising value", "drafting contract", "processing claim", "advising client", "marketing listing"],
        "people": ["homebuyer", "seller", "insurance agent", "real estate broker", "client", "underwriter", "claims adjuster", "negotiator", "lawyer", "property inspector"],
    },
    "visual": {
        "objects": ["easel", "canvas", "camera", "sculpting tool", "pottery wheel", "jewelry plier", "palette knife", "sketchbook", "exhibition catalog", "glaze bottle"],
        "actions": ["painting landscape", "sculpting clay", "taking photos", "throwing pottery", "cutting gemstone", "mixing colors", "framing artwork", "glazing ceramic", "setting stone", "sketching portrait"],
        "people": ["art collector", "gallery owner", "critic", "student", "model", "curator", "client", "fellow artist", "tourist", "art dealer"],
    },
    "performing": {
        "objects": ["microphone", "script", "dance shoes", "instrument case", "stage prop", "spotlight", "sheet music", "DJ deck", "costume rack", "stunt harness"],
        "actions": ["rehearsing lines", "performing scene", "choreographing dance", "playing set", "mixing tracks", "doing stunt", "recording voiceover", "tuning instrument", "conducting orchestra", "improvising comedy"],
        "people": ["director", "agent", "audience member", "producer", "fellow actor", "casting director", "critic", "fan", "stage manager", "choreographer"],
    },
    "media_film": {
        "objects": ["clapperboard", "camera rig", "storyboard", "editing timeline", "render farm", "boom mic", "light diffuser", "color grade panel", "script breakdown", "production schedule"],
        "actions": ["setting up shot", "editing footage", "animating frame", "directing scene", "color grading", "recording sound", "rendering CGI", "breaking down script", "scheduling shoot", "reviewing dailies"],
        "people": ["director", "producer", "actor", "editor", "animator", "cinematographer", "sound engineer", "studio exec", "critic", "agent"],
    },
    "design": {
        "objects": ["mood board", "fabric swatch", "floor plan", "color palette", "3D model", "sewing machine", "furniture catalog", "material sample", "tattoo stencil", "makeup palette"],
        "actions": ["sketching design", "draping fabric", "rendering interior", "drafting blueprint", "inking tattoo", "applying makeup", "selecting materials", "presenting concept", "fitting garment", "modeling space"],
        "people": ["client", "fashion buyer", "interior decorator", "architect", "model", "tattoo client", "bride", "magazine editor", "contractor", "design critic"],
    },
    "writing": {
        "objects": ["manuscript", "laptop", "notebook", "red pen", "deadline calendar", "publisher contract", "outline document", "research folder", "character sheet", "plot board"],
        "actions": ["writing chapter", "editing draft", "outlining plot", "researching topic", "pitching article", "revising manuscript", "developing character", "meeting deadline", "fact-checking", "formatting manuscript"],
        "people": ["editor", "publisher", "agent", "reader", "critic", "source", "fellow writer", "librarian", "bookstore owner", "fan"],
    },
    "driving": {
        "objects": ["steering wheel", "GPS unit", "fare meter", "route map", "fuel gauge", "passenger seat", "rearview mirror", "gear shift", "delivery manifest", "parking brake"],
        "actions": ["driving route", "picking up passenger", "delivering package", "navigating traffic", "reading map", "parking vehicle", "checking mirrors", "changing lane", "stopping at light", "merging onto highway"],
        "people": ["passenger", "dispatcher", "customer", "traffic cop", "fellow driver", "pedestrian", "toll operator", "mechanic", "rider", "delivery recipient"],
    },
    "emergency": {
        "objects": ["siren", "stretcher", "first aid kit", "radio", "jaws of life", "oxygen mask", "defibrillator", "incident report", "emergency light", "medical bag"],
        "actions": ["rushing to scene", "loading patient", "stabilizing victim", "navigating traffic", "radioing dispatch", "extinguishing fire", "extracting patient", "driving code 3", "clearing intersection", "transporting patient"],
        "people": ["patient", "paramedic", "firefighter", "dispatcher", "ER doctor", "bystander", "police officer", "family member", "witness", "nurse"],
    },
    "warehouse": {
        "objects": ["forklift", "pallet jack", "barcode scanner", "shipping label", "inventory tablet", "packing tape", "loading dock", "conveyor belt", "stock picker", "manifest clipboard"],
        "actions": ["driving forklift", "scanning barcode", "loading truck", "picking order", "packing box", "sorting parcels", "dispatching shipment", "stacking pallets", "checking inventory", "wrapping pallet"],
        "people": ["warehouse manager", "forklift operator", "truck driver", "dispatcher", "inventory clerk", "loader", "supplier", "delivery driver", "safety officer", "shift supervisor"],
    },
    "courier": {
        "objects": ["delivery bag", "bike helmet", "GPS phone", "package scanner", "lockbox", "thermobox", "route list", "cargo strap", "kickstand", "reflective vest"],
        "actions": ["riding bike", "delivering package", "navigating route", "scanning drop-off", "avoiding traffic", "locking up bike", "loading cargo", "calling customer", "rushing order", "crossing intersection"],
        "people": ["customer", "dispatcher", "restaurant owner", "recipient", "fellow courier", "traffic cop", "pedestrian", "doorman", "shop owner", "mechanic"],
    },
    "aviation": {
        "objects": ["control yoke", "altimeter", "throttle lever", "radar screen", "flight plan", "navigation chart", "radio headset", "landing gear lever", "transponder", "checklist clipboard"],
        "actions": ["flying plane", "taking off", "landing aircraft", "reading altimeter", "radioing tower", "navigating route", "checking instruments", "adjusting throttle", "managing fuel", "executing approach"],
        "people": ["air traffic controller", "co-pilot", "passenger", "flight attendant", "ground crew", "tower operator", "meteorologist", "maintenance tech", "dispatcher", "safety inspector"],
    },
    "maritime": {
        "objects": ["ship wheel", "anchor chain", "sonar display", "navigation chart", "cargo manifest", "life jacket", "radio set", "engine throttle", "depth finder", "mooring line"],
        "actions": ["steering ship", "dropping anchor", "reading sonar", "plotting course", "loading cargo", "monitoring engine", "radioing port", "docking vessel", "checking depth", "securing mooring"],
        "people": ["harbor master", "first mate", "deckhand", "port official", "cargo inspector", "navigator", "engineer", "pilot boat captain", "coast guard", "customs officer"],
    },
    "trans_management": {
        "objects": ["supply chain dashboard", "logistics map", "fleet schedule", "delivery route plan", "warehouse layout", "shipping contract", "freight invoice", "customs document", "KPI report", "carrier agreement"],
        "actions": ["optimizing route", "managing fleet", "coordinating delivery", "tracking shipment", "negotiating freight", "planning schedule", "analyzing supply chain", "managing warehouse", "processing customs", "reviewing KPIs"],
        "people": ["driver", "warehouse manager", "supplier", "client", "customs officer", "freight broker", "dispatcher", "logistics analyst", "carrier rep", "port authority"],
    },
}
