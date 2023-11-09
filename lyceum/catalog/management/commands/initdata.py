import os

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.core.management.base import BaseCommand

__all__ = ""


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Applying migrations..."))
        self.check_migrations()
        self.stdout.write(self.style.SUCCESS("Loaded"))

        self.stdout.write(self.style.SUCCESS("Loading fixtures..."))
        self.load_fixtures()
        self.stdout.write(self.style.SUCCESS("Loaded"))

        self.stdout.write(self.style.SUCCESS("Creating superuser..."))
        self.create_admin_user()

    def check_migrations(self):
        call_command("migrate")

    def load_fixtures(self):
        call_command("loaddata", "fixtures/data.json")

    def create_admin_user(self):
        username = "admina"
        if not User.objects.filter(username=username).exists():
            email = os.environ.get("DJANGO_ADMIN_EMAIL")
            password = os.environ.get("DJANGO_ADMIN_PASSWORD")
            if email is None:
                email = input("Enter admin email(you can skip by entering): ")
            while True:
                if password is None:
                    password = input("Enter admin password: ")
                try:
                    validate_password(password)
                except ValidationError as e:
                    for error in e.messages:
                        self.stdout.write(
                            self.style.ERROR(
                                error,
                            ),
                        )
                    choice = input(
                        (
                            "Bypass password validation and "
                            "create user anyway? [yes/no]: "
                        ),
                    )
                    if choice.lower() in ("yes", "y"):
                        break
                    self.stdout.write(
                        self.style.WARNING("Recreating password"),
                    )
                    password = None

            User.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS("Superuser created successfully"),
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    (
                        f'User with username "{username}" '
                        "is already exist, try changing username"
                    ),
                ),
            )
