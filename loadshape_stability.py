from locust import LoadTestShape

from locustfile import WebUser_UC01, WebUser_UC02


class LoadShape(LoadTestShape):
    """
    Stability / soak test с переключением сценарием
    """
    stages = [
        {"duration": 20, "users": 20, "spawn_rate": 1, "user_classes": [WebUser_UC01]},
        {"duration": 40, "users": 40, "spawn_rate": 1, "user_classes": [WebUser_UC02]},
        {"duration": 1800, "users": 50, "spawn_rate": 1}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return stage["users"], stage["spawn_rate"]
            run_time -= stage["duration"]

        return None
