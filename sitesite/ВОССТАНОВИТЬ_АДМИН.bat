@echo off
echo ========================================
echo ВОССТАНОВЛЕНИЕ АДМИН ФАЙЛОВ
echo ========================================

echo.
echo 1. Восстанавливаем admin.py из резервной копии...
copy "neopazdivay\app\routers\admin_backup.py" "neopazdivay\app\routers\admin.py"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось восстановить admin.py!
    pause
    exit /b 1
)

echo.
echo ✅ Файлы успешно восстановлены!
echo Теперь перезапустите сервер.
echo.
pause


