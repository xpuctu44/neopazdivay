@echo off
echo ========================================
echo ТЕСТ ИСПРАВЛЕННОГО ПЛАНИРОВАНИЯ
echo ========================================

echo.
echo 1. Останавливаем сервер...
taskkill /f /im python.exe >nul 2>&1

echo.
echo 2. Переходим в папку проекта...
cd neopazdivay

echo.
echo 3. Создаем базу данных...
python -c "from app.database import Base, engine; from app.models import *; Base.metadata.create_all(bind=engine); print('База данных создана')"

echo.
echo 4. Создаем тестового администратора...
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
echo 5. Запускаем сервер...
echo.
echo ========================================
echo СЕРВЕР ЗАПУЩЕН!
echo ========================================
echo.
echo Войдите в систему:
echo Администратор: admin@test.com / admin123
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

