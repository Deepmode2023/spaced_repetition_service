#!/bin/sh

echo "$POSTGRES_PASSWORD, $POSTGRES_DB, $POSTGRES_USER, $DB_HOST <========="

# Ожидаем, пока база данных будет доступна
until pg_isready -h $DB_HOST -U $POSTGRES_USER -d $POSTGRES_DB; do
    echo 'Waiting for DB...';
    sleep 2;
done;

# Проверяем, есть ли таблица alembic_version
if ! psql postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$DB_HOST/$POSTGRES_DB -c 'SELECT * FROM alembic_version' > /dev/null 2>&1; then
    echo 'No tables found. Running migrations...';
    alembic upgrade head;
else
    echo 'Migrations already applied.';
fi
