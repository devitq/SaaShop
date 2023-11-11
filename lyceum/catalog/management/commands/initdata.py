from django.core.management import call_command
from django.core.management.base import BaseCommand

__all__ = ""


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--interactive",
            type=str,
            help=(
                "Input superuser data in console"
                "instead of getting it from env"
            ),
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Applying migrations..."))
        call_command("migrate")
        self.stdout.write(self.style.SUCCESS("Loaded"))

        self.stdout.write(self.style.SUCCESS("Loading fixtures..."))
        call_command("loaddata", "fixtures/data.json")
        self.stdout.write(self.style.SUCCESS("Loaded"))

        self.stdout.write(self.style.SUCCESS("Creating superuser..."))
        if options["interactive"] and options["interactive"].lower() in (
            "yes",
            "y",
            "true",
            "t",
            "1",
        ):
            call_command("createsuperuser")
        else:
            call_command("createsuperuser", interactive=False)

        self.stdout.write(self.style.SUCCESS("Ended successfully"))
