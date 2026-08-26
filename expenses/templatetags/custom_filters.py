from django import template

register = template.Library()

@register.filter
def divide(value, arg):
    """Divides the value by arg."""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError, TypeError):
        return 0

@register.filter
def multiply(value, arg):
    """Multiplies the value by arg."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
