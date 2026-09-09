# Monthly Budget Planner

Plan how to divide your monthly take-home pay between expenses and savings. Enter your income, adjust your categories, and see how much is left to allocate.

**[Try the Live Demo](https://monthly-budget-planner-yfgjesuspchtoocycbz448.streamlit.app/)** — no installation needed.

Built with **Python, Streamlit and pandas** as project 1 of a coding challenge.

## Features

- Plan a month in South African rand (ZAR).
- Add, edit and remove budget categories.
- See take-home pay, total allocated and remaining balance update as you make changes.
- Get a warning when allocations exceed your income.
- View a chart of allocations by category.
- Download a CSV containing the month, income, allocations and totals.

## Try the example

The app opens with sample figures:

| Item | Amount |
| --- | ---: |
| Take-home pay | R15,000 |
| Rent | R5,000 |
| Groceries | R2,500 |
| Transport | R1,500 |
| Savings | R2,000 |
| **Left to allocate** | **R4,000** |

Change take-home pay to **R10,000** to see the over-budget warning.

Double-click a table cell to edit it and press Enter to apply the change. Add a category in the empty bottom row, or select a row and use the table's delete control to remove it. Savings count as an allocation.

## Storage and limitations

- Changes last for the current session only. Refreshing or closing the page can reset the plan.
- Download the CSV to keep a copy. CSV import is not available yet.
- Changing the month labels the current plan; it does not open a previously saved budget.
- This version supports ZAR only. It does not connect to bank accounts or track actual transactions.

## Run locally

You need **Git** and **Python 3.11 or newer**. Local verification was performed on Windows with Python 3.14.

Clone the repository and enter its folder:

```sh
git clone https://github.com/thembelaninofumba/monthly-budget-planner.git
cd monthly-budget-planner
```

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Once setup is complete, you can also double-click `run.bat` to start the app.

### macOS / Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

Open the local URL printed in the terminal, normally **http://localhost:8501**. Press **Ctrl+C** in the terminal to stop the app.

## Project structure

| File | Responsibility |
| --- | --- |
| [app.py](app.py) | Streamlit interface, editable table, metrics and chart |
| [budget.py](budget.py) | Input validation, currency calculations and CSV export |
| [tests/test_budget.py](tests/test_budget.py) | Calculation, validation and export tests |
| [tests/test_app.py](tests/test_app.py) | Streamlit interaction tests |
| [.streamlit/config.toml](.streamlit/config.toml) | Theme and usage telemetry settings |
| [requirements.txt](requirements.txt) | Pinned direct dependencies |
| [run.bat](run.bat) | Windows launcher |

Money inputs are converted to Python's `Decimal` type before calculations and rounded to cents. pandas organises the table data and groups category totals for the chart. Streamlit reruns the interface when inputs change.

## Run tests

After installing the dependencies, run:

**Windows**

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

**macOS / Linux**

```sh
.venv/bin/python -m unittest discover -s tests -v
```

The tests cover exact cents, overspending, zero income, invalid rows, CSV output and app interactions such as changing income and adding or deleting categories.

## Deploy your own copy

1. Fork this repository to your GitHub account.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) and select **Create app**.
3. Select your fork, branch `main`, and main file path **`app.py`**.
4. Choose a supported Python version of 3.11 or newer in advanced settings, then deploy.

See the [Streamlit deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) for details. GitHub stores the source code; Streamlit Community Cloud runs the Python interface.

## Possible next steps

- Import an exported CSV to reopen a plan.
- Save monthly budgets with SQLite.
- Compare planned allocations with actual spending.
