# Open Data AI Analytics

This repository contains a small university Git/GitHub lab project for working with open data, Python analysis scripts, branches, pull requests, merge conflicts, and release tagging.

The analytical purpose of the project is to explore the classic Iris flower dataset and use simple data analysis techniques to understand how flower measurements differ between species.

## Open Data Source

Dataset: [Iris Species CSV from the public seaborn-data repository](https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv)

The dataset contains sepal and petal measurements for three Iris species: setosa, versicolor, and virginica.

## Research Questions and Hypotheses

1. Virginica is expected to have the largest average petal length and petal width.
2. The dataset is expected to have no missing values and very few duplicate records.
3. How strongly are petal length and petal width related across all observations?

## CI/CD Pipeline

This project uses GitHub Actions for a simple Python CI/CD lab pipeline.

The main workflow is defined in `.github/workflows/ci.yml`. It runs on pushes to `main`, pull requests targeting `main`, and manual `workflow_dispatch` runs. The workflow uses `ubuntu-latest`, installs dependencies from `requirements.txt`, and runs a matrix mapped to the existing project scripts:

- `src/data_load.py`
- `src/data_quality_analysis.py`
- `src/data_research.py`
- `src/visualization.py`

The source dataset is downloaded once by `src/data_load.py` into `data/raw/iris.csv`. Processed tabular outputs and text reports are saved in `data/processed/`, while charts are saved in `reports/figures/`. The `artifacts/` directory is used by GitHub Actions for CI logs and copied final outputs uploaded with `actions/upload-artifact`.

To run the workflow manually, open the repository on GitHub, go to **Actions**, select **CI**, and click **Run workflow**.

Produced artifacts include:

- CI log files for each matrix module
- copied processed outputs from `data/processed/`
- copied charts from `reports/figures/`

The self-hosted runner workflow is defined in `.github/workflows/ci-selfhosted.yml`. It runs only manually and is intended to demonstrate how the same project can be executed on a configured self-hosted GitHub Actions runner. It runs `src/data_load.py` and `src/data_quality_analysis.py`, then uploads logs and processed outputs as artifacts.
