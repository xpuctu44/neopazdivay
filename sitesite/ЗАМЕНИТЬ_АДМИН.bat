@echo off
echo ========================================
echo ЗАМЕНА АДМИН ФАЙЛОВ
echo ========================================

echo.
echo 1. Создаем резервную копию...
copy "neopazdivay\app\routers\admin.py" "neopazdivay\app\routers\admin_backup.py"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать резервную копию!
    pause
    exit /b 1
)

echo.
echo 2. Заменяем admin.py на простую версию...
copy "neopazdivay\app\routers\admin_simple.py" "neopazdivay\app\routers\admin.py"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось заменить admin.py!
    pause
    exit /b 1
)

echo.
echo 3. Заменяем admin.html на простую версию...
copy "neopazdivay\app\templates\admin_simple.html" "neopazdivay\app\templates\admin.html"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось заменить admin.html!
    pause
    exit /b 1
)

echo.
echo ✅ Файлы успешно заменены!
echo Теперь перезапустите сервер и проверьте работу.
echo.
pause


