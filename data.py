import json
import random
from pathlib import Path

JSON_FILE = Path("input.json")


# ==========================================================
# STATUS ENGINE (Smart Rules)
# ==========================================================
def calculate_status(ita_percent: float, total_tcs: int):

    # Example intelligent logic
    if ita_percent >= 90:
        return "Achieved", 5
    elif ita_percent >= 70:
        return "In Progress", 4
    elif ita_percent >= 40:
        return "Lagging", 3
    elif ita_percent > 0:
        return "At Risk", 2
    else:
        return "Not Started", 1


# ==========================================================
# JSON LOADER + AUTO FIELD INJECTION
# ==========================================================
def load_projects():

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        raw_projects = json.load(f)

    updated = False
    projects = []

    for i, p in enumerate(raw_projects, start=1):

        # --------------------------------------------------
        # AUTO-GENERATE FIELDS IF MISSING
        # --------------------------------------------------
        total_tcs = p.get("total_tcs")
        automated_tcs = p.get("automated_tcs")
        ita_percent = p.get("ita_percent")

        if total_tcs is None:
            total_tcs = random.randint(150, 800)
            p["total_tcs"] = total_tcs
            updated = True

        if automated_tcs is None:
            automated_tcs = random.randint(0, total_tcs)
            p["automated_tcs"] = automated_tcs
            updated = True

        # Safety clamp
        automated_tcs = min(int(automated_tcs), int(total_tcs))

        if ita_percent is None:
            if total_tcs == 0:
                ita_percent = 0.0
            else:
                ita_percent = round((automated_tcs / total_tcs) * 100, 1)

            p["ita_percent"] = ita_percent
            updated = True

        ita_percent = float(ita_percent)

        # --------------------------------------------------
        # INTELLIGENT STATUS ENGINE
        # --------------------------------------------------
        status, priority = calculate_status(ita_percent, total_tcs)

        # --------------------------------------------------
        # DASHBOARD OBJECT
        # --------------------------------------------------
        projects.append({
            "rank": i,
            "name": p["name"],
            "status": status,
            "status_priority": priority,
            "percentage": ita_percent,
            "total": total_tcs,
            "automated": automated_tcs,
        })

    # --------------------------------------------------
    # WRITE BACK UPDATED JSON (AUTO-PERSIST NEW FIELDS)
    # --------------------------------------------------
    if updated:
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(raw_projects, f, indent=2, ensure_ascii=False)

    # Sort risk-first
    projects.sort(key=lambda x: x["status_priority"])

    return projects


# ==========================================================
# EXPORT FOR app.py
# ==========================================================
projects = load_projects()