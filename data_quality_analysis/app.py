from __future__ import annotations

import json
import os
import sqlite3
from collections import Counter
from pathlib import Path


TABLE_NAME = "iris_measurements"
NUMERIC_COLUMNS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
VALID_SPECIES = {"setosa", "versicolor", "virginica"}


def path_from_env(name: str, docker_default: str, local_default: str) -> Path:
    value = os.getenv(name)
    if value:
        return Path(value)
    docker_path = Path(docker_default)
    return docker_path if docker_path.exists() else Path(local_default)


DB_PATH = path_from_env("DB_PATH", "/app/db/project.db", "db/project.db")
REPORTS_DIR = path_from_env("REPORTS_DIR", "/app/reports", "reports")


def load_rows() -> list[dict[str, object]]:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}. Run data_load first.")

    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(f"SELECT * FROM {TABLE_NAME}").fetchall()
    return [dict(row) for row in rows]


def build_report(rows: list[dict[str, object]]) -> dict[str, object]:
    columns = NUMERIC_COLUMNS + ["species"]
    missing_values = {
        column: sum(row.get(column) in (None, "") for row in rows)
        for column in columns
    }
    duplicate_rows = len(rows) - len(
        {tuple(row.get(column) for column in columns) for row in rows}
    )
    numeric_validity = {
        column: {
            "non_numeric_or_missing": sum(
                not isinstance(row.get(column), (int, float)) for row in rows
            ),
            "minimum": min(float(row[column]) for row in rows) if rows else None,
            "maximum": max(float(row[column]) for row in rows) if rows else None,
        }
        for column in NUMERIC_COLUMNS
    }
    species_counts = Counter(str(row.get("species", "unknown")) for row in rows)
    unexpected_species = sorted(set(species_counts) - VALID_SPECIES)

    return {
        "status": "success",
        "rows_checked": len(rows),
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "numeric_validity": numeric_validity,
        "species_counts": dict(sorted(species_counts.items())),
        "unexpected_species": unexpected_species,
    }


def main() -> None:
    rows = load_rows()
    report = build_report(rows)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "data_quality_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"Quality report saved to: {report_path}")


if __name__ == "__main__":
    main()
