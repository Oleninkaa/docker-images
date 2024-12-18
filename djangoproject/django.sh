#!/bin/bash

# Очікуємо, поки база даних стане доступною
echo "Waiting for the database to be ready..."
/app/wait-for-it.sh $PG_HOST:$PG_PORT --timeout=30 --strict -- echo "Database is ready!"


echo "Create migrations"
python manage.py makemigrations djangoapp
echo "=================================="

echo "Migrate"
python manage.py migrate
echo "=================================="

# Завантажуємо початкові дані в базу даних
echo "Loading initial data..."
python manage.py loaddata initial_data.json
echo "=================================="

echo "Start server"
python manage.py runserver 0.0.0.0:8000