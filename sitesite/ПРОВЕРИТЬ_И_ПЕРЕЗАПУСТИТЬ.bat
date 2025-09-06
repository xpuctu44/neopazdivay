@echo off
echo ========================================
echo ПРОВЕРКА И ПЕРЕЗАПУСК СЕРВЕРА
echo ========================================

echo.
echo 1. Останавливаем все процессы на порту 8000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    echo Останавливаем процесс %%a
    taskkill /f /pid %%a
)

echo.
echo 2. Ждем 3 секунды...
timeout /t 3 /nobreak

echo.
echo 3. Запускаем сервер...
cd neopazdivay
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause

