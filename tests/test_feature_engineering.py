import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# Make src importable
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

from feature_engineering import (
    compute_distance_fields,
    add_time_features,
    add_weekend_flag,
    add_rush_hour_flag,
)


def test_compute_distance_fields_basic():
    # Two rows: one zero distance, one non-zero
    df = pd.DataFrame(
        {
            "Start Station Latitude": [43.6532, 43.6532],
            "Start Station Longitude": [-79.3832, -79.3832],
            "End Station Latitude": [43.6532, 43.6426],
            "End Station Longitude": [-79.3832, -79.3871],
        }
    )

    result = compute_distance_fields(df)

    assert "trip_distance_km" in result.columns
    # identical coordinates => distance ≈ 0
    assert result.loc[0, "trip_distance_km"] == pytest.approx(0.0, abs=1e-6)
    # second row should be positive distance
    assert result.loc[1, "trip_distance_km"] > 0
    assert np.issubdtype(result["trip_distance_km"].dtype, np.floating)


def test_compute_distance_fields_missing_columns_noop():
    # No lat/lon columns -> function should return df unchanged, without new field
    df = pd.DataFrame({"Trip Id": [1, 2], "Trip  Duration": [60, 120]})

    result = compute_distance_fields(df)

    assert "trip_distance_km" not in result.columns
    assert list(result.columns) == list(df.columns)
    assert result.equals(df)


@pytest.mark.filterwarnings("ignore:Could not infer format")
def test_add_time_features_raises_on_all_nat():

    df = pd.DataFrame(
        {
            "start_time": [
                "2024-08-01 08:15:00",  # Thursday
                "2024-08-03 15:30:00",  # Saturday
            ]
        }
    )

    result = add_time_features(df)

    assert "start_hour" in result.columns
    assert "start_day" in result.columns
    assert "start_month" in result.columns
    assert "start_weekday" in result.columns

    assert list(result["start_hour"]) == [8, 15]
    assert list(result["start_day"]) == [1, 3]
    assert list(result["start_month"]) == [8, 8]
    assert list(result["start_weekday"]) == ["Thursday", "Saturday"]


def test_add_time_features_raises_on_all_nat():
    df = pd.DataFrame({"start_time": ["bad", "not a date"]})

    with pytest.raises(ValueError):
        add_time_features(df)


def test_add_weekend_flag():
    df = pd.DataFrame(
        {
            "start_time": pd.to_datetime(
                ["2024-08-02 10:00:00",  # Friday
                 "2024-08-04 10:00:00"]  # Sunday
            )
        }
    )

    result = add_weekend_flag(df)

    assert "is_weekend" in result.columns
    assert list(result["is_weekend"]) == [False, True]


def test_add_rush_hour_flag():
    df = pd.DataFrame(
        {
            "start_hour": [6, 8, 12, 17, 20],
        }
    )

    result = add_rush_hour_flag(df)

    assert "is_rush_hour" in result.columns
    # 8 and 17 are inside rush hour ranges
    assert list(result["is_rush_hour"]) == [False, True, False, True, False]
