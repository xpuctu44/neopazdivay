@echo off
echo ========================================
echo ПРОСМОТР ЛОГОВ СЕРВЕРА
echo ========================================

echo.
echo ВНИМАНИЕ: Этот скрипт покажет логи сервера.
echo Если сервер не запущен, запустите его сначала.
echo.

echo Нажмите любую клавишу для продолжения...
pause >nul

echo.
echo Запускаем сервер с подробными логами...
echo Для остановки нажмите Ctrl+C
echo.

cd neopazdivay
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug

pause


