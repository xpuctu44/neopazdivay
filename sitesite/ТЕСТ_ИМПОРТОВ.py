#!/usr/bin/env python3
"""
Тест импортов для проверки работоспособности приложения
"""

import sys
import os

# Добавляем путь к приложению
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'neopazdivay'))

def test_imports():
    print("Тестируем импорты...")
    
    try:
        print("1. Тестируем database...")
        from app.database import engine, Base, get_db
        print("   ✅ database импортирован")
        
        print("2. Тестируем models...")
        from app import models
        print("   ✅ models импортированы")
        
        print("3. Тестируем main...")
        from app.main import app
        print("   ✅ main импортирован")
        
        print("4. Тестируем routers...")
        from app.routers import health, auth, attendance, admin
        print("   ✅ routers импортированы")
        
        print("5. Тестируем создание таблиц...")
        Base.metadata.create_all(bind=engine)
        print("   ✅ Таблицы созданы")
        
        print("\n🎉 Все импорты работают!")
        return True
        
    except Exception as e:
        print(f"\n❌ Ошибка импорта: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    if not success:
        sys.exit(1)


