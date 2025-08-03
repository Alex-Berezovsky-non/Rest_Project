from django.views.generic import ListView, TemplateView
from reviews.models import Review
from typing import Any

class HomeView(ListView):
    template_name = 'core/home.html'
    model = Review
    context_object_name = 'reviews'
    paginate_by = 5  # Пагинация
    
    def get_queryset(self):
        return Review.objects.filter(is_published=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Главная',
            'welcome_message': 'Добро пожаловать в Al Dente!',
            'address': 'г. Москва, ул. Гастрономическая, 15',  # Единый адрес
            'phone': '+7 (495) 123-45-67',  # Единый телефон
            'email': 'info@aldente.ru',
            'working_hours': '12:00 - 23:00 (без выходных)'
        })
        return context

class ContactsView(TemplateView):
    template_name = 'core/contacts.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Контакты',
            'address': 'г. Москва, ул. Гастрономическая, 15',
            'phone': '+7 (495) 123-45-67',
            'email': 'info@aldente.ru',
            'working_hours': '12:00 - 23:00 (без выходных)',
            'social_links': {
                'instagram': '#',
                'facebook': '#',
                'telegram': '#'
            }
        })
        return context