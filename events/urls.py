from django.urls import path
from .views import UpcomingEventsView, EventDetailView

app_name = 'events' 
urlpatterns = [
    path('', UpcomingEventsView.as_view(), name='upcoming_events'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),
]