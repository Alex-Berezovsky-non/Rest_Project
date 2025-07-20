from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

class Table(models.Model):
    TABLE_SHAPES = [
        ('round', 'Круглый'),
        ('square', 'Квадратный'),
        ('rectangular', 'Прямоугольный'),
    ]
    
    number = models.PositiveIntegerField(unique=True, verbose_name="Номер столика")
    seats = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="Количество мест"
    )
    shape = models.CharField(max_length=20, choices=TABLE_SHAPES, verbose_name="Форма")
    is_vip = models.BooleanField(default=False, verbose_name="VIP-столик")
    x_pos = models.FloatField(verbose_name="Позиция X на схеме")
    y_pos = models.FloatField(verbose_name="Позиция Y на схеме")

    class Meta:
        verbose_name = "Столик"
        verbose_name_plural = "Столики"
        ordering = ['number']

    def get_shape_display(self) -> str:
        return dict(self.TABLE_SHAPES).get(self.shape, '')

    def __str__(self) -> str:
        return f"Столик №{self.number} ({self.get_shape_display()}, {self.seats} мест)"


class Reservation(models.Model):
    table: 'models.ForeignKey[Table]' = models.ForeignKey('Table', on_delete=models.PROTECT, verbose_name="Столик")
    customer_name = models.CharField(max_length=100, verbose_name="Имя гостя")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон")
    customer_email = models.EmailField(verbose_name="Email")
    date = models.DateField(verbose_name="Дата брони")
    time = models.TimeField(verbose_name="Время брони")
    duration = models.PositiveIntegerField(
        default=2,
        validators=[MinValueValidator(1), MaxValueValidator(6)],
        verbose_name="Длительность (часы)"
    )
    guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Количество гостей"
    )
    special_requests = models.TextField(blank=True, verbose_name="Особые пожелания")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_confirmed = models.BooleanField(default=False, verbose_name="Подтверждено")

    if TYPE_CHECKING:
        table_set: 'RelatedManager[Reservation]'
        id: int

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-date', '-time']
        constraints = [
            models.UniqueConstraint(
                fields=['table', 'date', 'time'],
                name='unique_reservation'
            )
        ]

    def __str__(self) -> str:
        return f"Бронь #{self.id} на {self.date} {self.time} (Столик {self.table.number})"