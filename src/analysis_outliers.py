# analysis_outliers.py
from __future__ import annotations

import pandas as pd
import numpy as np
from utils import get_logger

logger = get_logger(__name__)


def detect_trip_duration_outliers(
    df: pd.DataFrame,
    method: str = "iqr",   # "iqr" or "zscore"
    z_thresh: float = 3.0  # typical: 3 or 3.5
):
    """
    Detects extremely long/short trips using IQR or Z-score.
    
    Returns:
        - outliers_df: DataFrame with flagged rows
        - insights: dictionary (JSON-ready) with summary statistics
    """

    df = df.copy()

    # Aseguramos que la duración sea numérica
    df["trip_duration_clean"] = pd.to_numeric(df["trip_duration_clean"], errors="coerce")

    duration = df["trip_duration_clean"].dropna()

    # ---------------------------------------------------------------------
    # METHOD A: IQR (Interquartile Range)
    # ---------------------------------------------------------------------
    if method == "iqr":
        Q1 = duration.quantile(0.25)
        Q3 = duration.quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        mask = (df["trip_duration_clean"] < lower_bound) | (df["trip_duration_clean"] > upper_bound)

        approach = "IQR-based outlier detection"

    # ---------------------------------------------------------------------
    # METHOD B: Z-SCORE
    # ---------------------------------------------------------------------
    elif method == "zscore":
        mean = duration.mean()
        std = duration.std()

        z_scores = (df["trip_duration_clean"] - mean) / std
        mask = (z_scores.abs() > z_thresh)

        lower_bound = mean - z_thresh * std
        upper_bound = mean + z_thresh * std
        approach = f"Z-score detection (threshold={z_thresh})"

    else:
        raise ValueError("method must be 'iqr' or 'zscore'")

    # ✅ Filtramos primero
    outliers_df = df[mask].copy()

    # ✅ Calculamos la razón SOLO con los outliers
    outliers_df["outlier_reason"] = np.where(
        outliers_df["trip_duration_clean"] < lower_bound,
        "Too short",
        np.where(outliers_df["trip_duration_clean"] > upper_bound, "Too long", "Unknown")
    )

    # ---------------------------------------------------------------------
    # Build JSON-ready insights dictionary
    # ---------------------------------------------------------------------
    insights = {
        "method": method,
        "approach": approach,
        "total_rows": int(len(df)),
        "total_outliers": int(len(outliers_df)),
        "percentage_outliers": round(100 * len(outliers_df) / len(df), 2) if len(df) > 0 else 0.0,
        "thresholds": {
            "lower_bound": float(lower_bound),
            "upper_bound": float(upper_bound)
        },
        "duration_summary": {
            "min": float(duration.min()),
            "max": float(duration.max()),
            "mean": float(duration.mean()),
            "median": float(duration.median()),
            "Q1": float(duration.quantile(0.25)),
            "Q3": float(duration.quantile(0.75)),
        },
        "examples": {
            "sample_too_short": outliers_df[outliers_df["outlier_reason"] == "Too short"]["trip_duration_clean"].head(5).tolist(),
            "sample_too_long": outliers_df[outliers_df["outlier_reason"] == "Too long"]["trip_duration_clean"].head(5).tolist(),
        },
    }

    logger.info("Outlier detection complete. %s outliers found.", len(outliers_df))

    return outliers_df, insights
