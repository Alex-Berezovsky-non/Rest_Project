from datetime import datetime, time, timedelta
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
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
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise ValidationError("Нельзя забронировать столик на прошедшую дату")
        if date > (timezone.now().date() + timedelta(days=30)):
            raise ValidationError("Бронирование возможно максимум на 30 дней вперед")
        return date

    def clean_time(self):
        time_val = self.cleaned_data['time']
        if time_val:
            if time_val < time(12, 0):
                raise ValidationError("Ресторан открывается в 12:00")
            if time_val >= time(23, 0):
                raise ValidationError("Последнее бронирование до 23:00")
        return time_val

    def clean_guests(self):
        guests = self.cleaned_data['guests']
        if guests and guests <= 0:
            raise ValidationError("Укажите корректное количество гостей")
        return guests

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time_val = cleaned_data.get('time')

        # Проверка минимального времени бронирования
        if date and time_val:
            booking_datetime = timezone.make_aware(
                datetime.combine(date, time_val)
            )
            now = timezone.now()
            
            if (booking_datetime - now).total_seconds() < 7200:
                self.add_error('time', "Бронируйте минимум за 2 часа")

        return cleaned_data