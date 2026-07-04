from config.job_requirements import JOB_REQUIREMENTS
from config.minigame_content import JOB_CONTENT
from config.jobs import JOBS, JOB_CATEGORIES, JOB_SUBCATEGORIES

# For each job, find which minigame types lack job-specific content
missing = {}
for jid, req in JOB_REQUIREMENTS.items():
    games = req.get("minigames", [req.get("minigame", "quick_pick")])
    existing = set(JOB_CONTENT.get(jid, {}).keys())
    for g in games:
        if g not in existing:
            missing.setdefault(g, []).append(jid)

print("=== Minigame types needing job-specific content ===")
for g, jobs in sorted(missing.items(), key=lambda x: -len(x[1])):
    print(f"  {g}: {len(jobs)} jobs need content")
    # Show a few examples grouped by category
    by_cat = {}
    for jid in jobs:
        cat = JOBS.get(jid, {}).get("category", "?")
        sub = JOBS.get(jid, {}).get("subcategory", "?")
        by_cat.setdefault(f"{cat}/{sub}", []).append(jid)
    for key, jids in list(by_cat.items())[:3]:
        print(f"    {key}: {jids[:5]}")

print(f"\nTotal content gaps: {sum(len(v) for v in missing.values())}")
print(f"Jobs needing 2 new content: {sum(1 for jid in JOB_REQUIREMENTS if len(set(JOB_REQUIREMENTS[jid].get('minigames',[])) - set(JOB_CONTENT.get(jid,{}).keys())) >= 2)}")
