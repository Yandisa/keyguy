#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Checking if initial data needs loading..."
python manage.py shell -c "
from core.models import SiteSettings
if not SiteSettings.objects.exists():
    print('LOAD_FIXTURES')
else:
    print('SKIP_FIXTURES')
" > /tmp/fixture_check.txt 2>&1

if grep -q "LOAD_FIXTURES" /tmp/fixture_check.txt; then
    echo "First deploy — loading initial data..."
    python manage.py loaddata core/fixtures/initial_data.json
    echo "Initial data loaded."
else
    echo "Data already exists — skipping fixtures. Admin changes are preserved."
fi

echo "Creating superuser if not exists..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@keyguy.co.za')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
if password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Superuser created.')
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
