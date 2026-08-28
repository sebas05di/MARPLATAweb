from django import template

from apps.core.formatting import format_price

register = template.Library()


@register.filter(name='price')
def price(value):
    """Format a number as Colombian pesos: dot as thousands separator, no decimals."""
    return format_price(value)
