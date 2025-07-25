from django import template

register = template.Library()

@register.filter
def stars(value: int): 
    return range(value)