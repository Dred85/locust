import logging

from locust import HttpUser, TaskSet, between, User

from fastapi_main_uc01 import open_index
from fastapi_contact_uc02 import open_contact
from fastapi_about_uc03 import open_about
from fastapi_projects_uc04 import open_projects


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
