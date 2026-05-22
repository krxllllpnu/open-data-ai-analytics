from __future__ import annotations

import json
import os
from pathlib import Path

from flask import Flask, render_template, send_from_directory


def path_from_env(name: str, docker_default: str, local_default: str) -> Path:
    value = os.getenv(name)
    if value:
        return Path(value)
    docker_path = Path(docker_default)
    return docker_path if docker_path.exists() else Path(local_default)


REPORTS_DIR = path_from_env("REPORTS_DIR", "/app/reports", "reports")
PLOTS_DIR = path_from_env("PLOTS_DIR", "/app/plots", "plots")
REPORT_FILES = {
    "Data load": "data_load_report.json",
    "Data quality": "data_quality_report.json",
    "Data research": "data_research_report.json",
    "Visualization": "visualization_report.json",
}

app = Flask(__name__)


def read_reports() -> dict[str, object]:
    reports: dict[str, object] = {}
    for title, filename in REPORT_FILES.items():
        report_path = REPORTS_DIR / filename
        if report_path.exists():
            reports[title] = json.loads(report_path.read_text(encoding="utf-8"))
        else:
            reports[title] = {"status": "missing", "path": str(report_path)}
    return reports


def list_plots() -> list[str]:
    if not PLOTS_DIR.exists():
        return []
    return sorted(path.name for path in PLOTS_DIR.glob("*.png"))


@app.get("/")
def index():
    return render_template(
        "index.html",
        reports=read_reports(),
        plots=list_plots(),
    )


@app.get("/plots/<path:filename>")
def plot_file(filename: str):
    return send_from_directory(PLOTS_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
