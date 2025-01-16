#!/bin/sh

until nc -z db 5432; do
    echo "Ждём, пока Postgres станет доступным..."
    sleep 1
done

echo "Postgres доступен. Выполняем миграции и сбор статики."

python manage.py migrate

python manage.py collectstatic --no-input --clear

exec "$@"