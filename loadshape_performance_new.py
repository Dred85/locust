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
        {"duration": 30, "users": 10, "spawn_rate": 2, "user_classes": [WebUser_UC01, WebUser_UC03, WebUser_UC04]},  # Прогрев
        {"duration": 60, "users": 30, "spawn_rate": 5, "user_classes": [WebUser_UC01, WebUser_UC02, WebUser_UC03, WebUser_UC04]},
        {"duration": 90, "users": 50, "spawn_rate": 2, "user_classes": [WebUser_UC05]},
        {"duration": 120, "users": 25, "spawn_rate": 2, "user_classes": [WebUser_UC05_API]},
        {"duration": 150, "users": 15, "spawn_rate": 3, "user_classes": [WebUser_UC06]}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]

        return None
