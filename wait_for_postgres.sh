
# Проверка подключения к базе данных PostgreSQL
until psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  echo "Waiting for PostgreSQL to be available..."
  sleep 2
done

echo "PostgreSQL is up and running!"