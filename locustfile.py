import logging

from locust import HttpUser, TaskSet, between

from fastapi_main_uc01 import open_index
from fastapi_contact_uc02 import open_contact
from fastapi_about_uc03 import open_about
from fastapi_projects_uc04 import open_projects
from fastapi_contact_post_uc05 import submit_contact_form, submit_contact_api
from fastapi_metrics_uc06 import check_metrics


# from loadshape_stability import LoadShape0552

class UserBehaviour_UC01(TaskSet):
    """
    TaskSet для FastAPI пользователя.
    Использует open_index как основной сценарий.
    """
    loglevel = 'ERROR'
    logger = logging.getLogger('udp_logger')
    logger.setLevel(loglevel)
    # dp = CSVReader('./pool.csv')
    tasks = [open_index]


class WebUser_UC01(HttpUser):
    host = "http://localhost:8000"  # обязательно для headless
    wait_time = between(1, 3)
    tasks = [UserBehaviour_UC01]


class UserBehaviour_UC02(TaskSet):
    """
    TaskSet для FastAPI пользователя.
    Использует open_index как основной сценарий.
    """
    loglevel = 'ERROR'
    logger = logging.getLogger('udp_logger')
    logger.setLevel(loglevel)
    # dp = CSVReader('./pool.csv')
    tasks = [open_contact]


class WebUser_UC02(HttpUser):
    host = "http://localhost:8000"  # обязательно для headless
    wait_time = between(1, 3)
    tasks = [UserBehaviour_UC02]


class UserBehaviour_UC03(TaskSet):
    """
    TaskSet для FastAPI пользователя.
    Использует /about
    """
    loglevel = 'ERROR'
    logger = logging.getLogger('udp_logger')
    logger.setLevel(loglevel)
    # dp = CSVReader('./pool.csv')
    tasks = [open_about]


class WebUser_UC03(HttpUser):
    host = "http://localhost:8000"  # обязательно для headless
    wait_time = between(1, 3)
    tasks = [UserBehaviour_UC03]


class UserBehaviour_UC04(TaskSet):
    """
    TaskSet для FastAPI пользователя.
    Использует /about
    """
    loglevel = 'ERROR'
    logger = logging.getLogger('udp_logger')
    logger.setLevel(loglevel)
    tasks = [open_projects]


class WebUser_UC04(HttpUser):
    host = "http://localhost:8000"  # обязательно для headless
    wait_time = between(1, 3)
    tasks = [UserBehaviour_UC04]


class UserBehaviour_UC05(TaskSet):
    """
    TaskSet для тестирования POST контактной формы.
    Проверяет производительность отправки форм.
    """
    loglevel = 'ERROR'
    logger = logging.getLogger('udp_logger')
    logger.setLevel(loglevel)
    tasks = [submit_contact_form]


class WebUser_UC05(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(2, 5)  # Больше задержка для POST запросов
    tasks = [UserBehaviour_UC05]


class UserBehaviour_UC05_API(TaskSet):
    """
    TaskSet для тестирования JSON API контактов.
    Проверяет производительность /api/contact.
    """
    loglevel = 'ERROR'
    logger = logging.getLogger('udp_logger')
    logger.setLevel(loglevel)
    tasks = [submit_contact_api]


class WebUser_UC05_API(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(2, 5)
    tasks = [UserBehaviour_UC05_API]


class UserBehaviour_UC06(TaskSet):
    """
    TaskSet для тестирования эндпоинта метрик.
    Проверяет производительность /metrics.
    """
    loglevel = 'ERROR'
    logger = logging.getLogger('udp_logger')
    logger.setLevel(loglevel)
    tasks = [check_metrics]


class WebUser_UC06(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(1, 2)  # Метрики проверяются чаще
    tasks = [UserBehaviour_UC06]
