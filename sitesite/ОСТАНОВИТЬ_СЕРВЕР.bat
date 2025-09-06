@echo off
chcp 65001 >nul
title Остановка сервера Time Tracker

echo.
echo ========================================
echo    ОСТАНОВКА СЕРВЕРА TIME TRACKER
echo ========================================
echo.

echo 🔍 Ищем процессы на порту 8000...
netstat -ano | findstr :8000

echo.
echo 🛑 Останавливаем процессы Python...
taskkill /f /im python.exe 2>nul
taskkill /f /im pythonw.exe 2>nul

echo.
echo ⏳ Ждем 3 секунды...
timeout /t 3 /nobreak >nul

echo.
echo 🔍 Проверяем, освободился ли порт...
netstat -an | findstr :8000
if errorlevel 1 (
    echo ✅ Порт 8000 освобожден!
) else (
    echo ⚠️  Порт 8000 все еще занят
    echo Попробуйте перезагрузить компьютер
)

echo.
echo 🚀 Теперь можете запустить сервер:
echo    ЗАПУСК_САЙТА.bat
echo.
pause


