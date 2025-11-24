from pathlib import Path
import pandas as pd

from src.utils import get_logger


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

logger = get_logger(__name__)


def load_bike_data(filename: str, **kwargs) -> pd.DataFrame:

    file_path = RAW_DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}\n"
            f"Expected inside: {RAW_DATA_DIR}"
        )

    logger.info("Loading bike data from %s", file_path)
    df = pd.read_csv(file_path, **kwargs)
    logger.info("Loaded dataset with shape %s rows x %s columns", df.shape[0], df.shape[1])

    return df
