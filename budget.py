"""Currency validation, budget totals and CSV export."""
import csv
import io
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENT = Decimal("0.01")
MAX_AMOUNT = Decimal("1000000000.00")


def money(value, label):
    """Validate an amount and round to cents."""
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{label} must be a number.") from None
    if not amount.is_finite() or amount < 0 or amount > MAX_AMOUNT:
        raise ValueError(f"{label} must be between R0 and R1,000,000,000.")
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class Budget:
    income: Decimal
    entries: tuple[tuple[str, Decimal], ...]
    allocated: Decimal
    remaining: Decimal


def summarize(income, rows):
    """Validate budget rows and calculate the balance."""
    pay = money(income, "Take-home pay")
    entries = []
    for number, row in enumerate(rows, start=1):
        category = str(row.get("Category") or "").strip()
        amount = row.get("Amount")
        if not category and (amount is None or amount == ""):
            continue
        if not category:
            raise ValueError(f"Row {number}: enter a category name or delete the row.")
        entries.append((category, money(amount, f"Amount for {category}")))
    allocated = sum((amount for _, amount in entries), Decimal("0.00"))
    return Budget(pay, tuple(entries), allocated, pay - allocated)


def export_csv(month, budget):
    """Export income, budget items and totals as CSV."""
    output = io.StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(["Month", "Type", "Category", "Amount (ZAR)"])

    def write_row(kind, category, amount):
        # Prevent a user-entered category being interpreted as a spreadsheet formula.
        if category.startswith(("=", "+", "-", "@", "\t", "\r", "\n")):
            category = "'" + category
        writer.writerow([month, kind, category, f"{amount:.2f}"])

    write_row("Income", "Take-home pay", budget.income)
    for category, amount in budget.entries:
        write_row("Allocation", category, amount)
    write_row("Summary", "Total allocated", budget.allocated)
    write_row("Summary", "Remaining", budget.remaining)
    return output.getvalue()
