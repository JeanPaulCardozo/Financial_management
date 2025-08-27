from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Budget
from datetime import datetime
from django.db.models.functions import ExtractMonth, ExtractYear
import calendar
import locale

# change languege to spanish
# This action return the name of month in spanish
locale.setlocale(locale.LC_TIME, "es_CO.UTF-8")


@login_required(login_url='/login')
def home(request):
    """Home page"""
    context = {"type_page": "home"}
    return render(request, 'expense_income/home.html', context)


@login_required(login_url='/login')
def category(request):
    """Category Section"""
    choices_category = Category.TypeCategory.choices
    order_income = request.GET.get("order_income", "asc")
    order_expense = request.GET.get("order_expense", "asc")
    list_categories_expenses = Category.objects.filter(
        user=request.user, type_category=Category.TypeCategory.EXPENSE)
    list_categories_incomes = Category.objects.filter(
        user=request.user, type_category=Category.TypeCategory.INCOME)

    categories_expense = list_categories_expenses.order_by(
        'name_category' if order_expense == "asc" else "-name_category")
    categories_income = list_categories_incomes.order_by(
        'name_category' if order_income == "asc" else "-name_category")
    order_income = "asc" if order_income == "asc" else "desc"
    order_expense = "asc" if order_expense == "asc" else "desc"

    context = {'choices_category': choices_category, 'user': request.user,
               'categories_income': categories_income,
               'categories_expense': categories_expense,
               'order_income': order_income, 'order_expense': order_expense,
               'type_page': 'category'
               }

    return render(request, 'expense_income/category.html', context)


@login_required(login_url='/login')
def create_category(request):
    """Create Category"""
    if request.method == 'POST':
        name = request.POST['category_name']
        category_type = request.POST['category_type']
        Category.objects.create(
            name_category=name, type_category=category_type, user=request.user)
        return redirect('expense_income:category')


@login_required(login_url='/login')
def edit_category(request, id_category):
    """Edit Category"""
    if request.method == 'POST':
        name = request.POST['category_name']
        category_type = request.POST['category_type']
        category = Category.objects.get(
            user=request.user, id_category=id_category)
        category.name_category = name
        category.type_category = category_type
        category.save()

        return redirect('expense_income:category')


@login_required(login_url='/login')
def remove_category(request, id_category):
    """Remove Category"""
    category = Category.objects.get(id_category=id_category, user=request.user)
    category.delete()
    return redirect('expense_income:category')


@login_required(login_url='/login')
def budget(request):
    """home budget"""

    # Options Period and Category
    choice_period = Budget.Period.choices
    choice_category = Category.objects.filter(user=request.user)

    # Get Year, Month and name category
    current_year = request.GET.get("year", datetime.now().year)
    current_month = request.GET.get("month", datetime.now().month)
    category_name = request.GET.get("q", "")

    budget_list = Budget.objects.filter(user=request.user)

    if category_name:
        my_budgets = budget_list.filter(date__year=current_year, date__month=current_month,
                                        category__name_category__icontains=category_name).order_by("-date")
    else:
        my_budgets = budget_list.filter(
            date__year=current_year, date__month=current_month).order_by("-date")

    list_years = budget_list.annotate(year=ExtractYear('date')).values_list(
        'year', flat=True).distinct().order_by("-year")

    # Get Months by Year
    get_months_by_year = budget_list.annotate(
        year=ExtractYear('date')).filter(year=current_year).distinct()
    list_months = get_months_by_year.annotate(number_month=ExtractMonth(
        'date')).values('number_month').order_by('number_month').distinct()
    for month in list_months:
        month["month"] = calendar.month_name[month["number_month"]].capitalize()

    context = {"type_page": "budget", "choice_period": choice_period,
               "choice_category": choice_category, 'user': request.user,
               "my_budgets": my_budgets,
               "list_years": list_years, "list_months": list_months}
    return render(request, 'expense_income/budget.html', context)


@login_required(login_url='/login')
def create_budget(request):
    """Create budget"""
    if request.method == "POST":
        category_id = request.POST["category"]
        category_instance = Category.objects.get(id_category=category_id)

        amount = request.POST["amount_budget"]
        period = request.POST["period"]

        Budget.objects.create(budget_limit=amount, date=datetime.now(
        ), period=period, user=request.user, category=category_instance)

        return redirect('expense_income:budget')


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

        return redirect('expense_income:budget')


@login_required(login_url="/login")
def remove_budget(request, id_budget):
    """Remove Budget"""
    budget = Budget.objects.get(id_budget=id_budget, user=request.user)
    budget.delete()

    return redirect('expense_income:budget')
