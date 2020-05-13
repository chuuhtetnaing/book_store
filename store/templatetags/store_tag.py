from django import template

register = template.Library()

@register.simple_tag
def cut_text(text):
    b = text[:70]
    return b