"""
Шаблоны профилей нагрузки для быстрого использования в редакторе

Эти шаблоны можно использовать как основу для создания собственных профилей.
Скопируйте нужный шаблон и измените параметры в визуальном редакторе.
"""

# Шаблон 1: Линейный рост (Simple Ramp-Up)
TEMPLATE_LINEAR_RAMP = [
    {"duration": 30, "users": 10, "spawn_rate": 1, "user_classes": ["WebUser_UC01"]},
    {"duration": 60, "users": 25, "spawn_rate": 1, "user_classes": ["WebUser_UC01", "WebUser_UC03"]},
    {"duration": 90, "users": 50, "spawn_rate": 2, "user_classes": ["WebUser_UC01", "WebUser_UC03", "WebUser_UC04"]},
    {"duration": 120, "users": 75, "spawn_rate": 2, "user_classes": ["WebUser_UC01", "WebUser_UC03", "WebUser_UC04"]},
    {"duration": 150, "users": 100, "spawn_rate": 3, "user_classes": ["WebUser_UC01", "WebUser_UC02", "WebUser_UC03", "WebUser_UC04"]},
]

# Шаблон 2: Spike Test (резкий всплеск нагрузки)
TEMPLATE_SPIKE_TEST = [
    {"duration": 30, "users": 10, "spawn_rate": 1, "user_classes": ["WebUser_UC01"]},  # Прогрев
    {"duration": 35, "users": 200, "spawn_rate": 50, "user_classes": ["WebUser_UC01", "WebUser_UC03"]},  # Резкий всплеск
    {"duration": 65, "users": 10, "spawn_rate": 1, "user_classes": ["WebUser_UC01"]},  # Восстановление
    {"duration": 95, "users": 200, "spawn_rate": 50, "user_classes": ["WebUser_UC04"]},  # Второй всплеск
    {"duration": 125, "users": 10, "spawn_rate": 1, "user_classes": ["WebUser_UC01"]},  # Финальное восстановление
]

# Шаблон 3: Soak Test (длительная стабильная нагрузка)
TEMPLATE_SOAK_TEST = [
    {"duration": 60, "users": 50, "spawn_rate": 2, "user_classes": ["WebUser_UC01", "WebUser_UC03"]},  # Прогрев
    {"duration": 3660, "users": 50, "spawn_rate": 1, "user_classes": ["WebUser_UC01", "WebUser_UC02", "WebUser_UC03", "WebUser_UC04"]},  # 1 час стабильной нагрузки
]

# Шаблон 4: Step Load (ступенчатая нагрузка)
TEMPLATE_STEP_LOAD = [
    {"duration": 30, "users": 20, "spawn_rate": 2, "user_classes": ["WebUser_UC01"]},
    {"duration": 60, "users": 40, "spawn_rate": 2, "user_classes": ["WebUser_UC01", "WebUser_UC03"]},
    {"duration": 90, "users": 60, "spawn_rate": 2, "user_classes": ["WebUser_UC01", "WebUser_UC03"]},
    {"duration": 120, "users": 80, "spawn_rate": 2, "user_classes": ["WebUser_UC01", "WebUser_UC03", "WebUser_UC04"]},
    {"duration": 150, "users": 100, "spawn_rate": 2, "user_classes": ["WebUser_UC01", "WebUser_UC02", "WebUser_UC03", "WebUser_UC04"]},
    {"duration": 180, "users": 120, "spawn_rate": 2, "user_classes": ["WebUser_UC01", "WebUser_UC02", "WebUser_UC03", "WebUser_UC04"]},
]

# Шаблон 5: Stress Test (постепенное увеличение до отказа)
TEMPLATE_STRESS_TEST = [
    {"duration": 30, "users": 10, "spawn_rate": 1, "user_classes": ["WebUser_UC01"]},
    {"duration": 60, "users": 50, "spawn_rate": 2, "user_classes": ["WebUser_UC01", "WebUser_UC03"]},
    {"duration": 90, "users": 100, "spawn_rate": 3, "user_classes": ["WebUser_UC01", "WebUser_UC03", "WebUser_UC04"]},
    {"duration": 120, "users": 200, "spawn_rate": 5, "user_classes": ["WebUser_UC01", "WebUser_UC03", "WebUser_UC04"]},
    {"duration": 150, "users": 400, "spawn_rate": 10, "user_classes": ["WebUser_UC01", "WebUser_UC03", "WebUser_UC04"]},
    {"duration": 180, "users": 800, "spawn_rate": 20, "user_classes": ["WebUser_UC01", "WebUser_UC03", "WebUser_UC04"]},
]

# Шаблон 6: Peak Hours Simulation (имитация пиковых часов)
TEMPLATE_PEAK_HOURS = [
    {"duration": 30, "users": 10, "spawn_rate": 1, "user_classes": ["WebUser_UC01"]},  # Раннее утро
    {"duration": 90, "users": 30, "spawn_rate": 1, "user_classes": ["WebUser_UC01", "WebUser_UC03"]},  # Утро
    {"duration": 180, "users": 80, "spawn_rate": 3, "user_classes": ["WebUser_UC01", "WebUser_UC02", "WebUser_UC03", "WebUser_UC04"]},  # Пик (обед)
    {"duration": 270, "users": 50, "spawn_rate": 2, "user_classes": ["WebUser_UC01", "WebUser_UC03"]},  # После обеда
    {"duration": 360, "users": 90, "spawn_rate": 3, "user_classes": ["WebUser_UC01", "WebUser_UC02", "WebUser_UC03", "WebUser_UC04"]},  # Вечерний пик
    {"duration": 450, "users": 20, "spawn_rate": 1, "user_classes": ["WebUser_UC01"]},  # Вечер
]

# Шаблон 7: API Performance Test (тестирование API)
TEMPLATE_API_TEST = [
    {"duration": 20, "users": 10, "spawn_rate": 1, "user_classes": ["WebUser_UC01"]},  # Прогрев
    {"duration": 50, "users": 30, "spawn_rate": 2, "user_classes": ["WebUser_UC05_API"]},  # Тест POST API
    {"duration": 80, "users": 50, "spawn_rate": 3, "user_classes": ["WebUser_UC05_API"]},  # Увеличение нагрузки
    {"duration": 110, "users": 80, "spawn_rate": 5, "user_classes": ["WebUser_UC05_API"]},  # Максимальная нагрузка
    {"duration": 140, "users": 30, "spawn_rate": 2, "user_classes": ["WebUser_UC06"]},  # Проверка метрик
]

# Шаблон 8: Quick Smoke Test (быстрая проверка)
TEMPLATE_SMOKE_TEST = [
    {"duration": 10, "users": 5, "spawn_rate": 1, "user_classes": ["WebUser_UC01"]},
    {"duration": 20, "users": 10, "spawn_rate": 1, "user_classes": ["WebUser_UC03"]},
    {"duration": 30, "users": 10, "spawn_rate": 1, "user_classes": ["WebUser_UC04"]},
    {"duration": 40, "users": 10, "spawn_rate": 1, "user_classes": ["WebUser_UC02"]},
    {"duration": 50, "users": 5, "spawn_rate": 1, "user_classes": ["WebUser_UC06"]},
]

# Шаблон 9: Breakpoint Test (поиск точки отказа)
TEMPLATE_BREAKPOINT_TEST = [
    {"duration": 30, "users": 10, "spawn_rate": 1, "user_classes": ["WebUser_UC01"]},
    {"duration": 60, "users": 25, "spawn_rate": 2, "user_classes": ["WebUser_UC01", "WebUser_UC03"]},
    {"duration": 90, "users": 50, "spawn_rate": 3, "user_classes": ["WebUser_UC01", "WebUser_UC03"]},
    {"duration": 120, "users": 100, "spawn_rate": 5, "user_classes": ["WebUser_UC01", "WebUser_UC03"]},
    {"duration": 150, "users": 200, "spawn_rate": 10, "user_classes": ["WebUser_UC01", "WebUser_UC03"]},
    {"duration": 180, "users": 400, "spawn_rate": 20, "user_classes": ["WebUser_UC01", "WebUser_UC03"]},
    {"duration": 210, "users": 800, "spawn_rate": 40, "user_classes": ["WebUser_UC01", "WebUser_UC03"]},
]

# Шаблон 10: Mixed Workload (смешанная нагрузка)
TEMPLATE_MIXED_WORKLOAD = [
    {"duration": 30, "users": 20, "spawn_rate": 2, "user_classes": ["WebUser_UC01"]},  # GET главная
    {"duration": 60, "users": 30, "spawn_rate": 2, "user_classes": ["WebUser_UC01", "WebUser_UC03"]},  # GET страницы
    {"duration": 90, "users": 40, "spawn_rate": 2, "user_classes": ["WebUser_UC01", "WebUser_UC03", "WebUser_UC04"]},  # Все GET
    {"duration": 120, "users": 50, "spawn_rate": 2, "user_classes": ["WebUser_UC01", "WebUser_UC02", "WebUser_UC03", "WebUser_UC04"]},  # + форма
    {"duration": 150, "users": 30, "spawn_rate": 2, "user_classes": ["WebUser_UC05"]},  # POST форма
    {"duration": 180, "users": 30, "spawn_rate": 2, "user_classes": ["WebUser_UC05_API"]},  # POST API
    {"duration": 210, "users": 20, "spawn_rate": 1, "user_classes": ["WebUser_UC06"]},  # Метрики
    {"duration": 300, "users": 60, "spawn_rate": 3, "user_classes": ["WebUser_UC01", "WebUser_UC02", "WebUser_UC03", "WebUser_UC04", "WebUser_UC06"]},  # Финал
]


# Описания шаблонов для документации
TEMPLATE_DESCRIPTIONS = {
    "TEMPLATE_LINEAR_RAMP": {
        "name": "Линейный рост",
        "duration": "150 секунд (2.5 минуты)",
        "max_users": 100,
        "use_case": "Базовое тестирование с постепенным увеличением нагрузки"
    },
    "TEMPLATE_SPIKE_TEST": {
        "name": "Spike Test",
        "duration": "125 секунд (2 минуты)",
        "max_users": 200,
        "use_case": "Проверка поведения при резких всплесках нагрузки"
    },
    "TEMPLATE_SOAK_TEST": {
        "name": "Soak Test",
        "duration": "3660 секунд (1 час)",
        "max_users": 50,
        "use_case": "Проверка стабильности при длительной нагрузке"
    },
    "TEMPLATE_STEP_LOAD": {
        "name": "Ступенчатая нагрузка",
        "duration": "180 секунд (3 минуты)",
        "max_users": 120,
        "use_case": "Постепенное увеличение нагрузки ступенями"
    },
    "TEMPLATE_STRESS_TEST": {
        "name": "Stress Test",
        "duration": "180 секунд (3 минуты)",
        "max_users": 800,
        "use_case": "Поиск пределов системы при экстремальной нагрузке"
    },
    "TEMPLATE_PEAK_HOURS": {
        "name": "Имитация пиковых часов",
        "duration": "450 секунд (7.5 минут)",
        "max_users": 90,
        "use_case": "Симуляция реальной нагрузки в течение рабочего дня"
    },
    "TEMPLATE_API_TEST": {
        "name": "API Performance Test",
        "duration": "140 секунд (2.3 минуты)",
        "max_users": 80,
        "use_case": "Тестирование производительности API эндпоинтов"
    },
    "TEMPLATE_SMOKE_TEST": {
        "name": "Quick Smoke Test",
        "duration": "50 секунд",
        "max_users": 10,
        "use_case": "Быстрая проверка работоспособности всех эндпоинтов"
    },
    "TEMPLATE_BREAKPOINT_TEST": {
        "name": "Breakpoint Test",
        "duration": "210 секунд (3.5 минуты)",
        "max_users": 800,
        "use_case": "Поиск точки отказа системы"
    },
    "TEMPLATE_MIXED_WORKLOAD": {
        "name": "Смешанная нагрузка",
        "duration": "300 секунд (5 минут)",
        "max_users": 60,
        "use_case": "Реалистичная смешанная нагрузка на все эндпоинты"
    }
}


def print_template_info():
    """Вывод информации о всех доступных шаблонах"""
    print("=" * 80)
    print("ДОСТУПНЫЕ ШАБЛОНЫ ПРОФИЛЕЙ НАГРУЗКИ")
    print("=" * 80)
    
    for template_name, info in TEMPLATE_DESCRIPTIONS.items():
        print(f"\n{info['name']} ({template_name})")
        print(f"  Длительность: {info['duration']}")
        print(f"  Максимум пользователей: {info['max_users']}")
        print(f"  Применение: {info['use_case']}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print_template_info()
