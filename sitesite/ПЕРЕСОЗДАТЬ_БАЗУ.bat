@echo off
echo ========================================
echo ПЕРЕСОЗДАНИЕ БАЗЫ ДАННЫХ
echo ========================================

echo.
echo 1. Останавливаем сервер...
taskkill /f /im python.exe 2>nul

echo.
echo 2. Удаляем старую базу данных...
cd neopazdivay
if exist time_tracker.db del time_tracker.db

echo.
echo 3. Создаем новую базу данных...
python -c "
from app.database import engine, Base
from app import models
Base.metadata.create_all(bind=engine)
print('База данных создана успешно!')
"

echo.
echo 4. Запускаем сервер...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo ========================================
echo ГОТОВО! База данных пересоздана!
echo ========================================
echo.
echo Теперь нужно зарегистрировать нового пользователя.
echo.
pause

