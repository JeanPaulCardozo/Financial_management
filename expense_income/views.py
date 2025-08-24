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
    categories_expense = Category.objects.filter(
        user=request.user, type_category=Category.TypeCategory.EXPENSE).order_by('-id_category')
    categories_income = Category.objects.filter(
        user=request.user, type_category=Category.TypeCategory.INCOME).order_by('-id_category')
    context = {'choices_category': choices_category, 'user': request.user,
               'categories_income': categories_income,
               'categories_expense': categories_expense}

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
def edit_category(request,id_category):
    """Edit Category"""
    if request.method == 'POST':
        name = request.POST['category_name']
        category_type = request.POST['category_type']
        category = Category.objects.get(user = request.user, id_category = id_category)
        category.name_category = name
        category.type_category = category_type
        category.save()

        return redirect('expense_income:category')
    

@login_required(login_url='/login')
def budget(request):
    return render(request, 'expense_income/budget.html')
