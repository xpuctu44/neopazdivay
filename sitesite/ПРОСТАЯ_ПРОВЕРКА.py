#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("=== ПРОСТАЯ ПРОВЕРКА ===")
print()

try:
    print("1. Проверяем Python...")
    import sys
    print(f"   Python версия: {sys.version}")
    print("   ✅ Python работает")
except Exception as e:
    print(f"   ❌ Ошибка Python: {e}")
    exit(1)

try:
    print("2. Проверяем импорт datetime...")
    from datetime import date, datetime
    print("   ✅ datetime импортирован")
except Exception as e:
    print(f"   ❌ Ошибка datetime: {e}")
    exit(1)

try:
    print("3. Проверяем импорт FastAPI...")
    from fastapi import FastAPI
    print("   ✅ FastAPI импортирован")
except Exception as e:
    print(f"   ❌ Ошибка FastAPI: {e}")
    exit(1)

try:
    print("4. Проверяем импорт SQLAlchemy...")
    from sqlalchemy import create_engine
    print("   ✅ SQLAlchemy импортирован")
except Exception as e:
    print(f"   ❌ Ошибка SQLAlchemy: {e}")
    exit(1)

try:
    print("5. Проверяем файлы проекта...")
    import os
    if os.path.exists("app"):
        print("   ✅ Папка app существует")
    else:
        print("   ❌ Папка app не найдена")
        
    if os.path.exists("app/main.py"):
        print("   ✅ app/main.py существует")
    else:
        print("   ❌ app/main.py не найден")
        
    if os.path.exists("app/models.py"):
        print("   ✅ app/models.py существует")
    else:
        print("   ❌ app/models.py не найден")
        
    if os.path.exists("app/database.py"):
        print("   ✅ app/database.py существует")
    else:
        print("   ❌ app/database.py не найден")
        
except Exception as e:
    print(f"   ❌ Ошибка проверки файлов: {e}")

try:
    print("6. Проверяем импорт app...")
    from app.database import engine
    print("   ✅ app.database импортирован")
except Exception as e:
    print(f"   ❌ Ошибка app.database: {e}")

try:
    print("7. Проверяем импорт models...")
    from app.models import User
    print("   ✅ app.models импортирован")
except Exception as e:
    print(f"   ❌ Ошибка app.models: {e}")

print()
print("=== ПРОВЕРКА ЗАВЕРШЕНА ===")

