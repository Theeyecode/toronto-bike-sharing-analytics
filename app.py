from __future__ import annotations
import sys
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Toronto Bike-Sharing Analytics",
    page_icon="🚲",
    layout="wide",
)

CUSTOM_CSS = """
<style>

/* Forzar modo oscuro en toda la app */
:root {
    color-scheme: dark !important;
}

/* Fondo general negro */
.stApp {
    background: #000000 !important;
    color: #ffffff !important;
}

/* Sidebar negro */
section[data-testid="stSidebar"] {
    background: #000000 !important;
    color: #ffffff !important;
}

/* Títulos del sidebar */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* Texto del sidebar */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #ffffff !important;
}

/* Contenedor principal tipo tarjeta */
.main-block {
    background-color: #111111 !important;
    color: #ffffff !important;
    border-radius: 18px;
    padding: 1.8rem 2.2rem;
    margin-top: 1rem;
    box-shadow: 0 0 25px rgba(255,255,255,0.08);
}

/* Títulos principales blancos */
.main-title, h1, h2, h3, h4, h5 {
    color: #ffffff !important;
}

/* Tablas oscuro total */
[data-testid="stDataFrame"] thead tr th {
    background-color: #111111 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
}

[data-testid="stDataFrame"] tbody tr:nth-child(even) {
    background-color: #1a1a1a !important;
    color: #ffffff !important;
}

[data-testid="stDataFrame"] tbody tr:nth-child(odd) {
    background-color: #000000 !important;
    color: #ffffff !important;
}

/* Inputs y selects tema oscuro */
input, textarea, select {
    background-color: #111111 !important;
    color: #ffffff !important;
    border: 1px solid #444444 !important;
}

.stTextInput input,
.stSelectbox div[data-baseweb="select"],
.stNumberInput input {
    background-color: #111111 !important;
    color: #ffffff !important;
    border: 1px solid #444444 !important;
}

/* Botones en modo oscuro */
.stButton button {
    background-color: #222222 !important;
    color: #ffffff !important;
    border: 1px solid #555555 !important;
}

.stButton button:hover {
    background-color: #333333 !important;
    color: #ffffff !important;
}

</style>
"""

def inject_custom_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

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
    from ui.destination_flow import render as render_destination_flow
except Exception as e:

    st.title("Toronto Bike-Sharing Analytics")
    st.error("❌ Failed to import modules from src/. Check folder names & files.")
    st.exception(e)
    st.stop()
    
def main() -> None:
        inject_custom_css()
        df = get_bike_data()

        st.sidebar.markdown("### 🚲 Toronto Bike-Sharing Analytics")
        st.sidebar.caption("Use the menu below to explore the insights:")

        page = st.sidebar.radio(
            "Go to",
            (
                "Overview",
                "Time-based Trends",
                "User & Duration Insights",
                "Station & Route Insights",
                "Destination Flow"
            ),
        )



       
        st.sidebar.markdown(
        """
        <div style="
            text-align: center;
            font-size: 20rem;       /* tamaño gigante */
            line-height: 1;
            margin-top: 2rem;
        ">
            🚲
        </div>
        """,
        unsafe_allow_html=True,
        )

        if page == "Overview":
            render_overview(df)
        elif page.startswith("Time-based Trends"):
            render_time_trends(df)
        elif page.startswith("User & Duration Insights"):
            render_user_duration(df)
        elif page.startswith("Station & Route Insights"):
            render_station_route(df)
        elif page.startswith("Destination Flow"):
            render_destination_flow(df)
        else:
            st.error("Unknown page selection.")
if __name__ == "__main__":
    main()
