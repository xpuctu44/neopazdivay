#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("=== ПРОСТАЯ ПРОВЕРКА ПЛАНИРОВАНИЯ ===")
print()

try:
    print("1. Проверяем импорт datetime...")
    from datetime import date, datetime
    print("   ✅ datetime импортирован")
except Exception as e:
    print(f"   ❌ Ошибка datetime: {e}")
    exit(1)

try:
    print("2. Проверяем импорт FastAPI...")
    from fastapi import FastAPI, Request
    print("   ✅ FastAPI импортирован")
except Exception as e:
    print(f"   ❌ Ошибка FastAPI: {e}")
    exit(1)

try:
    print("3. Проверяем импорт SQLAlchemy...")
    from sqlalchemy.orm import Session
    print("   ✅ SQLAlchemy импортирован")
except Exception as e:
    print(f"   ❌ Ошибка SQLAlchemy: {e}")
    exit(1)

try:
    print("4. Проверяем импорт app.database...")
    from app.database import get_db, engine
    print("   ✅ app.database импортирован")
except Exception as e:
    print(f"   ❌ Ошибка app.database: {e}")
    exit(1)

try:
    print("5. Проверяем импорт app.models...")
    from app.models import User, ScheduleEntry, Store
    print("   ✅ app.models импортирован")
except Exception as e:
    print(f"   ❌ Ошибка app.models: {e}")
    exit(1)

try:
    print("6. Проверяем импорт app.routers.admin...")
    from app.routers.admin import admin_planning
    print("   ✅ app.routers.admin импортирован")
except Exception as e:
    print(f"   ❌ Ошибка app.routers.admin: {e}")
    exit(1)

try:
    print("7. Проверяем базу данных...")
    from app.database import Base
    Base.metadata.create_all(bind=engine)
    print("   ✅ База данных создана")
except Exception as e:
    print(f"   ❌ Ошибка базы данных: {e}")
    exit(1)

try:
    print("8. Проверяем подключение к БД...")
    db = next(get_db())
    print("   ✅ Подключение к БД успешно")
except Exception as e:
    print(f"   ❌ Ошибка подключения к БД: {e}")
    exit(1)

try:
    print("9. Проверяем модели...")
    users = db.query(User).all()
    schedules = db.query(ScheduleEntry).all()
    stores = db.query(Store).all()
    print(f"   ✅ Пользователей: {len(users)}")
    print(f"   ✅ Записей расписания: {len(schedules)}")
    print(f"   ✅ Магазинов: {len(stores)}")
except Exception as e:
    print(f"   ❌ Ошибка запросов к БД: {e}")
    exit(1)

try:
    print("10. Проверяем функцию планирования...")
    from unittest.mock import Mock
    
    mock_request = Mock()
    mock_request.session = {"user_id": 1, "role": "admin"}
    
    result = admin_planning(mock_request, db)
    print("   ✅ Функция планирования работает")
except Exception as e:
    print(f"   ❌ Ошибка функции планирования: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print()
print("=== ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО ===")

