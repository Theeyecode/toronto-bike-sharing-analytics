from __future__ import annotations

import pandas as pd
import streamlit as st


def render(df: pd.DataFrame) -> None:
    st.title("User & Duration Insights — Javier & Ingrid")

    st.markdown(
            """
        This page is owned by **Javier**, with **Ingrid**.

        It will show:
        - Differences between **Casual** and **Annual** users
        - Trip duration distributions (using `trip_duration_clean`)
        - check Stroy #10 and #11
        - Possibly segmenting by time of day or station type
        """

       
    )

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
