@echo off
echo ========================================
echo ВОССТАНОВЛЕНИЕ ОРИГИНАЛЬНОГО MAIN.PY
echo ========================================

echo.
echo 1. Восстанавливаем main.py из резервной копии...
copy "neopazdivay\app\main_backup.py" "neopazdivay\app\main.py"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось восстановить main.py!
    pause
    exit /b 1
)

echo.
echo ✅ main.py успешно восстановлен!
echo Теперь перезапустите сервер.
echo.
pause

