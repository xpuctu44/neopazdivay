#!/usr/bin/env python3
"""
Скрипт для проверки содержимого базы данных
"""

import sqlite3
import os

def check_database():
    db_path = "neopazdivay/time_tracker.db"
    
    if not os.path.exists(db_path):
        print("❌ База данных не найдена!")
        return
    
    print("✅ База данных найдена!")
    print(f"📁 Путь: {db_path}")
    print(f"📊 Размер: {os.path.getsize(db_path)} байт")
    print()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверяем таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("📋 Таблицы в базе данных:")
        for table in tables:
            print(f"  - {table[0]}")
        print()
        
        # Проверяем пользователей
        if ('users',) in tables:
            cursor.execute("SELECT id, email, full_name, role, is_active, created_at FROM users;")
            users = cursor.fetchall()
            
            print("👥 Пользователи в базе данных:")
            if users:
                for user in users:
                    user_id, email, full_name, role, is_active, created_at = user
                    status = "✅ Активен" if is_active else "❌ Неактивен"
                    print(f"  ID: {user_id}")
                    print(f"  Email: {email}")
                    print(f"  Имя: {full_name}")
                    print(f"  Роль: {role}")
                    print(f"  Статус: {status}")
                    print(f"  Создан: {created_at}")
                    print("  " + "-" * 40)
            else:
                print("  ❌ Пользователи не найдены!")
        
        # Проверяем магазины
        if ('stores',) in tables:
            cursor.execute("SELECT id, name, address, phone FROM stores;")
            stores = cursor.fetchall()
            
            print("\n🏪 Магазины в базе данных:")
            if stores:
                for store in stores:
                    store_id, name, address, phone = store
                    print(f"  ID: {store_id}")
                    print(f"  Название: {name}")
                    print(f"  Адрес: {address}")
                    print(f"  Телефон: {phone}")
                    print("  " + "-" * 40)
            else:
                print("  ❌ Магазины не найдены!")
        
        # Проверяем посещения
        if ('attendances',) in tables:
            cursor.execute("SELECT COUNT(*) FROM attendances;")
            attendance_count = cursor.fetchone()[0]
            print(f"\n⏰ Записей о посещениях: {attendance_count}")
        
        # Проверяем график
        if ('schedule_entries',) in tables:
            cursor.execute("SELECT COUNT(*) FROM schedule_entries;")
            schedule_count = cursor.fetchone()[0]
            print(f"📅 Записей в графике: {schedule_count}")
        
        conn.close()
        print("\n✅ Проверка завершена успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при проверке базы данных: {e}")

if __name__ == "__main__":
    check_database()

