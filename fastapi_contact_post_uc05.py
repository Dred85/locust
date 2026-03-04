def submit_contact_form(user):
    """
    UC05: Тест производительности отправки контактной формы (POST)
    
    Проверки:
    - Статус код = 200
    - Время ответа < 1000ms (POST может быть медленнее из-за обработки)
    - Успешный ответ или сообщение об ошибке
    """
    # Тестовые данные для формы
    form_data = {
        "name": "Locust Test User",
        "email": "locust@test.com",
        "message": "Performance test message from Locust"
    }
    
    with user.client.post("/contact", data=form_data, catch_response=True) as response:
        # Проверка статус кода
        if response.status_code != 200:
            response.failure(f"Ожидался статус 200, получен {response.status_code}")
        
        # Проверка времени ответа (POST может быть медленнее)
        elif response.elapsed.total_seconds() > 1.0:
            response.failure(f"Слишком медленный ответ: {response.elapsed.total_seconds():.3f}s (ожидалось < 1.0s)")
        
        # Проверка что форма обработана (есть сообщение о результате)
        elif "успешно" not in response.text.lower() and "ошибка" not in response.text.lower() and "тестовый" not in response.text.lower():
            response.failure("Не найдено сообщение о результате обработки формы")
        
        else:
            response.success()


def submit_contact_api(user):
    """
    UC05_API: Тест производительности JSON API контактов (POST /api/contact)
    
    Проверки:
    - Статус код = 200
    - Время ответа < 1000ms
    - JSON ответ с полями status и message
    """
    # Тестовые данные для JSON API
    json_data = {
        "name": "Locust API Test",
        "email": "api@test.com",
        "message": "API performance test"
    }
    
    with user.client.post("/api/contact", json=json_data, catch_response=True) as response:
        # Проверка статус кода
        if response.status_code != 200:
            response.failure(f"Ожидался статус 200, получен {response.status_code}")
        
        # Проверка времени ответа
        elif response.elapsed.total_seconds() > 1.0:
            response.failure(f"Слишком медленный ответ: {response.elapsed.total_seconds():.3f}s")
        
        # Проверка JSON структуры
        else:
            try:
                data = response.json()
                if "status" not in data or "message" not in data:
                    response.failure("Отсутствуют обязательные поля в JSON ответе")
                elif data["status"] not in ["success", "error"]:
                    response.failure(f"Неправильное значение status: {data['status']}")
                else:
                    response.success()
            except Exception as e:
                response.failure(f"Ошибка парсинга JSON: {e}")
