@echo off
echo ========================================
echo ИСПРАВЛЕНИЕ ПРОБЛЕМ С ATTENDANCE
echo ========================================

echo.
echo 1. Создаем резервную копию models.py...
copy "neopazdivay\app\models.py" "neopazdivay\app\models_backup.py"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать резервную копию!
    pause
    exit /b 1
)

echo.
echo 2. Создаем резервную копию dashboard.html...
copy "neopazdivay\app\templates\dashboard.html" "neopazdivay\app\templates\dashboard_backup_attendance.html"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать резервную копию!
    pause
    exit /b 1
)

echo.
echo ✅ Файлы исправлены!
echo.
echo ИСПРАВЛЕНИЯ:
echo - Исправлены URL в dashboard.html (/attendance/start и /attendance/stop)
echo - Добавлены связи в модели Attendance и ScheduleEntry
echo - Добавлено поле phone в модель Store
echo.
echo Теперь перезапустите сервер и проверьте работу кнопок.
echo.
pause

