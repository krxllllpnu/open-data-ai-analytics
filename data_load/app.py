from __future__ import annotations

import csv
import json
import os
import sqlite3
from pathlib import Path


TABLE_NAME = "iris_measurements"
FIELDNAMES = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
    "species",
]


def path_from_env(name: str, docker_default: str, local_default: str) -> Path:
    value = os.getenv(name)
    if value:
        return Path(value)
    docker_path = Path(docker_default)
    return docker_path if docker_path.exists() else Path(local_default)


DATASET_PATH = path_from_env("DATASET_PATH", "/app/data/dataset.csv", "data/dataset.csv")
DB_PATH = path_from_env("DB_PATH", "/app/db/project.db", "db/project.db")
REPORTS_DIR = path_from_env("REPORTS_DIR", "/app/reports", "reports")


def read_dataset() -> list[dict[str, str]]:
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

    with DATASET_PATH.open("r", encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        rows = list(reader)

    missing_columns = [column for column in FIELDNAMES if column not in (reader.fieldnames or [])]
    if missing_columns:
        raise ValueError(f"Dataset is missing columns: {', '.join(missing_columns)}")
    return rows


def load_database(rows: list[dict[str, str]]) -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
        connection.execute(
            f"""
            CREATE TABLE {TABLE_NAME} (
                sepal_length REAL,
                sepal_width REAL,
                petal_length REAL,
                petal_width REAL,
                species TEXT
            )
            """
        )
        connection.executemany(
            f"""
            INSERT INTO {TABLE_NAME}
            (sepal_length, sepal_width, petal_length, petal_width, species)
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    float(row["sepal_length"]),
                    float(row["sepal_width"]),
                    float(row["petal_length"]),
                    float(row["petal_width"]),
                    row["species"],
                )
                for row in rows
            ],
        )
        connection.commit()


def write_report(row_count: int) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "data_load_report.json"
    report = {
        "status": "success",
        "dataset_path": str(DATASET_PATH),
        "database_path": str(DB_PATH),
        "table": TABLE_NAME,
        "rows_imported": row_count,
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report_path


def main() -> None:
    rows = read_dataset()
    load_database(rows)
    report_path = write_report(len(rows))
    print(f"Imported rows: {len(rows)}")
    print(f"SQLite database: {DB_PATH}")
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
