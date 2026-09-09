# Monthly Budget Planner

Build the working starter chosen by the user with Python, Streamlit and pandas. A single page accepts a month and take-home pay in ZAR, and an editable category/amount table. Start with an explicitly labelled example: income R15,000; rent R5,000; groceries R2,500; transport R1,500; savings R2,000. Display allocated funds, remaining balance, an over-budget warning and a category bar chart. Add/delete rows and download CSV with month, income, allocations and totals.

Keep calculation and export logic in budget.py, interface in app.py, tests in tests/, setup and learning instructions in README.md. Use Decimal with half-up rounding to cents. Reject negative, nonfinite or incomplete amounts and unnamed populated rows. Ignore wholly empty rows. Maximum per amount: R1,000,000,000.00. Support zero income and no expenses. Combine duplicate category names in the chart. Python 3.11 or newer; pin Streamlit and pandas after installing. Data lasts for the current session; explain that users must export to keep a copy. Persistence is a future learning step. No accounts or financial integrations. Publishing is a separate step after the user provides GitHub context.

Verify hand-calculated totals, exact cents, invalid inputs, CSV output and actual Streamlit reruns. Work in a separate new project directory.
