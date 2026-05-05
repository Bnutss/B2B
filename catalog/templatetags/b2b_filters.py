from django import template

register = template.Library()


@register.filter
def fmt_price(value):
    """Format number as price with space thousands separator: 160000 → 160 000"""
    try:
        n = int(float(str(value).replace(',', '.')))
        return f'{n:,}'.replace(',', ' ')
    except (ValueError, TypeError):
        return value
