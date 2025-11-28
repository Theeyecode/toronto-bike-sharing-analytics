from pathlib import Path
import pandas as pd

from utils import get_logger


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CLEAN_DATA_DIR = DATA_DIR / "clean" 

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

def save_cleaned_data(df: pd.DataFrame, filename: str, index: bool = False) -> Path:
    print("Saving cleaned data...")
    CLEAN_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = CLEAN_DATA_DIR / filename

    df.to_csv(output_path, index=index)
    logger.info("Saved cleaned dataset to %s", output_path)

    return output_path

