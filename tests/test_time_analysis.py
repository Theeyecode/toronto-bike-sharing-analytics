import pandas as pd
from feature_engineering import add_time_features
from time_analysis import trips_per_hour, trips_per_weekday, trips_per_month


def sample_df():
    return pd.DataFrame({
        "trip_id": [1, 2, 3],
        "start_time": [
            "2021-01-01 08:00",
            "2021-01-02 14:30",
            "2021-02-01 08:15"
        ]
    })


def test_trips_per_hour():
    df = add_time_features(sample_df())
    result = trips_per_hour(df)
    assert result[result.start_hour == 8].trip_count.iloc[0] == 2


def test_trips_per_weekday():
    df = add_time_features(sample_df())
    result = trips_per_weekday(df)
    assert result["trip_count"].sum() == 3
    assert "Monday" in result.start_weekday.values


def test_trips_per_month():
    df = add_time_features(sample_df())
    result = trips_per_month(df)
    assert result[result.start_month == 1].trip_count.iloc[0] == 2
