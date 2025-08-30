"""tag to greet"""

from django import template
from datetime import datetime

register = template.Library()


@register.filter
def greet(value=None):
    """get Greet by hour"""
    hora = datetime.now().hour
    if 6 <= hora < 12:
        return "Buenos días"
    elif 12 <= hora < 18:
        return "Buenas tardes"
    else:
        return "Buenas noches"
