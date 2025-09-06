@echo off
chcp 65001 >nul
title Time Tracker - Порт 8001

echo.
echo ========================================
echo    TIME TRACKER - ПОРТ 8001
echo ========================================
echo.

echo 🔍 Проверяем Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден!
    pause
    exit /b 1
)

echo ✅ Python найден!

echo.
echo 📁 Переходим в папку проекта...
cd neopazdivay

echo.
echo 📦 Устанавливаем зависимости...
python -m pip install -r requirements.txt --quiet

echo.
echo 🚀 Запускаем сервер на порту 8001...
echo.
echo ========================================
echo    САЙТ ДОСТУПЕН ПО АДРЕСУ:
echo    http://localhost:8001
echo ========================================
echo.
echo 📋 Доступные страницы:
echo    /register (секрет админа: 20252025)
echo    /login
echo    /dashboard
echo    /admin/planning
echo    /admin/reports
echo.
echo 🌐 Открываем браузер...
timeout /t 3 /nobreak >nul
start http://localhost:8001

echo.
echo ⚠️  Для остановки нажмите Ctrl+C
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

echo.
echo 👋 Сервер остановлен.
pause


