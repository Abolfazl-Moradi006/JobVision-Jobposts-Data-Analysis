"""Download the JobVision dataset, save it as parquet and check its shape.

Run from the project root:  python download_data.py

Dataset: JobVision/JobVision_Jobposts_Dataset (CC BY-NC 4.0, credit JobVision).
Safe to run twice: each step is skipped if its output already exists.
"""
import sys

import pandas as pd

from src.config import (
    EXPECTED_COLS,
    EXPECTED_ROWS,
    HF_DATASET,
    INTERIM_DIR,
    RAW_CSV_NAME,
    RAW_DIR,
    RAW_PARQUET,
)


def find_raw_csv():
    """Return an existing CSV in data/raw/ (any name), or None."""
    csvs = sorted(RAW_DIR.glob("*.csv"))
    return csvs[0] if csvs else None


def download_raw_csv():
    """Download from Hugging Face and save the raw CSV in data/raw/."""
    from datasets import load_dataset  # imported here so it is only needed for downloading

    print(f"Downloading {HF_DATASET} from Hugging Face ...")
    ds = load_dataset(HF_DATASET)
    split = "train" if "train" in ds else list(ds.keys())[0]
    csv_path = RAW_DIR / RAW_CSV_NAME
    ds[split].to_pandas().to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Saved raw CSV: {csv_path}")
    return csv_path


def csv_to_parquet(csv_path):
    """Convert the raw CSV to parquet (keeps data types, loads much faster)."""
    print(f"Reading {csv_path.name} ...")
    df = pd.read_csv(csv_path, encoding="utf-8", low_memory=False)
    try:
        df.to_parquet(RAW_PARQUET, index=False)
    except Exception:
        # Mixed-type text columns can break pyarrow; store them as strings instead.
        print("Mixed-type columns found; converting text columns to string.")
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype("string")
        df.to_parquet(RAW_PARQUET, index=False)
    print(f"Saved parquet: {RAW_PARQUET}")


def check_shape():
    """Compare the parquet file's shape with what we expect."""
    df = pd.read_parquet(RAW_PARQUET)
    rows, cols = df.shape
    print(f"Shape: {rows:,} rows x {cols} columns")
    if rows == EXPECTED_ROWS and cols == EXPECTED_COLS:
        print("OK: shape matches the expected 364,838 rows x 43 columns.")
        return True
    print(
        f"WARNING: expected about {EXPECTED_ROWS:,} rows x {EXPECTED_COLS} columns. "
        "Check that you have the right file."
    )
    return False


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)

    if RAW_PARQUET.exists():
        print(f"Parquet already exists, skipping: {RAW_PARQUET}")
    else:
        csv_path = find_raw_csv()
        if csv_path:
            print(f"Found raw CSV, skipping download: {csv_path}")
        else:
            try:
                csv_path = download_raw_csv()
            except Exception as exc:
                print(f"Download failed: {exc}")
                print(
                    "Get the CSV manually from the Hugging Face dataset page, "
                    f"put it in {RAW_DIR}, and run this script again."
                )
                sys.exit(1)
        csv_to_parquet(csv_path)

    sys.exit(0 if check_shape() else 1)


if __name__ == "__main__":
    main()