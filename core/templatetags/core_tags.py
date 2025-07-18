from django import template
from django.utils import timezone

register = template.Library()

@register.simple_tag
def current_time(format_string='%H:%M'):
    """Возвращает текущее время в указанном формате"""
    return timezone.now().strftime(format_string)

@register.inclusion_tag('core/includes/_social_links.html')
def show_social_links():
    """Генерирует блок соц-сетей"""
    return {
        'links': [
            {'name': 'Instagram', 'url': '#'},
            {'name': 'Facebook', 'url': '#'},
        ]
    }