"""Run with: python -m streamlit run app.py"""
from datetime import date

import pandas as pd
import streamlit as st

from budget import MAX_AMOUNT, export_csv, summarize


def rand(amount):
    return f"{'-' if amount < 0 else ''}R{abs(amount):,.2f}"


st.set_page_config(page_title="Monthly Budget Planner", page_icon="🌱", layout="wide")

st.caption("PROJECT 01 · PAYCHECK PLANNING")
st.title("Give your paycheck a plan.")
st.write("Plan your monthly expenses and savings, and see what you have left.")
st.caption("Start with the sample figures below, then replace them with your own.")

today = date.today()
months = [date(year, month, 1)
          for year in range(today.year - 1, today.year + 2)
          for month in range(1, 13)]

month_column, income_column = st.columns(2)
with month_column:
    month = st.selectbox(
        "Budget month", months,
        index=months.index(today.replace(day=1)),
        format_func=lambda value: value.strftime("%B %Y"),
        help="Labels this plan and its download. Changing it does not load a saved budget.",
        key="month",
    )
with income_column:
    income = st.number_input(
        "Monthly take-home pay (R)", min_value=0.0, max_value=float(MAX_AMOUNT),
        value=15000.0, step=100.0, format="%.2f", key="income",
        help="The amount you receive after deductions.",
    )

# This container reserves space so metrics appear above the table.
summary_area = st.container()
st.divider()
editor_column, chart_column = st.columns([1.1, 1], gap="large")

with editor_column:
    st.subheader("Where your money goes")
    st.caption("Edit a cell and press Enter. Add categories in the empty row; select rows to delete them.")
    sample = pd.DataFrame([
        {"Category": "Rent", "Amount": 5000.0},
        {"Category": "Groceries", "Amount": 2500.0},
        {"Category": "Transport", "Amount": 1500.0},
        {"Category": "Savings", "Amount": 2000.0},
    ])
    edited = st.data_editor(
        sample, num_rows="dynamic", hide_index=True, width="stretch",
        key="budget_editor",
        column_config={
            "Category": st.column_config.TextColumn("Category", required=True, max_chars=80),
            "Amount": st.column_config.NumberColumn(
                "Planned amount (R)", min_value=0.0, max_value=float(MAX_AMOUNT),
                step=0.01, format="R %.2f", required=True,
            ),
        },
    )
    st.caption("Savings are included in your allocations.")

# pandas represents empty cells as missing values; normalise them for validation.
rows = edited.astype(object).where(pd.notna(edited), None).to_dict("records")
try:
    budget = summarize(income, rows)
except ValueError as error:
    with summary_area:
        st.error(str(error))
    st.stop()

with summary_area:
    pay_metric, allocated_metric, remaining_metric = st.columns(3)
    pay_metric.metric("Take-home pay", rand(budget.income))
    allocated_metric.metric("Total allocated", rand(budget.allocated))
    remaining_metric.metric("Left to allocate", rand(budget.remaining))

    if budget.remaining < 0:
        st.warning(f"You're over budget by {rand(-budget.remaining)}. Adjust your allocations.")
    elif budget.income == 0:
        st.info("Enter your take-home pay to start planning.")
    elif budget.remaining == 0:
        st.success("Your paycheck is fully allocated.")
    else:
        st.success(f"You have {rand(budget.remaining)} available to allocate.")

    if budget.income > 0:
        proportion = float(budget.allocated / budget.income)
        st.progress(min(proportion, 1.0), text=f"{proportion:.1%} of your paycheck allocated")

with chart_column:
    st.subheader("Your allocation breakdown")
    if budget.allocated > 0:
        chart_data = pd.DataFrame(
            [(category, float(amount)) for category, amount in budget.entries],
            columns=["Category", "Amount (R)"],
        )
        chart_data = chart_data.groupby("Category", as_index=False)["Amount (R)"].sum()
        chart_data = chart_data[chart_data["Amount (R)"] > 0]
        st.bar_chart(
            chart_data, x="Category", y="Amount (R)", horizontal=True,
            color="#087F6D", height=300, width="stretch",
        )
    else:
        st.info("Add an amount to a category to see your breakdown.")

st.divider()
st.download_button(
    "Download budget CSV",
    data=export_csv(month.strftime("%Y-%m"), budget).encode("utf-8-sig"),
    file_name=f"budget-{month:%Y-%m}.csv",
    mime="text/csv", type="primary",
)
st.caption("Your plan stays in this session only. Download a CSV before closing or refreshing the page.")
