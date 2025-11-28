import pandas as pd
import re
from utils import get_logger

logger = get_logger(__name__)


def normalize_station_name(name: str | float) -> str:
    if pd.isna(name):
        return "Unknown Station"

    name = str(name).strip()
    name = name.replace("&", "and")
    name = re.sub(r"\s+", " ", name)
    name = name.strip(" ,.;:/\\")
    name = name.title()

    return name


def normalize_station_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "start_station_name_clean" not in df or "end_station_name_clean" not in df:
        logger.warning(
            "Station normalization skipped. Required cleaned station fields not found."
        )
        return df

    df["start_station_normalized"] = df["start_station_name_clean"].apply(normalize_station_name)
    df["end_station_normalized"] = df["end_station_name_clean"].apply(normalize_station_name)

    logger.info("Normalized station names for consistency.")

    return df