from __future__ import annotations

from storage import Expense


def validate_expense(e: Expense) -> None:
    if not e["category"].strip():
        raise ValueError("категория не может быть пустой или состоять из пробелов")
    if e["amount"] <= 0:
        raise ValueError(f"amount должен быть > 0, получено {e['amount']}")


def add_expense(items: list[Expense], e: Expense) -> list[Expense]:
    """Возвращает новый список с добавленной валидированной записью."""
    validate_expense(e)
    return [*items, e]


def total_by_category(items: list[Expense]) -> dict[str, int]:
    """Сумма копеек по категориям, ключи отсортированы."""
    totals: dict[str, int] = {}
    for e in items:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    return dict(sorted(totals.items()))


def total_in_period(items: list[Expense], start: str, end: str) -> int:
    """Сумма за [start, end] включительно; start > end → ValueError."""
    if start > end:
        raise ValueError(f"start={start} позже end={end}")
    return sum(e["amount"] for e in items if start <= e["date"] <= end)


def format_amount(kopecks: int) -> str:
    sign = "-" if kopecks < 0 else ""
    rub, kop = divmod(abs(kopecks), 100)
    return f"{sign}{rub}.{kop:02d} ₽"


def format_report(items: list[Expense]) -> str:
    if not items:
        return "Нет расходов"
    return "\n".join(
        f"{cat}: {format_amount(amount)}"
        for cat, amount in total_by_category(items).items()
    )