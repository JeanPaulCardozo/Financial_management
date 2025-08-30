from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Custom form create user"""

    class Meta:
        """Meta form"""

        model = User
        fields = ["name", "email", "password1", "password2"]
