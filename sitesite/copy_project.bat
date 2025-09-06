@echo off
echo Копирование проекта Time Tracker в папку sitesite...

echo Создаем структуру папок...
mkdir neopazdivay\app\routers 2>nul
mkdir neopazdivay\app\static\css 2>nul
mkdir neopazdivay\app\templates 2>nul

echo Копируем основные файлы...
copy "..\neopazdivay\app\*.py" "neopazdivay\app\" /Y
copy "..\neopazdivay\app\routers\*.py" "neopazdivay\app\routers\" /Y
copy "..\neopazdivay\app\static\css\*.css" "neopazdivay\app\static\css\" /Y
copy "..\neopazdivay\app\templates\*.html" "neopazdivay\app\templates\" /Y

echo Копируем вспомогательные файлы...
copy "..\start_time_tracker.bat" "." /Y
copy "..\ЗАПУСК_САЙТА.bat" "." /Y
copy "..\ОТКРЫТЬ_САЙТ.html" "." /Y
copy "..\CHECK_STATUS.html" "." /Y
copy "..\TROUBLESHOOTING.md" "." /Y
copy "..\DEVELOPER_README.md" "." /Y

echo Готово! Проект скопирован в папку sitesite.
echo Теперь вы можете работать в этой папке.
pause


