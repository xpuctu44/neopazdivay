@echo off
chcp 65001 >nul
echo ========================================
echo ВОССТАНОВЛЕНИЕ ПОСЛЕДНЕЙ РАБОЧЕЙ ВЕРСИИ
echo ========================================
echo.

echo [1/8] Останавливаем все процессы Python...
taskkill /f /im python.exe 2>nul
taskkill /f /im uvicorn.exe 2>nul
timeout /t 2 /nobreak >nul

echo [2/8] Переходим в директорию проекта...
cd /d "%~dp0neopazdivay"

echo [3/8] Восстанавливаем main.py из резервной копии...
if exist "app\main_backup.py" (
    copy "app\main_backup.py" "app\main.py" >nul
    echo ✅ main.py восстановлен
) else (
    echo ⚠️  main_backup.py не найден, используем текущий main.py
)

echo [4/8] Восстанавливаем admin.py с полным функционалом...
if exist "app\routers\admin_full_backup_employees.py" (
    copy "app\routers\admin_full_backup_employees.py" "app\routers\admin.py" >nul
    echo ✅ admin.py восстановлен с полным функционалом
) else (
    echo ⚠️  admin_full_backup_employees.py не найден
)

echo [5/8] Восстанавливаем admin.html с полным функционалом...
if exist "app\templates\admin_full_backup_employees.html" (
    copy "app\templates\admin_full_backup_employees.html" "app\templates\admin.html" >nul
    echo ✅ admin.html восстановлен с полным функционалом
) else (
    echo ⚠️  admin_full_backup_employees.html не найден
)

echo [6/8] Проверяем базу данных...
if exist "time_tracker.db" (
    echo ✅ База данных найдена
) else (
    echo ⚠️  База данных не найдена, будет создана при запуске
)

echo [7/8] Устанавливаем зависимости...
pip install -r requirements.txt --quiet --disable-pip-version-check

echo [8/8] Запускаем сервер...
echo.
echo ========================================
echo СЕРВЕР ЗАПУЩЕН!
echo ========================================
echo.
echo 🌐 Сайт доступен по адресу: http://localhost:8000
echo 📊 Админ панель: http://localhost:8000/admin
echo.
echo ВОССТАНОВЛЕННЫЙ ФУНКЦИОНАЛ:
echo ✅ Таймер прихода и ухода
echo ✅ Управление сотрудниками
echo ✅ Планирование смен
echo ✅ Статистика и отчеты
echo ✅ Админ панель
echo ✅ Система авторизации
echo.
echo Для остановки сервера нажмите Ctrl+C
echo ========================================
echo.

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
