from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean


PROCESSED_FILE = Path("data/processed/iris_processed.csv")
REPORT_FILE = Path("data/processed/research_report.txt")
MEASUREMENTS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]


def load_rows() -> list[dict[str, str]]:
    if not PROCESSED_FILE.exists():
        raise FileNotFoundError(
            f"{PROCESSED_FILE} does not exist. Run python src/data_load.py first."
        )

    with PROCESSED_FILE.open("r", encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def correlation(xs: list[float], ys: list[float]) -> float:
    x_mean = mean(xs)
    y_mean = mean(ys)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    x_variance = sum((x - x_mean) ** 2 for x in xs)
    y_variance = sum((y - y_mean) ** 2 for y in ys)
    if x_variance == 0 or y_variance == 0:
        return 0.0
    return numerator / (x_variance * y_variance) ** 0.5


def build_report(rows: list[dict[str, str]]) -> str:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["species"]].append(row)

    lines = [
        "Iris Research Analysis",
        "======================",
        f"Rows analyzed: {len(rows)}",
        "",
        "Average measurements by species:",
    ]

    for species, species_rows in sorted(grouped.items()):
        lines.append(f"- {species}:")
        for column in MEASUREMENTS:
            values = [float(row[column]) for row in species_rows]
            lines.append(f"  - average {column}: {mean(values):.2f}")

    petal_lengths = [float(row["petal_length"]) for row in rows]
    petal_widths = [float(row["petal_width"]) for row in rows]
    petal_correlation = correlation(petal_lengths, petal_widths)

    largest_petal_species = max(
        grouped,
        key=lambda species: mean(float(row["petal_length"]) for row in grouped[species]),
    )

    lines.extend(
        [
            "",
            f"Petal length and width correlation: {petal_correlation:.3f}",
            f"Species with largest average petal length: {largest_petal_species}",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    rows = load_rows()
    report = build_report(rows)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(report, encoding="utf-8")
    print(report)
    print(f"Research report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
