import os
"""
CRUD-приложение для работы с таблицей mobile_operator.tariffs

Реализованы операции:
CREATE  - добавление тарифа
READ    - просмотр тарифов
UPDATE  - изменение тарифа
DELETE  - удаление тарифа

Используется библиотека psycopg2 (Python DB-API)
"""

import psycopg2


# ============================================================
# ФУНКЦИЯ ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ
# ============================================================
def get_connection():
    """
    Создаёт и возвращает подключение к PostgreSQL.

    ВАЖНО:
    - dbname должен совпадать с вашей БД (например: shct_v5)
    - user и password — ваши реальные данные
    """
    return psycopg2.connect(
        dbname="shct_v5",  
        user="postgres",
        password=os.environ.get("DB_PASSWORD", ""),   
        host="95.31.166.209",
        port="16432"
    )


# ============================================================
# READ — ПРОСМОТР ВСЕХ ТАРИФОВ
# ============================================================
def show_tariffs(conn):
    """
    Выводит все записи из таблицы mobile_operator.tariffs.

    Используется SQL-запрос SELECT.
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT tariff_id, tariff_name, minutes_limit, mb_limit, monthly_fee
            FROM mobile_operator.tariffs
            ORDER BY tariff_id
        """)

        rows = cur.fetchall()

        if not rows:
            print("\n[!] Таблица тарифов пуста.\n")
            return

        print("\n📊 СПИСОК ТАРИФОВ")
        print("=" * 90)

        for row in rows:
            print(
                f"ID: {row[0]:<3} | "
                f"{row[1]:<10} | "
                f"Мин: {row[2]:<5} | "
                f"МБ: {row[3]:<6} | "
                f"Цена: {row[4]}"
            )

        print("=" * 90 + "\n")


# ============================================================
# CREATE — ДОБАВЛЕНИЕ НОВОГО ТАРИФА
# ============================================================
def add_tariff(conn):
    """
    Добавляет новый тариф в таблицу.

    Используется SQL-запрос INSERT.
    """
    print("\n➕ ДОБАВЛЕНИЕ ТАРИФА")

    tariff_name = input("Название тарифа: ")
    minutes_limit = int(input("Лимит минут: "))
    mb_limit = int(input("Лимит МБ: "))
    monthly_fee = float(input("Ежемесячная плата: "))

    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO mobile_operator.tariffs
            (tariff_name, minutes_limit, mb_limit, monthly_fee)
            VALUES (%s, %s, %s, %s)
        """, (tariff_name, minutes_limit, mb_limit, monthly_fee))

        # фиксируем изменения
        conn.commit()

    print("[✔] Тариф успешно добавлен!\n")


# ============================================================
# UPDATE — ИЗМЕНЕНИЕ ТАРИФА
# ============================================================
def update_tariff(conn):
    """
    Изменяет существующий тариф по ID.

    Используется SQL-запрос UPDATE.
    """
    print("\n✏️ ИЗМЕНЕНИЕ ТАРИФА")

    tariff_id = int(input("Введите ID тарифа: "))

    with conn.cursor() as cur:
        # Проверяем, существует ли тариф
        cur.execute("""
            SELECT tariff_id, tariff_name, minutes_limit, mb_limit, monthly_fee
            FROM mobile_operator.tariffs
            WHERE tariff_id = %s
        """, (tariff_id,))

        tariff = cur.fetchone()

        if tariff is None:
            print("[!] Тариф не найден.\n")
            return

        print("\nТекущие данные:")
        print(f"Название: {tariff[1]}")
        print(f"Минуты: {tariff[2]}")
        print(f"МБ: {tariff[3]}")
        print(f"Цена: {tariff[4]}")

        # Ввод новых значений
        new_name = input("Новое название: ")
        new_minutes = int(input("Новые минуты: "))
        new_mb = int(input("Новые МБ: "))
        new_fee = float(input("Новая цена: "))

        # Обновление записи
        cur.execute("""
            UPDATE mobile_operator.tariffs
            SET tariff_name = %s,
                minutes_limit = %s,
                mb_limit = %s,
                monthly_fee = %s
            WHERE tariff_id = %s
        """, (new_name, new_minutes, new_mb, new_fee, tariff_id))

        conn.commit()

    print("[✔] Тариф успешно обновлён!\n")


# ============================================================
# DELETE — УДАЛЕНИЕ ТАРИФА
# ============================================================
def delete_tariff(conn):
    """
    Удаляет тариф по ID.

    Используется SQL-запрос DELETE.
    """
    print("\n🗑 УДАЛЕНИЕ ТАРИФА")

    tariff_id = int(input("Введите ID тарифа: "))

    with conn.cursor() as cur:
        cur.execute("""
            SELECT tariff_id
            FROM mobile_operator.tariffs
            WHERE tariff_id = %s
        """, (tariff_id,))

        if cur.fetchone() is None:
            print("[!] Тариф не найден.\n")
            return

        confirm = input("Удалить тариф? (y/n): ")

        if confirm.lower() != 'y':
            print("[i] Удаление отменено.\n")
            return

        cur.execute("""
            DELETE FROM mobile_operator.tariffs
            WHERE tariff_id = %s
        """, (tariff_id,))

        conn.commit()

    print("[✔] Тариф удалён!\n")


# ============================================================
# ГЛАВНОЕ МЕНЮ ПРОГРАММЫ
# ============================================================
def menu():
    """
    Основной цикл программы.

    Позволяет пользователю выбирать CRUD-операции.
    """
    conn = None

    try:
        conn = get_connection()
        print("✅ Подключение к БД успешно!\n")

        while True:
            print("====== МЕНЮ ======")
            print("1 — Показать тарифы")
            print("2 — Добавить тариф")
            print("3 — Изменить тариф")
            print("4 — Удалить тариф")
            print("0 — Выход")

            choice = input("Выберите действие: ")

            if choice == "1":
                show_tariffs(conn)
            elif choice == "2":
                add_tariff(conn)
            elif choice == "3":
                update_tariff(conn)
            elif choice == "4":
                delete_tariff(conn)
            elif choice == "0":
                print("\n👋 Выход из программы.")
                break
            else:
                print("[!] Неверный ввод.\n")

    except Exception as e:
        print("\n❌ Ошибка при работе с БД:", e)

        # откат изменений при ошибке
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()
            print("🔌 Соединение закрыто.")


# ============================================================
# ТОЧКА ВХОДА
# ============================================================
if __name__ == "__main__":
    menu()