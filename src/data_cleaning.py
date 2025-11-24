from __future__ import annotations

from typing import Literal
import pandas as pd

from src.utils import get_logger

logger = get_logger(__name__)


def standardize_user_type(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    mapping = {
        "Casual Member": "Casual",
        "Annual Member": "Annual",
    }

    df["user_type_standardized"] = (
        df["User Type"]
        .map(mapping)
        .fillna("Unknown")
    )

    logger.info("Standardized user types. Value counts:\n%s",
                df["user_type_standardized"].value_counts())

    return df


def group_bike_model(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    raw_model = df["Model"].replace("NULL", pd.NA)

    known_models = {"ICONIC", "EFIT", "EFIT G5"}

    grouped = raw_model.where(raw_model.isin(known_models), other="Other")

    df["bike_model_group"] = grouped.fillna("Unknown")

    logger.info("Grouped bike models. Value counts:\n%s",
                df["bike_model_group"].value_counts())

    return df
def parse_datetime_columns(df: pd.DataFrame) -> pd.DataFrame:
 
    # Parse 'Start Time' and 'End Time' into pandas datetime.

    # Assumes format MM/DD/YYYY HH:MM, e.g. '08/01/2024 03:14'.

    df = df.copy()

    df["start_time"] = pd.to_datetime(
        df["Start Time"],
        format="%m/%d/%Y %H:%M",
        errors="coerce",
    )

    df["end_time"] = pd.to_datetime(
        df["End Time"],
        format="%m/%d/%Y %H:%M",
        errors="coerce",
    )

    # Basic logging / sanity check
    n_start_nat = df["start_time"].isna().sum()
    n_end_nat = df["end_time"].isna().sum()

    logger.info(
        "Parsed datetime columns. NaT counts - start_time: %s, end_time: %s",
        n_start_nat,
        n_end_nat,
    )

    if n_start_nat == 0 and n_end_nat == 0:
        logger.info(
            "start_time range: %s -> %s",
            df["start_time"].min(),
            df["start_time"].max(),
        )
        logger.info(
            "end_time range: %s -> %s",
            df["end_time"].min(),
            df["end_time"].max(),
        )

    return df

def clean_trip_duration(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Compute duration from timestamps (in seconds)
    df["computed_duration_sec"] = (
        df["end_time"] - df["start_time"]
    ).dt.total_seconds()

    raw = df["Trip  Duration"]

    # Start from the raw duration as the base
    df["trip_duration_clean"] = raw

    # Identify rows with invalid raw duration 
    mask_invalid = (raw <= 0) | raw.isna()

    #Replace invalid raw duration with computed duration
    df.loc[mask_invalid, "trip_duration_clean"] = df.loc[
        mask_invalid, "computed_duration_sec"
    ]

    logger.info(
        "Trip duration cleaning summary:\n"
        "- Invalid raw durations (<=0 or NaN): %s\n"
        "- Final cleaned duration min/max: %s / %s",
        mask_invalid.sum(),
        df["trip_duration_clean"].min(),
        df["trip_duration_clean"].max(),
    )

    return df
