from datetime import date
TARGET = 60

STATUS_PRIORITY = {
    "Not Started": 1,
    "At Risk": 2,
    "Lagging": 3,
    "In Progress": 4,
    "Achieved": 5
}

projects = []

for i in range(1, 26):
    total = 500 + (i * 40)

    # Coverage from 0% to 100%
    coverage_factor = (i % 11) / 9   # 0.0 → 1.0
    automated = int(total * coverage_factor)

    project = {
        "name": f"Project {i}",
        "total": total,
        "automated": automated,
        
        # 👇 NEW FIELDS
        "milestone": f"Milestone {((i - 1) % 3) + 1}",
        "closure_date": "Feb 28"
    }
    
    # Dummy closure dates spread around today
    closure_offset_days = (i % 10) - 5   # -5 to +4 days
    closure_dt = date.today().replace(day=28)  # stable base date

    project["closure_date"] = closure_dt.strftime("%b %d")
    project["days_remaining"] = closure_offset_days
    
    if project["days_remaining"] < 0:
        project["closure_status"] = "overdue"
    elif project["days_remaining"] == 0:
        project["closure_status"] = "due-today"
    else:
        project["closure_status"] = "on-track"

    # Automation percentage
    project["percentage"] = round(
        (project["automated"] / project["total"]) * 100, 1
    )

    percentage = project["percentage"]

    if percentage == 0:
        project["status"] = "Not Started"

    elif percentage <= 15:
        project["status"] = "At Risk"

    elif percentage <= 45:
        project["status"] = "Lagging"

    elif percentage <= 65:
        project["status"] = "In Progress"

    else:
        project["status"] = "Achieved"

    project["status_priority"] = STATUS_PRIORITY[project["status"]]

    projects.append(project)

# Default sort: Risk-first
projects.sort(key=lambda p: p["status_priority"])

# Assign rank after sorting
for idx, p in enumerate(projects, start=1):
    p["rank"] = idx