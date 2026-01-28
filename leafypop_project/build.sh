#!/usr/bin/env bash
set -o errexit

# Upgrade build tools first
pip install --upgrade pip setuptools wheel

# Install project requirements
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Restore products and FAQs automatically
python populate_db_v2.py
python populate_faqs.py

# Create superuser if environment variables are set
if [[ $DJANGO_SUPERUSER_USERNAME ]]; then
  # Try custom script first for better branding
  python create_leafypop_admin.py || true
  # Fallback to standard command
  python manage.py createsuperuser --no-input --email $DJANGO_SUPERUSER_EMAIL || true
fi
