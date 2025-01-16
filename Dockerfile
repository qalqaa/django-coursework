# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /task_manager

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev && \
    apt-get clean

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Копируем entrypoint.sh
COPY entrypoint.sh /task_manager/entrypoint.sh

# Делаем entrypoint.sh исполнимым
RUN chmod +x /task_manager/entrypoint.sh

# Экспортируем порт приложения
EXPOSE 8000

# Устанавливаем entrypoint
ENTRYPOINT ["/task_manager/entrypoint.sh"]