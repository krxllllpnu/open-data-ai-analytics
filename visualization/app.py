from __future__ import annotations

import json
import os
import sqlite3
from collections import defaultdict
from pathlib import Path
from statistics import mean

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


TABLE_NAME = "iris_measurements"
COLORS = {
    "setosa": "#2f7d32",
    "versicolor": "#1565c0",
    "virginica": "#c62828",
}


def path_from_env(name: str, docker_default: str, local_default: str) -> Path:
    value = os.getenv(name)
    if value:
        return Path(value)
    docker_path = Path(docker_default)
    return docker_path if docker_path.exists() else Path(local_default)


DB_PATH = path_from_env("DB_PATH", "/app/db/project.db", "db/project.db")
REPORTS_DIR = path_from_env("REPORTS_DIR", "/app/reports", "reports")
PLOTS_DIR = path_from_env("PLOTS_DIR", "/app/plots", "plots")


def load_rows() -> list[dict[str, object]]:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}. Run data_load first.")

    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(f"SELECT * FROM {TABLE_NAME}").fetchall()
    return [dict(row) for row in rows]


def grouped_rows(rows: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["species"])].append(row)
    return dict(sorted(grouped.items()))


def save_bar_chart(groups: dict[str, list[dict[str, object]]]) -> Path:
    averages = {
        species: mean(float(row["petal_length"]) for row in species_rows)
        for species, species_rows in groups.items()
    }
    species = list(averages)
    values = [averages[name] for name in species]
    colors = [COLORS.get(name, "#555555") for name in species]
    output = PLOTS_DIR / "average_petal_length.png"

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


def save_scatter_plot(groups: dict[str, list[dict[str, object]]]) -> Path:
    output = PLOTS_DIR / "petal_length_vs_width.png"

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


def write_report(outputs: list[Path]) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "visualization_report.json"
    report = {
        "status": "success",
        "charts": [str(output) for output in outputs],
        "chart_count": len(outputs),
    }
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report_path


def main() -> None:
    rows = load_rows()
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    groups = grouped_rows(rows)
    outputs = [save_bar_chart(groups), save_scatter_plot(groups)]
    report_path = write_report(outputs)
    for output in outputs:
        print(f"Saved chart: {output}")
    print(f"Visualization report saved to: {report_path}")


if __name__ == "__main__":
    main()
