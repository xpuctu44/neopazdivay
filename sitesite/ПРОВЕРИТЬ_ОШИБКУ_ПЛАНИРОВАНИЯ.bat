@echo off
echo ========================================
echo ДИАГНОСТИКА ОШИБКИ ПЛАНИРОВАНИЯ
echo ========================================

echo.
echo 1. Проверяем статус сервера...
netstat -aon | findstr :8000
if %errorlevel% neq 0 (
    echo Сервер не запущен!
    echo Запускаем сервер...
    cd neopazdivay
    start python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    timeout /t 5
    echo Сервер запущен, проверяем снова...
    netstat -aon | findstr :8000
)

echo.
echo 2. Проверяем файлы...
if exist "neopazdivay\app\routers\admin.py" (
    echo admin.py - OK
) else (
    echo admin.py - ОТСУТСТВУЕТ!
)

if exist "neopazdivay\app\templates\admin.html" (
    echo admin.html - OK
) else (
    echo admin.html - ОТСУТСТВУЕТ!
)

if exist "neopazdivay\app\models.py" (
    echo models.py - OK
) else (
    echo models.py - ОТСУТСТВУЕТ!
)

echo.
echo 3. Проверяем базу данных...
if exist "neopazdivay\time_tracker.db" (
    echo База данных - OK
) else (
    echo База данных - ОТСУТСТВУЕТ!
)

echo.
echo 4. Проверяем структуру базы данных...
cd neopazdivay
python -c "
from app.database import engine
from app.models import Base
try:
    Base.metadata.create_all(bind=engine)
    print('Структура базы данных - OK')
except Exception as e:
    print(f'Ошибка структуры базы: {e}')
"

echo.
echo 5. Проверяем импорты...
python -c "
try:
    from app.routers.admin import router
    print('Импорт admin.py - OK')
except Exception as e:
    print(f'Ошибка импорта admin.py: {e}')

try:
    from app.models import User, ScheduleEntry
    print('Импорт models.py - OK')
except Exception as e:
    print(f'Ошибка импорта models.py: {e}')
"

echo.
echo ========================================
echo ДИАГНОСТИКА ЗАВЕРШЕНА
echo ========================================
echo.
echo Если есть ошибки, исправьте их и перезапустите сервер.
echo.
pause

