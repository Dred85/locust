"""
Профиль нагрузки Locust для поиска максимальной производительности
Stress Test - постепенное увеличение нагрузки до точки отказа

⚠️  ВАЖНО: Установите DISABLE_EMAIL=true в .env файле!
   Иначе POST тесты (UC05) будут отправлять реальные email

Длительность: 60 минут (3600 секунд)
Этапов: 10 ступеней по 6 минут
Цель: Найти максимальное количество пользователей, которое система может обработать

Запуск:
  locust -f loadshape_maxperf.py --host=http://localhost:8000 --web-port 8090
"""
from locust import LoadTestShape, events

from locustfile import (
    WebUser_UC01,      # GET / - главная
    WebUser_UC02,      # GET /contact - страница формы
    WebUser_UC03,      # GET /about - о нас
    WebUser_UC04,      # GET /projects - проекты
    WebUser_UC05,      # POST /contact - отправка формы
    WebUser_UC05_API,  # POST /api/contact - JSON API
    WebUser_UC06       # GET /metrics - метрики Prometheus
)

# -----------------
# PROMETHEUS EXPORTER FOR LOCUST
# -----------------
try:
    from flask import Response
    from prometheus_client import (
        CollectorRegistry,
        Gauge,
        CONTENT_TYPE_LATEST,
        generate_latest,
    )

    _registry = CollectorRegistry()
    _locust_users_gauge = Gauge(
        "locust_users",
        "Number of running Locust users",
        registry=_registry,
    )

    @events.init.add_listener
    def _locust_init_prometheus(environment, **_kwargs):
        """
        Регистрируем /metrics на веб-приложении Locust и
        экспортируем текущий user_count.
        """
        if not environment.web_ui:
            return

        @environment.web_ui.app.route("/metrics")
        def metrics():  # type: ignore[func-name-mismatch]
            runner = environment.runner
            if runner is not None:
                user_count = getattr(runner, "user_count", None)
                if user_count is None:
                    user_count = len(getattr(runner, "user_instances", []))
            else:
                user_count = 0

            _locust_users_gauge.set(user_count)
            return Response(generate_latest(_registry), mimetype=CONTENT_TYPE_LATEST)

except ModuleNotFoundError:
    pass


class LoadShapeMaxPerf(LoadTestShape):
    """
    Stress Test для поиска максимальной производительности
    
    10 ступеней постепенного увеличения нагрузки:
    1. 0-6 мин: 10 пользователей (прогрев и baseline)
    2. 6-12 мин: 25 пользователей
    3. 12-18 мин: 50 пользователей
    4. 18-24 мин: 100 пользователей
    5. 24-30 мин: 200 пользователей
    6. 30-36 мин: 400 пользователей
    7. 36-42 мин: 600 пользователей
    8. 42-48 мин: 800 пользователей
    9. 48-54 мин: 1000 пользователей
    10. 54-60 мин: 1200 пользователей
    
    Критерии анализа:
    - Время ответа < 500ms для GET (норма)
    - Время ответа < 1000ms для POST (норма)
    - Response time 95th percentile
    - Количество ошибок (failures)
    - RPS (requests per second)
    """
    stages = [
        # Этап 1: 10 пользователей (0-6 мин = 0-360 сек)
        {"duration": 360, "users": 10, "spawn_rate": 2, "user_classes": [WebUser_UC01, WebUser_UC03, WebUser_UC04, WebUser_UC06]},
        
        # Этап 2: 25 пользователей (6-12 мин = 360-720 сек)
        {"duration": 720, "users": 25, "spawn_rate": 2, "user_classes": [WebUser_UC01, WebUser_UC02, WebUser_UC03, WebUser_UC04, WebUser_UC06]},
        
        # Этап 3: 50 пользователей (12-18 мин = 720-1080 сек)
        {"duration": 1080, "users": 50, "spawn_rate": 3, "user_classes": [WebUser_UC01, WebUser_UC02, WebUser_UC03, WebUser_UC04, WebUser_UC06]},
        
        # Этап 4: 100 пользователей (18-24 мин = 1080-1440 сек)
        {"duration": 1440, "users": 100, "spawn_rate": 5, "user_classes": [WebUser_UC01, WebUser_UC02, WebUser_UC03, WebUser_UC04, WebUser_UC06]},
        
        # Этап 5: 200 пользователей (24-30 мин = 1440-1800 сек)
        {"duration": 1800, "users": 200, "spawn_rate": 5, "user_classes": [WebUser_UC01, WebUser_UC02, WebUser_UC03, WebUser_UC04, WebUser_UC06]},
        
        # Этап 6: 400 пользователей (30-36 мин = 1800-2160 сек)
        {"duration": 2160, "users": 400, "spawn_rate": 10, "user_classes": [WebUser_UC01, WebUser_UC02, WebUser_UC03, WebUser_UC04, WebUser_UC06]},
        
        # Этап 7: 600 пользователей (36-42 мин = 2160-2520 сек)
        {"duration": 2520, "users": 600, "spawn_rate": 10, "user_classes": [WebUser_UC01, WebUser_UC03, WebUser_UC04, WebUser_UC06]},
        
        # Этап 8: 800 пользователей (42-48 мин = 2520-2880 сек)
        {"duration": 2880, "users": 800, "spawn_rate": 10, "user_classes": [WebUser_UC01, WebUser_UC03, WebUser_UC04, WebUser_UC06]},
        
        # Этап 9: 1000 пользователей (48-54 мин = 2880-3240 сек)
        {"duration": 3240, "users": 1000, "spawn_rate": 15, "user_classes": [WebUser_UC01, WebUser_UC03, WebUser_UC06]},
        
        # Этап 10: 1200 пользователей (54-60 мин = 3240-3600 сек)
        {"duration": 3600, "users": 1200, "spawn_rate": 20, "user_classes": [WebUser_UC01, WebUser_UC03, WebUser_UC06]}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"], stage["user_classes"])
                return tick_data

        return None
