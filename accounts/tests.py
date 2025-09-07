# cuentas/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Creamos un usuario de prueba
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
            name="Test User"
        )

    # -----------------------------
    # Test login
    # -----------------------------
    def test_login_user_success(self):
        response = self.client.post(reverse("accounts:login"), {
            "email": "test@example.com",
            "password": "testpassword"
        })
        self.assertRedirects(response, reverse("expense_income:home"))

    def test_login_user_fail(self):
        response = self.client.post(reverse("accounts:login"), {
            "email": "wrong@example.com",
            "password": "wrongpassword"
        })
        self.assertContains(response, "Credenciales Incorrectas")

    # -----------------------------
    # Test logout
    # -----------------------------
    def test_logout_view(self):
        self.client.login(email="test@example.com", password="testpassword")
        response = self.client.get(reverse("accounts:logout_view"))
        self.assertTemplateUsed(response, "accounts/login.html")

    # -----------------------------
    # Test settings requiere login
    # -----------------------------
    def test_settings_requires_login(self):
        response = self.client.get(reverse("accounts:settings"))
        self.assertRedirects(response, "/login?next=/settings")

    def test_settings_logged_in(self):
        self.client.login(email="test@example.com", password="testpassword")
        response = self.client.get(reverse("accounts:settings"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/Settings.html")
        self.assertContains(response, "Test User")

    # -----------------------------
    # Test update_user
    # -----------------------------
    def test_update_user(self):
        self.client.login(email="test@example.com", password="testpassword")
        response = self.client.post(reverse("accounts:update_user"), {
            "username": "New Name",
            "email": "newemail@example.com"
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "New Name")
        self.assertEqual(self.user.email, "newemail@example.com")
        self.assertRedirects(response, reverse("accounts:settings"))

    # -----------------------------
    # Test update_password
    # -----------------------------
    def test_update_password(self):
        self.client.login(email="test@example.com", password="testpassword")
        response = self.client.post(reverse("accounts:update_password"), {
            "new_password": "newpass123",
            "confirm_password": "newpass123"
        })
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass123"))
        self.assertRedirects(response, reverse("accounts:settings"))

    # -----------------------------
    # Test register_user
    # -----------------------------
    def test_register_user_get(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_register_user_post_valid(self):
        response = self.client.post(reverse("accounts:register"), {
            "email": "newuser@example.com",
            "name": "New User",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123"
        })
        self.assertRedirects(response, reverse("accounts:login"))
        new_user = User.objects.get(email="newuser@example.com")
        self.assertIsNotNone(new_user)

    def test_register_user_post_invalid(self):
        response = self.client.post(reverse("accounts:register"), {
            "email": "invalid-email",
            "name": "",
            "password1": "123",
            "password2": "456"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertContains(response, "error")
