import requests
import sys

def test_server():
    try:
        # Тестируем главную страницу
        response = requests.get("http://localhost:8001/", timeout=5)
        print(f"Главная страница: {response.status_code}")
        
        # Тестируем админ панель
        response = requests.get("http://localhost:8001/admin", timeout=5)
        print(f"Админ панель: {response.status_code}")
        
        # Тестируем планирование
        response = requests.get("http://localhost:8001/admin/planning", timeout=5)
        print(f"Планирование: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Сервер работает!")
        else:
            print("❌ Есть ошибки!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Сервер не запущен на порту 8001")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_server()


