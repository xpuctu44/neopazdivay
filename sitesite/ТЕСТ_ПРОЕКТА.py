print("Тест проекта...")

try:
    print("1. Проверяем папку neopazdivay...")
    import os
    if os.path.exists("neopazdivay"):
        print("✅ Папка neopazdivay найдена")
    else:
        print("❌ Папка neopazdivay не найдена")
        exit(1)
except Exception as e:
    print(f"❌ Ошибка проверки папки: {e}")
    exit(1)

try:
    print("2. Переходим в папку neopazdivay...")
    os.chdir("neopazdivay")
    print(f"✅ Текущая папка: {os.getcwd()}")
except Exception as e:
    print(f"❌ Ошибка перехода в папку: {e}")
    exit(1)

try:
    print("3. Проверяем файлы проекта...")
    if os.path.exists("app"):
        print("✅ Папка app найдена")
    else:
        print("❌ Папка app не найдена")
        exit(1)
        
    if os.path.exists("app/main.py"):
        print("✅ app/main.py найден")
    else:
        print("❌ app/main.py не найден")
        exit(1)
        
    if os.path.exists("app/models.py"):
        print("✅ app/models.py найден")
    else:
        print("❌ app/models.py не найден")
        exit(1)
        
    if os.path.exists("app/database.py"):
        print("✅ app/database.py найден")
    else:
        print("❌ app/database.py не найден")
        exit(1)
        
except Exception as e:
    print(f"❌ Ошибка проверки файлов: {e}")
    exit(1)

try:
    print("4. Проверяем импорт app...")
    from app.database import engine
    print("✅ app.database импортирован")
except Exception as e:
    print(f"❌ Ошибка импорта app.database: {e}")
    exit(1)

try:
    print("5. Проверяем импорт models...")
    from app.models import User
    print("✅ app.models импортирован")
except Exception as e:
    print(f"❌ Ошибка импорта app.models: {e}")
    exit(1)

print("✅ Все тесты проекта пройдены успешно!")

