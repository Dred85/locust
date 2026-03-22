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
        {"duration": 60, "users": 10, "spawn_rate": 1, "user_classes": [WebUser_UC01]},  # Прогрев
        {"duration": 120, "users": 10, "spawn_rate": 1, "user_classes": [WebUser_UC02]},
        {"duration": 180, "users": 10, "spawn_rate": 1, "user_classes": [WebUser_UC03]},
        {"duration": 186, "users": 5, "spawn_rate": 1, "user_classes": [WebUser_UC01, WebUser_UC02, WebUser_UC03, WebUser_UC04, WebUser_UC05, WebUser_UC05_API, WebUser_UC06]},
        {"duration": 192, "users": 1, "spawn_rate": 1, "user_classes": [WebUser_UC01, WebUser_UC02, WebUser_UC03, WebUser_UC04, WebUser_UC05, WebUser_UC05_API, WebUser_UC06]}

    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        return None
