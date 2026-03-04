# 🐝 Locust - Тесты производительности

## 📋 Use Cases с проверками производительности

| UC | Файл | Эндпоинт | Метод | SLA | Описание |
|----|------|----------|-------|-----|----------|
| **UC01** | `fastapi_main_uc01.py` | `/` | GET | < 500ms | Главная страница |
| **UC02** | `fastapi_contact_uc02.py` | `/contact` | GET | < 500ms | Страница контактов |
| **UC03** | `fastapi_about_uc03.py` | `/about` | GET | < 500ms | Страница "О нас" |
| **UC04** | `fastapi_projects_uc04.py` | `/projects` | GET | < 500ms | Страница проектов |
| **UC05** | `fastapi_contact_post_uc05.py` | `/contact` | POST | < 1000ms | Отправка формы |
| **UC05_API** | `fastapi_contact_post_uc05.py` | `/api/contact` | POST | < 1000ms | JSON API |
| **UC06** | `fastapi_metrics_uc06.py` | `/metrics` | GET | < 200ms | Метрики Prometheus |

## 🔒 ВАЖНО: Заглушка email

Перед запуском POST тестов (UC05) добавь в `.env`:

```env
DISABLE_EMAIL=true
```

Иначе на почту `adrolv@rambler.ru` придёт **много спама**! 📧🚫

## 🚀 Быстрый старт

### Docker Compose (рекомендуется)

```bash
# 1. Добавь в .env
echo "DISABLE_EMAIL=true" >> .env

# 2. Запуск полного теста (5 минут)
docker compose up --build

# 3. Или быстрый тест (3 минуты)
docker compose -f docker-compose.performance.yml up --build

# 4. Открой Locust UI
firefox http://localhost:8089
```

### Локальный запуск

```bash
# 1. Установи зависимости
pip install locust

# 2. Запусти приложение с заглушкой
DISABLE_EMAIL=true uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# 3. Запусти Locust
cd locust
locust -f loadshape_stability.py --host=http://localhost:8000

# 4. Открой UI
firefox http://localhost:8089
```

## 📊 LoadShapes (сценарии нагрузки)

### loadshape_stability.py (полный тест)

- **Длительность:** ~5 минут
- **Максимум пользователей:** 80
- **Этапы:** 8 этапов с разными UC
- **Включает:** POST тесты (UC05)

### loadshape_performance.py (быстрый тест)

- **Длительность:** 3 минуты
- **Максимум пользователей:** 50
- **Этапы:** 6 этапов
- **Автозавершение:** да (--headless --run-time 3m)

## 🎯 Что проверяется

### Функциональные проверки (в каждом UC):

```python
# Пример из UC01
with user.client.get("/", catch_response=True) as response:
    if response.status_code != 200:
        response.failure(f"Статус {response.status_code}")
    elif response.elapsed.total_seconds() > 0.5:
        response.failure(f"Медленно: {response.elapsed.total_seconds():.3f}s")
    elif len(response.content) < 1000:
        response.failure("Мало контента")
    elif "text/html" not in response.headers.get("content-type", ""):
        response.failure("Неправильный content-type")
    else:
        response.success()  # ✅ Всё хорошо
```

### Что логируется как failure:

- ❌ Неправильный статус код (не 200)
- ❌ Превышение SLA по времени ответа
- ❌ Недостаточный размер контента
- ❌ Неправильный Content-Type
- ❌ Отсутствие ожидаемой структуры (форма, JSON поля)

## 📈 Анализ результатов

### Locust UI - Statistics

```
Type     Name                # reqs  # fails   Avg    Min   Max   Median  req/s
--------------------------------------------------------------------------------
GET      /                   5000    0(0%)     45ms   23    234   42      167.0
POST     /contact            500     0(0%)     142ms  87    456   135     16.7
--------------------------------------------------------------------------------

✅ 0% failures = все проверки пройдены!
```

### Locust UI - Charts

- **Total Requests per Second** - стабильность нагрузки
- **Response Times (ms)** - время ответа (50%, 95%, 99%)
- **Number of Users** - количество виртуальных пользователей

### Prometheus запросы

```promql
# Среднее время ответа
rate(http_request_duration_seconds_sum[1m]) / rate(http_request_duration_seconds_count[1m])

# 95-й перцентиль
histogram_quantile(0.95, http_request_duration_seconds_bucket)

# RPS по эндпоинту
rate(http_requests_total{handler="/"}[1m])

# Количество Locust юзеров
locust_users
```

## 🐛 Troubleshooting

### Проблема: Много failures на /contact POST

**Причина:** DISABLE_EMAIL не установлен, реальная SMTP отправка медленная.

**Решение:**
```bash
# Добавь в .env
DISABLE_EMAIL=true

# Пересобери
docker compose down
docker compose up --build
```

### Проблема: Response time > SLA

**Причина:** Недостаточно ресурсов или проблема в коде.

**Решение:**
```bash
# Проверь CPU/Memory
docker stats

# Оптимизируй код или увеличь ресурсы
# Или измени SLA в UC файлах
```

### Проблема: Locust показывает 0 users

**Причина:** LoadShape завершился или ошибка в stages.

**Решение:**
```bash
# Проверь логи
docker compose logs locust

# Проверь метрики
curl http://localhost:8089/metrics
```

## 🎁 Бонус: Расширенные метрики

Каждый UC записывает в Locust:
- ✅ Количество запросов
- ✅ Количество failures с причинами
- ✅ Время ответа (avg, min, max, percentiles)
- ✅ RPS (requests per second)

Все это видно в:
- Locust UI (http://localhost:8089)
- Prometheus (http://localhost:9090)
- Grafana (http://localhost:3000)

## 🎉 Итог

✅ **7 Use Cases** с проверками производительности  
✅ **Автоматические SLA проверки**  
✅ **Заглушка email** для POST тестов  
✅ **2 сценария** - полный и быстрый  
✅ **Готово к запуску** без спама на почту!  

---

**🔥 Запускай: `docker compose up --build` 🔥**

*(Не забудь `DISABLE_EMAIL=true` в `.env`!)*
