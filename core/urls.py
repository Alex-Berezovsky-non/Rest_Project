from django.urls import path
from .views import HomeView, ContactsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),       # Главная страница /
    path('contacts/', ContactsView.as_view(), name='contacts'),  # Контакты /contacts/
]