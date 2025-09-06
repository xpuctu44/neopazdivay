@echo off
echo ========================================
echo ПРОВЕРКА РАБОТЫ САЙТА
echo ========================================

echo.
echo 1. Проверяем доступность сайта...
curl -s -o nul -w "HTTP Status: %%{http_code}\n" http://localhost:8000/
if %errorlevel% neq 0 (
    echo curl не работает, пробуем PowerShell...
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/' -TimeoutSec 5; Write-Host 'HTTP Status:' $response.StatusCode } catch { Write-Host 'Ошибка:' $_.Exception.Message }"
)

echo.
echo 2. Проверяем админ панель...
curl -s -o nul -w "HTTP Status: %%{http_code}\n" http://localhost:8000/admin
if %errorlevel% neq 0 (
    echo curl не работает, пробуем PowerShell...
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/admin' -TimeoutSec 5; Write-Host 'HTTP Status:' $response.StatusCode } catch { Write-Host 'Ошибка:' $_.Exception.Message }"
)

echo.
echo 3. Проверяем планирование...
curl -s -o nul -w "HTTP Status: %%{http_code}\n" http://localhost:8000/admin/planning
if %errorlevel% neq 0 (
    echo curl не работает, пробуем PowerShell...
    powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:8000/admin/planning' -TimeoutSec 5; Write-Host 'HTTP Status:' $response.StatusCode } catch { Write-Host 'Ошибка:' $_.Exception.Message }"
)

echo.
echo ========================================
echo ПРОВЕРКА ЗАВЕРШЕНА
echo ========================================
echo.
echo Если все статусы 200 - сайт работает!
echo Если есть ошибки - покажите их мне.
echo.
pause


