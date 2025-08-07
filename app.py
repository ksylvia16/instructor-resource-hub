import streamlit as st
import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import os
import json
from functions import (
    clean_and_parse_date,
    add_ordinal_suffix,
    get_milestone_due_days,
    adjust_to_most_recent_friday,
    generate_friday_messages,
    get_fridays_between
)

# -------------------------------
# 🔧 App Config
# -------------------------------
st.set_page_config(page_icon='books', page_title="Instructor Resource Hub", layout="wide")


# -------------------------------
# 📂 Get list of available local CSVs
# -------------------------------
local_csvs = [
    f.replace(".csv", "") for f in os.listdir("csv_data") if f.endswith(".csv")
]

# -------------------------------
# 🖱️ Sidebar Controls
# -------------------------------
with st.sidebar:
    st.header("📂 Choose a Section")
    selected_sheet = st.selectbox("Section", [""] + sorted(local_csvs))

if selected_sheet:
    st.title(f"📚 Instructor Resource Hub — :blue[**{selected_sheet}**]")
else:
    st.title("📚 Instructor Resource Hub")

# -------------------------------
# 📥 Cached Google Loader
# -------------------------------
@st.cache_data(ttl=3600)
def fetch_sheet_data(sheet_name):
    ws = spreadsheet.worksheet(sheet_name)
    values = ws.get_all_values("A1:I25")
    if not values:
        return pd.DataFrame()
    df = pd.DataFrame(values[1:], columns=values[0])
    df["section"] = sheet_name
    df["date"] = df["date"].apply(lambda x: clean_and_parse_date(x))
    return df

# -------------------------------
# 🔁 Track selection and reset Google toggle
# -------------------------------
if "prev_selected_sheet" not in st.session_state:
    st.session_state.prev_selected_sheet = ""

if selected_sheet != st.session_state.prev_selected_sheet:
    st.session_state.use_google = False
    st.session_state.prev_selected_sheet = selected_sheet

# -------------------------------
# 📊 Tabs: LiveLab Schedule + HQ Announcements
# -------------------------------
if selected_sheet:
    col1, col2 = st.columns([1, 1.3]) 

    with col1:
        st.markdown(f"##### 📅 LiveLab Schedule")
        st.caption("This is your section's full LiveLab schedule — use to double check dates, topics, and plan ahead!")
        # ✅ Google Sheets toggle at bottom of all tabs
        st.toggle(
            "Is something missing? Toggle to connect to [this Google Sheet](https://docs.google.com/spreadsheets/d/1uRZxn6l4h41ek2dkR7Dfe-a-vzePoSRYPwaTEi2K6iw/edit?usp=sharing) for the most up-to-date version. _(⚠️ Heads up: Connecting via the API may take a few moments.)_",
            value=st.session_state.get("use_google", False),
            key="use_google")
        
        # Load data
        if st.session_state.get("use_google", False):
            # 🔐 Google Sheets Setup
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

            # Convert Streamlit secrets to dictionary
            creds_dict = dict(st.secrets["google_credentials"])

            # Create credentials with scope
            creds = Credentials.from_service_account_info(creds_dict, scopes=scope)

            # Authorize gspread client
            client = gspread.authorize(creds)

            # Open spreadsheet
            spreadsheet = client.open("Curriculum Schedules All Tracks")

            with st.spinner(f"Loading data for {selected_sheet} from Google Sheets..."):
                df = fetch_sheet_data(selected_sheet)
                df["section"] = selected_sheet
                df["date_display"] = df["date"].apply(lambda x: add_ordinal_suffix(x))
        else:
            csv_path = f"./csv_data/{selected_sheet}.csv"
            if os.path.exists(csv_path):
                with st.spinner(f"Loading data for {selected_sheet} from local file..."):
                    df = pd.read_csv(csv_path)
                    df["section"] = selected_sheet
                    df["date"] = df["date"].apply(lambda x: clean_and_parse_date(x))
                    df["date_display"] = df["date"].apply(lambda x: add_ordinal_suffix(x))

            else:
                st.error(f"⚠️ Local CSV not found: {csv_path}")
                st.stop()

        # Row count check
        num_labs = df["livelab_title"].notna().sum()
        if num_labs < 12:
            st.warning(f"⚠️ Only {num_labs} LiveLabs loaded from {selected_sheet}. "
                        "This might be incomplete — try toggling Google Sheets for the most up-to-date version.")

        # Display DataFrame (cleaned)
        display_df = df[["LL_num", "date_display", "livelab_title"]].rename(columns={
            "LL_num": "LiveLab #",
            "date_display": "Date",
            "livelab_title": "LiveLab Title"
        })
        st.dataframe(display_df, use_container_width=True, hide_index=True, height = 875)
    
    with col2:
        st.markdown(f"##### 📣 HQ Announcement Templates")
        st.caption("Quick-access templates you can copy for your Friday announcements, with each one customized based on your LiveLab schedule! Please just use these as *templates*, and feel free to make them your own!")
        
        if df["date"].notna().any():
            start_date = df["date"].min()
            end_date = df["date"].max()
            section = df["wave_section"].iloc[0] if "wave_section" in df.columns else None
            track = df["track"].iloc[0] if "track" in df.columns else None

            fridays = get_fridays_between(start_date, end_date)

            for friday in fridays:
                generate_friday_messages(df, track, friday, section=section)

        else:
            st.warning("⚠️ No dates found in the schedule.")


else:
    # -------------------------------
    # 💡 Simple Welcome Message
    # -------------------------------
    with st.container():
        st.write("This app was created to help instructors plan ahead, save time when writing HQ announcements, and easily find important due dates — no more digging through HQ each week. It brings everything you need into one place to keep your teaching workflow smooth and organized.")
        st.info("To get started, use the sidebar on the left to **select your section**.", icon = '⬅️')


    st.caption("Have a question, notice something off, or want to request a feature? [Message Katie Sylvia on Slack!](https://podiumglobal.slack.com/team/U03TJUYNSF8)")


