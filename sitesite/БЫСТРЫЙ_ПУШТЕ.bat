@echo off
chcp 65001 >nul
echo ========================================
echo БЫСТРАЯ ОТПРАВКА НА GITHUB
echo ========================================

cd /d "%~dp0"

echo Добавляем файлы...
git add .

echo Создаем коммит...
git commit -m "Auto update - %date% %time%"

echo Отправляем на GitHub...
git push

echo.
echo ✅ Готово! Изменения отправлены на GitHub
echo.
timeout /t 3 /nobreak >nul
