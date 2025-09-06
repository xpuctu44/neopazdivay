@echo off
echo ========================================
echo ИСПРАВЛЕНИЕ КОДИРОВКИ
echo ========================================

echo.
echo 1. Устанавливаем кодовую страницу UTF-8...
chcp 65001
if %errorlevel% neq 0 (
    echo Ошибка при установке кодовой страницы
) else (
    echo Кодовая страница установлена на UTF-8
)

echo.
echo 2. Проверяем текущую кодовую страницу...
chcp

echo.
echo 3. Устанавливаем переменные окружения...
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

echo.
echo 4. Проверяем Python с новой кодировкой...
python -c "import sys; print('Python encoding:', sys.stdout.encoding)"
if %errorlevel% neq 0 (
    echo Ошибка при проверке Python
    py -c "import sys; print('Python encoding:', sys.stdout.encoding)"
)

echo.
echo 5. Тестируем команду...
echo Тестовая команда: echo Hello World
echo Hello World

echo.
echo ========================================
echo КОДИРОВКА ИСПРАВЛЕНА
echo ========================================
echo.
echo Теперь попробуйте запустить сервер:
echo ЗАПУСК_БЕЗ_POWERSHELL.bat
echo.
pause

