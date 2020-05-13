from django import template
from store.models import Genre

register = template.Library()

@register.simple_tag
def genres():
    b = [a.genre for a in Genre.objects.all()]
    b.sort()
    return b

@register.simple_tag
def cut_text(text):
    b = text[:70]
    return b