from django import template
from typing import Union

register = template.Library()

@register.filter(name='stars')
def stars(value: Union[str, int, float]) -> range:
    return range(int(value))