import json
from pathlib import Path

JSON_FILE = Path("input.json")


# ==========================================================
# STATUS ENGINE (Smart Rules)
# ==========================================================
def calculate_status(ita_percent: float, total_tcs: int):

    if ita_percent >= 60:
        return "Achieved", 5
    elif 45 <= ita_percent < 59:
        return "In Progress", 4
    elif 0 <= ita_percent < 44:
        return "At Risk", 3
    else:
        return "Not Started", 1


# ==========================================================
# JSON LOADER (READ ONLY FROM JSON)
# ==========================================================
def load_projects():

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    raw_projects = data["projects"]
    org_summary = data["summary"]

    projects = []

    for i, p in enumerate(raw_projects, start=1):

        total_tcs = int(p["total_tcs"])
        automated_tcs = int(p["automated_tcs"])
        ita_percent = float(p["ita_percent"])

        # --------------------------------------------------
        # STATUS ENGINE
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

    # Sort risk-first
    projects.sort(key=lambda x: x["status_priority"])

    return projects, org_summary


# ==========================================================
# EXPORT FOR app.py
# ==========================================================
projects, org_summary = load_projects()