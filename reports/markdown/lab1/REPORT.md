# Звіт до лабораторної роботи №1

## Мета лабораторної роботи

Метою цієї лабораторної роботи було відпрацювати повний Git і GitHub workflow на прикладі невеликого проєкту з аналітики відкритих даних. Робота включала ініціалізацію репозиторію, коміти, feature-гілки, GitHub Pull Requests, навмисний merge conflict, розв’язання конфлікту, скрипти для обробки й аналізу даних, візуалізації, створення changelog та release tag.

## Структура репозиторію

- `README.md` — огляд проєкту, джерело відкритих даних і питання для аналізу.
- `.gitignore` — виключає Python cache-файли, checkpoint-файли notebook-ів, віртуальні середовища, environment-файли та сирі дані.
- `data/README.md` — пояснює призначення директорії з даними.
- `data/processed/` — містить невеликі оброблені дані та згенеровані текстові звіти.
- `notebooks/` — зарезервована директорія для notebook-ів.
- `src/` — містить Python-скрипти.
- `reports/figures/` — містить згенеровані SVG-графіки.
- `CHANGELOG.md` — документує версію `v0.1.0`.
- `REPORT.md` — документує Git/GitHub workflow лабораторної роботи.

## Виконана робота за кроками

1. Створено GitHub-репозиторій `open-data-ai-analytics`.
2. Додано необхідну структуру проєкту.
3. Налаштовано `.gitignore` для `__pycache__/`, `.ipynb_checkpoints/`, `.venv/`, `.env` і `data/raw/`, після чого виконано коміт ініціалізації проєкту.
4. Заповнено `README.md`: додано мету проєкту, публічне джерело CSV-даних Iris і три питання для аналізу, після чого виконано коміт документації.
5. Створено гілку `feature/data_load`, додано `src/data_load.py` і виконано коміт скрипта для завантаження даних.
6. Змерджено `feature/data_load` у `main` за допомогою звичайного merge commit.
7. Створено гілки `feature/data_quality_analysis` і `feature/data_research` від `main`. Додано перевірки якості даних у `src/data_quality_analysis.py` та дослідницькі підсумки у `src/data_research.py`.
8. Обидві гілки запушено на GitHub і змерджено через реальні GitHub Pull Requests.
9. Створено реальний README-конфлікт за допомогою гілок `feature/readme-conflict-a` і `feature/readme-conflict-b`, після чого конфлікт було розв’язано й закомічено.
10. Створено гілку `feature/visualization`, додано `src/visualization.py` і змерджено її у `main`.
11. Додано `CHANGELOG.md` для `v0.1.0` і створено Git-тег `v0.1.0`.

## Використані гілки

- `main`
- `feature/data_load`
- `feature/data_quality_analysis`
- `feature/data_research`
- `feature/readme-conflict-a`
- `feature/readme-conflict-b`
- `feature/visualization`

## Pull Requests / Merge Requests

- Pull Request #1: `feature/data_quality_analysis` у `main`
  - Додано перевірку пропущених значень, перевірку дублікатів рядків, визначення типів колонок і підрахунок кількості записів за видами.
  - Додано `src/data_quality_analysis.py`.
  - Команда для перевірки: `python src/data_load.py`, потім `python src/data_quality_analysis.py`.

- Pull Request #2: `feature/data_research` у `main`
  - Додано середні значення вимірювань на рівні видів, кореляцію між довжиною та шириною пелюстки, а також визначення виду з найбільшою середньою довжиною пелюстки.
  - Додано `src/data_research.py`.
  - Команда для перевірки: `python src/data_load.py`, потім `python src/data_research.py`.

## Merge Conflict і його розв’язання

Merge conflict було створено у файлі `README.md` шляхом зміни одного й того самого розділу з дослідницькими питаннями у двох різних гілках:

- `feature/readme-conflict-a` змінила розділ на `Research Questions and Hypotheses` і переписала питання у вигляді гіпотез.
- `feature/readme-conflict-b` змінила той самий розділ на `Analysis Questions` і переписала питання по-іншому.

Після злиття `feature/readme-conflict-a` у `main`, злиття `feature/readme-conflict-b` спричинило реальний content conflict у `README.md`. Конфлікт було розв’язано шляхом збереження заголовка у форматі гіпотез і перших двох гіпотез із гілки A, а також збереження питання про зв’язок між довжиною та шириною пелюстки з гілки B.

## Вивід Git Log

Точний вивід отримано командою:

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

## Висновок

У результаті лабораторної роботи було створено повноцінний open data analytics репозиторій на GitHub. Фінальний проєкт містить скрипти для завантаження даних, аналізу якості даних, дослідницького аналізу та візуалізації; Git-гілки й коміти; два GitHub Pull Requests; задокументований merge conflict; changelog; а також тег `v0.1.0`.
