from django import template

from apps.core.formatting import format_price

register = template.Library()


@register.filter(name='price')
def price(value):
    """Format a number as Colombian pesos: dot as thousands separator, no decimals."""
    return format_price(value)


@register.filter(name='format_whatsapp')
def format_whatsapp(value):
    """Format a WhatsApp number like 573052432022 as +57 305 243 2022."""
    if not value:
        return value
    digits = str(value).strip().lstrip('+')
    if len(digits) == 12 and digits.startswith('57'):
        return f"+{digits[:2]} {digits[2:5]} {digits[5:8]} {digits[8:]}"
    return value
