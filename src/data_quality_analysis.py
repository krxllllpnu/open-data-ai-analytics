from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


PROCESSED_FILE = Path("data/processed/iris_processed.csv")
REPORT_FILE = Path("data/processed/quality_report.txt")


def load_rows() -> tuple[list[str], list[dict[str, str]]]:
    if not PROCESSED_FILE.exists():
        raise FileNotFoundError(
            f"{PROCESSED_FILE} does not exist. Run python src/data_load.py first."
        )

    with PROCESSED_FILE.open("r", encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        return list(reader.fieldnames or []), list(reader)


def infer_type(values: list[str]) -> str:
    non_empty = [value for value in values if value != ""]
    if not non_empty:
        return "empty"
    try:
        for value in non_empty:
            float(value)
        return "numeric"
    except ValueError:
        return "text"


def build_report(fieldnames: list[str], rows: list[dict[str, str]]) -> str:
    missing_counts = {
        column: sum(1 for row in rows if row.get(column, "") == "")
        for column in fieldnames
    }
    duplicate_count = len(rows) - len(
        {tuple(row.get(column, "") for column in fieldnames) for row in rows}
    )
    type_summary = {
        column: infer_type([row.get(column, "") for row in rows])
        for column in fieldnames
    }
    species_counts = Counter(row.get("species", "unknown") for row in rows)

    lines = [
        "Iris Data Quality Report",
        "========================",
        f"Rows checked: {len(rows)}",
        f"Columns checked: {len(fieldnames)}",
        "",
        "Missing values by column:",
    ]
    lines.extend(f"- {column}: {count}" for column, count in missing_counts.items())
    lines.extend(
        [
            "",
            f"Duplicate rows: {duplicate_count}",
            "",
            "Inferred column types:",
        ]
    )
    lines.extend(f"- {column}: {kind}" for column, kind in type_summary.items())
    lines.extend(["", "Species counts:"])
    lines.extend(f"- {species}: {count}" for species, count in sorted(species_counts.items()))
    return "\n".join(lines) + "\n"


def main() -> None:
    fieldnames, rows = load_rows()
    report = build_report(fieldnames, rows)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(report, encoding="utf-8")
    print(report)
    print(f"Quality report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
