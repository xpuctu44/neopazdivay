@echo off
echo Запускаем сервер на порту 8001 с подробными логами...
cd neopazdivay
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload --log-level debug

pause


