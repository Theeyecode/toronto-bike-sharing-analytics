# analysis.py
from __future__ import annotations

import pandas as pd
from utils import get_logger

logger = get_logger(__name__)


def summarize_trip_duration_by_user_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute mean/median trip duration per user type.
    Uses the column 'trip_duration_clean' and 'user_type_standardized'.
    """

    df = df.copy()

    # Aseguramos que la duración esté en numérico
    df["trip_duration_clean"] = pd.to_numeric(df["trip_duration_clean"], errors="coerce")

    summary = (
        df.groupby("user_type_standardized")["trip_duration_clean"]
          .agg(
              trips_count="count",
              duration_mean_sec="mean",
              duration_median_sec="median"
          )
          .reset_index()
    )

    logger.info("Computed trip duration summary by user type:\n%s", summary)

    return summary


def get_peak_stations_by_user_type(
    df: pd.DataFrame,
    top_n: int = 10
) -> dict[str, pd.DataFrame]:
    """
    Identify peak stations (start & end) for Casual vs Annual riders.
    Returns dictionary with two DataFrames:
      - 'start_stations'
      - 'end_stations'
    """

    df = df.copy()

    # Nos quedamos con los tipos conocidos
    df = df[df["user_type_standardized"].isin(["Casual", "Annual"])]

    # Top estaciones de inicio
    start_peak = (
        df.groupby(["user_type_standardized", "start_station_normalized"])
          .size()
          .reset_index(name="trip_count")
          .sort_values(["user_type_standardized", "trip_count"], ascending=[True, False])
    )

    # Nos quedamos con los top_n por tipo de usuario
    start_peak = (
        start_peak
        .groupby("user_type_standardized")
        .head(top_n)
        .reset_index(drop=True)
    )

    # Top estaciones de fin
    end_peak = (
        df.groupby(["user_type_standardized", "end_station_normalized"])
          .size()
          .reset_index(name="trip_count")
          .sort_values(["user_type_standardized", "trip_count"], ascending=[True, False])
    )

    end_peak = (
        end_peak
        .groupby("user_type_standardized")
        .head(top_n)
        .reset_index(drop=True)
    )

    logger.info("Computed peak START stations by user type:\n%s", start_peak)
    logger.info("Computed peak END stations by user type:\n%s", end_peak)

    return {
        "start_stations": start_peak,
        "end_stations": end_peak,
    }


def summarize_time_of_day_by_user_type(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summaries created for time-of-day vs user type.
    Conteo de viajes por hora del día y tipo de usuario.
    """

    df = df.copy()

    # Por seguridad, nos aseguramos de que start_hour exista
    if "start_hour" not in df.columns:
        raise KeyError(
            "Column 'start_hour' not found. "
            "Make sure you called add_time_features(df) before this summary."
        )

    summary = (
        df.groupby(["start_hour", "user_type_standardized"])
          .size()
          .reset_index(name="trip_count")
          .sort_values(["start_hour", "user_type_standardized"])
    )

    logger.info("Computed time-of-day vs user type summary:\n%s", summary)

    return summary
