from django.urls import path
from .views import UpcomingEventsView, EventDetailView

urlpatterns = [
    path('', UpcomingEventsView.as_view(), name='upcoming_events'),
    path('<int:pk>/', EventDetailView.as_view(), name='event_detail'),
]