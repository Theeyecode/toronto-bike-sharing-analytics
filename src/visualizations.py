from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd
import matplotlib.pyplot as plt

from utils import get_logger

logger = get_logger(__name__)


def _ensure_dir(out_dir: str | Path) -> Path:
    """Create the output directory if it does not exist and return it as Path."""
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    return out_path


def _save_fig(fig: plt.Figure, out_dir: str | Path, filename: str) -> Path:
    """Helper to save a figure and log the path."""
    out_path = _ensure_dir(out_dir)
    output_file = out_path / filename
    fig.savefig(output_file, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved figure to %s", output_file)
    return output_file


def plot_hourly_demand(
    df: pd.DataFrame,
    out_dir: str | Path = "outputs/plots",
    time_col: str = "start_time",
    figsize: Tuple[int, int] = (10, 5),
) -> Path:
    """
    Plot number of trips by hour of day.

    Assumes `time_col` is a datetime column (e.g., start_time).
    """
    df = df.copy()

    if not pd.api.types.is_datetime64_any_dtype(df[time_col]):
        raise ValueError(f"{time_col} must be a datetime column")

    df["hour"] = df[time_col].dt.hour
    hourly_counts = df["hour"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(hourly_counts.index, hourly_counts.values)
    ax.set_title("Hourly Demand (Number of Trips)")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Number of Trips")
    ax.set_xticks(range(0, 24))
    ax.set_xticklabels(range(0, 24))
    fig.tight_layout()

    return _save_fig(fig, out_dir, "hourly_demand.png")


def plot_trip_duration_distribution(
    df: pd.DataFrame,
    out_dir: str | Path = "outputs/plots",
    duration_col: str = "trip_duration_clean",
    bins: int = 50,
    max_minutes: int | None = 120,
    figsize: Tuple[int, int] = (10, 5),
) -> Path:
    """
    Plot distribution of trip duration (in minutes).

    max_minutes: optional cap to avoid very long trips distorting the plot.
    """
    df = df.copy()

    duration = df[duration_col]

    if max_minutes is not None:
        duration = duration[duration <= max_minutes * 60]

    duration_min = duration / 60

    fig, ax = plt.subplots(figsize=figsize)
    ax.hist(duration_min, bins=bins)
    ax.set_title("Trip Duration Distribution")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Number of Trips")
    fig.tight_layout()

    return _save_fig(fig, out_dir, "trip_duration_distribution.png")

def plot_top_busiest_stations(
    df: pd.DataFrame,
    out_dir: str | Path = "outputs/plots",
    station_col: str = "start_station_name_clean",
    top_n: int = 10,
    figsize: Tuple[int, int] = (10, 6),
) -> Path:
    """
    Plot top N busiest start stations by number of trips.
    """
    df = df.copy()

    station_counts = (
        df[station_col]
        .value_counts()
        .head(top_n)
        .sort_values(ascending=True)
    )

    fig, ax = plt.subplots(figsize=figsize)
    ax.barh(station_counts.index, station_counts.values)
    ax.set_title(f"Top {top_n} Busiest Start Stations")
    ax.set_xlabel("Number of Trips")
    ax.set_ylabel("Station")
    fig.tight_layout()

    return _save_fig(fig, out_dir, "top_busiest_stations.png")


def plot_user_type_comparison(
    df: pd.DataFrame,
    out_dir: str | Path = "outputs/plots",
    user_type_col: str = "user_type_standardized",
    figsize: Tuple[int, int] = (6, 6),
) -> Path:
    """
    Plot comparison of trips by user type (e.g., Casual vs Annual).
    """
    df = df.copy()

    counts = df[user_type_col].value_counts()

    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(counts.index, counts.values)
    ax.set_title("Trips by User Type")
    ax.set_xlabel("User Type")
    ax.set_ylabel("Number of Trips")
    fig.tight_layout()

    return _save_fig(fig, out_dir, "user_type_comparison.png")

def plot_daily_trips_decomposition(
    df: pd.DataFrame,
    out_dir: str | Path = "outputs/plots",
    time_col: str = "start_time",
    window: int = 7,
    figsize: tuple[int, int] = (12, 8),
) -> Path:
    """visualization"""

    df = df.copy()

    if not pd.api.types.is_datetime64_any_dtype(df[time_col]):
        raise ValueError(f"{time_col} must be a datetime column")

    df["date"] = df[time_col].dt.date
    daily = df.groupby("date").size().rename("trips").to_frame()
    daily.index = pd.to_datetime(daily.index)

    daily["trend"] = daily["trips"].rolling(window=window, center=True).mean()

    daily["resid"] = daily["trips"] - daily["trend"]

    fig, axes = plt.subplots(3, 1, figsize=figsize, sharex=True)

    # 1) Original series
    axes[0].plot(daily.index, daily["trips"])
    axes[0].set_title("Daily Trips")
    axes[0].set_ylabel("Trips")

    # 2) Trend (rolling)
    axes[1].plot(daily.index, daily["trend"])
    axes[1].set_title(f"{window}-Day Rolling Trend")
    axes[1].set_ylabel("Trips")

    # 3) Residuals
    axes[2].scatter(daily.index, daily["resid"], s=10)
    axes[2].axhline(0, linewidth=0.8)
    axes[2].set_title("Residuals (Trips - Trend)")
    axes[2].set_ylabel("Trips")
    axes[2].set_xlabel("Date")
    for ax in axes:
        ax.set_xticks(daily.index)
        ax.set_xticklabels(daily.index.day)

    fig.tight_layout()

    return _save_fig(fig, out_dir, "daily_trips_decomposition.png")