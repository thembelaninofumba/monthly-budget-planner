import csv
import io
import unittest
from decimal import Decimal

from budget import export_csv, summarize


class BudgetTests(unittest.TestCase):
    def test_sample_paycheck_has_four_thousand_remaining(self):
        result = summarize(15000, [
            {"Category": "Rent", "Amount": 5000},
            {"Category": "Groceries", "Amount": 2500},
            {"Category": "Transport", "Amount": 1500},
            {"Category": "Savings", "Amount": 2000},
        ])
        self.assertEqual(result.allocated, Decimal("11000.00"))
        self.assertEqual(result.remaining, Decimal("4000.00"))

    def test_overspending_retains_negative_balance(self):
        self.assertEqual(summarize(100, [{"Category": "Rent", "Amount": 120}]).remaining,
                         Decimal("-20.00"))

    def test_zero_income_and_empty_budget(self):
        self.assertEqual(summarize(0, []).remaining, Decimal("0.00"))

    def test_currency_uses_exact_cents_and_half_up_rounding(self):
        result = summarize("0.30", [
            {"Category": "A", "Amount": 0.1},
            {"Category": "B", "Amount": 0.2},
        ])
        self.assertEqual(result.remaining, Decimal("0.00"))
        self.assertEqual(summarize("1.005", []).income, Decimal("1.01"))

    def test_invalid_money_cannot_be_used(self):
        for value in [-1, "NaN", "Infinity", "abc", None, True, "1000000000.01"]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    summarize(value, [])
                with self.assertRaises(ValueError):
                    summarize(100, [{"Category": "Rent", "Amount": value}])

    def test_incomplete_rows_rejected_but_empty_rows_ignored(self):
        for row in [{"Category": "", "Amount": 10}, {"Category": "Rent", "Amount": None}]:
            with self.assertRaises(ValueError):
                summarize(100, [row])
        self.assertEqual(summarize(100, [{"Category": None, "Amount": None}]).remaining,
                         Decimal("100.00"))

    def test_csv_includes_month_income_categories_and_totals(self):
        result = summarize(100, [{"Category": "Food, snacks", "Amount": 25}])
        rows = list(csv.DictReader(io.StringIO(export_csv("2026-09", result))))
        self.assertEqual(rows, [
            {"Month": "2026-09", "Type": "Income", "Category": "Take-home pay", "Amount (ZAR)": "100.00"},
            {"Month": "2026-09", "Type": "Allocation", "Category": "Food, snacks", "Amount (ZAR)": "25.00"},
            {"Month": "2026-09", "Type": "Summary", "Category": "Total allocated", "Amount (ZAR)": "25.00"},
            {"Month": "2026-09", "Type": "Summary", "Category": "Remaining", "Amount (ZAR)": "75.00"},
        ])

    def test_csv_treats_formula_like_categories_as_text(self):
        result = summarize(100, [{"Category": "=1+1", "Amount": 25}])
        rows = list(csv.DictReader(io.StringIO(export_csv("2026-09", result))))
        self.assertEqual(rows[1]["Category"], "'=1+1")


if __name__ == "__main__":
    unittest.main()
