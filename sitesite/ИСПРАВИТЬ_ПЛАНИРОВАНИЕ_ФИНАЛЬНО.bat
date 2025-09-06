@echo off
echo ========================================
echo ИСПРАВЛЕНИЕ ПЛАНИРОВАНИЯ - ФИНАЛЬНАЯ ВЕРСИЯ
echo ========================================

echo.
echo 1. Останавливаем сервер...
taskkill /f /im python.exe >nul 2>&1

echo.
echo 2. Переходим в папку проекта...
cd neopazdivay

echo.
echo 3. Удаляем старую базу данных...
if exist "time_tracker.db" del "time_tracker.db"
echo Старая база данных удалена

echo.
echo 4. Создаем новую базу данных...
python -c "from app.database import Base, engine; from app.models import *; Base.metadata.create_all(bind=engine); print('База данных создана')"

echo.
echo 5. Создаем тестового администратора...
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
        print('Администратор создан: admin@test.com / admin123')
    else:
        print('Администратор уже существует')
finally:
    db.close()
"

echo.
echo 6. Создаем тестового сотрудника...
python -c "
from app.database import SessionLocal
from app.models import User
from app.security import hash_password

db = SessionLocal()
try:
    employee = db.query(User).filter(User.email == 'employee@test.com').first()
    if not employee:
        employee = User(
            email='employee@test.com',
            full_name='Тестовый Сотрудник',
            password_hash=hash_password('emp123'),
            role='employee',
            is_active=True
        )
        db.add(employee)
        db.commit()
        print('Сотрудник создан: employee@test.com / emp123')
    else:
        print('Сотрудник уже существует')
finally:
    db.close()
"

echo.
echo 7. Тестируем функцию планирования...
python -c "
from app.routers.admin import admin_planning
from app.database import SessionLocal
from unittest.mock import Mock

db = SessionLocal()
try:
    mock_request = Mock()
    mock_request.session = {'user_id': 1, 'role': 'admin'}
    
    result = admin_planning(mock_request, db)
    print('Функция планирования работает корректно')
except Exception as e:
    print(f'Ошибка в функции планирования: {e}')
finally:
    db.close()
"

echo.
echo 8. Запускаем сервер...
echo.
echo ========================================
echo СЕРВЕР ЗАПУЩЕН!
echo ========================================
echo.
echo Войдите в систему:
echo Администратор: admin@test.com / admin123
echo Сотрудник: employee@test.com / emp123
echo.
echo Сайт: http://localhost:8000
echo.
echo Для остановки нажмите Ctrl+C
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo ========================================
echo СЕРВЕР ОСТАНОВЛЕН
echo ========================================
pause