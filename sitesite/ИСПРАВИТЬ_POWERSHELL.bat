@echo off
echo ========================================
echo ИСПРАВЛЕНИЕ ПРОБЛЕМЫ POWERSHELL
echo ========================================

echo.
echo Проблема: PowerShell добавляет букву 'с' перед командами
echo Решение: Используем cmd напрямую
echo.

echo 1. Проверяем текущую директорию...
cd
echo Текущая директория: %CD%

echo.
echo 2. Проверяем Python...
python --version
if %errorlevel% neq 0 (
    echo Python не найден в PATH
    echo Попробуйте: py --version
    py --version
)

echo.
echo 3. Проверяем файлы проекта...
if exist "neopazdivay\app\main.py" (
    echo main.py - OK
) else (
    echo main.py - НЕ НАЙДЕН!
)

if exist "neopazdivay\app\models.py" (
    echo models.py - OK
) else (
    echo models.py - НЕ НАЙДЕН!
)

if exist "neopazdivay\app\routers\admin.py" (
    echo admin.py - OK
) else (
    echo admin.py - НЕ НАЙДЕН!
)

echo.
echo 4. Проверяем базу данных...
if exist "neopazdivay\time_tracker.db" (
    echo База данных - OK
) else (
    echo База данных - НЕ НАЙДЕНА!
)

echo.
echo 5. Проверяем процессы Python...
tasklist | findstr python.exe
if %errorlevel% neq 0 (
    echo Python процессы не найдены
) else (
    echo Найдены Python процессы
)

echo.
echo ========================================
echo ДИАГНОСТИКА ЗАВЕРШЕНА
echo ========================================
echo.
echo Рекомендации:
echo 1. Используйте bat файлы вместо PowerShell команд
echo 2. Все команды должны выполняться через cmd
echo 3. Проверьте кодировку системы (должна быть UTF-8)
echo.
pause

