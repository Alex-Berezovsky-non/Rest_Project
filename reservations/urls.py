from django.urls import path
from .views import ReservationCreateView, success_view, TableAvailabilityAPIView
from django.views.generic import TemplateView
app_name = 'reservations'

urlpatterns = [
    path('', ReservationCreateView.as_view(), name='create'),
    path('success/', success_view, name='success'),
    path('api/tables/availability/', TableAvailabilityAPIView.as_view(), name='tables-availability'),
    path('map/', TemplateView.as_view(template_name='reservations/map.html'), name='map'),
     path('tables/availability/', TableAvailabilityAPIView.as_view(), name='tables-availability'),
]