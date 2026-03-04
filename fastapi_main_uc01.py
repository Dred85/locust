def open_index(user):
    """
    UC01: Тест производительности главной страницы
    
    Проверки:
    - Статус код = 200
    - Время ответа < 500ms
    - Размер контента > 1000 байт
    """
    with user.client.get("/", catch_response=True) as response:
        # Проверка статус кода
        if response.status_code != 200:
            response.failure(f"Ожидался статус 200, получен {response.status_code}")
        
        # Проверка времени ответа (должно быть < 500ms для главной)
        elif response.elapsed.total_seconds() > 0.5:
            response.failure(f"Слишком медленный ответ: {response.elapsed.total_seconds():.3f}s (ожидалось < 0.5s)")
        
        # Проверка наличия контента
        elif len(response.content) < 1000:
            response.failure(f"Слишком маленький контент: {len(response.content)} байт")
        
        # Проверка что это HTML
        elif "text/html" not in response.headers.get("content-type", ""):
            response.failure(f"Неправильный content-type: {response.headers.get('content-type')}")
        
        else:
            response.success()
