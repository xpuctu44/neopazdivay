@echo off
chcp 65001 >nul
title Проверка порта 8000

echo.
echo ========================================
echo    ПРОВЕРКА ПОРТА 8000
echo ========================================
echo.

echo 🔍 Детальная информация о порте 8000:
echo.
netstat -ano | findstr :8000

echo.
echo 📋 Процессы, использующие порт 8000:
echo.
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Процесс ID: %%a
    tasklist /fi "pid eq %%a" /fo table
    echo.
)

echo.
echo 🌐 Проверяем доступность сайта...
echo.
curl -s http://localhost:8000/health 2>nul
if errorlevel 1 (
    echo ❌ Сайт не отвечает на http://localhost:8000
    echo Возможно, процесс завис или есть ошибка
) else (
    echo ✅ Сайт отвечает на http://localhost:8000
    echo Попробуйте открыть в браузере:
    echo    http://localhost:8000
)

echo.
echo ========================================
echo    РЕКОМЕНДАЦИИ
echo ========================================
echo.
echo 1. Если сайт отвечает - откройте браузер:
echo    http://localhost:8000
echo.
echo 2. Если сайт не отвечает - остановите процессы:
echo    ОСТАНОВИТЬ_СЕРВЕР.bat
echo.
echo 3. Или запустите на другом порту:
echo    ЗАПУСК_ПОРТ_8001.bat
echo.
pause


