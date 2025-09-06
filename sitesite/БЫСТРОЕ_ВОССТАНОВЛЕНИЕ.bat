@echo off
chcp 65001 >nul
echo ========================================
echo БЫСТРОЕ ВОССТАНОВЛЕНИЕ РАБОЧЕЙ ВЕРСИИ
echo ========================================

echo Останавливаем сервер...
taskkill /f /im python.exe 2>nul

echo Восстанавливаем файлы...
cd /d "%~dp0neopazdivay"
copy "app\routers\admin_full_backup_employees.py" "app\routers\admin.py" >nul
copy "app\templates\admin_full_backup_employees.html" "app\templates\admin.html" >nul

echo Запускаем сервер...
start "Time Tracker Server" cmd /k "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo ✅ Готово! Сервер запущен в новом окне
echo 🌐 Сайт: http://localhost:8000
echo.
timeout /t 3 /nobreak >nul
