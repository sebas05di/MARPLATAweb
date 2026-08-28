def format_price(value):
    """Format a number as Colombian pesos: dot as thousands separator, no decimals.

    Examples:
        110000 -> "110.000"
        1500000 -> "1.500.000"
    """
    if value is None or value == '':
        return value
    try:
        number = float(value)
        return '{:,.0f}'.format(number).replace(',', '.')
    except (ValueError, TypeError):
        return value
