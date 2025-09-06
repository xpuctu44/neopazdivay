print("Тест FastAPI...")

try:
    from fastapi import FastAPI
    print("✅ FastAPI импортирован успешно")
except Exception as e:
    print(f"❌ Ошибка импорта FastAPI: {e}")
    exit(1)

try:
    from fastapi.templating import Jinja2Templates
    print("✅ Jinja2Templates импортирован успешно")
except Exception as e:
    print(f"❌ Ошибка импорта Jinja2Templates: {e}")
    exit(1)

try:
    from sqlalchemy import create_engine
    print("✅ SQLAlchemy импортирован успешно")
except Exception as e:
    print(f"❌ Ошибка импорта SQLAlchemy: {e}")
    exit(1)

try:
    from sqlalchemy.orm import Session
    print("✅ SQLAlchemy Session импортирован успешно")
except Exception as e:
    print(f"❌ Ошибка импорта SQLAlchemy Session: {e}")
    exit(1)

print("✅ Все основные модули импортированы успешно!")

