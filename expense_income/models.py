from django.db import models
from accounts.models import User

# Create your models here.


class Category(models.Model):
    """ "Model Category"""

    class TypeCategory(models.TextChoices):
        """Choice Type Category"""

        INCOME = "ingreso", "Ingreso"
        EXPENSE = "gasto", "Gasto"

    id_category = models.AutoField(primary_key=True)
    name_category = models.CharField(max_length=200)
    type_category = models.CharField(max_length=10, choices=TypeCategory.choices)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_category


class Budget(models.Model):
    """Model Budget"""

    class Period(models.TextChoices):
        """Choice Period"""

        MONTHLY = "mensual", "Mensual"
        WEEKLY = "semanal", "Semanal"

    id_budget = models.AutoField(primary_key=True)
    budget_limit = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    period = models.CharField(max_length=10, choices=Period.choices)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name_category


class Transaction(models.Model):
    """Model Transaction"""

    class PaymentMethod(models.TextChoices):
        """Choice Payment Method"""

        CASH = "efectivo", "Efectivo"
        CARD = "tarjeta", "Tarjeta"
        TRANSFER = "transaccion", "Transacción"

    id_transaction = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    payment_method = models.CharField(max_length=12, choices=PaymentMethod.choices)
    notes = models.TextField()
    title = models.CharField(max_length=200)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, null=True)
