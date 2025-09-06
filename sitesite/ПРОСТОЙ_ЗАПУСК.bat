@echo off
echo Запуск сайта...
cd neopazdivay
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause

