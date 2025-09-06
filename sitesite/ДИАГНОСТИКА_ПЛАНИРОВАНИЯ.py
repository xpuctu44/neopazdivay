#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback
from datetime import date, datetime

print("=== ДИАГНОСТИКА ПЛАНИРОВАНИЯ ===")
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
    print("5. Проверяем структуру ScheduleEntry...")
    if schedules:
        schedule = schedules[0]
        print(f"   ✅ Поля ScheduleEntry:")
        print(f"      - id: {schedule.id}")
        print(f"      - user_id: {schedule.user_id}")
        print(f"      - work_date: {schedule.work_date}")
        print(f"      - shift_type: {schedule.shift_type}")
        print(f"      - published: {schedule.published}")
        print(f"      - created_at: {schedule.created_at}")
    else:
        print("   ⚠️ Нет записей расписания для проверки")
except Exception as e:
    print(f"   ❌ Ошибка структуры ScheduleEntry: {e}")
    traceback.print_exc()

try:
    print("6. Проверяем функцию планирования...")
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
    print("7. Проверяем шаблон...")
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="app/templates")
    
    # Проверяем, что шаблон существует
    import os
    if os.path.exists("app/templates/admin.html"):
        print("   ✅ Шаблон admin.html существует")
        
        # Читаем шаблон и проверяем синтаксис
        with open("app/templates/admin.html", "r", encoding="utf-8") as f:
            content = f.read()
            
        # Проверяем наличие проблемных мест
        if "{{ date(" in content:
            print("   ⚠️ Найдено использование функции date() в шаблоне")
        if "start_time" in content:
            print("   ⚠️ Найдено использование start_time в шаблоне")
        if "end_time" in content:
            print("   ⚠️ Найдено использование end_time в шаблоне")
            
    else:
        print("   ❌ Шаблон admin.html не найден")
        
except Exception as e:
    print(f"   ❌ Ошибка шаблона: {e}")
    traceback.print_exc()

try:
    print("8. Проверяем маршруты...")
    from app.main import app
    routes = [route.path for route in app.routes]
    if "/admin/planning" in routes:
        print("   ✅ Маршрут /admin/planning найден")
    else:
        print("   ❌ Маршрут /admin/planning не найден")
        
except Exception as e:
    print(f"   ❌ Ошибка маршрутов: {e}")
    traceback.print_exc()

print()
print("=== ДИАГНОСТИКА ЗАВЕРШЕНА ===")

