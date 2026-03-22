"""
Loadshape для быстрого тестирования производительности всех эндпоинтов.

Запуск:
  locust -f locust/loadshape_performance.py --host=http://localhost:8000 --headless --run-time 3m

Или через Docker Compose:
  docker compose up locust_performance
"""
from locust import LoadTestShape, events

from locustfile import (
    WebUser_UC01,      # GET /
    WebUser_UC02,      # GET /contact
    WebUser_UC03,      # GET /about
    WebUser_UC04,      # GET /projects
    WebUser_UC05,      # POST /contact
    WebUser_UC05_API,  # POST /api/contact
    WebUser_UC06       # GET /metrics
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
        """Регистрируем /metrics на веб-приложении Locust"""
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


class LoadShapePerformance(LoadTestShape):
    """
    БЫСТРЫЙ тест производительности всех эндпоинтов (3 минуты).
    
    Проверяет:
    - GET запросы (/, /about, /projects, /contact)
    - POST запросы (форма и JSON API)
    - Метрики Prometheus
    - Производительность под нагрузкой
    
    Критерии:
    - Время ответа < 500ms для GET
    - Время ответа < 1000ms для POST
    - Время ответа < 200ms для /metrics
    - Статус код = 200
    - Корректный формат ответа
    """
    stages = [
        # Этап 1: Прогрев (30 секунд)
        {"duration": 30, "users": 10, "spawn_rate": 2, "user_classes": [WebUser_UC01, WebUser_UC03, WebUser_UC04]},
        
        # Этап 2: Увеличение нагрузки на GET (60 секунд)
        {"duration": 60, "users": 30, "spawn_rate": 5, "user_classes": [WebUser_UC01, WebUser_UC02, WebUser_UC03, WebUser_UC04]},
        
        # Этап 3: ТЕСТ POST /contact форма (90 секунд)
        {"duration": 90, "users": 20, "spawn_rate": 2, "user_classes": [WebUser_UC05]},
        
        # Этап 4: ТЕСТ POST /api/contact JSON (120 секунд)
        {"duration": 120, "users": 25, "spawn_rate": 2, "user_classes": [WebUser_UC05_API]},
        
        # Этап 5: Проверка метрик (150 секунд)
        {"duration": 150, "users": 15, "spawn_rate": 3, "user_classes": [WebUser_UC06]},
        
        # Этап 6: Комплексный тест всех GET + метрики (180 секунд)
        {"duration": 180, "users": 50, "spawn_rate": 5, "user_classes": [
            WebUser_UC01, WebUser_UC02, WebUser_UC03, WebUser_UC04, WebUser_UC06
        ]}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        return None
