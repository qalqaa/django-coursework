# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /task_manager

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev && \
    apt-get clean

# Копируем скрипт ожидания
COPY wait_for_postgres.sh /task_manager/wait_for_postgres.sh

# Делаем скрипт исполнимым
RUN chmod +x /task_manager/wait_for_postgres.sh

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Экспортируем порт приложения
EXPOSE 8000

# Запуск сервера разработки Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]