from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# -------------------------------------------------------------------
# Make the src/ folder importable so we can reuse the pipeline code
# -------------------------------------------------------------------
SRC_DIR = Path(__file__).resolve().parents[1]  # .../src
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from data_loader import load_bike_data
from data_cleaning import (
    standardize_user_type,
    group_bike_model,
    parse_datetime_columns,
    clean_trip_duration,
    clean_station_fields,
)
from station_normalization import normalize_station_fields
from feature_engineering import (
    compute_distance_fields,
    add_time_features,
    add_weekend_flag,
    add_rush_hour_flag,
)

from insights.user_duration_insights import render as render_user_duration_insights


# -------------------------------------------------------------------
# Data loading + preparation (same lógica que en main.py)
# -------------------------------------------------------------------
@st.cache_data(show_spinner="Loading & preparing Toronto bike data...")
def get_prepared_data() -> pd.DataFrame:
    """Load raw CSV and apply cleaning & feature engineering pipeline."""
    df = load_bike_data("toronto-bike.csv")

    # Cleaning & standardization
    df = standardize_user_type(df)
    df = group_bike_model(df)
    df = parse_datetime_columns(df)
    df = clean_trip_duration(df)
    df = clean_station_fields(df)
    df = normalize_station_fields(df)

    # Feature engineering
    df = compute_distance_fields(df)
    df = add_time_features(df)
    df = add_weekend_flag(df)
    df = add_rush_hour_flag(df)

    return df


# -------------------------------------------------------------------
# Streamlit app
# -------------------------------------------------------------------
def main() -> None:
    st.set_page_config(
        page_title="Toronto Bike Sharing – User & Duration Insights",
        layout="wide",
    )

    st.sidebar.title("Toronto Bike Analytics")
    st.sidebar.markdown(
        """
        **Story #9 – User Type Visualizations**

        This dashboard uses the cleaned & engineered dataset
        from our pipeline to explore:
        - User types (Casual vs Annual)
        - Trip durations
        - Behaviour patterns
        """
    )

    df = get_prepared_data()

    with st.expander("🔍 Dataset preview & schema", expanded=False):
        st.write("Shape:", df.shape)
        st.write(df.head())
        st.write("Columns:", list(df.columns))

    # Render the dedicated insights page (Javier & Ingrid)
    render_user_duration_insights(df)


if __name__ == "__main__":
    main()
