from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

ROLE_NAMES = ["Employee", "HR", "Finance", "Inventory"]

class Command(BaseCommand):
    help = "Create default user groups (Employee, HR, Finance, Inventory)."

    def handle(self, *args, **options):
        created = 0
        for name in ROLE_NAMES:
            _, was_created = Group.objects.get_or_create(name=name)
            created += 1 if was_created else 0
        self.stdout.write(self.style.SUCCESS(f"Done. Groups created: {created} (existing groups kept)."))
        self.stdout.write("Next: Admin > Users > add users to groups, and link each User to an Employee record.")
