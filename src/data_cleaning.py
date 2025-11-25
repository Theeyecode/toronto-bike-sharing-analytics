from __future__ import annotations

from typing import Literal
import pandas as pd

from utils import get_logger

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

    def map_model(x):
        if pd.isna(x):
            return "Unknown"
        x = x.strip().upper()

        if x == "ICONIC":
            return "ICONIC"
        elif x == "EFIT":
            return "EFIT"
        elif x == "EFIT G5":
            return "EFIT G5"
        else:
            return "Unknown"

    df["bike_model_group"] = df["Model"].apply(map_model)

    logger.info("Grouped bike models. Value counts:\n%s", df["bike_model_group"].value_counts())

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
def clean_station_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Build lookup 
    start_lookup = (
        df.dropna(subset=["Start Station Name"])
          .drop_duplicates(subset=["Start Station Id"])[["Start Station Id", "Start Station Name"]]
          .set_index("Start Station Id")["Start Station Name"]
          .to_dict()
    )

    end_lookup = (
        df.dropna(subset=["End Station Name"])
          .drop_duplicates(subset=["End Station Id"])[["End Station Id", "End Station Name"]]
          .set_index("End Station Id")["End Station Name"]
          .to_dict()
    )

    missing_start_before = df["Start Station Name"].isna().sum()
    missing_end_before = df["End Station Name"].isna().sum()

    # Fill missing names 
    df["start_station_name_clean"] = df.apply(
        lambda row: start_lookup.get(row["Start Station Id"], f"Unknown Station {row['Start Station Id']}")
        if pd.isna(row["Start Station Name"]) else row["Start Station Name"],
        axis=1
    )

    df["end_station_name_clean"] = df.apply(
        lambda row: end_lookup.get(row["End Station Id"], f"Unknown Station {row['End Station Id']}")
        if pd.isna(row["End Station Name"]) else row["End Station Name"],
        axis=1
    )

    missing_start_after = df["start_station_name_clean"].eq("Unknown Station").sum()
    missing_end_after = df["end_station_name_clean"].eq("Unknown Station").sum()

    logger.info(
        "Station field cleaning summary:\n"
        "- Original missing Start Station Names: %s\n"
        "- Original missing End Station Names: %s\n"
        "- Missing that could not be inferred (Start): %s\n"
        "- Missing that could not be inferred (End): %s",
        missing_start_before,
        missing_end_before,
        missing_start_after,
        missing_end_after,
    )

    return df

