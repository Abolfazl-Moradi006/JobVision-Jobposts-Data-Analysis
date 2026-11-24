"""Shared project settings. Notebooks and scripts import from here
instead of defining their own paths or seeds."""
from pathlib import Path

RANDOM_STATE = 42

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
TABLES_DIR = OUTPUTS_DIR / "tables"

# Dataset
HF_DATASET = "JobVision/JobVision_Jobposts_Dataset"
RAW_CSV_NAME = "jobvision_jobposts.csv"
RAW_PARQUET = INTERIM_DIR / "jobposts_raw.parquet"

EXPECTED_ROWS = 364_838
EXPECTED_COLS = 43