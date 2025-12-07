from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
import streamlit as st

from data_loader import load_bike_data
from data_cleaning import (
    standardize_user_type,
    group_bike_model,
    parse_datetime_columns,
    clean_trip_duration,
    clean_station_fields,
)
from feature_engineering import (
    compute_distance_fields,
    add_time_features,
    add_weekend_flag,
    add_rush_hour_flag,
)
from station_normalization import normalize_station_fields
from utils import get_logger

logger = get_logger(__name__)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CLEAN_DATA_DIR = DATA_DIR / "clean"


@st.cache_data(show_spinner=True)
def get_bike_data(use_clean_file: bool = True) -> pd.DataFrame:

   #This is cached by Streamlit so multiple pages share the same df.
    
    clean_path = CLEAN_DATA_DIR / "toronto-bike-clean.csv"

    if use_clean_file and clean_path.exists():
        logger.info("Loading cleaned dataset from %s", clean_path)
        df = pd.read_csv(clean_path)
        #I am checking the presence of a datetime field and ensuring its [passed] if present
        for col in ["start_time", "end_time"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        return df

    logger.info("Cleaned file not found. Running full pipeline from raw.")
    df = load_bike_data("toronto-bike.csv")
    df = standardize_user_type(df)
    df = group_bike_model(df)
    df = parse_datetime_columns(df)
    df = clean_trip_duration(df)
    df = clean_station_fields(df)
    df = normalize_station_fields(df)
    df = compute_distance_fields(df)
    df = add_time_features(df)
    df = add_weekend_flag(df)
    df = add_rush_hour_flag(df)

    return df
