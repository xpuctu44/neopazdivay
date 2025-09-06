@echo off
echo ========================================
echo ТЕСТ КОМАНД БЕЗ ПРОБЛЕМ С КОДИРОВКОЙ
echo ========================================

echo.
echo 1. Проверяем текущую директорию...
echo Текущая директория: %CD%

echo.
echo 2. Список файлов в текущей папке...
dir /b

echo.
echo 3. Проверяем Python...
python --version
if %errorlevel% neq 0 (
    echo Python не найден, пробуем py...
    py --version
)

echo.
echo 4. Проверяем файлы проекта...
if exist "neopazdivay\app\main.py" (
    echo main.py - НАЙДЕН
) else (
    echo main.py - НЕ НАЙДЕН
)

echo.
echo 5. Проверяем базу данных...
if exist "neopazdivay\time_tracker.db" (
    echo База данных - НАЙДЕНА
) else (
    echo База данных - НЕ НАЙДЕНА
)

echo.
echo 6. Останавливаем Python процессы...
taskkill /f /im python.exe >nul 2>&1
echo Python процессы остановлены

echo.
echo 7. Переходим в папку neopazdivay...
cd neopazdivay
echo Текущая директория: %CD%

echo.
echo 8. Создаем базу данных...
python -c "from app.database import Base, engine; from app.models import *; Base.metadata.create_all(bind=engine); print('База данных создана успешно')"

echo.
echo 9. Создаем тестового администратора...
python -c "
from app.database import SessionLocal
from app.models import User
from app.security import hash_password

db = SessionLocal()
try:
    admin = db.query(User).filter(User.role == 'admin').first()
    if not admin:
        admin = User(
            email='admin@test.com',
            full_name='Администратор',
            password_hash=hash_password('admin123'),
            role='admin',
            is_active=True
        )
        db.add(admin)
        db.commit()
        print('Тестовый администратор создан: admin@test.com / admin123')
    else:
        print('Администратор уже существует')
finally:
    db.close()
"

echo.
echo 10. Запускаем сервер...
echo Сервер запускается на http://localhost:8000
echo Для остановки нажмите Ctrl+C
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo ========================================
echo СЕРВЕР ОСТАНОВЛЕН
echo ========================================
pause

