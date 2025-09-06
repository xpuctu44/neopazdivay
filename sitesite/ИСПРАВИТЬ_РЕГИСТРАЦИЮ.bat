@echo off
echo ========================================
echo ИСПРАВЛЕНИЕ РЕГИСТРАЦИИ
echo ========================================

echo.
echo 1. Останавливаем сервер...
taskkill /f /im python.exe 2>nul

echo.
echo 2. Ждем 3 секунды...
timeout /t 3 /nobreak

echo.
echo 3. Запускаем сервер с исправлениями...
cd neopazdivay
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo ========================================
echo ГОТОВО! Регистрация исправлена!
echo ========================================
echo.
echo Исправления:
echo - Исправлено поле password_hash в регистрации
echo - Исправлена проверка пароля при входе
echo.
echo Теперь регистрация должна работать!
echo.
pause

