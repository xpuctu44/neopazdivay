#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback
from datetime import date, datetime

print("=== ДИАГНОСТИКА ОШИБКИ ПЛАНИРОВАНИЯ ===")
print()

try:
    print("1. Проверяем импорты...")
    from app.database import get_db, engine
    from app.models import User, ScheduleEntry, Store, Base
    from app.routers.admin import admin_planning
    print("   ✅ Импорты успешны")
except Exception as e:
    print(f"   ❌ Ошибка импорта: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    print("2. Проверяем базу данных...")
    Base.metadata.create_all(bind=engine)
    print("   ✅ База данных создана")
except Exception as e:
    print(f"   ❌ Ошибка базы данных: {e}")
    traceback.print_exc()

try:
    print("3. Проверяем подключение к БД...")
    from sqlalchemy.orm import Session
    db = next(get_db())
    print("   ✅ Подключение к БД успешно")
except Exception as e:
    print(f"   ❌ Ошибка подключения к БД: {e}")
    traceback.print_exc()

try:
    print("4. Проверяем модели...")
    users = db.query(User).all()
    schedules = db.query(ScheduleEntry).all()
    stores = db.query(Store).all()
    print(f"   ✅ Пользователей: {len(users)}")
    print(f"   ✅ Записей расписания: {len(schedules)}")
    print(f"   ✅ Магазинов: {len(stores)}")
except Exception as e:
    print(f"   ❌ Ошибка запросов к БД: {e}")
    traceback.print_exc()

try:
    print("5. Проверяем функцию планирования...")
    from fastapi import Request
    from unittest.mock import Mock
    
    # Создаем мок-объект request
    mock_request = Mock()
    mock_request.session = {"user_id": 1, "role": "admin"}
    
    # Пытаемся вызвать функцию планирования
    result = admin_planning(mock_request, db)
    print("   ✅ Функция планирования работает")
except Exception as e:
    print(f"   ❌ Ошибка функции планирования: {e}")
    traceback.print_exc()

try:
    print("6. Проверяем шаблон...")
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="app/templates")
    
    # Проверяем, что шаблон существует
    import os
    if os.path.exists("app/templates/admin.html"):
        print("   ✅ Шаблон admin.html существует")
    else:
        print("   ❌ Шаблон admin.html не найден")
        
except Exception as e:
    print(f"   ❌ Ошибка шаблона: {e}")
    traceback.print_exc()

print()
print("=== ДИАГНОСТИКА ЗАВЕРШЕНА ===")

