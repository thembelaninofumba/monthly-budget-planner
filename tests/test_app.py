import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


class AppTests(unittest.TestCase):
    def setUp(self):
        self.app = AppTest.from_file(str(APP), default_timeout=15).run()

    def test_example_renders_calculated_balance_and_chart(self):
        self.assertEqual(len(self.app.exception), 0)
        self.assertEqual([metric.value for metric in self.app.metric],
                         ["R15,000.00", "R11,000.00", "R4,000.00"])
        self.assertEqual(len(self.app.get("vega_lite_chart")), 1)

    def test_income_change_updates_balance_and_warns(self):
        self.app.number_input(key="income").set_value(10000.0).run()
        self.assertEqual(len(self.app.exception), 0)
        self.assertEqual(self.app.metric[2].value, "-R1,000.00")
        self.assertEqual(len(self.app.warning), 1)

    def test_zero_income_does_not_crash(self):
        self.app.number_input(key="income").set_value(0.0).run()
        self.assertEqual(len(self.app.exception), 0)
        self.assertEqual(self.app.metric[2].value, "-R11,000.00")

    def test_balanced_budget_is_recognised(self):
        self.app.number_input(key="income").set_value(11000.0).run()
        self.assertEqual(len(self.app.exception), 0)
        self.assertEqual(self.app.metric[2].value, "R0.00")
        self.assertEqual(len(self.app.success), 1)

    def test_editing_category_amount_changes_totals(self):
        self.app.session_state["budget_editor"] = {
            "edited_rows": {0: {"Amount": 6000.0}}, "added_rows": [], "deleted_rows": [],
        }
        self.app.run()
        self.assertEqual(len(self.app.exception), 0)
        self.assertEqual(self.app.metric[2].value, "R3,000.00")

    def test_invalid_category_stops_summary_and_download(self):
        self.app.session_state["budget_editor"] = {
            "edited_rows": {0: {"Category": ""}}, "added_rows": [], "deleted_rows": [],
        }
        self.app.run()
        self.assertEqual(len(self.app.exception), 0)
        self.assertEqual(len(self.app.error), 1)
        self.assertEqual(len(self.app.metric), 0)
        self.assertEqual(len(self.app.get("download_button")), 0)

    def test_deleting_every_row_leaves_all_income_available(self):
        self.app.session_state["budget_editor"] = {
            "edited_rows": {}, "added_rows": [], "deleted_rows": [0, 1, 2, 3],
        }
        self.app.run()
        self.assertEqual(len(self.app.exception), 0)
        self.assertEqual(self.app.metric[2].value, "R15,000.00")

    def test_adding_row_includes_it_in_allocations(self):
        self.app.session_state["budget_editor"] = {
            "edited_rows": {}, "added_rows": [{"Category": "Phone", "Amount": 500.0}],
            "deleted_rows": [],
        }
        self.app.run()
        self.assertEqual(len(self.app.exception), 0)
        self.assertEqual(self.app.metric[2].value, "R3,500.00")


if __name__ == "__main__":
    unittest.main()
