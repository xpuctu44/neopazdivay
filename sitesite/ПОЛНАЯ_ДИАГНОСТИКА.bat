@echo off
echo ========================================
echo ПОЛНАЯ ДИАГНОСТИКА СЕРВЕРА
echo ========================================

echo.
echo 1. Проверяем процессы Python...
tasklist | findstr python.exe
if %errorlevel% neq 0 (
    echo Нет запущенных процессов Python
) else (
    echo Найдены процессы Python
)

echo.
echo 2. Проверяем порт 8000...
netstat -an | findstr :8000
if %errorlevel% neq 0 (
    echo Порт 8000 свободен
) else (
    echo Порт 8000 занят
)

echo.
echo 3. Проверяем порт 8001...
netstat -an | findstr :8001
if %errorlevel% neq 0 (
    echo Порт 8001 свободен
) else (
    echo Порт 8001 занят
)

echo.
echo 4. Проверяем файлы проекта...
if exist "neopazdivay\app\main.py" (
    echo main.py найден
) else (
    echo main.py НЕ найден!
)

if exist "neopazdivay\app\routers\admin.py" (
    echo admin.py найден
) else (
    echo admin.py НЕ найден!
)

if exist "neopazdivay\app\templates\admin.html" (
    echo admin.html найден
) else (
    echo admin.html НЕ найден!
)

echo.
echo 5. Проверяем Python...
python --version
if %errorlevel% neq 0 (
    echo Python НЕ установлен!
) else (
    echo Python работает
)

echo.
echo 6. Проверяем uvicorn...
python -m uvicorn --help >nul 2>&1
if %errorlevel% neq 0 (
    echo uvicorn НЕ установлен!
) else (
    echo uvicorn работает
)

echo.
echo ========================================
echo ДИАГНОСТИКА ЗАВЕРШЕНА
echo ========================================
pause


