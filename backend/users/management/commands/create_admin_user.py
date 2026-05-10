import getpass

from django.core.management.base import BaseCommand, CommandError

from users.models import User


class Command(BaseCommand):
    help = "Create a simple admin user with email, name, and password."

    def add_arguments(self, parser):
        parser.add_argument("--email", type=str, help="Admin email")
        parser.add_argument("--name", type=str, help="Admin name")
        parser.add_argument("--password", type=str, help="Admin password")

    def handle(self, *args, **options):
        email = options.get("email") or input("Email: ").strip()
        name = options.get("name") or input("Name: ").strip()
        password = options.get("password") or getpass.getpass("Password: ")

        if not email:
            raise CommandError("Email is required.")
        if not name:
            raise CommandError("Name is required.")
        if not password:
            raise CommandError("Password is required.")

        if User.objects.filter(email=email).exists():
            raise CommandError("A user with this email already exists.")

        user = User.objects.create_user(
            email=email,
            name=name,
            password=password,
            user_type=User.USER_TYPE_ADMIN,
            is_staff=True,
            is_active=True,
        )

        self.stdout.write(self.style.SUCCESS(f"Admin user created: {user.email}"))
