from datetime import datetime, timedelta
import pandas as pd

# -------------------------------
# 🧹 Clean and Parse Dates
# -------------------------------
def clean_and_parse_date(date_str, fallback_year=None):
    """
    Extracts MM/DD from strings like 'Monday, 09/01 SKIPPED FOR HOLIDAY!' 
    and returns a datetime object.
    """
    try:
        parts = date_str.split(", ")
        if len(parts) < 2:
            return None
        mmdd_part = parts[1].strip().split()[0]  # "09/01"
        if fallback_year is None:
            fallback_year = datetime.now().year
        return datetime.strptime(f"{mmdd_part}/{fallback_year}", "%m/%d/%Y")
    except Exception:
        return None

# -------------------------------
# 📅 Add Ordinal Suffix to Dates
# -------------------------------
def add_ordinal_suffix(date):
    """
    Adds an ordinal suffix (st, nd, rd, th) to the day of a datetime object.
    """
    if date is None:
        return "Unknown Date"

    day = date.day
    if 11 <= day <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

    return date.strftime(f"%A, %B {day}{suffix}")

# -------------------------------
# 📆 Get Milestone Due Days by Section
# -------------------------------
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

# -------------------------------
# 🗓️ Adjust to Most Recent Friday
# -------------------------------
def adjust_to_most_recent_friday(date):
    """
    Given any date, returns the most recent Friday (or the same day if it's already Friday).
    """
    return date - timedelta(days=(date.weekday() - 4) % 7)


# -------------------------------
# 🗓️ Get list of Fridays
# -------------------------------
def get_fridays_between(start_date, end_date):
    fridays = []
    current = start_date
    # Go forward to the first Friday
    while current.weekday() != 4:
        current += timedelta(days=1)
    while current <= end_date:
        fridays.append(current)
        current += timedelta(weeks=1)
    return fridays

# -------------------------------
# 🗓️ Generate Messages
# -------------------------------

def generate_friday_messages(df, track, friday_date, section=None):
    import streamlit as st
    from datetime import datetime, timedelta
    import pandas as pd

    if isinstance(friday_date, str):
        try:
            friday_date = datetime.strptime(friday_date, "%m-%d-%Y")
        except ValueError:
            st.warning("⚠️ Invalid date format. Use MM-DD-YYYY.")
            return

    if friday_date.weekday() != 4:
        st.warning(f"⚠️ {add_ordinal_suffix(friday_date)} is not a Friday.")
        friday_date = adjust_to_most_recent_friday(friday_date)
        st.info(f"🔄 Adjusted to most recent Friday: {add_ordinal_suffix(friday_date)}")

    df = df[df["track"] == track]
    sections_to_process = [section] if section else df["wave_section"].unique()

    for sec in sections_to_process:
        section_df = df[df["wave_section"] == sec]
        upcoming = section_df[section_df["date"] > friday_date].sort_values("date")
        past = section_df[section_df["date"] <= friday_date].sort_values("date", ascending=False)

        if past.empty:
            st.error(f"❌ No past LiveLabs for section {sec}.")
            continue

        last = past.iloc[0]
        last_ll_num = last["LL_num"]
        last_ll_title = last["livelab_title"]
        last_ll_date = last["date"]

        next_lab = upcoming.iloc[0] if not upcoming.empty else None
        if next_lab is not None:
            next_ll_num = next_lab["LL_num"]
            next_ll_title = next_lab["livelab_title"] if pd.notna(next_lab["livelab_title"]) else "an upcoming LiveLab"
            next_ll_date = next_lab["date"]
            next_ll_description = next_lab["notes"] if pd.notna(next_lab["notes"]) else "No description available 😅"
            skillbuilder_before = next_lab["videos_watch_by"] if pd.notna(next_lab["videos_watch_by"]) else None
        else:
            next_ll_num = next_ll_title = next_ll_date = next_ll_description = skillbuilder_before = None

        future_skillbuilder = upcoming[upcoming["videos_watch_by"].notna()].iloc[0] if not upcoming[upcoming["videos_watch_by"].notna()].empty else None
        future_skillbuilder_name = future_skillbuilder["videos_watch_by"] if future_skillbuilder is not None else None
        future_skillbuilder_ll = future_skillbuilder["LL_num"] if future_skillbuilder is not None else None
        future_skillbuilder_date = future_skillbuilder["date"] if future_skillbuilder is not None else None

        milestone_due = last.get("assignment_due_after", None)
        milestone_due_date = None
        if pd.notna(milestone_due):
            due_days = get_milestone_due_days(sec)
            for day in due_days:
                idx = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(day)
                possible_due = last_ll_date + timedelta((idx - last_ll_date.weekday()) % 7)
                if milestone_due_date is None or possible_due < milestone_due_date:
                    milestone_due_date = possible_due

        next_milestone_lab = upcoming[upcoming["assignment_due_after"].notna()].iloc[0] if not upcoming[upcoming["assignment_due_after"].notna()].empty else None
        next_milestone = next_milestone_due_date = None
        if next_milestone_lab is not None:
            next_milestone = next_milestone_lab["assignment_due_after"]
            base_date = next_milestone_lab["date"]
            due_days = get_milestone_due_days(sec)
            for day in due_days:
                idx = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(day)
                possible_due = base_date + timedelta((idx - base_date.weekday()) % 7)
                if next_milestone_due_date is None or possible_due < next_milestone_due_date:
                    next_milestone_due_date = possible_due

        with st.expander(f"📢 Post on **:blue[{add_ordinal_suffix(friday_date)}]**"):
            st.warning(f'**INSTRUCTOR SANITY CHECK**: The most recent LiveLab was **{last_ll_num}: {last_ll_title}** on {add_ordinal_suffix(last_ll_date)}', icon="🔎")
            st.markdown("""
                ### Hey everyone! 👋

                Thanks for hanging out with me in lab this week! Here's what's coming up ⬇️
                """)
            if milestone_due and milestone_due_date and (next_ll_date is None or milestone_due_date <= next_ll_date):
                st.markdown(f"🎯 **Don't forget!** **:green[{milestone_due}]** is due on **{add_ordinal_suffix(milestone_due_date)}**. Swing by a drop-in session or reach out to the HelpHub with any questions!")
            elif next_milestone and next_milestone_due_date:
                st.markdown(f"🔜 **Heads up!** Your next milestone, {next_milestone}, is due on **{add_ordinal_suffix(next_milestone_due_date)}**.")
            else:
                st.markdown("ℹ️ No scheduled milestones to announce.")

            if next_lab is not None:
                if str(next_ll_title).strip().lower() == "holiday":
                    st.markdown(f"🎉 The next scheduled day, **{add_ordinal_suffix(next_ll_date)}**, is a holiday — there will be no LiveLab that day. Enjoy your break!")
                else:
                    st.markdown(f"⏭️ Your next LiveLab is **{next_ll_title}** on **{add_ordinal_suffix(next_ll_date)}**. {next_ll_description}")
                    if skillbuilder_before:
                        st.markdown(f"🍿 To prepare, please be sure to watch **:blue[{skillbuilder_before}]** before then.")
                    elif future_skillbuilder_name and future_skillbuilder_ll:
                        st.markdown(f"📌 While there's no SkillBuilder due before the next LiveLab, your next one will be **{future_skillbuilder_name}** for {future_skillbuilder_ll} on **{add_ordinal_suffix(future_skillbuilder_date)}**.")
                    else:
                        st.markdown("📌 No upcoming SkillBuilders found in the schedule.")
            else:
                st.markdown("⏭️ No upcoming LiveLabs scheduled.")
            
            st.markdown("Have a wonderful weekend, and see you all next week!")



