import pandas as pd
import plotly.express as px

def plotly_trips_per_hour(df: pd.DataFrame):
    hourly = (
        df.groupby("start_hour")
        .size()
        .reset_index(name="trip_count")
        .sort_values("start_hour")
    )

    fig = px.bar(
        hourly,
        x="start_hour",
        y="trip_count",
        title="Trips per Hour",
        labels={"start_hour": "Hour of Day", "trip_count": "Trip Count"}
    )
    return fig


def plotly_trips_per_weekday(df: pd.DataFrame):
    weekday_order = ["Monday", "Tuesday", "Wednesday",
                     "Thursday", "Friday", "Saturday", "Sunday"]

    weekday_counts = (
        df["start_weekday"]
        .value_counts()
        .reindex(weekday_order)
        .fillna(0)
        .reset_index()
    )
    weekday_counts.columns = ["start_weekday", "trip_count"]

    fig = px.bar(
        weekday_counts,
        x="start_weekday",
        y="trip_count",
        title="Trips per Weekday",
        labels={"start_weekday": "Weekday", "trip_count": "Trip Count"}
    )
    return fig


def plotly_trips_per_month(df: pd.DataFrame):
    monthly = (
        df.groupby("start_month")
        .size()
        .reset_index(name="trip_count")
        .sort_values("start_month")
    )

    fig = px.line(
        monthly,
        x="start_month",
        y="trip_count",
        title="Trips per Month",
        markers=True,
        labels={"start_month": "Month", "trip_count": "Trip Count"}
    )
    return fig

import plotly.express as px

def plotly_trips_by_user_type(df):
    fig = px.bar(
        df,
        x="User Type",
        y="trip_count",
        title="Casual vs Annual Riders",
        color="User Type",
        text="trip_count"
    )
    fig.update_layout(xaxis_title="User Type", yaxis_title="Trip Count")
    return fig

