@echo off
echo ========================================
echo ВОССТАНОВЛЕНИЕ ПРОСТОЙ ВЕРСИИ
echo ========================================

echo.
echo 1. Восстанавливаем admin.py из резервной копии...
copy "neopazdivay\app\routers\admin_backup_simple.py" "neopazdivay\app\routers\admin.py"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось восстановить admin.py!
    pause
    exit /b 1
)

echo.
echo 2. Восстанавливаем admin.html из резервной копии...
copy "neopazdivay\app\templates\admin_backup_simple.html" "neopazdivay\app\templates\admin.html"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось восстановить admin.html!
    pause
    exit /b 1
)

echo.
echo ✅ Файлы успешно восстановлены на простую версию!
echo Теперь перезапустите сервер.
echo.
pause

