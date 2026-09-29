# Expense Summary CLI

[绠€浣撲腑鏂嘳(README.zh-CN.md)

Summarize a local expense CSV by month and category, with date/category filters and CSV or JSON reports.

## Features

- Configurable date, amount, category, and description column names.
- Monthly and category totals using decimal arithmetic.
- Inclusive date filters and repeatable category filters.
- Supports currency symbols, thousands separators, and parenthesized negative amounts.
- Optional positive-value normalization with `--absolute`.
- Works locally; no bank login or financial service connection.

## Install

```bash
git clone https://github.com/jellywong343-sys/expense-summary-cli.git
cd expense-summary-cli
python -m pip install -e .
```

## Usage

```bash
expense-summary examples/expenses.csv
expense-summary expenses.csv --start 2026-01-01 --end 2026-01-31
expense-summary expenses.csv --category Food --category Transport
expense-summary expenses.csv --json report.json --csv summary.csv
```

Review your bank export's sign convention. Use `--absolute` only if negative charges should be treated as positive spending.

## Privacy

All processing is local. Example data is fictional. Avoid committing real financial records to a public repository.

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT

