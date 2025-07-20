from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Reservation, Table  
from .forms import ReservationForm

class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/create.html'
    success_url = reverse_lazy('reservations:success')

    def form_valid(self, form):

        guests = form.cleaned_data['guests']
        date = form.cleaned_data['date']
        time = form.cleaned_data['time']
        
        available_tables = Table.objects.filter(
            seats__gte=guests
        ).exclude(
            reservation__date=date,
            reservation__time=time
        ).order_by('seats')
        
        if not available_tables:
            messages.error(self.request, "Нет доступных столиков на выбранное время")
            return self.form_invalid(form)
            
        form.instance.table = available_tables.first()
        response = super().form_valid(form)
        messages.success(self.request, "Бронирование успешно создано!")
        return response

success_view = TemplateView.as_view(template_name='reservations/success.html')