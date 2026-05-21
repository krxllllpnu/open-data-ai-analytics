# Changelog

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