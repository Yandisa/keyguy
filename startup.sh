#!/bin/sh
# Coolify can run this as a "Start Command" or you can run it once manually
# after first deploy via Coolify's terminal

set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Loading initial data..."
python manage.py loaddata core/fixtures/initial_data.json || echo "Fixtures already loaded or skipped"

echo "Creating superuser from env vars (if set)..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@keyguy.co.za')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
if password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created.')
else:
    print('Superuser already exists or no password set — skipping.')
" || echo "Superuser step skipped"

echo "Starting gunicorn..."
exec gunicorn keyguy.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile -
