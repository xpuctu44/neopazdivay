@echo off
echo ========================================
echo ЗАПУСК ЧЕРЕЗ CMD
echo ========================================

echo.
echo 1. Останавливаем сервер...
taskkill /f /im python.exe 2>nul

echo.
echo 2. Создаем папку static...
cd neopazdivay\app
if not exist static mkdir static
if not exist static\styles.css (
    echo body { font-family: Arial, sans-serif; } > static\styles.css
)

echo.
echo 3. Возвращаемся в папку neopazdivay...
cd ..

echo.
echo 4. Запускаем сервер через CMD...
cmd /c "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

pause

