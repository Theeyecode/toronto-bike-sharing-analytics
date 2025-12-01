from __future__ import annotations

import pandas as pd
import streamlit as st


def render(df: pd.DataFrame) -> None:
    st.title("Station & Route Insights — Jorge & Ingrid")

    st.markdown(
    
    """
        This page is owned by **Jorge**, with **Ingrid**.

        It will include:
        - Top **start stations** and **end stations**
        - Station usage by user type or time
        - check Story 9 for more details
        - **Origin–Destination (OD) flows** (most common routes)
        """

       
    )

    st.subheader("Layout Placeholder")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Top Stations")
        st.info("TODO (Jorge): Add tables / bar charts for busiest start/end stations.")
    with col2:
        st.markdown("#### Route Flows / OD Pairs")
        st.info("TODO (Jorge): Add visual for popular station-to-station routes.")

    st.markdown(
     
             """
        **Developer notes goes here :**

        """

    )
