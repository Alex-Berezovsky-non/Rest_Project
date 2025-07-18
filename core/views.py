from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
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