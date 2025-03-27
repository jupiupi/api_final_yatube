import requests

def test_jwt():
    """Тестирование получения и использования JWT-токенов."""
    
    print("\nПолучение токена:")
    url = "http://127.0.0.1:8000/api/v1/jwt/create/"
    data = {
        "username": "regular_user",
        "password": "iWannaBeAdmin"
    }
    
    response = requests.post(url, json=data)
    print(f"Статус: {response.status_code}")
    
    if response.status_code == 200:
        tokens = response.json()
        print("Токены получены:")
        print(f"Access token: {tokens.get('access')}")
        print(f"Refresh token: {tokens.get('refresh')}")
        
        # Проверка токена
        print("\nПроверка токена:")
        url = "http://127.0.0.1:8000/api/v1/jwt/verify/"
        data = {"token": tokens.get('access')}
        
        response = requests.post(url, json=data)
        print(f"Статус: {response.status_code}")
        
        # Обновление токена
        print("\nОбновление токена:")
        url = "http://127.0.0.1:8000/api/v1/jwt/refresh/"
        data = {"refresh": tokens.get('refresh')}
        
        response = requests.post(url, json=data)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            print(f"Новый access token: {response.json().get('access')}")
            
        # Проверка доступа к защищенному эндпоинту
        print("\nДоступ к защищенному эндпоинту (follow):")
        url = "http://127.0.0.1:8000/api/v1/follow/"
        headers = {"Authorization": f"Bearer {tokens.get('access')}"}
        
        response = requests.get(url, headers=headers)
        print(f"Статус: {response.status_code}")
        print(f"Данные: {response.json()}")
        
    else:
        print(f"Ошибка: {response.json()}")

if __name__ == "__main__":
    test_jwt() 