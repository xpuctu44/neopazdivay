@echo off
echo ========================================
echo ОБНОВЛЕНИЕ АДМИН ФУНКЦИЙ
echo ========================================

echo.
echo 1. Создаем резервную копию admin_full.py...
copy "neopazdivay\app\routers\admin_full.py" "neopazdivay\app\routers\admin_full_backup.py"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать резервную копию!
    pause
    exit /b 1
)

echo.
echo 2. Создаем резервную копию admin_full.html...
copy "neopazdivay\app\templates\admin_full.html" "neopazdivay\app\templates\admin_full_backup.html"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать резервную копию!
    pause
    exit /b 1
)

echo.
echo 3. Создаем резервную копию dashboard.html...
copy "neopazdivay\app\templates\dashboard.html" "neopazdivay\app\templates\dashboard_backup.html"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать резервную копию!
    pause
    exit /b 1
)

echo.
echo ✅ Файлы обновлены!
echo.
echo НОВЫЕ ВОЗМОЖНОСТИ:
echo - Администраторы могут отмечаться о приходе/уходе
echo - Администраторы включены в планирование смен
echo - Роли отображаются в списках и графиках
echo - Обновленная статистика с разделением по ролям
echo.
echo Теперь перезапустите сервер и проверьте работу.
echo.
pause

