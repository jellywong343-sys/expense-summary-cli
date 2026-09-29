import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from expense_summary_cli.cli import parse_amount, read_expenses, summarize

class ExpenseTests(unittest.TestCase):
    def test_amount_formats(self):
        self.assertEqual(str(parse_amount("¥1,234.50")), "1234.50")
        self.assertEqual(str(parse_amount("(20.00)")), "-20.00")

    def test_summary_and_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "expenses.csv"
            path.write_text(
                "date,category,amount,description\n"
                "2026-01-05,Food,20.50,Lunch\n"
                "2026-01-20,Transport,10.00,Metro\n"
                "2026-02-01,Food,30.00,Dinner\n", encoding="utf-8")
            expenses = read_expenses(path, encoding="utf-8")
            report = summarize(expenses)
            self.assertEqual(report["total"], "60.50")
            self.assertEqual(report["by_category"]["Food"], "50.50")
            filtered = summarize(expenses, start="2026-02-01")
            self.assertEqual(filtered["total"], "30.00")

if __name__ == "__main__": unittest.main()
