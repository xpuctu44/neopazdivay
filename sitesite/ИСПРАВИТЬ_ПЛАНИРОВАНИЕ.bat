@echo off
echo ========================================
echo ИСПРАВЛЕНИЕ ПЛАНИРОВАНИЯ
echo ========================================

echo.
echo 1. Останавливаем сервер...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    echo Останавливаем процесс %%a
    taskkill /f /pid %%a
)

echo.
echo 2. Ждем 3 секунды...
timeout /t 3 /nobreak

echo.
echo 3. Запускаем сервер с исправлениями...
cd neopazdivay
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo ========================================
echo ГОТОВО! Планирование исправлено!
echo ========================================
echo.
echo Исправления:
echo - Добавлена переменная entry_map в роутеры
echo - Исправлены модели Attendance и ScheduleEntry
echo - Добавлены недостающие relationships
echo.
pause

