from storage import Expense

def validate_expense(e: Expense) -> None:
    if not Expense["category"].strip():
        raise ValueError("категория не может быть пустой или соятоять из пробелов")
    if not Expense["amount"] <= 0:
        raise ValueError(f"amount должен быть > 0, получено {e["amount"]}")

def add_expense(items: list[Expense], e: Expense) -> list[Expense]:
    pass

def total_by_category(items: list[Expense]) -> dict[str, int]:
    pass

def ormat_amount(kopecks: int) -> str:
    pass

def format_report(items: list[Expense]) -> str:
    for item in items
