from django import template
from django.utils.html import escape, format_html
register = template.Library()

@register.simple_tag
def cut_text(text):
    b = text[:70]
    return b

@register.simple_tag
def price(cart):
    b = (len(cart) * 100 ) - 30
    return b

@register.simple_tag
def cart_count(request):
    if request.session.get('cart') is None:
        return ""
    elif len(request.session.get('cart')) == 0:
        return ""
    count =  format_html(f"<span class='badge badge-secondary badge-pill'> {len(request.session.get('cart'))}</span>")
    return count

