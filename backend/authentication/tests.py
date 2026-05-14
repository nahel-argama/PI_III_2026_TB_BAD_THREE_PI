from io import StringIO

from django.core.management import call_command, CommandError
from django.test import TestCase
from unittest.mock import patch

from users.models import User


class CreateAdminUserCommandTestCase(TestCase):
    def test_create_admin_user_interactively(self):
        with patch("builtins.input", side_effect=["admin@example.com", "Admin User"]), patch(
            "getpass.getpass", return_value="SecurePass123"
        ):
            output = StringIO()
            call_command("create_admin_user", stdout=output)

        user = User.objects.get(email="admin@example.com")
        self.assertEqual(user.name, "Admin User")
        self.assertEqual(user.user_type, User.USER_TYPE_ADMIN)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password("SecurePass123"))

    def test_create_admin_user_rejects_existing_email(self):
        User.objects.create_user(
            email="admin@example.com",
            name="Existing Admin",
            password="SecurePass123",
            user_type=User.USER_TYPE_ADMIN,
            is_staff=True,
            is_active=True,
        )

        with patch("builtins.input", side_effect=["admin@example.com", "Admin User"]), patch(
            "getpass.getpass", return_value="SecurePass123"
        ):
            with self.assertRaises(CommandError):
                call_command("create_admin_user")
