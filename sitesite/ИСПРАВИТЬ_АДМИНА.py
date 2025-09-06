#!/usr/bin/env python3
"""
Скрипт для проверки и исправления аккаунта администратора
"""

import sqlite3
import os
from datetime import datetime

def fix_admin_account():
    db_path = "neopazdivay/time_tracker.db"
    
    if not os.path.exists(db_path):
        print("❌ База данных не найдена!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Проверяем всех пользователей
        cursor.execute("SELECT id, email, full_name, role, is_active, created_at FROM users;")
        users = cursor.fetchall()
        
        print("👥 Все пользователи в базе данных:")
        admin_found = False
        
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
            
            if role == "admin":
                admin_found = True
                if not is_active:
                    print(f"🔧 Исправляем статус администратора {email}...")
                    cursor.execute("UPDATE users SET is_active = 1 WHERE id = ?", (user_id,))
                    conn.commit()
                    print(f"✅ Администратор {email} теперь активен!")
        
        if not admin_found:
            print("❌ Администраторы не найдены!")
            print("💡 Создаем тестового администратора...")
            
            # Создаем тестового администратора
            test_email = "admin@test.com"
            test_password = "admin123"  # В реальном приложении должен быть хеш
            test_name = "Администратор"
            
            cursor.execute("""
                INSERT INTO users (email, password_hash, full_name, role, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (test_email, test_password, test_name, "admin", True, datetime.now().isoformat()))
            
            conn.commit()
            print(f"✅ Создан тестовый администратор: {test_email} / {test_password}")
        
        # Проверяем результат
        cursor.execute("SELECT id, email, full_name, role, is_active FROM users WHERE role = 'admin';")
        admins = cursor.fetchall()
        
        print("\n👑 Администраторы после исправления:")
        for admin in admins:
            user_id, email, full_name, role, is_active = admin
            status = "✅ Активен" if is_active else "❌ Неактивен"
            print(f"  {email} - {status}")
        
        conn.close()
        print("\n✅ Проверка и исправление завершены!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    fix_admin_account()

