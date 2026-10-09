# Telecom Database Tools

Я разработал инструменты для работы с базами данных: импорт и агрегации MongoDB, а также CRUD-операции PostgreSQL для тарифов.

## Запуск

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Устройство проекта

Подключение MongoDB задаётся через `MONGO_URI`; по умолчанию используется локальный сервер. Для PostgreSQL настройте параметры в `crud_tariffs.py`, пароль через `DB_PASSWORD`. Меню содержит удаление коллекций — работайте только с учебной базой.

Я публикую исходный код без локальных паролей, окружений, баз и журналов. Для воспроизведения анализа я указываю необходимые данные и зависимости.

## Автор

Антон Никитин — [anton-nikitin21](https://github.com/anton-nikitin21).
