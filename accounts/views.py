from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


@login_required(login_url="login/")
def update_password(request):
    """Update Password"""
    if request.method == "POST":
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

        user = request.user
        if user and new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect(
                "accounts:settings"
            )  # Redirect to settings page after update


@login_required(login_url="login/")
def update_user(request):
    """Update User Information"""
    if request.method == "POST":
        user = request.user
        username = request.POST["username"]
        email = request.POST["email"]

        user.name = username
        user.email = email
        user.save()
        return redirect("accounts:settings")  # Redirect to settings page after update

    context = {"type_page": "settings", "user": request.user}
    return render(request, "accounts/Settings.html", context)


def logout_view(request):
    """Logout view"""
    logout(request)
    return render(request, "accounts/login.html")


@login_required(login_url="login/")
def settings(request):
    """Settings Page"""
    context = {"type_page": "settings", "user": request.user}
    return render(request, "accounts/Settings.html", context)


def login_user(request):
    """Login"""
    global context
    context = {"message": ""}
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)

            request.session.set_expiry(3600)  # expire in 1 hour

            # If there's a "next", redirect there, if not, to home
            next_url = request.GET.get("next") or request.POST.get("next")
            return redirect(next_url if next_url else "expense_income:home")

        context = {"message": "Credenciales Incorrectas"}
    return render(request, "accounts/login.html", context)


def register_user(request):
    """Register"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Use UserManager Model
            return redirect("accounts:login")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})
