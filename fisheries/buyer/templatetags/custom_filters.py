from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        # Convert arguments to Decimal for precise decimal arithmetic
        value = Decimal(str(value))
        arg = Decimal(str(arg))
        return value * arg
    except (ValueError, TypeError, InvalidOperation):
        return 0 