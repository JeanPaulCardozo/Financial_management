from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category


@login_required(login_url='/login')
def home(request):
    """Home page"""
    return render(request, 'expense_income/home.html')


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
               'order_income': order_income, 'order_expense': order_expense
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
    category = Category.objects.get(id_category=id_category)
    category.delete()
    return redirect('expense_income:category')


@login_required(login_url='/login')
def budget(request):
    return render(request, 'expense_income/budget.html')
