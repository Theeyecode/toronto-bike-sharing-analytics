from __future__ import annotations

import pandas as pd
import streamlit as st


def render(df: pd.DataFrame) -> None:
    st.title("Station & Route Insights — Jorge & Ingrid")

    st.markdown(
        """
        This page is owned by **Jorge**, with **Ingrid**.

        It includes:
        - Top **start stations** and **end stations**
        - Story 9 insights
        - **Origin–Destination (OD) flows** (most common routes)
        """
    )

    df["route"] = df["Start Station Name"] + " → " + df["End Station Name"]

    top_start = (
        df["Start Station Name"]
        .value_counts()
        .reset_index(name="Trips")
        .rename(columns={"index": "Start Station Name"})
        .head(10)
    )

    top_end = (
        df["End Station Name"]
        .value_counts()
        .reset_index(name="Trips")
        .rename(columns={"index": "End Station Name"})
        .head(10)
    )


    top_routes = (
        df["route"]
        .value_counts()
        .reset_index(name="Trips")
        .rename(columns={"index": "Route"})
        .head(10)
    )

    st.subheader("Station & Route Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🚲 Top Start Stations")
        st.dataframe(top_start, use_container_width=True)

        st.bar_chart(
            top_start.set_index("Start Station Name")["Trips"],
            use_container_width=True,
        )

        st.markdown("### 🅿️ Top End Stations")
        st.dataframe(top_end, use_container_width=True)

        st.bar_chart(
            top_end.set_index("End Station Name")["Trips"],
            use_container_width=True,
        )

    with col2:
        st.markdown("### 🔀 Most Common Origin–Destination Routes")
        st.dataframe(top_routes, use_container_width=True)

        st.bar_chart(
            top_routes.set_index("route")["Trips"],
            use_container_width=True,
        )

    st.markdown("---")
    st.markdown(
        """
        ### Developer Notes
        - Uses columns: **Start Station Name**, **End Station Name**.
        - Computes OD pair as `"start → end"`.
        - Shows top 10 busiest stations & routes.
        - Fully compatible with cleaned dataset.
        """
    )