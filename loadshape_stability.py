"""
Locust LoadShape для тестирования стабильности и производительности.

⚠️  ВАЖНО: Установите DISABLE_EMAIL=true в .env файле!
   Иначе POST тесты (UC05) будут отправлять реальные email на adrolv@rambler.ru

Запуск:
  docker compose up --build
  
Или локально:
  DISABLE_EMAIL=true uvicorn app.main:app --host 0.0.0.0 --port 8000 &
  locust -f locust/loadshape_stability.py --host=http://localhost:8000
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
    # Эти импорты будут работать после установки prometheus_client внутри контейнера locust
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
                # В разных версиях Locust есть user_count или список user_instances
                user_count = getattr(runner, "user_count", None)
                if user_count is None:
                    user_count = len(getattr(runner, "user_instances", []))
            else:
                user_count = 0

            _locust_users_gauge.set(user_count)
            return Response(generate_latest(_registry), mimetype=CONTENT_TYPE_LATEST)

except ModuleNotFoundError:
    # В локальной среде без prometheus_client просто не поднимаем /metrics
    pass


class LoadShape(LoadTestShape):
    """
    Stability / soak test с переключением сценариев и проверкой производительности
    
    Этапы:
    1. UC01 - GET / (главная страница)
    2. UC03 - GET /about (о нас)
    3. UC04 - GET /projects (проекты)
    4. UC02 - GET /contact (форма контактов)
    5. UC05 - POST /contact (отправка формы) - ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ
    6. UC05_API - POST /api/contact (JSON API) - ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ
    7. UC06 - GET /metrics (метрики Prometheus)
    8. Финальная стабильность - все UC вместе
    """
    stages = [
        # Прогрев - главная страница
        {"duration": 20, "users": 20, "spawn_rate": 2, "user_classes": [WebUser_UC01]},
        
        # Проверка страниц GET
        {"duration": 40, "users": 40, "spawn_rate": 2, "user_classes": [WebUser_UC03]},
        {"duration": 60, "users": 60, "spawn_rate": 2, "user_classes": [WebUser_UC04]},
        {"duration": 80, "users": 60, "spawn_rate": 2, "user_classes": [WebUser_UC02]},
        
        # 🔥 ТЕСТЫ ПРОИЗВОДИТЕЛЬНОСТИ POST запросов
        {"duration": 100, "users": 40, "spawn_rate": 2, "user_classes": [WebUser_UC05]},
        {"duration": 120, "users": 50, "spawn_rate": 2, "user_classes": [WebUser_UC05_API]},
        
        # Проверка метрик
        {"duration": 140, "users": 30, "spawn_rate": 2, "user_classes": [WebUser_UC06]},
        
        # Финальный этап - стабильность со всеми UC (кроме POST для избежания спама)
        {"duration": 300, "users": 80, "spawn_rate": 2, "user_classes": [WebUser_UC01, WebUser_UC02, WebUser_UC03, WebUser_UC04, WebUser_UC06]}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
            run_time -= stage["duration"]

        return None
