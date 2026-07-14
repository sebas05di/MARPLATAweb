#!/usr/bin/env bash
# Build script for production (Render, VPS, CI/CD, etc.)
set -o errexit
set -o pipefail

python -m pip install --upgrade pip
pip install -r requirements/prod.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py seed_pages
