@echo off
echo ========================================
echo    КОПИРОВАНИЕ ВСЕХ ФАЙЛОВ ПРОЕКТА
echo ========================================
echo.

echo Создаем структуру папок...
mkdir neopazdivay\app\routers 2>nul
mkdir neopazdivay\app\static\css 2>nul
mkdir neopazdivay\app\templates 2>nul

echo Копируем файлы приложения...
if exist "..\neopazdivay\app\*.py" (
    copy "..\neopazdivay\app\*.py" "neopazdivay\app\" /Y
    echo ✅ Основные файлы приложения скопированы
) else (
    echo ⚠️  Файлы приложения не найдены в родительской папке
)

if exist "..\neopazdivay\app\routers\*.py" (
    copy "..\neopazdivay\app\routers\*.py" "neopazdivay\app\routers\" /Y
    echo ✅ Роутеры скопированы
)

if exist "..\neopazdivay\app\static\css\*.css" (
    copy "..\neopazdivay\app\static\css\*.css" "neopazdivay\app\static\css\" /Y
    echo ✅ Стили скопированы
)

if exist "..\neopazdivay\app\templates\*.html" (
    copy "..\neopazdivay\app\templates\*.html" "neopazdivay\app\templates\" /Y
    echo ✅ Шаблоны скопированы
)

echo.
echo Копируем вспомогательные файлы...
if exist "..\start_time_tracker.bat" (
    copy "..\start_time_tracker.bat" "." /Y
    echo ✅ Скрипт запуска скопирован
)

if exist "..\ЗАПУСК_САЙТА.bat" (
    copy "..\ЗАПУСК_САЙТА.bat" "." /Y
    echo ✅ Основной скрипт запуска скопирован
)

if exist "..\ОТКРЫТЬ_САЙТ.html" (
    copy "..\ОТКРЫТЬ_САЙТ.html" "." /Y
    echo ✅ HTML страница скопирована
)

if exist "..\CHECK_STATUS.html" (
    copy "..\CHECK_STATUS.html" "." /Y
    echo ✅ Страница проверки статуса скопирована
)

if exist "..\TROUBLESHOOTING.md" (
    copy "..\TROUBLESHOOTING.md" "." /Y
    echo ✅ Руководство по устранению неполадок скопировано
)

if exist "..\DEVELOPER_README.md" (
    copy "..\DEVELOPER_README.md" "." /Y
    echo ✅ Документация разработчика скопирована
)

echo.
echo ========================================
echo    КОПИРОВАНИЕ ЗАВЕРШЕНО!
echo ========================================
echo.
echo Теперь вы можете:
echo 1. Запустить ЗАПУСК_САЙТА.bat для запуска сайта
echo 2. Прочитать ИНСТРУКЦИЯ.md для подробной информации
echo.
pause


