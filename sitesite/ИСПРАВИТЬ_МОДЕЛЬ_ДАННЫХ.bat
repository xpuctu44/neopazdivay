@echo off
echo ========================================
echo ИСПРАВЛЕНИЕ МОДЕЛИ ДАННЫХ
echo ========================================

echo.
echo 1. Останавливаем сервер...
taskkill /f /im python.exe 2>nul

echo.
echo 2. Ждем 3 секунды...
timeout /t 3 /nobreak

echo.
echo 3. Удаляем старую базу данных...
cd neopazdivay
if exist "time_tracker.db" del "time_tracker.db"

echo.
echo 4. Создаем новую базу данных...
python -c "
from app.database import Base, engine
from app.models import User, ScheduleEntry, Store, Attendance
Base.metadata.create_all(bind=engine)
print('База данных создана с правильной структурой')
"

echo.
echo 5. Создаем тестового администратора...
python -c "
from app.database import SessionLocal
from app.models import User
from app.security import hash_password
from datetime import date

db = SessionLocal()
try:
    # Проверяем, есть ли уже админ
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
echo 6. Запускаем сервер...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo ========================================
echo ГОТОВО! Модель данных исправлена!
echo ========================================
echo.
echo Исправления:
echo - Удалены несуществующие поля start_time, end_time, store_id, notes
echo - Используется только shift_type и published
echo - Создана новая база данных
echo - Добавлен тестовый администратор
echo.
echo Войдите как: admin@test.com / admin123
echo.
pause

