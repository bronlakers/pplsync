#!/usr/bin/env bash
# Exit on error
set -o errexit

# Why: Render runs this on every deploy to prepare your app for production.
# 1) Install dependencies
pip install -r requirements.txt

# 2) Collect static files for WhiteNoise (/static/)
python manage.py collectstatic --noinput

# 3) Apply database migrations (safe to run repeatedly)
python manage.py migrate
