@echo off
echo ========================================
echo ТЕСТ МИНИМАЛЬНОГО СЕРВЕРА
echo ========================================

echo.
echo 1. Останавливаем все Python процессы...
taskkill /f /im python.exe >nul 2>&1

echo.
echo 2. Ждем 3 секунды...
timeout /t 3 /nobreak >nul

echo.
echo 3. Переходим в папку проекта...
cd neopazdivay

echo.
echo 4. Запускаем простую проверку...
python ..\ПРОСТАЯ_ПРОВЕРКА.py

echo.
echo 5. Запускаем минимальный сервер...
echo.
echo ========================================
echo МИНИМАЛЬНЫЙ СЕРВЕР ЗАПУЩЕН!
echo ========================================
echo.
echo Сайт: http://localhost:8000
echo Тест шаблона: http://localhost:8000/test
echo.
echo Для остановки нажмите Ctrl+C
echo.
python app/main_simple.py

echo.
echo ========================================
echo СЕРВЕР ОСТАНОВЛЕН
echo ========================================
pause

