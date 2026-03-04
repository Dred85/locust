#!/bin/sh

# Устанавливаем prometheus_client для экспорта метрик из Locust
pip install --no-cache-dir prometheus_client >/dev/null 2>&1

# Передаём управление стандартному entrypoint Locust
exec locust "$@"

