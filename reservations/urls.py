from django.urls import path
from .views import ReservationCreateView, success_view 

app_name = 'reservations'

urlpatterns = [
    path('', ReservationCreateView.as_view(), name='create'),
    path('success/', success_view, name='success'),
]