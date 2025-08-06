from datetime import datetime, time, timedelta
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Reservation, Table

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'table',
            'customer_name', 'customer_phone', 'customer_email',
            'date', 'time', 'duration', 'guests', 'special_requests'
        ]
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'min': timezone.now().strftime('%Y-%m-%d'),
                'max': (timezone.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'min': '12:00',
                'max': '22:30'
            }),
            'table': forms.Select(attrs={'class': 'form-control'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'guests' in self.initial:
            self.fields['table'].queryset = self.get_available_tables_for_guests(self.initial['guests'])

    def get_available_tables_for_guests(self, guests):
        """Возвращает queryset столов, подходящих для указанного количества гостей"""
        return Table.objects.filter(seats__gte=guests).order_by('seats')

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if not date:
            return date
            
        today = timezone.now().date()
        max_date = today + timedelta(days=30)
        
        if date < today:
            raise ValidationError("Нельзя забронировать столик на прошедшую дату")
        if date > max_date:
            raise ValidationError("Бронирование возможно максимум на 30 дней вперед")
        return date

    def clean_time(self):
        time_val = self.cleaned_data.get('time')
        if not time_val:
            return time_val
            
        if time_val < time(12, 0):
            raise ValidationError("Ресторан открывается в 12:00")
        if time_val >= time(23, 0):
            raise ValidationError("Последнее бронирование до 23:00")
        return time_val

    def clean_guests(self):
        guests = self.cleaned_data.get('guests')
        if not guests:
            return guests
            
        if guests <= 0:
            raise ValidationError("Укажите корректное количество гостей")
        if guests > 12:
            raise ValidationError("Максимальное количество гостей - 12")

        if 'table' in self.fields:
            self.fields['table'].queryset = self.get_available_tables_for_guests(guests)
            
        return guests

    def clean_duration(self):
        duration = self.cleaned_data.get('duration', 2)
        if duration < 1 or duration > 6:
            raise ValidationError("Длительность должна быть от 1 до 6 часов")
        return duration

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time_val = cleaned_data.get('time')
        duration = cleaned_data.get('duration', 2)
        guests = cleaned_data.get('guests')  
        table = cleaned_data.get('table')

        if date and time_val:
            try:
                booking_datetime = timezone.make_aware(datetime.combine(date, time_val))
                now = timezone.now()
                
                if (booking_datetime - now).total_seconds() < 7200:
                    self.add_error('time', "Бронируйте минимум за 2 часа")
            except (TypeError, ValueError):
                self.add_error(None, "Некорректные данные даты или времени")

        if time_val and duration:
            try:
                end_time = (datetime.combine(datetime.today(), time_val) + 
                          timedelta(hours=duration)).time()
                if end_time > time(23, 0):
                    self.add_error(
                        'duration',
                        "Бронь заканчивается после закрытия ресторана (23:00). "
                        "Уменьшите продолжительность или выберите более раннее время."
                    )
            except (TypeError, ValueError):
                self.add_error(None, "Некорректные данные времени или длительности")

        if date and time_val and duration and guests:
            try:
                available_tables = Table.get_available_tables(
                    date, time_val, duration, guests
                )
                
                if not available_tables.exists():
                    raise ValidationError(
                        "Нет свободных столиков на выбранное время. "
                        "Попробуйте другое время или уменьшите количество гостей."
                    )
                
                if table and table not in available_tables:
                    self.add_error(
                        'table',
                        "Этот столик уже занят на выбранное время. "
                        "Пожалуйста, выберите другой из доступных."
                    )
                    self.fields['table'].queryset = available_tables
            except Exception as e:
                self.add_error(None, f"Ошибка проверки доступности столов: {str(e)}")
        if date and time_val and table:
            try:
                conflicting_reservations = Reservation.objects.filter(
                    table=table,
                    date=date,
                    time=time_val
                )
                
                if self.instance and self.instance.pk:
                    conflicting_reservations = conflicting_reservations.exclude(pk=self.instance.pk)
                    
                if conflicting_reservations.exists():
                    raise ValidationError(
                        "Этот столик уже забронирован на выбранное время. "
                        "Пожалуйста, выберите другое время или столик."
                    )
            except Exception as e:
                self.add_error(None, f"Ошибка проверки уникальности бронирования: {str(e)}")

        return cleaned_data