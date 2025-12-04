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

/* Fondo general suave */
.stApp {
    background: linear-gradient(135deg, #f5f7ff 0%, #e3f2fd 40%, #ffffff 100%);
}

/* SIDEBAR: fondo azul oscuro y texto blanco grande */
section[data-testid="stSidebar"] {
    background: #020617;  /* azul muy oscuro */
    color: #e5e7eb;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #f9fafb;
    font-size: 1.4rem;
    font-weight: 700;
}

/* Texto del menú (radio buttons, labels, etc.) */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #ffffff !important;
    font-size: 1.05rem !important;
    font-weight: 500 !important;
}

/* Contenedor principal tipo "tarjeta" (si lo usas en las páginas) */
.main-block {
    background-color: rgba(255, 255, 255, 0.96);
    border-radius: 18px;
    padding: 1.8rem 2.2rem;
    margin-top: 1rem;
    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.08);
}

/* Título principal más grande y elegante */
.main-title, h1 {
    font-size: 2.4rem !important;
    font-weight: 800 !important;
}

/* Estilos para la tabla de muestra (st.dataframe) */
[data-testid="stDataFrame"] thead tr th {
    background-color: #0f172a !important;
    color: #f9fafb !important;
    font-weight: 600;
}

[data-testid="stDataFrame"] tbody tr:nth-child(even) {
    background-color: #f1f5f9 !important;
}

[data-testid="stDataFrame"] tbody tr:nth-child(odd) {
    background-color: #ffffff !important;
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
        else:
            st.error("Unknown page selection.")
if __name__ == "__main__":
    main()
