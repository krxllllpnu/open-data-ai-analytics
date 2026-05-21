# Open Data AI Analytics Lab Report

## Purpose of the Lab

The purpose of this lab was to practice a complete Git and GitHub workflow using a small open data analytics project. The work included repository initialization, real commits, feature branches, GitHub Pull Requests, a deliberate merge conflict, conflict resolution, scripts for data processing and analysis, visualizations, changelog creation, and release tagging.

## Repository Structure

- `README.md` - project overview, open data source, and analysis questions.
- `.gitignore` - excludes Python cache files, notebook checkpoints, virtual environments, environment files, and raw data.
- `data/README.md` - explains the data directory.
- `data/processed/` - contains small processed data and generated text reports.
- `notebooks/` - reserved for notebooks.
- `src/` - contains Python scripts.
- `reports/figures/` - contains generated SVG charts.
- `CHANGELOG.md` - documents version `v0.1.0`.
- `REPORT.md` - documents the Git/GitHub lab workflow.

## Work Completed by Step

1. Created the GitHub repository `open-data-ai-analytics`.
2. Added the required project structure.
3. Configured `.gitignore` for `__pycache__/`, `.ipynb_checkpoints/`, `.venv/`, `.env`, and `data/raw/`, then committed the project initialization.
4. Filled `README.md` with the project purpose, the public Iris CSV data source, and three analysis questions, then committed the documentation.
5. Created `feature/data_load`, added `src/data_load.py`, and committed the data loading script.
6. Merged `feature/data_load` into `main` using a normal merge commit.
7. Created `feature/data_quality_analysis` and `feature/data_research` from `main`. Added quality checks in `src/data_quality_analysis.py` and research summaries in `src/data_research.py`.
8. Pushed both branches to GitHub and merged them through real GitHub Pull Requests.
9. Created a real README conflict using `feature/readme-conflict-a` and `feature/readme-conflict-b`, then resolved and committed the merge conflict.
10. Created `feature/visualization`, added `src/visualization.py`, and merged it into `main`.
11. Added `CHANGELOG.md` for `v0.1.0` and created the Git tag `v0.1.0`.
12. Added this lab report.
13. Ran the project scripts and verified outputs.

## Branches Used

- `main`
- `feature/data_load`
- `feature/data_quality_analysis`
- `feature/data_research`
- `feature/readme-conflict-a`
- `feature/readme-conflict-b`
- `feature/visualization`

## Pull Requests / Merge Requests

- Pull Request #1: `feature/data_quality_analysis` into `main`
  - Added missing value checks, duplicate row checks, inferred column type checks, and species counts.
  - Added `src/data_quality_analysis.py`.
  - Check command: `python src/data_load.py`, then `python src/data_quality_analysis.py`.

- Pull Request #2: `feature/data_research` into `main`
  - Added species-level measurement averages, petal length and width correlation, and the species with the largest average petal length.
  - Added `src/data_research.py`.
  - Check command: `python src/data_load.py`, then `python src/data_research.py`.

## Merge Conflict and Resolution

The merge conflict was created in `README.md` by changing the same research-question section on two branches:

- `feature/readme-conflict-a` changed the section to `Research Questions and Hypotheses` and rewrote the questions as hypotheses.
- `feature/readme-conflict-b` changed the same section to `Analysis Questions` and rewrote the questions differently.

After merging `feature/readme-conflict-a` into `main`, merging `feature/readme-conflict-b` caused a real content conflict in `README.md`. The conflict was resolved by keeping the hypothesis-based heading and first two hypothesis statements from branch A, while keeping the petal length and width relationship question from branch B.

## How to Run the Scripts

Run the scripts from the repository root:

```powershell
python src/data_load.py
python src/data_quality_analysis.py
python src/data_research.py
python src/visualization.py
```

If `python` is not available on `PATH`, use the Python executable installed on the machine or add it to `PATH` first.

## Git Log Output

Exact output captured from:

```powershell
git log --oneline --graph --decorate --all
```

```text
* f6d3e92 (HEAD -> main) chore: add generated analysis outputs
* 9dcfc15 (tag: v0.1.0) docs: add changelog for v0.1.0
*   76a6892 merge: add visualization feature
|\  
| * eedea62 (feature/visualization) feat: add data visualizations
|/  
*   cfdd001 merge: apply README analysis wording
|\  
| * f254da7 (feature/readme-conflict-b) docs: revise README analysis questions
* |   a53ba9a merge: apply README hypothesis wording
|\ \  
| |/  
|/|   
| * 250cfea (feature/readme-conflict-a) docs: refine README research hypotheses
|/  
*   04055f5 (origin/main) Merge pull request #2 from feature/data_research
|\  
| * a785f27 (origin/feature/data_research, feature/data_research) feat: add data research analysis
* |   af8e0c9 Merge pull request #1 from feature/data_quality_analysis
|\ \  
| |/  
|/|   
| * 94fd4ad (origin/feature/data_quality_analysis, feature/data_quality_analysis) feat: add data quality analysis
|/  
*   33c7631 merge: add data loading feature
|\  
| * 6f95bda (feature/data_load) feat: add data loading script
|/  
* 91ded11 docs: add project overview and research questions
* a076d68 chore: initialize project structure and gitignore
```

## Conclusion

The lab produced a complete GitHub-backed open data analytics repository. The final project includes scripts for data loading, quality analysis, research analysis, and visualization; real Git branches and commits; two real GitHub Pull Requests; a documented merge conflict; a changelog; and the `v0.1.0` tag.
