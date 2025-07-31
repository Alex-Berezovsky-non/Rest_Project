from django.db import models
from django.urls import reverse
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    date = models.DateTimeField(verbose_name="Дата и время")
    image = models.ImageField(upload_to='events/', blank=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"
        ordering = ['-date']

    def __str__(self):
        return str(self.title)  

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})

    @property
    def is_upcoming(self):
        return self.date >= timezone.now()