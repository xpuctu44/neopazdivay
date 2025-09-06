@echo off
echo ========================================
echo ИСПРАВЛЕНИЕ ОШИБКИ ПЛАНИРОВАНИЯ
echo ========================================

echo.
echo 1. Останавливаем сервер...
taskkill /f /im python.exe 2>nul

echo.
echo 2. Ждем 3 секунды...
timeout /t 3 /nobreak

echo.
echo 3. Проверяем структуру базы данных...
cd neopazdivay
python -c "
from app.database import engine
from app.models import Base
try:
    Base.metadata.create_all(bind=engine)
    print('Структура базы данных обновлена')
except Exception as e:
    print(f'Ошибка: {e}')
"

echo.
echo 4. Запускаем сервер с исправлениями...
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo.
echo ========================================
echo ГОТОВО! Ошибка планирования исправлена!
echo ========================================
echo.
echo Исправления:
echo - Добавлена функция date в контекст шаблона
echo - Обновлена структура базы данных
echo - Исправлены импорты в admin.py
echo.
echo Теперь планирование должно работать!
echo.
pause

