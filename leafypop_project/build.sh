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

# Restore products and FAQs automatically (v3 uploads images to Cloudinary)
python populate_db_v3.py

# Create superuser using custom script
if [[ $DJANGO_SUPERUSER_USERNAME ]]; then
  python create_leafypop_admin.py || true
fi
