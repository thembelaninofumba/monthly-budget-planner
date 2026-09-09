# Monthly Budget Planner Implementation Plan

> Execute inline using the executing-plans skill; user selected a working starter and walkthrough.

**Goal:** A runnable monthly budget planner with beginner documentation.

**Architecture:** Pure validated currency calculations and CSV export in budget.py; Streamlit interface in app.py with pandas tables and charts.

**Tech Stack:** Python 3.11+, Streamlit, pandas, unittest.

**Spec:** docs/superpowers/specs/2026-09-09-monthly-budget-design.md

## Global constraints

ZAR currency; Decimal cents; maximum R1,000,000,000.00 per amount; session-only data with CSV export; new project directory.

## Tasks

- [x] Write and run failing tests for summarize(income, rows): 15000 - 11000 = 4000; 100 - 120 = -20; zero income; exact cents; invalid inputs. Implement Budget with income, entries, allocated and remaining fields.
- [x] Test export_csv(month, budget) by parsing output with csv.DictReader. Include income, allocations and totals; escape formula-like category names as spreadsheet text.
- [x] Test actual Streamlit sample display and reruns for changed income, zero income and invalid category rows. Implement month selector, income field, dynamic editor, metrics, status, chart and CSV download.
- [x] Install and pin dependencies in .venv. Run python -m unittest discover -s tests -v, then start the server and verify its health endpoint.
- [x] Write README with Windows commands, PHP-to-Python learning notes and deployment steps. Include a Windows launcher. Review files and report verified behavior and limitations.

## Verification record

On 2026-09-09, all 16 unittest cases passed with Python 3.14, Streamlit 1.63.0 and pandas 3.0.5. pip check reported no broken requirements. The actual Streamlit server returned HTTP 200 for both / and /_stcore/health (body: ok). The code review found no confirmed application bugs. Category add/edit/delete checks use AppTest editor-state injection; retaining edits through a sequence of real browser interactions has not been browser-tested. No visual screenshot review was performed. Streamlit emits its documented bare-mode ScriptRunContext warning during AppTest. The initial chart assertion was corrected to the rendered vega_lite_chart element name.

The project has a local Git repository. Environment files, secrets and downloaded budgets are ignored. GitHub push and public deployment are not performed; README contains the account-dependent steps.
