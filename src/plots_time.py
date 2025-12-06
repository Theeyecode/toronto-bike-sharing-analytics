from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple
from utils import save_fig

def plot_trips_per_hour(df: pd.DataFrame,
                        out_dir="outputs/plots/time_based_analysis",
                        figsize: Tuple[int, int] = (10, 5)):
    hourly = df.groupby("start_hour").size()
    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(hourly.index, hourly.values)
    ax.set_title("Trips per Hour")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Trip Count")
    ax.set_xticks(range(0, 24))
    return save_fig(fig, out_dir, "trips_per_hour.png")
    
    


def plot_trips_per_weekday(df: pd.DataFrame,
                           out_dir="outputs/plots/time_based_analysis",
                           figsize: Tuple[int, int] = (10, 5)):
    weekday_order = ["Monday", "Tuesday", "Wednesday",
                     "Thursday", "Friday", "Saturday", "Sunday"]

    weekday_counts = (
        df["start_weekday"]
        .value_counts()
        .reindex(weekday_order)
        .fillna(0)
    )

    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(weekday_counts.index, weekday_counts.values)
    ax.set_title("Trips per Weekday")
    ax.set_xlabel("Weekday")
    ax.set_ylabel("Trip Count")
    plt.xticks(rotation=20)
    return save_fig(fig, out_dir, "trips_per_weekday.png")
    

def plot_trips_per_month(df: pd.DataFrame,
                         out_dir="outputs/plots/time_based_analysis",
                         figsize: Tuple[int, int] = (10, 5)):
    monthly = df.groupby("start_month").size()

    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(monthly.index, monthly.values, marker="o")
    ax.set_title("Trips per Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Trip Count")
    ax.set_xticks(range(1, 13))
    return save_fig(fig, out_dir, "trips_per_month.png")
    











# import plotly.express as px

# def plot_trips_per_hour(df):
#     fig = px.bar(df, x="start_hour", y="trip_count", title="Trips per Hour")
#     return fig

# def plot_trips_per_weekday(df):
#     fig = px.bar(df, x="start_weekday", y="trip_count", title="Trips by Weekday")
#     return fig

# def plot_trips_per_month(df):
#     fig = px.line(df, x="start_month", y="trip_count", title="Trips per Month")
#     fig.update_traces(mode="lines+markers")
#     return fig
