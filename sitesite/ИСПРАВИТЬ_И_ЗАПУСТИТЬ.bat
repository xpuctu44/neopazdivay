@echo off
echo ========================================
echo ИСПРАВЛЕНИЕ И ЗАПУСК САЙТА
echo ========================================

echo.
echo 1. Останавливаем все процессы Python...
taskkill /f /im python.exe 2>nul

echo.
echo 2. Создаем недостающую папку static...
cd neopazdivay\app
mkdir static 2>nul

echo.
echo 3. Создаем файл styles.css...
echo body { font-family: Arial, sans-serif; } > static\styles.css

echo.
echo 4. Возвращаемся в корень проекта...
cd ..\..

echo.
echo 5. Запускаем сервер...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo ========================================
echo ГОТОВО! Сайт запущен!
echo ========================================
echo.
echo Откройте браузер и перейдите на:
echo http://localhost:8000
echo.
pause

