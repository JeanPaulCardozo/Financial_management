from django.urls import path
from .views import home, category, budget, create_category,edit_category,remove_category

app_name = 'expense_income'
urlpatterns = [
    path('', home, name="home"),
    path('budget/', budget, name='budget'),
    path('category/', category, name='category'),
    path('category/create', create_category, name="create_category"),
    path('category/edit/<int:id_category>', edit_category, name="edit_category"),
    path('category/remove/<int:id_category>',remove_category,name="remove_category")
]
