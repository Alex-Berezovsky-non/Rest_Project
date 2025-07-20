from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Reservation
import datetime

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'customer_name', 'customer_phone', 'customer_email',
            'date', 'time', 'duration', 'guests', 'special_requests'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise ValidationError("Нельзя забронировать столик на прошедшую дату")
        if date > (timezone.now().date() + datetime.timedelta(days=30)):
            raise ValidationError("Бронирование возможно максимум на 30 дней вперед")
        return date

    def clean_guests(self):
        guests = self.cleaned_data['guests']
        table = self.cleaned_data.get('table')
        if table and guests > table.seats:
            raise ValidationError(f"Этот столик вмещает максимум {table.seats} гостей")
        return guests