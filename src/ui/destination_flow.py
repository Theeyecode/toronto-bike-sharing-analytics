from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

def render(df: pd.DataFrame) -> None:
    st.title("Destination Flow Insights — Major Station Pairs")

    st.markdown(
        """
        This page is owned by **Jorge**.

        **Includes:**
        - Sankey / Flow network visualization  
        - Top high-traffic origin–destination station pairs  
        - Optimized for large datasets  
        """
    )

    df["route"] = df["Start Station Name"] + " → " + df["End Station Name"]

    top_routes = (
        df["route"]
        .value_counts()
        .reset_index(name="Trips")
        .rename(columns={"index": "Route"})
        .head(20)         # LIMIT — improves Sankey performance
    )

    top_routes[ "Start" ] = top_routes["route"].str.split(" → ").str[0]
    top_routes[ "End" ]   = top_routes["route"].str.split(" → ").str[1]

    st.subheader("Top 20 Most Common Origin–Destination Routes")
    st.dataframe(top_routes, use_container_width=True)

    stations = list(pd.concat([top_routes["Start"], top_routes["End"]]).unique())

    id_map = {station: idx for idx, station in enumerate(stations)}

    # Build Sankey links
    source_indices = top_routes["Start"].map(id_map)
    target_indices = top_routes["End"].map(id_map)
    values = top_routes["Trips"]

    sankey_fig = go.Figure(
        data=[
            go.Sankey(
                node=dict(
                    pad=18,
                    thickness=18,
                    line=dict(color="white", width=0.5),
                    label=stations,
                    color="#1e293b"  # dark slate
                ),
                link=dict(
                    source=source_indices,
                    target=target_indices,
                    value=values,
                    color="rgba(59,130,246,0.4)"  # translucent blue
                ),
            )
        ]
    )

    sankey_fig.update_layout(
        title="Major Station Movement Flow (Sankey Diagram)",
        font=dict(color="white", size=14),
        paper_bgcolor="black",
        plot_bgcolor="black"
    )

    st.subheader("🔀 Route Flow Network (Sankey Chart)")
    st.plotly_chart(sankey_fig, use_container_width=True)

    st.markdown("---")
    st.markdown(
        """
        ### Developer Notes
        - **Uses Plotly Sankey** for high-performance visualization.
        - Optimized by limiting to **Top 20 OD pairs**.
        - Uses columns:  
          - `Start Station Name`  
          - `End Station Name`  
        - Automatically constructs node indexing and flow weights.
        - Fully compatible with your dark theme.
        """
    )