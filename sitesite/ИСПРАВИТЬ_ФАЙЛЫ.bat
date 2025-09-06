@echo off
echo ========================================
echo ИСПРАВЛЕНИЕ ФАЙЛОВ ADMIN
echo ========================================

echo.
echo 1. Удаляем старый admin.py...
del "neopazdivay\app\routers\admin.py"

echo.
echo 2. Переименовываем admin_full.py в admin.py...
ren "neopazdivay\app\routers\admin_full.py" "admin.py"

echo.
echo 3. Удаляем старый admin.html...
del "neopazdivay\app\templates\admin.html"

echo.
echo 4. Переименовываем admin_full.html в admin.html...
ren "neopazdivay\app\templates\admin_full.html" "admin.html"

echo.
echo ✅ Файлы успешно исправлены!
echo Теперь вкладка "Сотрудники" должна появиться в админ панели.
echo.
pause

