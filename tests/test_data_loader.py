import sys
from pathlib import Path

import pandas as pd
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.append(str(SRC_DIR))

import data_loader  


def test_load_bike_data_success(tmp_path, monkeypatch):
    # Create a temporary raw dir and CSV file
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()

    csv_path = raw_dir / "test_bike.csv"
    df_in = pd.DataFrame({
        "Trip Id": [1, 2],
        "Trip  Duration": [60, 120],
    })
    df_in.to_csv(csv_path, index=False)


    monkeypatch.setattr(data_loader, "RAW_DATA_DIR", raw_dir)

    df_out = data_loader.load_bike_data("test_bike.csv")

    assert df_out.shape == (2, 2)
    assert list(df_out["Trip Id"]) == [1, 2]


def test_load_bike_data_missing_file(tmp_path, monkeypatch):
    # Empty raw dir
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()

    monkeypatch.setattr(data_loader, "RAW_DATA_DIR", raw_dir)

    with pytest.raises(FileNotFoundError):
        data_loader.load_bike_data("does_not_exist.csv")
