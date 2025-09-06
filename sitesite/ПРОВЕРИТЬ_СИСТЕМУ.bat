@echo off
echo ========================================
echo ПРОВЕРКА СИСТЕМЫ
echo ========================================

echo.
echo 1. Информация о системе...
echo Операционная система: %OS%
echo Архитектура: %PROCESSOR_ARCHITECTURE%
echo Версия: %OSVERSION%

echo.
echo 2. Проверка кодировки...
chcp
echo Текущая кодовая страница: %CODEPAGE%

echo.
echo 3. Проверка PATH...
echo Python в PATH:
where python 2>nul
if %errorlevel% neq 0 (
    echo Python не найден в PATH
    where py 2>nul
    if %errorlevel% neq 0 (
        echo py также не найден
    ) else (
        echo Найден py launcher
    )
) else (
    echo Python найден в PATH
)

echo.
echo 4. Проверка переменных окружения...
echo PYTHONPATH: %PYTHONPATH%
echo PYTHONHOME: %PYTHONHOME%

echo.
echo 5. Проверка региональных настроек...
echo LANG: %LANG%
echo LC_ALL: %LC_ALL%

echo.
echo 6. Проверка PowerShell...
powershell -Command "Get-Host | Select-Object Name, Version"
if %errorlevel% neq 0 (
    echo Ошибка при запуске PowerShell
) else (
    echo PowerShell работает
)

echo.
echo ========================================
echo ПРОВЕРКА ЗАВЕРШЕНА
echo ========================================
echo.
echo Рекомендации:
echo 1. Установите кодовую страницу 65001 (UTF-8): chcp 65001
echo 2. Проверьте региональные настройки Windows
echo 3. Перезагрузите компьютер
echo 4. Используйте cmd вместо PowerShell
echo.
pause

