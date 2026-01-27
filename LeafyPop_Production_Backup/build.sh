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
