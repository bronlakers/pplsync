# Cloud Run-friendly container
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Collect static at build time (optional; can also run at deploy)
RUN python manage.py collectstatic --noinput || true

ENV PORT=8080
CMD exec gunicorn biztrack.wsgi:application --bind :$PORT --workers 2 --threads 8 --timeout 0
