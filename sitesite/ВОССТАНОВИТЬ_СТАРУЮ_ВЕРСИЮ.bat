@echo off
echo ========================================
echo ВОССТАНОВЛЕНИЕ СТАРОЙ РАБОЧЕЙ ВЕРСИИ
echo ========================================

echo.
echo 1. Останавливаем сервер...
taskkill /f /im python.exe 2>nul

echo.
echo 2. Восстанавливаем admin.py...
cd neopazdivay\app\routers
del admin.py
copy admin_full_backup_employees.py admin.py

echo.
echo 3. Восстанавливаем admin.html...
cd ..\templates
del admin.html
copy admin_full_backup_employees.html admin.html

echo.
echo 4. Возвращаемся в корень...
cd ..\..

echo.
echo 5. Запускаем сервер...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo ========================================
echo ГОТОВО! Старая версия восстановлена!
echo ========================================
pause

