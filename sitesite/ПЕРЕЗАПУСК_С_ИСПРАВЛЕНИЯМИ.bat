@echo off
echo ========================================
echo ПЕРЕЗАПУСК С ИСПРАВЛЕНИЯМИ
echo ========================================

echo.
echo 1. Останавливаем сервер...
taskkill /f /im python.exe 2>nul

echo.
echo 2. Ждем 3 секунды...
timeout /t 3 /nobreak

echo.
echo 3. Создаем папку static если не существует...
cd neopazdivay\app
if not exist static mkdir static
if not exist static\styles.css (
    echo body { font-family: Arial, sans-serif; } > static\styles.css
)

echo.
echo 4. Возвращаемся в папку neopazdivay...
cd ..

echo.
echo 5. Запускаем сервер...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo ========================================
echo ГОТОВО! Сервер запущен с исправлениями!
echo ========================================
echo.
echo Исправления:
echo - Упрощены модели данных
echo - Удалены неиспользуемые модели Project и TimeEntry
echo - Создана папка static
echo.
echo Откройте браузер: http://localhost:8000
echo.
pause

