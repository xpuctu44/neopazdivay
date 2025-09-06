@echo off
echo ========================================
echo ПРОВЕРКА И ЗАПУСК СЕРВЕРА
echo ========================================

echo.
echo 1. Проверяем порт 8000...
netstat -aon | findstr :8000
if %errorlevel% == 0 (
    echo Порт 8000 занят, останавливаем процессы...
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
        echo Останавливаем процесс %%a
        taskkill /f /pid %%a
    )
    timeout /t 3 /nobreak
) else (
    echo Порт 8000 свободен
)

echo.
echo 2. Запускаем сервер...
cd neopazdivay
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause

