from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st

PLOTS_DIR = Path(__file__).resolve().parents[2] / "outputs" / "plots"

def render(df: pd.DataFrame) -> None:
    st.title("User & Duration Insights")
    st.markdown("### User Type Breakdown")

    PLOTS_DIR = Path(__file__).resolve().parents[2] / "outputs" / "plots"

def render(df):
    st.title("User & Duration Insights")

    col1, col2 = st.columns(2)

    # Gráfica 1: Trips by User Type
    user_type_img = PLOTS_DIR / "user_type_comparison.png"

    with col1:
        if user_type_img.exists():
            st.image(
                str(user_type_img),
                caption="Trips by User Type",
                use_column_width=True,
            )
        else:
            st.warning(f"Image not found: {user_type_img}")

    with col2:
        st.info("Placeholder for chart 2 (e.g. Trip duration distribution).")

    # ---------------- SEGUNDA FILA (gráficas 3 y 4) ----------------
    col3, col4 = st.columns(2)

    with col3:
        st.info("Placeholder for chart 3.")

    with col4:
        st.info("Placeholder for chart 4.")

        st.subheader("Layout Placeholder")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### User Type Breakdown")
            st.info("TODO (Javier): Add charts comparing Casual vs Annual usage.")
        with col2:
            st.markdown("#### Trip Duration Distribution")
            st.info("TODO (Javier): Add histogram / boxplot of trip_duration_clean.")

    st.markdown(
       
     
             """
        **Developer notes goes here :**

        """
    
    )
