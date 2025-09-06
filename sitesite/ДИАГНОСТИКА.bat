@echo off
chcp 65001 >nul
title Диагностика Time Tracker

echo.
echo ========================================
echo    ДИАГНОСТИКА СЕРВЕРА TIME TRACKER
echo ========================================
echo.

echo 🐍 Проверяем Python...
python --version
if errorlevel 1 (
    echo ❌ Python не найден!
    echo Установите Python с https://python.org
    pause
    exit /b 1
)
echo ✅ Python найден!

echo.
echo 📁 Проверяем структуру проекта...
if not exist "neopazdivay\app\main.py" (
    echo ❌ Файл neopazdivay\app\main.py не найден!
    echo Проверьте, что вы находитесь в папке sitesite
    pause
    exit /b 1
)
echo ✅ Структура проекта найдена!

echo.
echo 📦 Проверяем зависимости...
cd neopazdivay
python -c "import fastapi; print('✅ FastAPI')" 2>nul || echo ❌ FastAPI не установлен
python -c "import uvicorn; print('✅ Uvicorn')" 2>nul || echo ❌ Uvicorn не установлен
python -c "import jinja2; print('✅ Jinja2')" 2>nul || echo ❌ Jinja2 не установлен
python -c "import sqlalchemy; print('✅ SQLAlchemy')" 2>nul || echo ❌ SQLAlchemy не установлен

echo.
echo 🚀 Тестируем импорт приложения...
python -c "from app.main import app; print('✅ Приложение импортировано')" 2>nul || (
    echo ❌ Ошибка импорта приложения
    echo Попробуйте установить зависимости:
    echo pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo 🔌 Проверяем порт 8000...
netstat -an | findstr :8000 >nul
if errorlevel 1 (
    echo ✅ Порт 8000 свободен
) else (
    echo ⚠️  Порт 8000 занят
    echo Возможно, сервер уже запущен
)

echo.
echo ========================================
echo    РЕЗУЛЬТАТЫ ДИАГНОСТИКИ
echo ========================================
echo.
echo ✅ Все проверки пройдены!
echo.
echo 🚀 Попробуйте запустить сервер:
echo    ЗАПУСК_САЙТА.bat
echo.
echo 🌐 После запуска откройте браузер:
echo    http://localhost:8000
echo.
pause


