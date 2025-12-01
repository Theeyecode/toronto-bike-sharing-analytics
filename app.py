from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Ensure src is importable
PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

try:
    from app_data import get_bike_data
    from ui.overview import render as render_overview
    from ui.time_trends import render as render_time_trends
    from ui.user_duration_insights import render as render_user_duration
    from ui.station_route_insights import render as render_station_route
except Exception as e:
    st.set_page_config(page_title="Toronto Bike-Sharing Analytics", page_icon="🚲", layout="wide")
    st.title("Toronto Bike-Sharing Analytics")
    st.error("❌ Failed to import modules from src/. Check folder names & files.")
    st.exception(e)
    st.stop()



def main() -> None:
    st.set_page_config(
        page_title="Toronto Bike-Sharing Analytics",
        page_icon="🚲",
        layout="wide",
    )

    df = get_bike_data()

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        (
            "Overview",
            "Time-based Trends (Dhruv)",
            "User & Duration Insights (Javier & Ingrid)",
            "Station & Route Insights (Jorge & Ingrid)",
        ),
    )

    if page == "Overview":
        render_overview(df)
    elif page.startswith("Time-based Trends"):
        render_time_trends(df)
    elif page.startswith("User & Duration Insights"):
        render_user_duration(df)
    elif page.startswith("Station & Route Insights"):
        render_station_route(df)
    else:
        st.error("Unknown page selection.")


if __name__ == "__main__":
    main()
