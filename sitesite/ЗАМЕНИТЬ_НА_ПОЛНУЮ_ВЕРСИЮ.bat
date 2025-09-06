@echo off
echo ========================================
echo ЗАМЕНА НА ПОЛНОФУНКЦИОНАЛЬНУЮ ВЕРСИЮ
echo ========================================

echo.
echo 1. Создаем резервную копию admin.py...
copy "neopazdivay\app\routers\admin.py" "neopazdivay\app\routers\admin_backup_simple.py"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать резервную копию!
    pause
    exit /b 1
)

echo.
echo 2. Заменяем admin.py на полнофункциональную версию...
copy "neopazdivay\app\routers\admin_full.py" "neopazdivay\app\routers\admin.py"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось заменить admin.py!
    pause
    exit /b 1
)

echo.
echo 3. Создаем резервную копию admin.html...
copy "neopazdivay\app\templates\admin.html" "neopazdivay\app\templates\admin_backup_simple.html"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать резервную копию admin.html!
    pause
    exit /b 1
)

echo.
echo 4. Заменяем admin.html на полнофункциональную версию...
copy "neopazdivay\app\templates\admin_full.html" "neopazdivay\app\templates\admin.html"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось заменить admin.html!
    pause
    exit /b 1
)

echo.
echo ✅ Файлы успешно заменены на полнофункциональную версию!
echo.
echo НОВЫЕ ВОЗМОЖНОСТИ:
echo - Создание и управление сменами
echo - Просмотр графика по датам
echo - Управление магазинами
echo - Статистика и отчеты
echo.
echo Теперь перезапустите сервер и проверьте работу.
echo.
pause

