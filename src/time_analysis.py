import pandas as pd

def trips_per_hour(df: pd.DataFrame) -> pd.DataFrame:
    if "start_hour" not in df.columns:
        raise ValueError("Missing column: start_hour")
    return (
        df.groupby("start_hour")["trip_id"]
        .count()
        .reset_index(name="trip_count")
        .sort_values("start_hour")
    )

def trips_per_weekday(df: pd.DataFrame) -> pd.DataFrame:
    if "start_weekday" not in df.columns:
        raise ValueError("Missing column: start_weekday")

    weekday_order = [
        "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"
    ]

    return (
        df.groupby("start_weekday")["trip_id"]
        .count()
        .reindex(weekday_order)
        .fillna(0)
        .reset_index(name="trip_count")
    )

def trips_per_month(df: pd.DataFrame) -> pd.DataFrame:
    if "start_month" not in df.columns:
        raise ValueError("Missing column: start_month")

    return (
        df.groupby("start_month")["trip_id"]
        .count()
        .reset_index(name="trip_count")
        .sort_values("start_month")
    )
