"""
Профиль нагрузки Locust
Создано в визуальном редакторе
"""
from locust import LoadTestShape

from locustfile import (
    WebUser_UC01,
    WebUser_UC02,
    WebUser_UC03,
    WebUser_UC04,
    WebUser_UC05,
    WebUser_UC05_API,
    WebUser_UC06
)


class LoadShape(LoadTestShape):
    """Профиль нагрузки"""
    stages = [
        {"duration": 60, "users": 10, "spawn_rate": 1, "user_classes": [WebUser_UC01]},  # Прогрев
        {"duration": 120, "users": 10, "spawn_rate": 1, "user_classes": [WebUser_UC02]},
        {"duration": 180, "users": 10, "spawn_rate": 1, "user_classes": [WebUser_UC03]},
        {"duration": 240, "users": 100, "spawn_rate": 1, "user_classes": [WebUser_UC01, WebUser_UC02, WebUser_UC03, WebUser_UC04, WebUser_UC05]}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        return None
