from django.urls import path
from .views import (
    ReservationCreateView, 
    success_view, 
    TableAvailabilityAPIView,
    HallMapView  
)

app_name = 'reservations'

urlpatterns = [
    path('', ReservationCreateView.as_view(), name='create'),
    path('success/', success_view, name='success'),
    path('api/tables/availability/', TableAvailabilityAPIView.as_view(), name='tables-availability'),
    path('map/', HallMapView.as_view(), name='map'),
]