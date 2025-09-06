@echo off
echo Останавливаем сервер...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

echo Запускаем сервер заново...
cd neopazdivay
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause


