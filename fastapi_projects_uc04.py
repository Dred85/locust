def open_projects(user):
    """
    UC04: Тест производительности страницы проектов
    
    Проверки:
    - Статус код = 200
    - Время ответа < 500ms
    - Наличие контента
    """
    with user.client.get("/projects", catch_response=True) as response:
        # Проверка статус кода
        if response.status_code != 200:
            response.failure(f"Ожидался статус 200, получен {response.status_code}")
        
        # Проверка времени ответа
        elif response.elapsed.total_seconds() > 0.5:
            response.failure(f"Слишком медленный ответ: {response.elapsed.total_seconds():.3f}s")
        
        # Проверка наличия контента
        elif len(response.content) < 500:
            response.failure(f"Слишком маленький контент: {len(response.content)} байт")
        
        # Проверка что это HTML
        elif "text/html" not in response.headers.get("content-type", ""):
            response.failure(f"Неправильный content-type: {response.headers.get('content-type')}")
        
        else:
            response.success()