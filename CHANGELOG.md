# Changelog

## v0.3.0

Docker containerization lab release.

- Added Dockerfiles for data loading, data quality analysis, data research, visualization, and web services.
- Added `compose.yaml` for running the full project with Docker Compose.
- Configured shared volumes for data, database, reports, and plots.
- Added SQLite database support for storing imported dataset records.
- Updated data quality analysis and data research modules to generate JSON reports.
- Added Flask web dashboard for viewing reports and generated plots.
- Added `.env.example` with Docker-related environment variables.
- Updated `.gitignore` for generated database, report, and plot artifacts.
- Updated README with Docker Compose run instructions and lab documentation.

## v0.2.0

CI/CD lab release.

- Added GitHub Actions CI workflow in `.github/workflows/ci.yml`.
- Configured CI triggers for `push`, `pull_request`, and manual `workflow_dispatch`.
- Added matrix-based execution for existing project scripts.
- Added artifact upload for generated reports, logs, and figures.
- Added self-hosted runner workflow in `.github/workflows/ci-selfhosted.yml`.
- Tested CI execution on both GitHub-hosted and self-hosted runners.
- Updated visualization script to use `matplotlib`.
- Updated `requirements.txt` with required Python dependencies.

## v0.1.0

Initial university Git/GitHub lab release.

- Initialized repository structure and `.gitignore`.
- Added project README with open data source and research questions.
- Added data loading script for the Iris open dataset.
- Added data quality analysis script.
- Added research analysis script.
- Practiced GitHub Pull Request merges for analysis branches.
- Created and resolved a README merge conflict.
- Added visualization script that generates two SVG charts.