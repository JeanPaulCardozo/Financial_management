from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Transaction, Budget, Category
from django.utils import timezone

User = get_user_model()


class ReportTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@test.com", password="password123"
        )
        self.url = reverse("expense_income:reports")

    def test_redirect_if_not_logged_in(self):
        """Validate if user is not logged in, redirect to login"""
        response = self.client.get(self.url)
        login_url = reverse("accounts:login")
        self.assertRedirects(response, f"{login_url}?next={self.url}")

    def test_redirect_if_logged_in(self):
        """ "
        Validate if user is logged in"""
        self.client.login(email="test@test.com", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def tesxt_report_context_keys(self):
        """Validate de context contains the expected keys"""
        self.client.login(email="test@test.com", password="password123")
        response = self.client.get(self.url)
        for key in [
            "expenses_by_category",
            "monthly_summary",
            "budget_vs_spent",
            "payments",
            "top_transactions",
            "type_page",
        ]:
            self.assertIn(key, response.context)

    def test_expenses_by_category_calculation(self):
        """Validate category calculation in report view"""
        self.client.login(email="test@test.com", password="password123")

        cat = Category.objects.create(
            name_category="Comida",
            type_category=Category.TypeCategory.EXPENSE,
            user=self.user,
        )
        budget = Budget.objects.create(
            user=self.user,
            category=cat,
            budget_limit=500,
            period=Budget.Period.MONTHLY,
            date=timezone.now(),
        )
        Transaction.objects.create(
            title="Compra 1",
            user=self.user,
            budget=budget,
            amount=200,
            date=timezone.now(),
            payment_method=Transaction.PaymentMethod.CARD,
        )

        response = self.client.get(self.url)
        expenses = response.context["expenses_by_category"]

        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["budget__category__name_category"], "Comida")
        self.assertEqual(expenses[0]["total"], 200)


class HomeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email="test@test.com", password="password123"
        )
        self.url = reverse("expense_income:home")

    def test_redirect_if_not_logged_in(self):
        """Validate if user is not logged in, redirect to login"""
        response = self.client.get(self.url)
        login_url = reverse("accounts:login")
        self.assertRedirects(response, f"{login_url}?next={self.url}")

    def test_redirect_if_logged_in(self):
        """Validate if user is logged in"""
        self.client.login(email="test@test.com", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_context_keys(self):
        """Validate the context contains the expected keys"""
        self.client.login(email="test@test.com", password="password123")
        response = self.client.get(self.url)
        for key in [
            "type_page",
            "user",
            "transactions",
            "category_expense",
            "choices_method",
            "choices_budget",
            "budget_info",
            "total_balance",
            "total_remaining",
        ]:
            self.assertIn(key, response.context)


class CategoryViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@test.com", password="password123"
        )
        self.client = Client()
        self.url = reverse("expense_income:category")
        self.category = Category.objects.create(
            name_category="Comida",
            type_category=Category.TypeCategory.EXPENSE,
            user=self.user,
        )

    def test_category_list_view(self):
        """Validate category list view"""
        self.client.login(email="test@test.com", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "expense_income/category.html")
        self.assertIn("categories_expense", response.context)
        self.assertIn("categories_income", response.context)

    def test_create_category_view(self):
        """Validate category creation"""
        self.client.login(email="test@test.com", password="password123")
        response = self.client.post(
            reverse("expense_income:create_category"),
            {"category_name": "Salud", "category_type": Category.TypeCategory.EXPENSE},
        )
        self.assertRedirects(response, self.url)
        self.assertTrue(
            Category.objects.filter(name_category="Salud", user=self.user).exists()
        )

    def test_edit_category_view(self):
        """Validate category edition"""
        self.client.login(email="test@test.com", password="password123")
        response = self.client.post(
            reverse("expense_income:edit_category", args=[self.category.id_category]),
            {
                "category_name": "Comida Editada",
                "category_type": Category.TypeCategory.EXPENSE,
            },
        )
        self.assertRedirects(response, self.url)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name_category, "Comida Editada")

    def test_remove_category_view(self):
        """Validate category removal"""
        self.client.login(email="test@test.com", password="password123")
        response = self.client.get(
            reverse("expense_income:remove_category", args=[self.category.id_category])
        )
        self.assertRedirects(response, self.url)
        self.assertFalse(
            Category.objects.filter(id_category=self.category.id_category).exists()
        )


class BudgetViewsTest(TestCase):
    def setUp(self):
        """Setup test data and test client"""
        self.client = Client()
        self.user = User.objects.create_user(email="testuser", password="password123")
        self.category = Category.objects.create(name_category="Food", user=self.user)
        self.budget = Budget.objects.create(
            budget_limit=500,
            date=timezone.now(),
            period=Budget.Period.MONTHLY,
            user=self.user,
            category=self.category,
        )
        self.url = reverse("expense_income:budget")

    def test_budget_view_authenticated(self):
        """Validate budget list view for authenticated user"""
        self.client.login(email="testuser", password="password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "expense_income/budget.html")

    def test_budget_view_redirect_if_not_logged_in(self):
        """Ensure budget view redirects unauthenticated users to login"""
        response = self.client.get(self.url)
        login_url = reverse("accounts:login")
        self.assertRedirects(response, f"{login_url}?next={self.url}")

    def test_create_budget(self):
        """Validate creating a new budget"""
        self.client.login(email="testuser", password="password123")
        response = self.client.post(
            reverse("expense_income:create_budget"),
            {
                "category": self.category.id_category,
                "amount_budget": 300,
                "period": "Monthly",
            },
        )
        self.assertEqual(Budget.objects.count(), 2)
        self.assertRedirects(response, self.url)

    def test_edit_budget(self):
        """Validate editing an existing budget"""
        self.client.login(email="testuser", password="password123")
        response = self.client.post(
            reverse("expense_income:edit_budget", args=[self.budget.id_budget]),
            {
                "category": self.category.id_category,
                "amount_budget": 800,
                "period": Budget.Period.MONTHLY,
            },
        )
        self.budget.refresh_from_db()
        self.assertEqual(self.budget.budget_limit, 800)
        self.assertEqual(self.budget.period, Budget.Period.MONTHLY)
        self.assertRedirects(response, self.url)

    def test_remove_budget(self):
        """Validate removing a budget"""
        self.client.login(email="testuser", password="password123")
        response = self.client.post(
            reverse("expense_income:remove_budget", args=[self.budget.id_budget])
        )
        self.assertEqual(Budget.objects.count(), 0)
        self.assertRedirects(response, self.url)


class TransactionViewsTest(TestCase):
    """Tests for Transaction views"""

    def setUp(self):
        """Create test user, category, and budget"""
        self.client = Client()
        self.user = User.objects.create_user(email="testuser", password="testpass")
        self.category = Category.objects.create(
            id_category=1,
            name_category="Food",
            type_category=Category.TypeCategory.EXPENSE,
            user=self.user,
        )
        self.url = reverse("expense_income:transaction")
        self.budget = Budget.objects.create(
            id_budget=1,
            budget_limit=500,
            date=timezone.now(),
            period=Budget.Period.MONTHLY,
            user=self.user,
            category=self.category,
        )
        self.transaction = Transaction.objects.create(
            id_transaction=1,
            date=timezone.now(),
            budget=self.budget,
            user=self.user,
            title="Groceries",
            payment_method=Transaction.PaymentMethod.CASH,
            amount=50,
            notes="Supermarket",
        )

    def test_transaction_view_redirect_if_not_logged_in(self):
        """Ensure transaction view redirects unauthenticated users"""
        response = self.client.get(self.url)
        login_url = reverse("accounts:login")
        self.assertRedirects(response, f"{login_url}?next={self.url}")

    def test_transaction_view_logged_in(self):
        """Validate transaction list view for logged-in user"""
        self.client.login(email="testuser", password="testpass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "expense_income/transaction.html")
        self.assertContains(response, "Groceries")

    def test_create_transaction(self):
        """Validate create transaction"""
        self.client.login(email="testuser", password="testpass")
        data = {
            "transaction_title": "Taxi",
            "transaction_method": Transaction.PaymentMethod.CARD,
            "transaction_amount": 30,
            "transaction_notes": "Airport ride",
            "transaction_budget": self.budget.id_budget,
        }
        response = self.client.post(reverse("expense_income:create_transaction"), data)
        self.assertEqual(Transaction.objects.count(), 2)
        self.assertRedirects(response, self.url)

    def test_edit_transaction(self):
        """Validate edit transaction"""
        self.client.login(email="testuser", password="testpass")
        url = reverse(
            "expense_income:edit_transaction", args=[self.transaction.id_transaction]
        )
        data = {
            "transaction_title": "Updated Groceries",
            "transaction_method": Transaction.PaymentMethod.CARD,
            "transaction_amount": 75,
            "transaction_notes": "Updated notes",
            "transaction_budget": self.budget.id_budget,
        }
        response = self.client.post(url, data)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.title, "Updated Groceries")
        self.assertEqual(self.transaction.amount, 75)
        self.assertRedirects(response, self.url)

    def test_remove_transaction(self):
        """Validate remove transaction"""
        self.client.login(email="testuser", password="testpass")
        url = reverse(
            "expense_income:remove_transaction", args=[self.transaction.id_transaction]
        )
        response = self.client.post(url)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertRedirects(response, self.url)
