# Monthly Budget Planner

A small Python data app for planning where your monthly paycheck goes. Project 1 of a coding challenge.

## What it does

- Enter take-home pay in South African rand and choose the month.
- Add, rename, edit and delete budget categories.
- See income, total allocated and remaining balance update immediately.
- Get an over-budget warning and a chart of allocations.
- Download a CSV containing the full plan and totals.

The starting amounts are sample data: R15,000 income, R11,000 allocated and R4,000 remaining. Savings count as allocated money.

**Storage:** This starter keeps your changes in the current browser session only. Refreshing or closing the session can reset the plan. Download the CSV to keep a copy. Changing the month labels the current plan; it does not retrieve a saved budget. CSV import and a database are future improvements.

## Run on Windows

Install Python 3.11 or newer from [python.org](https://www.python.org/downloads/windows/) if needed. This starter was tested with Python 3.14.

Open PowerShell in this project folder. For a new checkout:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

If the environment is already set up, run this from the project folder:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Or double-click **run.bat**. Open the local URL printed in the terminal, normally http://localhost:8501. Press Ctrl+C in that terminal to stop the server. No environment activation or PowerShell execution-policy change is required.

## Try it

1. The example starts with R4,000 left to allocate.
2. Change take-home pay to R10,000: the remaining balance becomes -R1,000 and a warning appears.
3. Edit an amount by double-clicking its table cell and pressing Enter.
4. Add a category in the empty bottom row. Select a row and use the table's delete control to remove it.
5. Choose **Download budget CSV** to save your current plan.

Use invented numbers when taking a screenshot for the public repository.

## How the code works

Read these files in this order:

| File | Purpose | What you learn |
| --- | --- | --- |
| `budget.py` | Validates inputs, calculates totals and creates CSV | Functions, loops, dataclasses, Decimal, exceptions |
| `app.py` | Draws inputs, the table, metrics and chart | Streamlit, pandas DataFrames and reruns |
| `tests/test_budget.py` | Checks money calculations with known answers | Automated testing and edge cases |
| `tests/test_app.py` | Exercises the actual app | Testing user interactions |
| `.streamlit/config.toml` | Sets colours and disables usage telemetry | App configuration |
| `requirements.txt` | Pins direct dependency versions | Python dependency management |

### Coming from PHP

Python variable names do not start with a dollar sign. Indentation defines blocks instead of braces. A dictionary resembles a PHP associative array:

```python
expense = {"Category": "Groceries", "Amount": 2500}
print(expense["Category"])
```

The essential calculation is:

```python
allocated = sum(amount for category, amount in entries)
remaining = income - allocated
```

The actual implementation uses `Decimal` amounts so money is calculated in exact cents. A `ValueError` tells the interface to show a helpful message when input is invalid.

Streamlit runs `app.py` again when an input changes. The edited table becomes a list of dictionaries, `summarize()` validates and calculates it, and the results are rendered. pandas groups category totals for the chart. The input widgets and chart use floats; inputs are converted to Decimal before calculating money totals.

### Small exercises after the walkthrough

1. Add an emergency-fund category to the example.
2. Add a metric showing savings as a percentage of income; handle zero income.
3. Add CSV import so users can reopen a downloaded plan.
4. Save months in SQLite, then practise SQL queries comparing allocations over time.

## Run the tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The tests cover exact cents, overspending, zero income, incomplete/invalid input, spreadsheet-safe CSV exports and Streamlit interactions.

## Put the code on GitHub

Create an empty repository named `monthly-budget-planner` in your GitHub account. From this project folder, use the following if you have not already initialised Git:

```powershell
git init -b main
git add .
git commit -m "Build monthly budget planner"
```

Then follow GitHub's **push an existing repository** instructions to add your repository as `origin` and push. The project's `.gitignore` excludes the Python environment, secrets and downloaded budget CSVs.

Add a screenshot and the live app URL to this README after deployment.

## Host the interface

Use [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud). It connects to your GitHub repository and hosts the Python app.

1. Push the source files, including `app.py`, `budget.py` and `requirements.txt`, to GitHub.
2. Sign in to Streamlit Community Cloud and choose **Create app**.
3. Select your repository and branch; set the entrypoint to `app.py`.
4. Select a supported Python version of 3.11 or newer in advanced settings.
5. Deploy, then place the resulting `.streamlit.app` link in your GitHub repository description.

GitHub Pages cannot run the Streamlit Python server. See [GitHub Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).

## References

- [Streamlit data editor](https://docs.streamlit.io/develop/api-reference/data/st.data_editor)
- [Streamlit app testing](https://docs.streamlit.io/develop/concepts/app-testing/get-started)
- [pandas getting started](https://pandas.pydata.org/docs/getting_started/)
