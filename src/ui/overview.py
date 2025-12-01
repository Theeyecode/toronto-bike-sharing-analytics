from __future__ import annotations

import pandas as pd
import streamlit as st


def render(df: pd.DataFrame) -> None:
    st.title("Toronto Bike-Sharing — Overview")



    total_trips = len(df)
    start_date = df["start_time"].min() if "start_time" in df.columns else None
    end_date = df["start_time"].max() if "start_time" in df.columns else None
    n_users = df["user_type_standardized"].nunique() if "user_type_standardized" in df.columns else None

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Trips", f"{total_trips:,}")
    if start_date is not None and end_date is not None:
        col2.metric("Date Range", f"{start_date.date()} → {end_date.date()}")
    if n_users is not None:
        col3.metric("User Types", n_users)

    st.markdown("### Sample of Cleaned Data")
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown(
        #Dashboard explanation goes here
         
             """
        **Developer notes goes here :**

        """
    )
