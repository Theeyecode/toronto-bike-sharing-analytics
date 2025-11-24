# Toronto Bike Sharing — README

Modular Python project for exploratory data analysis (EDA), cleaning, and basic analysis on a financial transactions dataset.
This README explains the modular architecture, why modular design is beneficial, how to install dependencies from ⁠ requirements.txt ⁠, how to add new modules, and how to run the project locally.

---

## 1. Overview and Motivation (Theory)

This project follows a _modular architecture_: each responsibility is separated into small, cohesive modules (data loading, cleaning, EDA, analysis, utilities). Key benefits:

•⁠ ⁠*Maintainability:* changes in one part (e.g., loader) do not break the rest.
•⁠ ⁠*Reusability:* functions and utilities can be imported in other scripts or notebooks.
•⁠ ⁠*Testability:* each module can be tested in isolation.
•⁠ ⁠*Scalability:* add new modules (e.g., ⁠ features.py ⁠, ⁠ models.py ⁠) without rewriting the pipeline.
•⁠ ⁠*Interoperability:* ⁠ src ⁠ is a Python package; it can be run as a module (⁠ python -m src.main ⁠), imported into other projects, or used in a Docker container.

_Recommended design principles:_

•⁠ ⁠Write pure functions whenever possible (no side effects).
•⁠ ⁠Document with docstrings and add type hints.
•⁠ ⁠Keep ⁠ main.py ⁠ as an orchestrator that ties small modules together.
•⁠ ⁠Save outputs (CSV, JSON, images) in a ⁠ project_output/ ⁠ folder for reproducibility.

---


## 2. Project Structure






## 3. Installing Dependencies

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

---