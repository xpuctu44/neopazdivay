@echo off
echo ========================================
echo ДОБАВЛЕНИЕ ВКЛАДКИ СОТРУДНИКИ
echo ========================================

echo.
echo 1. Создаем резервную копию admin_full.py...
copy "neopazdivay\app\routers\admin_full.py" "neopazdivay\app\routers\admin_full_backup_employees.py"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать резервную копию!
    pause
    exit /b 1
)

echo.
echo 2. Создаем резервную копию admin_full.html...
copy "neopazdivay\app\templates\admin_full.html" "neopazdivay\app\templates\admin_full_backup_employees.html"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать резервную копию!
    pause
    exit /b 1
)

echo.
echo ✅ Вкладка "Сотрудники" добавлена!
echo.
echo НОВЫЕ ВОЗМОЖНОСТИ:
echo - Вкладка "Сотрудники" в админ панели
echo - Список всех сотрудников с их данными
echo - Назначение магазина каждому сотруднику
echo - Активация/деактивация сотрудников
echo - Уведомления об успешных операциях
echo.
echo ФУНКЦИИ:
echo - Просмотр всех данных сотрудников
echo - Выпадающий список для назначения магазина
echo - Кнопки активации/деактивации
echo - Цветовая индикация статусов
echo - Подтверждение действий
echo.
echo Перезапустите сервер и проверьте новую вкладку.
echo.
pause

