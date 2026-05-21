from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


PROCESSED_FILE = Path("data/processed/iris_processed.csv")
FIGURES_DIR = Path("reports/figures")
MEASUREMENTS = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
COLORS = {
    "setosa": "#2f7d32",
    "versicolor": "#1565c0",
    "virginica": "#c62828",
}


def load_rows() -> list[dict[str, str]]:
    if not PROCESSED_FILE.exists():
        raise FileNotFoundError(
            f"{PROCESSED_FILE} does not exist. Run python src/data_load.py first."
        )

    with PROCESSED_FILE.open("r", encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def grouped_rows(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["species"]].append(row)
    return dict(sorted(grouped.items()))


def save_bar_chart(groups: dict[str, list[dict[str, str]]]) -> Path:
    averages = {
        species: mean(float(row["petal_length"]) for row in species_rows)
        for species, species_rows in groups.items()
    }

    species = list(averages)
    values = [averages[name] for name in species]
    colors = [COLORS.get(name, "#555555") for name in species]
    output = FIGURES_DIR / "average_petal_length.png"

    plt.figure(figsize=(8, 5))
    bars = plt.bar(species, values, color=colors)
    plt.title("Average Petal Length by Species")
    plt.xlabel("Species")
    plt.ylabel("Average petal length")
    plt.bar_label(bars, fmt="%.2f", padding=3)
    plt.tight_layout()
    plt.savefig(output, dpi=150)
    plt.close()
    return output


def save_scatter_plot(rows: list[dict[str, str]]) -> Path:
    groups = grouped_rows(rows)
    output = FIGURES_DIR / "petal_length_vs_width.png"

    plt.figure(figsize=(8, 5))
    for species, species_rows in groups.items():
        xs = [float(row["petal_length"]) for row in species_rows]
        ys = [float(row["petal_width"]) for row in species_rows]
        plt.scatter(
            xs,
            ys,
            label=species,
            color=COLORS.get(species, "#555555"),
            alpha=0.8,
        )
    plt.title("Petal Length vs Petal Width")
    plt.xlabel("Petal length")
    plt.ylabel("Petal width")
    plt.legend(title="Species")
    plt.tight_layout()
    plt.savefig(output, dpi=150)
    plt.close()
    return output


def main() -> None:
    rows = load_rows()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    groups = grouped_rows(rows)
    outputs = [save_bar_chart(groups), save_scatter_plot(rows)]
    for output in outputs:
        print(f"Saved chart: {output}")


if __name__ == "__main__":
    main()
