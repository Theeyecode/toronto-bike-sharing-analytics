# Toronto Bike-Sharing Analytics Tool

Modular Python project for data loading, cleaning, validation, and exploratory analysis on a **Toronto bike-sharing trips dataset**.

This README explains:

- the modular architecture
- how to install dependencies
- how to run the cleaning pipeline
- how to run tests
- how teammates can use the cleaned data in notebooks

---

## 1. Overview and Motivation

This project follows a **modular architecture**: each responsibility is separated into small, focused modules (data loading, cleaning, validation, analysis utilities).

**Why modular?**

- **Maintainability** – Changes in one part (e.g., loader) don’t break everything else.
- **Reusability** – Cleaning and loading functions are reusable in scripts and notebooks.
- **Testability** – Each module can be unit-tested in isolation (via `pytest`).
- **Scalability** – New modules (e.g., `analysis_user_type.py`, `analysis_time_patterns.py`) can be added without rewriting the core pipeline.
- **Collaboration** – Clear structure lets each teammate own specific modules and add features safely.

**Design principles used:**

- Small, pure functions where possible.
- Type hints and docstrings.
- `src/main.py` acts as an **orchestrator**, not a dumping ground.
- Raw data is kept immutable in `data/raw/`.
- Cleaned data is saved in `data/clean/` for reproducibility.
- Plots, tables, and exports can live in `outputs/`.

---

## 2. Project Structure

Current structure (Sprint 1):

```text
.
├── data/
│   ├── raw/              # original CSV files (e.g., toronto-bike.csv)
│   └── clean/            # cleaned / processed datasets (created by main.py)
├── notebooks/            # Jupyter notebooks for EDA & analysis
├── outputs/              # figures, tables, exports for the report/dashboard
├── src/
│   ├── __init__.py
│   ├── main.py           # orchestrates full pipeline (load → clean → save)
│   ├── data_loader.py    # load raw CSV, save cleaned CSV
│   ├── data_cleaning.py  # cleaning & enhancement functions:
│   │                     #   - standardize_user_type
│   │                     #   - group_bike_model
│   │                     #   - parse_datetime_columns
│   │                     #   - clean_trip_duration
│   │                     #   - clean_station_fields
│   └── utils.py          # shared logger and utility helpers
├── tests/
│   ├── test_data_cleaning.py  # pytest unit tests for cleaning functions
│   └── test_data_loader.py    # pytest unit tests for loader
├── requirements.txt
├── .gitignore
└── README.md
```

##  3. Installing Dependencies

Recommended: use a virtual environment to isolate dependencies.

_macOS / Linux:_

⁠ bash

# create and activate venv

python3 -m venv .venv
source .venv/bin/activate

# install dependencies

pip install --upgrade pip
pip install -r requirements.txt
 ⁠

_Windows (PowerShell):_

⁠ powershell
python -m venv .venv
.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt
 ⁠

_Conda (alternative):_

⁠ bash
conda create -n financial-env python=3.10
conda activate financial-env
pip install -r requirements.txt
 ⁠

⁠ requirements.txt ⁠ should contain at least:

pandas
numpy

## 4. Running Locally

1. upload the dataset into data/raw and name it "toronto-bike.csv"

2.  python src/main.py      OR
    python3 src/main.py 
This will:
- load data/raw/toronto-bike.csv
- apply the functions
- save rhe cleaned dataset to  "data/clean/toronto-bike-clean.csv"



## 5. Run test 
1. if you wrote your test using pytest then use : 
pytest -q 
