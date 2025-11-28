import logging
import matplotlib.pyplot as plt
from pathlib import Path


def get_logger(name: str) -> logging.Logger:
  
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

def _ensure_dir(out_dir: str | Path) -> Path:
    """Create the output directory if it does not exist and return it as Path."""
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    return out_path


def save_fig(fig: plt.Figure, out_dir: str | Path, filename: str) -> Path:
    """Helper to save a figure and log the path."""
    out_path = _ensure_dir(out_dir)
    output_file = out_path / filename
    fig.savefig(output_file, bbox_inches="tight")
    plt.close(fig)
    logger = get_logger(__name__)
    logger.info("Saved figure to %s", output_file)

    return output_file
