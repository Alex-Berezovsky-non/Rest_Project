from django.views.generic import ListView, DetailView
from django.utils import timezone  
from .models import Event

class UpcomingEventsView(ListView):
    model = Event
    template_name = 'events/upcoming.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(
            is_active=True,
            date__gte=timezone.now()  
        ).order_by('date')

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'