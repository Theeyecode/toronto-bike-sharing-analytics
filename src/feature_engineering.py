import pandas as pd
from utils import get_logger
import numpy as np

logger = get_logger(__name__)


def compute_distance_fields(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # Check necessary columns
    required_cols = [
        "Start Station Latitude", "Start Station Longitude",
        "End Station Latitude", "End Station Longitude"
    ]

    if not all(col in df.columns for col in required_cols):
        logger.warning("Distance fields cannot be computed — missing lat/lon columns.")
        return df

    R = 6371  # Earth radius in km

    lat1 = np.radians(df["Start Station Latitude"])
    lon1 = np.radians(df["Start Station Longitude"])
    lat2 = np.radians(df["End Station Latitude"])
    lon2 = np.radians(df["End Station Longitude"])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2 +
        np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    )
    c = 2 * np.arcsin(np.sqrt(a))

    df["trip_distance_km"] = R * c

    logger.info("Computed distance fields.")
    return df


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # Ensure start_time is a datetime type
    df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")

    # Raise error if conversion failed (all NaT)
    if df["start_time"].isna().all():
        raise ValueError("start_time column cannot be converted to datetime")

    df["start_hour"] = df["start_time"].dt.hour
    df["start_day"] = df["start_time"].dt.day
    df["start_month"] = df["start_time"].dt.month
    df["start_weekday"] = df["start_time"].dt.day_name()

    logger.info("Added time-extracted fields (hour, day, month, weekday).")
    return df


def add_weekend_flag(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["is_weekend"] = df["start_time"].dt.weekday >= 5  # Sat=5, Sun=6

    logger.info("Added weekend flag.")
    return df


def add_rush_hour_flag(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    hour = df["start_hour"]

    df["is_rush_hour"] = (
        ((hour >= 7) & (hour <= 9)) |
        ((hour >= 16) & (hour <= 18))
    )

    logger.info("Added rush-hour flag.")
    return df