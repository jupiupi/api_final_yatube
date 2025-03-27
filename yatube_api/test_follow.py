"""Тестирование подписок."""
import requests
import json

def test_follow_creation():
    """Тест создания подписки."""
    # Получение токена
    print("\nПолучение токена:")
    url = "http://127.0.0.1:8000/api/v1/jwt/create/"
    data = {
        "username": "second_user",
        "password": "5eCretPaSsw0rD"
    }
    
    response = requests.post(url, json=data)
    print(f"Статус получения токена: {response.status_code}")
    
    if response.status_code == 200:
        token = response.json().get('access')
        
        # Удаление существующей подписки (если есть)
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("http://127.0.0.1:8000/api/v1/follow/", headers=headers)
        follows = response.json()
        for follow in follows:
            if follow.get('following') == 'regular_user':
                print(f"Найдена существующая подписка, пропускаем тест...")
                return
        
        # Создание подписки
        print("\nСоздание подписки:")
        url = "http://127.0.0.1:8000/api/v1/follow/"
        headers = {"Authorization": f"Bearer {token}"}
        data = {"following": "regular_user"}
        
        response = requests.post(url, json=data, headers=headers)
        print(f"Статус создания подписки: {response.status_code}")
        print(f"Ответ: {response.text}")
        
        try:
            response_data = response.json()
            print("\nПроверка полей в ответе:")
            print(f"Поле 'user': {response_data.get('user')}")
            print(f"Поле 'following': {response_data.get('following')}")
        except json.JSONDecodeError:
            print("Не удалось декодировать JSON-ответ")
        
        # Получение списка подписок
        print("\nПолучение списка подписок:")
        url = "http://127.0.0.1:8000/api/v1/follow/"
        
        response = requests.get(url, headers=headers)
        print(f"Статус получения списка: {response.status_code}")
        print(f"Ответ: {response.json()}")
        
    else:
        print(f"Ошибка получения токена: {response.json()}")

def test_anonymous_access():
    """Тест доступа анонимного пользователя."""
    
    # Попытка создания поста
    print("\nПопытка создания поста анонимным пользователем:")
    url = "http://127.0.0.1:8000/api/v1/posts/"
    data = {"text": "Тестовый пост от анонима"}
    
    response = requests.post(url, json=data)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.text}")
    
    # Попытка создания комментария
    print("\nПопытка создания комментария анонимным пользователем:")
    url = "http://127.0.0.1:8000/api/v1/posts/1/comments/"
    data = {"text": "Тестовый комментарий от анонима"}
    
    response = requests.post(url, json=data)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.text}")
    
    # Попытка доступа к подпискам
    print("\nПопытка доступа к подпискам анонимным пользователем:")
    url = "http://127.0.0.1:8000/api/v1/follow/"
    
    response = requests.get(url)
    print(f"Статус: {response.status_code}")
    print(f"Ответ: {response.text}")

if __name__ == "__main__":
    test_follow_creation()
    test_anonymous_access() 