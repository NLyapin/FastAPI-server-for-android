# Мониторинг Android-приложения с использованием FastAPI, Prometheus и Grafana

## [Андроид-приложение здесь](https://github.com/NLyapin/location_tracker)

Этот репозиторий содержит серверную часть проекта для мониторинга активности Android-приложения. Сервер принимает данные от Android-приложения через WebSocket, сохраняет их и предоставляет метрики для мониторинга с использованием Prometheus и Grafana.

## Структура репозитория 
 
- **`main.py`** : Основной файл сервера, реализующий прием данных через WebSocket и REST API для отображения состояния устройства.
 
- **`docker-compose.yml`** : Конфигурация Docker Compose для запуска сервера FastAPI, Prometheus и Grafana.
 
- **`prometheus.yml`** : Конфигурационный файл Prometheus для настройки источников данных.
 
- **`Dockerfile`** : Dockerfile для сборки образа сервера FastAPI.


---


## Быстрый старт 
### 1. Сборка и запуск контейнеров 

Убедитесь, что у вас установлен Docker и Docker Compose. Затем выполните:


```bash
docker-compose up --build
```

### 2. Компоненты системы 

После запуска будут доступны:
 
- **FastAPI сервер** : 
  - Адрес: `http://localhost:8000`
 
  - Метрики Prometheus: `http://localhost:8000/metrics`
 
- **Prometheus** : 
  - Адрес: `http://localhost:9090`
 
- **Grafana** : 
  - Адрес: `http://localhost:3000`
 
  - Логин/пароль по умолчанию: `admin/admin`


---


## Настройка Grafana 
 
1. Перейдите в Grafana (`http://localhost:3000`).
 
2. Добавьте источник данных Prometheus: 
  - URL: `http://prometheus:9090`.

3. Импортируйте готовый дашборд или создайте свои панели с использованием Prometheus-запросов.


---


## Пример метрик Prometheus 
 
- **HTTP-запросы по статусам** :

```promql
sum(http_requests_total) by (status)
```
 
- **Использование памяти процессом Python** :

```promql
process_resident_memory_bytes
```
 
- **Количество WebSocket-соединений** :

```promql
sum(active_websockets_total)
```


---


## Расширение 
 
- Добавьте дополнительные метрики или эндпоинты в `main.py` по мере необходимости.

- Настройте собственные дашборды Grafana для более глубокого анализа данных.