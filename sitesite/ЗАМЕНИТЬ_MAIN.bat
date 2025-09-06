@echo off
echo ========================================
echo ЗАМЕНА MAIN.PY НА УПРОЩЕННУЮ ВЕРСИЮ
echo ========================================

echo.
echo 1. Создаем резервную копию main.py...
copy "neopazdivay\app\main.py" "neopazdivay\app\main_backup.py"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать резервную копию!
    pause
    exit /b 1
)

echo.
echo 2. Заменяем main.py на упрощенную версию...
copy "neopazdivay\app\main_simple.py" "neopazdivay\app\main.py"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось заменить main.py!
    pause
    exit /b 1
)

echo.
echo ✅ main.py успешно заменен на упрощенную версию!
echo Теперь перезапустите сервер и проверьте работу.
echo.
pause

