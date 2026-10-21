import json
from pathlib import Path
from typing import TypedDict, Optional

class Expense(TypedDict):
    id: int # индевикатор
    date: str # дата
    category: str # категория товара
    amount: int # копейки
    note: str # примечание

class StorageError(Exception):
    """Файл хранилища повреждён или имеет неожидаемую структуру."""

def load_expense(path: Path) -> list[Expense]:
    """Читает список расходов. Нет файла → []. Битый JSON/форма → StorageError."""
    if not path.exists():
        return []
    
    try:
        raw = json.load(path.read_text(encoding="UTF-8"))
    except json.JSONDecodeError as e:
        raise StorageError(f"Поврежденный/битый JSON файл в {path}: {e}")
    return raw

def save_expense(path: Path, items: list[Expense]) -> None:
    "Cохраняет JSON, но перед этим создается временный файл на всякий случай"
    tmp = path.with_suffix(suffix=".tmp") 
    tmp.write_text(
        json.dumps(items,
                   ensure_ascii=False, 
                   indent=4,
                   encoding = "UTF-8"
                   )
    )
    tmp.replace(path)