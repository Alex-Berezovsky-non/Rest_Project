from django.views.generic import ListView, TemplateView
from reviews.models import Review
from typing import Any

class HomeView(ListView):
    template_name = 'core/home.html'
    model = Review
    context_object_name = 'reviews'
    
    def get_queryset(self):
        # Возвращаем только опубликованные отзывы, отсортированные по дате
        return Review.objects.filter(is_published=True).order_by('-created_at')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Главная',
            'welcome_message': 'Добро пожаловать в Al Dente!',
            'address': 'ул. Итальянская, 42',
            'phone': '+7 (123) 456-78-90'
        })
        return context

class ContactsView(TemplateView):
    template_name = 'core/contacts.html'
    extra_context = {
        'page_title': 'Контакты',
        'address': 'ул. Итальянская, 42',
        'phone': '+7 (123) 456-78-90'
    }