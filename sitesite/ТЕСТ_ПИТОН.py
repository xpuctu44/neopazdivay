print("Python работает!")
print("Тест 1: базовый вывод")

try:
    import sys
    print(f"Python версия: {sys.version}")
    print("Тест 2: импорт sys - OK")
except Exception as e:
    print(f"Ошибка импорта sys: {e}")

try:
    from datetime import date
    print(f"Сегодня: {date.today()}")
    print("Тест 3: импорт datetime - OK")
except Exception as e:
    print(f"Ошибка импорта datetime: {e}")

try:
    import os
    print(f"Текущая папка: {os.getcwd()}")
    print("Тест 4: импорт os - OK")
except Exception as e:
    print(f"Ошибка импорта os: {e}")

print("Все базовые тесты завершены!")

