from datetime import datetime


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 📆 MUST EDIT: Get Milestone Due Days by Section
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def get_milestone_due_days(section_name):
    """
    Returns a list of due days (e.g., ['Sunday', 'Wednesday']) based on section suffix.
    """
    suffix = section_name.strip().split()[-1]  # Expects something like "1A", "2B", etc.

    if suffix in ["1A", "2A", "3A"]:
        return ["Tuesday", "Saturday"]
    elif suffix in ["1B", "2B"]:
        return ["Wednesday", "Sunday"]
    elif suffix == "2C":
        return ["Thursday", "Monday"]
    else:
        return []


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 📆 MUST EDIT: Custom Project Due Dates
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PROJECT_DUE_DATES = {
    ("DA Section 1A", "portfolio project: analyzing website data with the grammys"): datetime(2025, 10, 5),
    ("DA Section 1B", "portfolio project: analyzing website data with the grammys"): datetime(2025, 10, 5),
    ("DA Section 2A", "portfolio project: analyzing website data with the grammys"): datetime(2025, 10, 5),
    ("DA Section 2B", "portfolio project: analyzing website data with the grammys"): datetime(2025, 10, 5),
    ("DA Section 2C", "portfolio project: analyzing website data with the grammys"): datetime(2025, 10, 5),
    ("DC Section 1A", "portfolio project: an intel data center"): datetime(2025, 10, 5),
    ("DC Section 1B", "portfolio project: an intel data center"): datetime(2025, 10, 5),
    ("DC Section 2A", "portfolio project: an intel data center"): datetime(2025, 10, 5),
    ("DC Section 2B", "portfolio project: an intel data center"): datetime(2025, 10, 5),
    ("DC Section 2C", "portfolio project: an intel data center"): datetime(2025, 10, 5),
    ("DM Section 1A", "portfolio project"): datetime(2025, 10, 5),
    ("DM Section 1B", "portfolio project"): datetime(2025, 10, 5),
    ("DM Section 2A", "portfolio project"): datetime(2025, 10, 5),
    ("DM Section 2B", "portfolio project"): datetime(2025, 10, 5),
    ("DM Section 2C", "portfolio project"): datetime(2025, 10, 5),
    ("DA Section 1A", "portfolio project: build a data center with intel"): datetime(2025, 11, 30),
    ("DA Section 1B", "portfolio project: build a data center with intel"): datetime(2025, 11, 30),
    ("DA Section 2A", "portfolio project: build a data center with intel"): datetime(2025, 11, 16),
    ("DA Section 2B", "portfolio project: build a data center with intel"): datetime(2025, 11, 16),
    ("DA Section 2C", "portfolio project: build a data center with intel"): datetime(2025, 11, 16),
    ("DC Section 1A", "portfolio project: analyzing website performance for the grammys"): datetime(2025, 11, 30),
    ("DC Section 1B", "portfolio project: analyzing website performance for the grammys"): datetime(2025, 11, 30),
    ("DC Section 2A", "portfolio project: analyzing website performance for the grammys"): datetime(2025, 11, 16),
    ("DC Section 2B", "portfolio project: analyzing website performance for the grammys"): datetime(2025, 11, 16),
    ("DC Section 2C", "portfolio project: analyzing website performance for the grammys"): datetime(2025, 11, 16),

}