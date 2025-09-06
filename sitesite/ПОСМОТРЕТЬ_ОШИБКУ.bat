@echo off
echo ========================================
echo ПРОСМОТР ПОДРОБНОЙ ОШИБКИ
echo ========================================

echo.
echo Запускаем сервер с максимально подробными логами...
echo Для остановки нажмите Ctrl+C
echo.

cd neopazdivay
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level trace

pause