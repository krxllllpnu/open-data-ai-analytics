from __future__ import annotations

import csv
from pathlib import Path
from urllib.request import urlopen


DATA_URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
RAW_FILE = RAW_DIR / "iris.csv"
PROCESSED_FILE = PROCESSED_DIR / "iris_processed.csv"


def download_dataset() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with urlopen(DATA_URL, timeout=30) as response:
        RAW_FILE.write_bytes(response.read())


def process_dataset() -> int:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    with RAW_FILE.open("r", encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        rows = list(reader)

    fieldnames = [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "species",
    ]
    with PROCESSED_FILE.open("w", encoding="utf-8", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def main() -> None:
    download_dataset()
    row_count = process_dataset()
    print(f"Downloaded dataset from: {DATA_URL}")
    print(f"Raw file saved to: {RAW_FILE}")
    print(f"Processed file saved to: {PROCESSED_FILE}")
    print(f"Processed rows: {row_count}")


if __name__ == "__main__":
    main()
