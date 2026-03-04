def check_metrics(user):
    """
    UC06: Тест производительности эндпоинта метрик Prometheus
    
    Проверки:
    - Статус код = 200
    - Время ответа < 200ms (метрики должны быть быстрыми)
    - Наличие метрик в формате Prometheus
    """
    with user.client.get("/metrics", catch_response=True) as response:
        # Проверка статус кода
        if response.status_code != 200:
            response.failure(f"Ожидался статус 200, получен {response.status_code}")
        
        # Проверка времени ответа (метрики должны быть очень быстрыми)
        elif response.elapsed.total_seconds() > 0.2:
            response.failure(f"Слишком медленный ответ для метрик: {response.elapsed.total_seconds():.3f}s (ожидалось < 0.2s)")
        
        # Проверка формата Prometheus
        elif "# HELP" not in response.text and "# TYPE" not in response.text:
            response.failure("Не найден формат метрик Prometheus")
        
        # Проверка наличия метрик
        elif len(response.content) < 50:
            response.failure(f"Слишком мало метрик: {len(response.content)} байт")
        
        else:
            response.success()
