from datetime import time
from typing import Any, Dict, List
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.forms import BaseModelForm
from django.db.models import QuerySet
from .models import Table, Reservation
from .forms import ReservationForm


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/create.html'
    success_url = reverse_lazy('reservations:success')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        available_tables: QuerySet[Table] = form.fields['table'].queryset

        if not available_tables.exists():
            messages.error(
                self.request,
                "Нет свободных столиков на выбранное время. Попробуйте другое время или уменьшите количество гостей."
            )
            return self.form_invalid(form)

        form.instance.table = available_tables.first()
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Бронирование успешно создано! Столик №{form.instance.table.number}"
        )
        return response


class TableAvailabilityAPIView(TemplateView):
    def get(self, request: Any, *args: Any, **kwargs: Any) -> JsonResponse:
        date = request.GET.get('date', timezone.now().date())
        time_val = request.GET.get('time', '19:00')
        
        try:
            hours, minutes = map(int, time_val.split(':'))
            time_obj = time(hours, minutes)
        except (ValueError, AttributeError):
            time_obj = time(19, 0)
        
        tables: QuerySet[Table] = Table.objects.all()
        reserved_tables: QuerySet[int] = Reservation.objects.filter(
            date=date,
            time__lte=time_obj
        ).values_list('table_id', flat=True)
        
        data: List[Dict[str, Any]] = []
        for table in tables:
            table_data = {
                'id': table.id,
                'number': table.number,
                'seats': table.seats,
                'x_pos': table.x_pos,
                'y_pos': table.y_pos,
                'color': table.color or '#4CAF50',
                'rotation': table.rotation or 0,
                'is_vip': table.is_vip,
                'is_reserved': table.id in reserved_tables
            }
            if table_data['is_reserved']:
                table_data['color'] = '#F44336'
            data.append(table_data)
        
        return JsonResponse(data, safe=False)


success_view = TemplateView.as_view(template_name='reservations/success.html')