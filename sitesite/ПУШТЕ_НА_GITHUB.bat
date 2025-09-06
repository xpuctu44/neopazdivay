@echo off
chcp 65001 >nul
echo ========================================
echo ОТПРАВКА ИЗМЕНЕНИЙ НА GITHUB
echo ========================================
echo.

cd /d "%~dp0"

echo [1/6] Проверяем статус git репозитория...
git status 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Git репозиторий не найден!
    echo Инициализируем новый репозиторий...
    git init
    echo ✅ Git репозиторий инициализирован
)

echo.
echo [2/6] Добавляем все файлы в индекс...
git add .
if %errorlevel% neq 0 (
    echo ❌ Ошибка при добавлении файлов!
    pause
    exit /b 1
)
echo ✅ Все файлы добавлены в индекс

echo.
echo [3/6] Создаем коммит...
set commit_msg="Update: Added restore scripts and improvements - %date% %time%"
git commit -m %commit_msg%
if %errorlevel% neq 0 (
    echo ⚠️  Нет изменений для коммита или ошибка коммита
    echo Проверяем статус...
    git status
)

echo.
echo [4/6] Проверяем удаленный репозиторий...
git remote -v 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Удаленный репозиторий не настроен!
    echo.
    echo Пожалуйста, добавьте удаленный репозиторий:
    echo git remote add origin https://github.com/ваш-username/ваш-репозиторий.git
    echo.
    echo Или укажите URL вашего GitHub репозитория:
    set /p repo_url="Введите URL репозитория: "
    if not "!repo_url!"=="" (
        git remote add origin !repo_url!
        echo ✅ Удаленный репозиторий добавлен
    ) else (
        echo ❌ URL не указан, выход
        pause
        exit /b 1
    )
)

echo.
echo [5/6] Получаем последние изменения с сервера...
git pull origin main --rebase 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Ветка main не найдена, попробуем master...
    git pull origin master --rebase 2>nul
    if %errorlevel% neq 0 (
        echo ⚠️  Не удалось получить изменения, продолжаем без pull
    )
)

echo.
echo [6/6] Отправляем изменения на GitHub...
git push origin main 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  Ошибка при пуше в main, попробуем master...
    git push origin master 2>nul
    if %errorlevel% neq 0 (
        echo ⚠️  Попробуем установить upstream и запушить...
        git push -u origin main 2>nul
        if %errorlevel% neq 0 (
            git push -u origin master 2>nul
            if %errorlevel% neq 0 (
                echo ❌ Не удалось отправить изменения!
                echo.
                echo Возможные причины:
                echo - Неправильный URL репозитория
                echo - Нет прав доступа
                echo - Проблемы с аутентификацией
                echo.
                echo Попробуйте выполнить команды вручную:
                echo git remote -v
                echo git push origin main
                echo.
                pause
                exit /b 1
            )
        )
    )
)

echo.
echo ========================================
echo ✅ ИЗМЕНЕНИЯ УСПЕШНО ОТПРАВЛЕНЫ!
echo ========================================
echo.
echo Отправленные файлы:
echo - ВОССТАНОВИТЬ_ПОСЛЕДНЮЮ_РАБОЧУЮ_ВЕРСИЮ.bat
echo - БЫСТРОЕ_ВОССТАНОВЛЕНИЕ.bat  
echo - СОЗДАТЬ_РЕЗЕРВНУЮ_КОПИЮ.bat
echo - Все остальные изменения проекта
echo.
echo 🌐 Проверьте ваш репозиторий на GitHub!
echo.
pause
