FROM python:3.9

WORKDIR /task_manager

RUN apt-get update && apt-get install -y \
    libpq-dev gcc netcat-openbsd

COPY requirements.txt /task_manager/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /task_manager/

RUN chmod +x /task_manager/entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/task_manager/entrypoint.sh"]