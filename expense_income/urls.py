from django.urls import path
from .views import home

app_name = 'expense_income'
urlpatterns = [
    path('', home, name="home")
]
