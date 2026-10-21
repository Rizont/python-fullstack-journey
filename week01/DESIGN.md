# Проектирование

## 1. Запись о расходе
`TypedDict Expense` — контракт для всех модулей:
- `date: str` — ISO-8601 (`YYYY-MM-DD`), сравнивается лексикографически;
- `category: str` — непустая после `.strip()`;
- `amount: int` — сумма в копейках, строго > 0;
- `note: str` — комментарий, может быть пустым (не `None`).
Отдельного `id` нет — удаление по идентификатору в этом модуле не предусмотрено.

## 2. Хранение суммы
Сумма хранится как `int` в копейках. Float даёт ошибки округления (0.1 + 0.2 != 0.3),
а Decimal тяжело сериализуется в JSON (нужен кастомный энкодер). Копейки — точность
и компактный JSON; в рубли переводим только на выводе (`format_amount`).

## 3. Функции

### Работают с файлом (side effects)
- `load_expense(path: Path) -> list[Expense]` — читает JSON (UTF-8). Нет файла → `[]`.
  Битый JSON или не список → `StorageError`.
- `save_expense(path: Path, items: list[Expense]) -> None` — пишет JSON (UTF-8,
  `ensure_ascii=False`, `indent=4`). Атомарно: temp-файл рядом + `Path.replace`.

### Чистые (без I/O)
- `validate_expense(e: Expense) -> None` — `ValueError` при пустой категории
  или `amount <= 0`; вызывается из `add_expense`.
- `add_expense(items: list[Expense], e: Expense) -> list[Expense]` — валидирует,
  возвращает новый список с добавленной записью.
- `total_by_category(items: list[Expense]) -> dict[str, int]` — сумма копеек
  по категориям, ключи отсортированы.
- `total_in_period(items: list[Expense], start: str, end: str) -> int` — сумма
  за `[start, end]` включительно; `start > end` → `ValueError`.
- `format_amount(kopecks: int) -> str` — `"12.34 ₽"`, знак учитывается.
- `format_report(items: list[Expense]) -> str` — по строке на категорию
  `"Еда: 123.45 ₽"`, по алфавиту; пустой список → `"Нет расходов"`.

## 4. Ошибки и реакция
- **Пустая категория** → `ValueError` в `validate_expense`; CLI печатает, код 1.
- **Отрицательная/нулевая сумма** → `ValueError` там же; CLI просит ввести заново.
- **Файла нет** → `load_expense` возвращает `[]` (первый запуск — не ошибка).
- **Повреждённый JSON** → `StorageError` (наш класс, наследник `Exception`),
  а не голый `json.JSONDecodeError`; CLI пишет «файл повреждён», код 2,
  файл **не перезаписывается**.

## 5. Атомарность записи
`save_expense` пишет в `path.with_suffix(path.suffix + ".tmp")` в той же директории,
затем `Path.replace(path)` — атомарная замена в пределах одной ФС. Падение
посреди записи не оставит полу-записанный `expenses.json`.