import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

from data_cleaning import (
    standardize_user_type,
    group_bike_model,
    parse_datetime_columns,
    clean_trip_duration,
    clean_station_fields,
)


def test_standardize_user_type():
    df = pd.DataFrame({
        "User Type": ["Casual Member", "Annual Member", "Something Else"]
    })

    result = standardize_user_type(df)

    assert list(result["user_type_standardized"]) == ["Casual", "Annual", "Unknown"]


def test_group_bike_model():
    df = pd.DataFrame({
        "Model": ["ICONIC", "EFIT", "EFIT G5", None]
    })

    result = group_bike_model(df)

    assert list(result["bike_model_group"]) == [
        "ICONIC",
        "EFIT",
        "EFIT G5",
        "Unknown",
    ]


def test_parse_datetime_columns():
    df = pd.DataFrame({
        "Start Time": ["08/01/2024 00:00", "08/01/2024 12:30"],
        "End Time":   ["08/01/2024 00:10", "08/01/2024 13:00"],
    })

    result = parse_datetime_columns(df)

    assert pd.api.types.is_datetime64_any_dtype(result["start_time"])
    assert pd.api.types.is_datetime64_any_dtype(result["end_time"])
    assert result["start_time"].min() == pd.Timestamp("2024-08-01 00:00")
    assert result["end_time"].max() == pd.Timestamp("2024-08-01 13:00")


def test_clean_trip_duration():
    # One valid, one invalid (0) duration
    df = pd.DataFrame({
        "Start Time": ["08/01/2024 00:00", "08/01/2024 00:00"],
        "End Time":   ["08/01/2024 00:02", "08/01/2024 00:02"],
        "Trip  Duration": [120, 0],
    })

    df = parse_datetime_columns(df)
    result = clean_trip_duration(df)

    # First row: stays as raw
    assert result.loc[0, "trip_duration_clean"] == 120

    # Second row: was 0, should be replaced by computed (120 sec)
    assert result.loc[1, "trip_duration_clean"] == 120
    assert result.loc[1, "computed_duration_sec"] == 120


def test_clean_station_fields():
    # Row 0: has name
    # Row 1: missing start/end names but same IDs as row 0 -> should be filled
    df = pd.DataFrame({
        "Start Station Id": [7001, 7001],
        "Start Station Name": ["Union Station", pd.NA],
        "End Station Id": [7002, 7002],
        "End Station Name": ["Queens Quay / Yonge St", pd.NA],
        "Trip Id": [1, 2],
        "Trip  Duration": [60, 120],
        "Start Time": ["08/01/2024 00:00", "08/01/2024 00:10"],
        "End Time": ["08/01/2024 00:01", "08/01/2024 00:12"],
        "Bike Id": [100, 101],
        "User Type": ["Casual Member", "Annual Member"],
        "Model": ["ICONIC", "EFIT"],
    })

    result = clean_station_fields(df)

    assert result.loc[0, "start_station_name_clean"] == "Union Station"
    assert result.loc[1, "start_station_name_clean"] == "Union Station"

    assert result.loc[0, "end_station_name_clean"] == "Queens Quay / Yonge St"
    assert result.loc[1, "end_station_name_clean"] == "Queens Quay / Yonge St"
