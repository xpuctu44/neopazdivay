@echo off
echo ========================================
echo ЗАПУСК СЕРВЕРА БЕЗ POWERSHELL
echo ========================================

echo.
echo 1. Останавливаем все Python процессы...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im uvicorn.exe >nul 2>&1

echo.
echo 2. Ждем 3 секунды...
timeout /t 3 /nobreak >nul

echo.
echo 3. Переходим в папку проекта...
cd neopazdivay

echo.
echo 4. Проверяем Python...
python --version
if %errorlevel% neq 0 (
    echo Ошибка: Python не найден!
    echo Попробуйте: py --version
    py --version
    if %errorlevel% neq 0 (
        echo Критическая ошибка: Python не установлен!
        pause
        exit /b 1
    )
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

echo.
echo 5. Создаем базу данных...
%PYTHON_CMD% -c "from app.database import Base, engine; from app.models import *; Base.metadata.create_all(bind=engine); print('База данных создана')"

echo.
echo 6. Запускаем сервер...
echo Используем команду: %PYTHON_CMD% -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
echo.
%PYTHON_CMD% -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo ========================================
echo СЕРВЕР ОСТАНОВЛЕН
echo ========================================
pause

