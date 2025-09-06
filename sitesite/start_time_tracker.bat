@echo off
echo ========================================
echo    Time Tracker - Система учета времени
echo ========================================
echo.

echo Переходим в директорию проекта...
cd /d "%~dp0neopazdivay"

echo Проверяем наличие файлов...
if not exist "requirements.txt" (
    echo ОШИБКА: Файл requirements.txt не найден!
    echo Убедитесь, что вы находитесь в правильной директории.
    pause
    exit /b 1
)

echo Устанавливаем зависимости...
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo ОШИБКА: Не удалось установить зависимости!
    echo Проверьте, что Python установлен и добавлен в PATH.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Запускаем приложение...
echo ========================================
echo.
echo Откройте браузер и перейдите по адресу:
echo    http://localhost:8000
echo.
echo Доступные страницы:
echo    /register (Admin secret: 20252025)
echo    /login
echo    /dashboard
echo    /admin/planning
echo    /admin/reports
echo.
echo Для остановки нажмите Ctrl+C
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo Приложение остановлено.
pause

