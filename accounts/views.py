from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm


def login_user(request):
    """Login"""
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
             # Si hay un "next", redirige allí, si no, al home
            next_url = request.GET.get('next') or request.POST.get('next')
            return redirect(next_url if next_url else 'expense_income:home')
    return render(request, 'accounts/login.html', {'message': 'Credenciales incorrectas'})


def register_user(request):
    """Register"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Use UserManager Model
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
