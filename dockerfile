# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install --no-cache-dir fastapi uvicorn[standard] prometheus-fastapi-instrumentator jinja2 websockets

# Открываем порт для WebSocket и HTTP
EXPOSE 8000

# Указываем команду для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]