from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Budget, Transaction
from datetime import datetime
from django.db.models.functions import ExtractMonth, ExtractYear, Coalesce
from django.db.models import Sum, Value, DecimalField, F
import calendar
import locale

# change languege to spanish
# This action return the name of month in spanish
locale.setlocale(locale.LC_TIME, "es_CO.UTF-8")


@login_required(login_url="/login")
def home(request):
    """Home page"""
    transactions = Transaction.objects.filter(user=request.user).order_by("-date")[:3]
    choices_method = Transaction.PaymentMethod.choices
    budgets = Budget.objects.filter(user=request.user)
    category_expense = Category.TypeCategory.EXPENSE

    current_month = datetime.now().month
    current_year = datetime.now().year
    total_budget = (
        budgets.annotate(number_month=ExtractMonth("date"), year=ExtractYear("date"))
        .filter(number_month=current_month, year=current_year)
        .aggregate(total=Sum("budget_limit"))
    )
    total_balance = (
        Transaction.objects.filter(user=request.user)
        .annotate(number_month=ExtractMonth("date"), year=ExtractYear("date"))
        .filter(number_month=current_month, year=current_year)
        .aggregate(total=Sum("amount"))
    )
    total_remaining = total_budget["total"] - total_balance["total"]

    context = {
        "type_page": "home",
        "user": request.user,
        "transactions": transactions,
        "category_expense": category_expense,
        "choices_method": choices_method,
        "choices_budget": budgets,
        "budget_info": total_budget,
        "total_balance": total_balance,
        "total_remaining": total_remaining,
    }
    request.session["info_type_page"] = {"type_page": "home"}
    return render(request, "expense_income/home.html", context)


@login_required(login_url="/login")
def category(request):
    """Category Section"""
    choices_category = Category.TypeCategory.choices
    order_income = request.GET.get("order_income", "asc")
    order_expense = request.GET.get("order_expense", "asc")
    list_categories_expenses = Category.objects.filter(
        user=request.user, type_category=Category.TypeCategory.EXPENSE
    )
    list_categories_incomes = Category.objects.filter(
        user=request.user, type_category=Category.TypeCategory.INCOME
    )

    categories_expense = list_categories_expenses.order_by(
        "name_category" if order_expense == "asc" else "-name_category"
    )
    categories_income = list_categories_incomes.order_by(
        "name_category" if order_income == "asc" else "-name_category"
    )
    order_income = "asc" if order_income == "asc" else "desc"
    order_expense = "asc" if order_expense == "asc" else "desc"

    context = {
        "choices_category": choices_category,
        "user": request.user,
        "categories_income": categories_income,
        "categories_expense": categories_expense,
        "order_income": order_income,
        "order_expense": order_expense,
        "type_page": "category",
    }

    return render(request, "expense_income/category.html", context)


@login_required(login_url="/login")
def create_category(request):
    """Create Category"""
    if request.method == "POST":
        name = request.POST["category_name"]
        category_type = request.POST["category_type"]
        Category.objects.create(
            name_category=name, type_category=category_type, user=request.user
        )
        return redirect("expense_income:category")


@login_required(login_url="/login")
def edit_category(request, id_category):
    """Edit Category"""
    if request.method == "POST":
        name = request.POST["category_name"]
        category_type = request.POST["category_type"]
        category = Category.objects.get(user=request.user, id_category=id_category)
        category.name_category = name
        category.type_category = category_type
        category.save()

        return redirect("expense_income:category")


@login_required(login_url="/login")
def remove_category(request, id_category):
    """Remove Category"""
    category = Category.objects.get(id_category=id_category, user=request.user)
    category.delete()
    return redirect("expense_income:category")


@login_required(login_url="/login")
def budget(request):
    """home budget"""

    # Options Period and Category
    choice_period = Budget.Period.choices
    choice_category = Category.objects.filter(user=request.user)

    # Get Year, Month and name category
    current_year = request.GET.get("year", datetime.now().year)
    current_month = request.GET.get("month", datetime.now().month)
    category_name = request.GET.get("q", "")

    budget_list = Budget.objects.filter(user=request.user).annotate(
        balance=Coalesce(
            Sum("transaction__amount"), Value(0, output_field=DecimalField())
        ),
        remaining=F("budget_limit")
        - Coalesce(Sum("transaction__amount"), Value(0, output_field=DecimalField())),
        percent=(
            Coalesce(Sum("transaction__amount"), Value(0, output_field=DecimalField()))
            / F("budget_limit")
        )
        * 100,
    )
    if category_name:
        my_budgets = budget_list.filter(
            date__year=current_year,
            date__month=current_month,
            category__name_category__icontains=category_name,
        ).order_by("-date")
    else:
        my_budgets = budget_list.filter(
            date__year=current_year, date__month=current_month
        ).order_by("-date")

    list_years = (
        budget_list.annotate(year=ExtractYear("date"))
        .values_list("year", flat=True)
        .distinct()
        .order_by("-year")
    )

    # Get Months by Year
    get_months_by_year = (
        budget_list.annotate(year=ExtractYear("date"))
        .filter(year=current_year)
        .distinct()
    )
    list_months = (
        get_months_by_year.annotate(number_month=ExtractMonth("date"))
        .values("number_month")
        .order_by("number_month")
        .distinct()
    )
    for month in list_months:
        month["month"] = calendar.month_name[month["number_month"]].capitalize()

    context = {
        "type_page": "budget",
        "choice_period": choice_period,
        "choice_category": choice_category,
        "user": request.user,
        "my_budgets": my_budgets,
        "list_years": list_years,
        "list_months": list_months,
    }
    return render(request, "expense_income/budget.html", context)


@login_required(login_url="/login")
def create_budget(request):
    """Create budget"""
    if request.method == "POST":
        category_id = request.POST["category"]
        category_instance = Category.objects.get(id_category=category_id)

        amount = request.POST["amount_budget"]
        period = request.POST["period"]

        Budget.objects.create(
            budget_limit=amount,
            date=datetime.now(),
            period=period,
            user=request.user,
            category=category_instance,
        )

        return redirect("expense_income:budget")


@login_required(login_url="/login")
def edit_budget(request, id_budget):
    """Edit Budget"""
    if request.method == "POST":
        category_id = request.POST["category"]
        category_instance = Category.objects.get(id_category=category_id)
        budget = Budget.objects.get(user=request.user, id_budget=id_budget)
        budget.budget_limit = request.POST["amount_budget"]
        budget.period = request.POST["period"]
        budget.category = category_instance
        budget.save()

        return redirect("expense_income:budget")


@login_required(login_url="/login")
def remove_budget(request, id_budget):
    """Remove Budget"""
    budget = Budget.objects.get(id_budget=id_budget, user=request.user)
    budget.delete()

    return redirect("expense_income:budget")


@login_required(login_url="/login")
def transaction(request):
    """Get Transaction Home"""
    transactions = Transaction.objects.filter(user=request.user).order_by("-date")
    choices_method = Transaction.PaymentMethod.choices
    choices_budget = Budget.objects.filter(user=request.user)
    category_expense = Category.TypeCategory.EXPENSE
    context = {
        "transactions": transactions,
        "type_page": "transaction",
        "choices_method": choices_method,
        "choices_budget": choices_budget,
        "category_expense": category_expense,
    }

    request.session["info_type_page"] = {"type_page": "transaction"}

    return render(request, "expense_income/transaction.html", context)


@login_required(login_url="/login")
def create_transaction(request):
    """Create Transaction"""
    if request.method == "POST":
        title = request.POST["transaction_title"]
        method = request.POST["transaction_method"]
        amount = request.POST["transaction_amount"]
        notes = request.POST["transaction_notes"]
        budget = request.POST["transaction_budget"]

        budget_instance = Budget.objects.get(id_budget=budget)

        Transaction.objects.create(
            date=datetime.now(),
            budget=budget_instance,
            user=request.user,
            title=title,
            payment_method=method,
            amount=amount,
            notes=notes,
        )

        response_session = request.session.get("info_type_page", {})

        return redirect(
            "expense_income:home"
            if response_session["type_page"] == "home"
            else "expense_income:transaction"
        )


@login_required(login_url="/login")
def edit_transaction(request, id_transaction):
    """Edit Transaction"""
    if request.method == "POST":
        transaction = Transaction.objects.get(
            id_transaction=id_transaction, user=request.user
        )

        budget = Budget.objects.get(
            id_budget=request.POST["transaction_budget"], user=request.user
        )

        transaction.title = request.POST["transaction_title"]
        transaction.payment_method = request.POST["transaction_method"]
        transaction.amount = request.POST["transaction_amount"]
        transaction.notes = request.POST["transaction_notes"]
        transaction.budget = budget

        transaction.save()

        return redirect("expense_income:transaction")


@login_required(login_url="/login")
def remove_transaction(request, id_transaction):
    """Remove Transaction"""
    transaction = Transaction.objects.get(
        id_transaction=id_transaction, user=request.user
    )
    transaction.delete()

    return redirect("expense_income:transaction")
