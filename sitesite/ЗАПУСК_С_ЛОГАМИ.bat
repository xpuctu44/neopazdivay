@echo off
chcp 65001 >nul
title Time Tracker - Запуск с логами

echo.
echo ========================================
echo    TIME TRACKER - ЗАПУСК С ЛОГАМИ
echo ========================================
echo.

echo 🔍 Проверяем Python...
python --version
if errorlevel 1 (
    echo ❌ Python не найден!
    pause
    exit /b 1
)

echo.
echo 📁 Переходим в папку проекта...
cd neopazdivay
if not exist "app\main.py" (
    echo ❌ Файл app\main.py не найден!
    echo Убедитесь, что вы находитесь в папке sitesite
    pause
    exit /b 1
)

echo.
echo 📦 Устанавливаем зависимости...
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Ошибка установки зависимостей!
    pause
    exit /b 1
)

echo.
echo 🚀 Запускаем сервер...
echo.
echo ========================================
echo    СЕРВЕР ЗАПУЩЕН
echo ========================================
echo.
echo 🌐 Откройте браузер и перейдите по адресу:
echo    http://localhost:8000
echo.
echo 📋 Доступные страницы:
echo    / - Главная страница
echo    /register - Регистрация (секрет админа: 20252025)
echo    /login - Вход в систему
echo    /dashboard - Рабочая панель
echo.
echo ⚠️  Для остановки нажмите Ctrl+C
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level info

echo.
echo 👋 Сервер остановлен.
pause


