from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class ReportTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="paul@test.com", password="password123"
        )
        self.url = reverse("expense_income:reports")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        login_url = reverse("accounts:login")
        self.assertRedirects(response, f"{login_url}?next={self.url}")

    def test_redirect_if_logged_in(self):
        self.client.login(email="paul@test.com", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
