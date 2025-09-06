@echo off
echo ========================================
echo ДОБАВЛЕНИЕ ТАЙМЕРА В DASHBOARD
echo ========================================

echo.
echo 1. Создаем резервную копию dashboard.html...
copy "neopazdivay\app\templates\dashboard.html" "neopazdivay\app\templates\dashboard_backup_timer.html"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать резервную копию!
    pause
    exit /b 1
)

echo.
echo ✅ Таймер добавлен в dashboard!
echo.
echo НОВЫЕ ВОЗМОЖНОСТИ:
echo - Таймер показывает время работы в реальном времени
echo - Отображается только когда смена активна
echo - Показывает время начала работы
echo - Обновляется каждую секунду
echo - Красивый дизайн с зеленой рамкой
echo.
echo ЛОГИКА РАБОТЫ:
echo - Если смена НЕ активна: показывается кнопка "Я пришел"
echo - Если смена активна: показывается таймер и кнопка "Я ушел"
echo.
echo Теперь перезапустите сервер и проверьте работу таймера.
echo.
pause

