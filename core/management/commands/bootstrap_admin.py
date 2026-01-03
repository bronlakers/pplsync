# core/management/commands/bootstrap_admin.py
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create an initial superuser if none exists (idempotent)."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not (username and email and password):
            self.stdout.write("bootstrap_admin: env vars missing, skipping")
            return

        User = get_user_model()
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("bootstrap_admin: superuser already exists, skipping")
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(f"bootstrap_admin: created superuser '{username}'")
