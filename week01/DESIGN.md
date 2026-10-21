# Проектирование 

### 1.	Запись о расходе.
- `date: str` - ISO-8601 (`YYYY-MM-DD`); 
- `category: str` - непустая строка;
- `amount: int` — сумма в копейках (целое, может быть > 0);
- `note: str` — необязательный комментарий (может быть пустым).

### 2.	Хранение суммы.
    Хранение суммы осуществляется в формате int в виде копеек. Это сделано с целью сохранить целостность данных, ведь Float дает ошибки округления (0.1 + 0.2 != 0.3), а Decimal тяжело сериализуется в формат JSON.

### Функции
#### Работа с файлом
`load_expense(path: Path) -> list[Expense]` - Читает JSON-файл; при его отсутсвии возращает []
`save_expense(path: Path | None, items: list[Expense]) -> None` - сохраняет JSON.   

#### Чистые функции
### Чистые (без I/O)
- `parse_expense(raw: dict) -> Expense` — валидирует и нормализует одну запись.
- `validate_expense(e: Expense) -> None` — бросает `ValueError` при пустой категории или `amount <= 0`.
- `add_expense(items: list[Expense], e: Expense) -> list[Expense]` — возвращает новый список с добавленной записью.
- `total_by_category(items: list[Expense]) -> dict[str, int]` — сумма копеек по категориям.
- `format_amount(kopecks: int) -> str` — форматирует как `"12.34 ₽"`.
- `format_report(items: list[Expense]) -> str` — текстовый отчёт для печати.

## 4. Ошибки и реакция
- **Пустая категория** → `ValueError` в `validate_expense`; CLI печатает сообщение, код возврата 1.
- **Отрицательная/нулевая сумма** → `ValueError` там же; CLI просит ввести заново.
- **Файла нет** → `load_expenses` возвращает `[]` (первый запуск — не ошибка).
- **Повреждённый JSON** → `json.JSONDecodeError` пробрасывается; CLI пишет «файл повреждён» и завершается с кодом 2, не перезаписывая данные.