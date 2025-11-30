from __future__ import annotations

import pandas as pd
import streamlit as st


def render(df: pd.DataFrame) -> None:
    st.title("Time-based Trends — Dhruv")

    st.markdown(
        
          """
        This page is owned by **Dhruv**.

        It will include:
        - Trip counts by **hour of day**
        - Patterns by **day of week / weekend vs weekday**
        - Possibly **monthly/seasonal** 
        - check Story #8 for more details

        Ingrid will help here later with design & styling of the charts.
        """


       
    )

    st.subheader("Layout Placeholder")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Trips by Hour of Day")
        st.info("TODO (Dhruv): Add line/bar chart of trips vs hour_of_day.")
    with col2:
        st.markdown("#### Trips by Day of Week")
        st.info("TODO (Dhruv): Add chart using weekday / weekend flags.")

    st.markdown(
        

             """
        **Developer notes goes here :**

        """
       
    )
