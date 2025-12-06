from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st

PLOTS_DIR = Path(__file__).resolve().parents[2] / "outputs" / "plots"

def render(df: pd.DataFrame) -> None:
    st.title("Station & Route Insights")

    st.markdown(
        """
        This page is owned by **Jorge**, with **Ingrid**.

        It will include:
        - Top **start stations** and **end stations**
        - Station usage by user type or time
        - Check Story #9 for more details
        - **Origin–Destination (OD) flows** (most common routes)
        """
    )

    st.subheader("Station & Route Overview")

    col1, col2 = st.columns(2)

    top_stations_img = PLOTS_DIR / "top_busiest_stations.png"

    with col1:
        st.markdown("#### Top 10 Busiest Start Stations")
        if top_stations_img.exists():
            st.image(
                str(top_stations_img),
                use_column_width=True,
            )
        else:
            st.warning(f"Image not found: {top_stations_img}")

    with col2:
        st.markdown("#### Busiest End Stations")
        st.info("Placeholder for busiest end stations chart (to be added).")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### Route Flows / OD Pairs")
        st.info("Placeholder for OD flows visual (e.g. most common routes).")

    with col4:
        st.markdown("#### Station Usage by User Type / Time")
        st.info("Placeholder for heatmap or time-of-day vs station chart.")

    st.markdown(
        """
        **Developer notes goes here :**
        - Add charts/tables for end stations and OD flows.
        - Replace placeholders as new visuals are ready.
        """
    )