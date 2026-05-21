from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean


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
    width, height = 760, 460
    chart_left, chart_bottom = 90, 380
    chart_height, bar_width = 280, 110
    max_value = max(averages.values())
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="380" y="42" text-anchor="middle" font-family="Arial" font-size="24" font-weight="700">Average Petal Length by Species</text>',
        f'<line x1="{chart_left}" y1="80" x2="{chart_left}" y2="{chart_bottom}" stroke="#333"/>',
        f'<line x1="{chart_left}" y1="{chart_bottom}" x2="690" y2="{chart_bottom}" stroke="#333"/>',
    ]
    for index, (species, value) in enumerate(averages.items()):
        bar_height = int((value / max_value) * chart_height)
        x = chart_left + 90 + index * 185
        y = chart_bottom - bar_height
        color = COLORS.get(species, "#555555")
        parts.extend(
            [
                f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" fill="{color}"/>',
                f'<text x="{x + bar_width / 2}" y="{y - 10}" text-anchor="middle" font-family="Arial" font-size="16">{value:.2f}</text>',
                f'<text x="{x + bar_width / 2}" y="414" text-anchor="middle" font-family="Arial" font-size="16">{species}</text>',
            ]
        )
    parts.append("</svg>")
    output = FIGURES_DIR / "average_petal_length.svg"
    output.write_text("\n".join(parts), encoding="utf-8")
    return output


def save_scatter_plot(rows: list[dict[str, str]]) -> Path:
    width, height = 760, 500
    left, top, plot_width, plot_height = 90, 70, 590, 340
    xs = [float(row["petal_length"]) for row in rows]
    ys = [float(row["petal_width"]) for row in rows]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    def scale_x(value: float) -> float:
        return left + ((value - min_x) / (max_x - min_x)) * plot_width

    def scale_y(value: float) -> float:
        return top + plot_height - ((value - min_y) / (max_y - min_y)) * plot_height

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<text x="380" y="38" text-anchor="middle" font-family="Arial" font-size="24" font-weight="700">Petal Length vs Petal Width</text>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" stroke="#333"/>',
        f'<line x1="{left}" y1="{top + plot_height}" x2="{left + plot_width}" y2="{top + plot_height}" stroke="#333"/>',
        '<text x="385" y="470" text-anchor="middle" font-family="Arial" font-size="16">Petal length</text>',
        '<text x="24" y="250" text-anchor="middle" font-family="Arial" font-size="16" transform="rotate(-90 24 250)">Petal width</text>',
    ]
    for row in rows:
        species = row["species"]
        x = scale_x(float(row["petal_length"]))
        y = scale_y(float(row["petal_width"]))
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{COLORS.get(species, "#555555")}" opacity="0.82"/>'
        )
    for index, species in enumerate(COLORS):
        legend_y = 95 + index * 24
        parts.append(f'<circle cx="705" cy="{legend_y}" r="6" fill="{COLORS[species]}"/>')
        parts.append(
            f'<text x="718" y="{legend_y + 5}" font-family="Arial" font-size="14">{species}</text>'
        )
    parts.append("</svg>")
    output = FIGURES_DIR / "petal_length_vs_width.svg"
    output.write_text("\n".join(parts), encoding="utf-8")
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
