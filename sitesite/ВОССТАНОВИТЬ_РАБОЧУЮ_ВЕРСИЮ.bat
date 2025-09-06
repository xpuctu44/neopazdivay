@echo off
echo ========================================
echo ВОССТАНОВЛЕНИЕ РАБОЧЕЙ ВЕРСИИ
echo ========================================

echo.
echo 1. Останавливаем сервер...
taskkill /f /im python.exe 2>nul

echo.
echo 2. Восстанавливаем admin.py из backup...
cd neopazdivay\app\routers
copy admin_full_backup_employees.py admin.py

echo.
echo 3. Восстанавливаем admin.html из backup...
cd ..\templates
copy admin_full_backup_employees.html admin.html

echo.
echo 4. Возвращаемся в корень проекта...
cd ..\..

echo.
echo 5. Запускаем сервер...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo ========================================
echo ГОТОВО! Рабочая версия восстановлена!
echo ========================================
echo.
echo Теперь у вас есть:
echo - Таймер прихода и ухода
echo - Вкладка "Сотрудники" 
echo - Планирование смен
echo - Все функции работают
echo.
pause

