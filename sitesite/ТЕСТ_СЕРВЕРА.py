#!/usr/bin/env python3
"""
Скрипт для тестирования и диагностики сервера Time Tracker
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def test_python():
    """Проверяет Python"""
    print("🐍 Проверяем Python...")
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✅ Python: {result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"❌ Python не найден: {e}")
        return False

def test_dependencies():
    """Проверяет зависимости"""
    print("\n📦 Проверяем зависимости...")
    required_packages = [
        "fastapi",
        "uvicorn", 
        "jinja2",
        "sqlalchemy",
        "pydantic",
        "passlib"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - не установлен")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Отсутствуют пакеты: {', '.join(missing)}")
        print("Установите их командой:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    return True

def test_project_structure():
    """Проверяет структуру проекта"""
    print("\n📁 Проверяем структуру проекта...")
    
    required_files = [
        "neopazdivay/app/main.py",
        "neopazdivay/app/database.py",
        "neopazdivay/app/models.py",
        "neopazdivay/app/security.py",
        "neopazdivay/app/routers/__init__.py",
        "neopazdivay/app/routers/health.py",
        "neopazdivay/app/routers/auth.py",
        "neopazdivay/app/routers/attendance.py",
        "neopazdivay/app/static/css/styles.css",
        "neopazdivay/app/templates/base.html",
        "neopazdivay/requirements.txt"
    ]
    
    missing = []
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - не найден")
            missing.append(file_path)
    
    if missing:
        print(f"\n⚠️  Отсутствуют файлы: {len(missing)}")
        return False
    
    return True

def test_server_startup():
    """Проверяет запуск сервера"""
    print("\n🚀 Тестируем запуск сервера...")
    
    try:
        # Переходим в папку проекта
        os.chdir("neopazdivay")
        
        # Пытаемся импортировать приложение
        sys.path.insert(0, ".")
        from app.main import app
        print("✅ Приложение импортировано успешно")
        
        # Проверяем, что приложение создано
        if app:
            print("✅ FastAPI приложение создано")
            return True
        else:
            print("❌ FastAPI приложение не создано")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при импорте приложения: {e}")
        return False

def test_port_availability():
    """Проверяет доступность порта"""
    print("\n🔌 Проверяем доступность порта 8000...")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            print("✅ Порт 8000 занят (сервер уже запущен)")
            return True
        else:
            print(f"⚠️  Порт 8000 отвечает, но статус: {response.status_code}")
            return True
    except requests.exceptions.ConnectionError:
        print("✅ Порт 8000 свободен")
        return True
    except Exception as e:
        print(f"❌ Ошибка проверки порта: {e}")
        return False

def main():
    print("=" * 60)
    print("    ДИАГНОСТИКА СЕРВЕРА TIME TRACKER")
    print("=" * 60)
    
    tests = [
        ("Python", test_python),
        ("Зависимости", test_dependencies),
        ("Структура проекта", test_project_structure),
        ("Запуск приложения", test_server_startup),
        ("Порт", test_port_availability)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Ошибка в тесте {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("    РЕЗУЛЬТАТЫ ДИАГНОСТИКИ")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ ПРОЙДЕН" if result else "❌ ПРОВАЛЕН"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("Сервер должен запускаться без проблем.")
        print("\nПопробуйте запустить:")
        print("ЗАПУСК_САЙТА.bat")
    else:
        print("❌ ЕСТЬ ПРОБЛЕМЫ!")
        print("Исправьте ошибки выше и попробуйте снова.")
    
    print("\nНажмите Enter для выхода...")
    input()

if __name__ == "__main__":
    main()


