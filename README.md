# BUDGET PLANNER

A monthly budget app built with Python, Streamlit and pandas. Enter your take-home pay, budget for expenses and savings, and check what's left.

[Open the app](https://monthly-budget-planner-yfgjesuspchtoocycbz448.streamlit.app/)

## Using the app

Choose a month and enter your income in rand. Edit the category names and amounts in the table, add rows for other expenses, or delete rows you don't need.

The totals and chart update as you edit. If you budget more than your income, the app shows how much you're over. Savings count towards the budget total.

The example starts with R15,000 income and R11,000 budgeted, leaving R4,000. Replace these figures with your own.

Use **Download budget CSV** to keep a copy of your income, budget items and totals.

### What gets saved?

Changes last for the current session only. Refreshing or closing the page can reset them, so download your CSV first. Changing the month doesn't load a saved budget.

There is no CSV import or bank connection. The app uses South African rand (ZAR) and records planned amounts, not actual transactions.

## Local setup

You'll need Git and Python 3.11 or newer. Tested on Windows with Python 3.14.

```sh
git clone https://github.com/thembelaninofumba/monthly-budget-planner.git
cd monthly-budget-planner
```

### Windows

Run in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

After setup, double-clicking `run.bat` also starts the app.

### macOS / Linux

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py
```

Open the address printed in the terminal, usually http://localhost:8501. Press Ctrl+C to stop the app.

## Code

- [app.py](app.py): inputs, budget table, chart and download button.
- [budget.py](budget.py): validation, totals and CSV export. Calculations use `Decimal` and round to cents.
- [tests/](tests/): calculation and interface tests.
- [.streamlit/config.toml](.streamlit/config.toml): colours and app settings.
- [requirements.txt](requirements.txt): dependency versions.

## Tests

With dependencies installed:

```powershell
# Windows
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

```sh
# macOS / Linux
.venv/bin/python -m unittest discover -s tests -v
```

Tests cover rounding, invalid inputs, overspending, CSV exports and changes to the budget table.

## Deploy a copy

Fork the repository, then sign in to [Streamlit Community Cloud](https://share.streamlit.io/) and choose **Create app**. Select your fork, use branch `main`, and set the main file to **`app.py`**.

Choose Python 3.11 or newer in advanced settings and deploy. The [Streamlit guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) has the full steps.
