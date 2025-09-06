@echo off
echo ========================================
echo ИСПРАВЛЕНИЕ АККАУНТА АДМИНИСТРАТОРА
echo ========================================

cd neopazdivay
python ..\ИСПРАВИТЬ_АДМИНА.py

echo.
echo ========================================
echo ПЕРЕЗАПУСК СЕРВЕРА
echo ========================================

echo Останавливаем сервер...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /f /pid %%a
)

echo Ждем 3 секунды...
timeout /t 3 /nobreak

echo Запускаем сервер...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause

