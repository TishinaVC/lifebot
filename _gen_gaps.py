import json
from config.job_requirements import JOB_REQUIREMENTS
from config.minigame_content import JOB_CONTENT
from config.jobs import JOBS

result = {}
for jid, req in JOB_REQUIREMENTS.items():
    games = req.get("minigames", [req.get("minigame", "quick_pick")])
    existing = set(JOB_CONTENT.get(jid, {}).keys())
    missing = [g for g in games if g not in existing]
    if missing:
        result[jid] = {
            "name": JOBS.get(jid, {}).get("name", jid),
            "category": JOBS.get(jid, {}).get("category", ""),
            "subcategory": JOBS.get(jid, {}).get("subcategory", ""),
            "description": JOBS.get(jid, {}).get("description", ""),
            "missing": missing,
            "existing": list(existing),
        }

with open("_content_gaps.json", "w") as f:
    json.dump(result, f, indent=2)

print(f"Total jobs needing content: {len(result)}")
print(f"Total content entries needed: {sum(len(v['missing']) for v in result.values())}")
