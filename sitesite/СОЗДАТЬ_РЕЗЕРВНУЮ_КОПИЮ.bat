@echo off
chcp 65001 >nul
echo ========================================
echo СОЗДАНИЕ РЕЗЕРВНОЙ КОПИИ
echo ========================================

set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%

echo Создаем резервную копию от %timestamp%...

cd /d "%~dp0neopazdivay"

echo [1/4] Создаем резервную копию main.py...
copy "app\main.py" "app\main_backup_%timestamp%.py" >nul
echo ✅ main.py сохранен как main_backup_%timestamp%.py

echo [2/4] Создаем резервную копию admin.py...
copy "app\routers\admin.py" "app\routers\admin_backup_%timestamp%.py" >nul
echo ✅ admin.py сохранен как admin_backup_%timestamp%.py

echo [3/4] Создаем резервную копию admin.html...
copy "app\templates\admin.html" "app\templates\admin_backup_%timestamp%.html" >nul
echo ✅ admin.html сохранен как admin_backup_%timestamp%.html

echo [4/4] Создаем резервную копию базы данных...
if exist "time_tracker.db" (
    copy "time_tracker.db" "time_tracker_backup_%timestamp%.db" >nul
    echo ✅ База данных сохранена как time_tracker_backup_%timestamp%.db
) else (
    echo ⚠️  База данных не найдена
)

echo.
echo ========================================
echo РЕЗЕРВНАЯ КОПИЯ СОЗДАНА!
echo ========================================
echo.
echo Файлы сохранены с меткой времени: %timestamp%
echo.
echo Для восстановления используйте:
echo ВОССТАНОВИТЬ_ПОСЛЕДНЮЮ_РАБОЧУЮ_ВЕРСИЮ.bat
echo.
pause
