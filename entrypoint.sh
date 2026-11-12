#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Loading cultural data..."
python manage.py loaddata fixtures/initial_data.json || true

echo "Ensuring admin and demo accounts exist with known passwords..."
python manage.py shell -c "
from accounts.models import UserProfile
# Ensure admin user
admin_user, created = UserProfile.objects.get_or_create(username='admin')
admin_user.set_password('admin123')
admin_user.email = 'admin@bharatverse.org'
admin_user.role = 'curator'
admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.save()

# Ensure contributor_demo user
contributor, _ = UserProfile.objects.get_or_create(username='contributor_demo')
contributor.set_password('contributor123')
contributor.role = 'contributor'
contributor.save()

print('Default accounts configured: admin/admin123 and contributor_demo/contributor123')
" || true

echo "Starting Gunicorn server..."
exec gunicorn bharatverse.wsgi:application --bind 0.0.0.0:8000
