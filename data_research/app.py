from __future__ import annotations

import json
import os
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean


TABLE_NAME = "iris_measurements"
MEASUREMENTS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]


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


def correlation(xs: list[float], ys: list[float]) -> float:
    x_mean = mean(xs)
    y_mean = mean(ys)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    x_variance = sum((x - x_mean) ** 2 for x in xs)
    y_variance = sum((y - y_mean) ** 2 for y in ys)
    if x_variance == 0 or y_variance == 0:
        return 0.0
    return numerator / (x_variance * y_variance) ** 0.5


def build_report(rows: list[dict[str, object]]) -> dict[str, object]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["species"])].append(row)

    averages_by_species = {}
    for species, species_rows in sorted(grouped.items()):
        averages_by_species[species] = {
            measurement: round(mean(float(row[measurement]) for row in species_rows), 3)
            for measurement in MEASUREMENTS
        }

    petal_lengths = [float(row["petal_length"]) for row in rows]
    petal_widths = [float(row["petal_width"]) for row in rows]
    largest_petal_species = max(
        grouped,
        key=lambda species: mean(float(row["petal_length"]) for row in grouped[species]),
    )

    return {
        "status": "success",
        "rows_analyzed": len(rows),
        "species_counts": dict(sorted(Counter(row["species"] for row in rows).items())),
        "averages_by_species": averages_by_species,
        "petal_length_width_correlation": round(correlation(petal_lengths, petal_widths), 3),
        "species_with_largest_average_petal_length": largest_petal_species,
    }


def main() -> None:
    rows = load_rows()
    report = build_report(rows)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "data_research_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"Research report saved to: {report_path}")


if __name__ == "__main__":
    main()
