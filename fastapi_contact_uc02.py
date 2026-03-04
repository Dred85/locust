def open_contact(user):
    """
    UC02: Тест производительности страницы контактов (GET)
    
    Проверки:
    - Статус код = 200
    - Время ответа < 500ms
    - Наличие HTML формы
    """
    with user.client.get("/contact", catch_response=True) as response:
        # Проверка статус кода
        if response.status_code != 200:
            response.failure(f"Ожидался статус 200, получен {response.status_code}")
        
        # Проверка времени ответа
        elif response.elapsed.total_seconds() > 0.5:
            response.failure(f"Слишком медленный ответ: {response.elapsed.total_seconds():.3f}s")
        
        # Проверка наличия формы
        elif "<form" not in response.text:
            response.failure("Форма контактов не найдена на странице")
        
        # Проверка что это HTML
        elif "text/html" not in response.headers.get("content-type", ""):
            response.failure(f"Неправильный content-type: {response.headers.get('content-type')}")
        
        else:
            response.success()
