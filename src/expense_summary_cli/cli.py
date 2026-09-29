from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y")

@dataclass(frozen=True)
class Expense:
    date: str
    month: str
    category: str
    amount: Decimal
    description: str


def parse_date(value: str) -> datetime:
    value = value.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unsupported date: {value}")


def parse_amount(value: str) -> Decimal:
    cleaned = value.strip().replace(",", "").replace("¥", "").replace("$", "")
    if cleaned.startswith("(") and cleaned.endswith(")"):
        cleaned = "-" + cleaned[1:-1]
    try:
        return Decimal(cleaned)
    except InvalidOperation as exc:
        raise ValueError(f"Invalid amount: {value}") from exc


def read_expenses(path: Path, date_column: str = "date", amount_column: str = "amount",
                  category_column: str = "category", description_column: str = "description",
                  encoding: str = "utf-8-sig", absolute: bool = False) -> list[Expense]:
    sample = path.read_text(encoding=encoding)[:8192]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    expenses = []
    with path.open("r", encoding=encoding, newline="") as handle:
        reader = csv.DictReader(handle, dialect=dialect)
        required = {date_column, amount_column, category_column}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            missing = sorted(required - set(reader.fieldnames or []))
            raise ValueError("Missing required column(s): " + ", ".join(missing))
        for line, row in enumerate(reader, 2):
            if not any((value or "").strip() for value in row.values()):
                continue
            try:
                date = parse_date(row[date_column] or "")
                amount = parse_amount(row[amount_column] or "")
            except ValueError as exc:
                raise ValueError(f"Line {line}: {exc}") from exc
            if absolute:
                amount = abs(amount)
            expenses.append(Expense(
                date=date.strftime("%Y-%m-%d"), month=date.strftime("%Y-%m"),
                category=(row[category_column] or "Uncategorized").strip() or "Uncategorized",
                amount=amount,
                description=(row.get(description_column) or "").strip(),
            ))
    return expenses


def summarize(expenses: list[Expense], start: str | None = None, end: str | None = None,
              categories: set[str] | None = None) -> dict:
    selected = []
    for item in expenses:
        if start and item.date < start:
            continue
        if end and item.date > end:
            continue
        if categories and item.category.lower() not in categories:
            continue
        selected.append(item)
    by_month: dict[str, Decimal] = defaultdict(Decimal)
    by_category: dict[str, Decimal] = defaultdict(Decimal)
    by_month_category: dict[str, dict[str, Decimal]] = defaultdict(lambda: defaultdict(Decimal))
    for item in selected:
        by_month[item.month] += item.amount
        by_category[item.category] += item.amount
        by_month_category[item.month][item.category] += item.amount
    money = lambda value: str(value.quantize(Decimal("0.01")))
    return {
        "transactions": len(selected),
        "total": money(sum((item.amount for item in selected), Decimal())),
        "by_month": {key: money(value) for key, value in sorted(by_month.items())},
        "by_category": {key: money(value) for key, value in sorted(by_category.items(), key=lambda pair: (-pair[1], pair[0]))},
        "by_month_category": {
            month: {key: money(value) for key, value in sorted(values.items())}
            for month, values in sorted(by_month_category.items())
        },
    }


def write_csv_report(path: Path, report: dict) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["section", "period_or_category", "amount"])
        for month, amount in report["by_month"].items():
            writer.writerow(["month", month, amount])
        for category, amount in report["by_category"].items():
            writer.writerow(["category", category, amount])


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize expense CSV files by month and category.")
    parser.add_argument("file")
    parser.add_argument("--date-column", default="date")
    parser.add_argument("--amount-column", default="amount")
    parser.add_argument("--category-column", default="category")
    parser.add_argument("--description-column", default="description")
    parser.add_argument("--start", help="Inclusive YYYY-MM-DD")
    parser.add_argument("--end", help="Inclusive YYYY-MM-DD")
    parser.add_argument("--category", action="append", default=[])
    parser.add_argument("--absolute", action="store_true", help="Convert amounts to positive values")
    parser.add_argument("--encoding", default="utf-8-sig")
    parser.add_argument("--json", dest="json_path")
    parser.add_argument("--csv", dest="csv_path")
    args = parser.parse_args()
    expenses = read_expenses(Path(args.file), args.date_column, args.amount_column, args.category_column,
                             args.description_column, args.encoding, args.absolute)
    categories = {item.lower() for item in args.category} or None
    report = summarize(expenses, args.start, args.end, categories)
    print(f"Transactions: {report['transactions']}  Total: {report['total']}")
    print("\nBy month:")
    for key, value in report["by_month"].items():
        print(f"  {key}: {value}")
    print("\nBy category:")
    for key, value in report["by_category"].items():
        print(f"  {key}: {value}")
    if args.json_path:
        Path(args.json_path).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.csv_path:
        write_csv_report(Path(args.csv_path), report)

if __name__ == "__main__": main()
