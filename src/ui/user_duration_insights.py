from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st
import numpy as np
import altair as alt

PLOTS_DIR = Path(__file__).resolve().parents[2] / "outputs" / "plots"

def render(df: pd.DataFrame) -> None:
    st.title("User & Duration Insights")

    st.markdown(
        """
        This page was created by **Javier**,and **Ingrid**.

        ### Purpose
        This section fulfills **Story #10 and #11**, providing:
        - Comparative metrics between **Casual** and **Annual** users
        - Trip duration distributions using the cleaned column `trip_duration_clean`
        - Segmentation by standardized user type
        """
    )

    # Resolve column names
    user_type_col = "user_type_standardized"
    duration_col = "trip_duration_clean"

    # Validate columns
    if user_type_col not in df.columns:
        st.error(f"Column '{user_type_col}' not found in dataset.")
        st.write("Available columns:", df.columns.tolist())
        return

    if duration_col not in df.columns:
        st.error(f"Column '{duration_col}' not found in dataset.")
        st.write("Available columns:", df.columns.tolist())
        return

    # Convert duration to minutes for all visualizations & stats
    duration_min = df[duration_col] / 60

    # --- USER TYPE BREAKDOWN ---
    st.subheader("User Type Breakdown")
    user_counts = df[user_type_col].value_counts()

    col1, col2 = st.columns(2)
    user_type_img = PLOTS_DIR / "user_type_comparison.png"

    with col1:
        st.markdown("#### Total Trips by User Type")
        st.bar_chart(user_counts, use_container_width=True)

        if user_type_img.exists():
            st.image(
                str(user_type_img),
                caption="Trips by User Type",
                use_container_width=True,
            )
        else:
            st.warning(f"Image not found: {user_type_img}")

    with col2:
        st.markdown("#### Percentage Breakdown")
        st.write((user_counts / user_counts.sum() * 100).round(2))

    # --- TRIP DURATION DISTRIBUTION ---
    st.subheader("Trip Duration Distribution (trip_duration_clean)")
    st.markdown("Trip durations shown in **minutes** (cleaned).")

    st.write("Summary Statistics (minutes):")
    st.write(duration_min.describe())

    st.markdown("#### Histogram (minutes)")
    hist_vals, hist_edges = np.histogram(duration_min, bins=30)

    st.bar_chart(
        pd.DataFrame({"count": hist_vals}, index=hist_edges[:-1]),
        use_container_width=True,
    )

    # --- BOXPLOT (MINUTES) ---
    st.markdown("#### Boxplot (minutes)")
    sample = df.sample(n=5000, random_state=42) if len(df) > 5000 else df
    sample = sample.copy()
    sample["duration_min"] = sample[duration_col] / 60

    box = alt.Chart(sample).mark_boxplot().encode(
        y=alt.Y("duration_min:Q", title="Trip Duration (min)"),
        color=alt.Color(f"{user_type_col}:N", title="User Type"),
    )

    st.altair_chart(box, use_container_width=True)

    # --- SEGMENTATION BY USER TYPE ---
    st.subheader("Trip Duration by User Type (minutes)")
    grouped = (
        df.assign(duration_min=duration_min)
        .groupby(user_type_col)["duration_min"]
        .describe()
    )
    st.write(grouped)

    # --- DEVELOPER NOTES ---
    st.info("Developer notes:")
    st.markdown(
        """
        - Using column: `user_type_standardized` for segmentation
        - Using column: `trip_duration_clean` converted to **minutes** for all stats and charts
        - Charts configured with `use_container_width=True` for responsive layout
        - Ready for **Story #10 & #11** (Casual vs Annual user insights + duration distribution)
        """
    )
