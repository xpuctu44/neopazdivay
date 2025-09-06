@echo off
echo ========================================
echo ЗАПУСК СЕРВЕРА С ПРОВЕРКОЙ
echo ========================================

echo.
echo 1. Переходим в папку проекта...
cd neopazdivay
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось перейти в папку neopazdivay!
    pause
    exit /b 1
)

echo.
echo 2. Проверяем файлы...
if not exist "app\main.py" (
    echo ОШИБКА: Файл app\main.py не найден!
    pause
    exit /b 1
)

if not exist "app\routers\admin.py" (
    echo ОШИБКА: Файл app\routers\admin.py не найден!
    pause
    exit /b 1
)

echo.
echo 3. Устанавливаем зависимости...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось установить зависимости!
    pause
    exit /b 1
)

echo.
echo 4. Запускаем сервер...
echo Сервер будет доступен по адресу: http://localhost:8000
echo Для остановки нажмите Ctrl+C
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause


