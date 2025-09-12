from django.urls import path
from .views import (
    home,
    category,
    budget,
    create_category,
    edit_category,
    remove_category,
    create_budget,
    edit_budget,
    remove_budget,
    transaction,
    create_transaction,
    edit_transaction,
    remove_transaction,
    report,
)

app_name = "expense_income"
urlpatterns = [
    path("", home, name="home"),
    path("budget", budget, name="budget"),
    path("budget/create", create_budget, name="create_budget"),
    path("budget/edit/<int:id_budget>", edit_budget, name="edit_budget"),
    path("budget/remove/<int:id_budget>", remove_budget, name="remove_budget"),
    path("category", category, name="category"),
    path("category/create", create_category, name="create_category"),
    path("category/edit/<int:id_category>", edit_category, name="edit_category"),
    path("category/remove/<int:id_category>", remove_category, name="remove_category"),
    path("transaction", transaction, name="transaction"),
    path("transaction/create", create_transaction, name="create_transaction"),
    path(
        "transaction/edit/<int:id_transaction>",
        edit_transaction,
        name="edit_transaction",
    ),
    path(
        "transaction/remove/<int:id_transaction>",
        remove_transaction,
        name="remove_transaction",
    ),
    path("reports", report, name="reports"),
]
