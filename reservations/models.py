from datetime import datetime, timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Table(models.Model):
    TABLE_SHAPES = [
        ('round', 'Круглый'),
        ('square', 'Квадратный'),
        ('rectangular', 'Прямоугольный'),
    ]
    
    COLOR_CHOICES = [
        ('#4CAF50', 'Зеленый'),
        ('#2196F3', 'Синий'),
        ('#FFC107', 'Желтый'),
        ('#F44336', 'Красный'),
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
    color = models.CharField(
        max_length=7, 
        choices=COLOR_CHOICES, 
        default='#4CAF50',
        verbose_name="Цвет на схеме"
    )
    rotation = models.IntegerField(
        default=0,
        verbose_name="Поворот (градусы)",
        help_text="Для нестандартного расположения"
    )

    class Meta:
        verbose_name = "Столик"
        verbose_name_plural = "Столики"
        ordering = ['number']

    def get_shape_display(self) -> str:
        """Возвращает читаемое название формы столика"""
        return dict(self.TABLE_SHAPES).get(self.shape, '')

    def __str__(self) -> str:
        return f"Столик №{self.number} ({self.get_shape_display()}, {self.seats} мест)"

    @classmethod
    def get_available_tables(cls, date, time_val, duration, guests):
        """
        Возвращает QuerySet доступных столиков на указанное время
        """
        end_time = (datetime.combine(date, time_val) + timedelta(hours=duration)).time()

        potential_conflicts = Reservation.objects.filter(
            date=date,
            time__lt=end_time,
        ).select_related('table')
        
        conflicting_ids = []
        for reservation in potential_conflicts:
            res_end_time = (datetime.combine(reservation.date, reservation.time) + 
                          timedelta(hours=reservation.duration)).time()
            if res_end_time > time_val:
                conflicting_ids.append(reservation.table_id)
        
        return cls.objects.exclude(
            id__in=conflicting_ids
        ).filter(
            seats__gte=guests
        ).order_by('seats')


class Reservation(models.Model):
    table = models.ForeignKey(
        'Table', 
        on_delete=models.PROTECT, 
        verbose_name="Столик"
    )
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

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ['-date', '-time']
        constraints = [
            models.UniqueConstraint(
                fields=['table', 'date', 'time'],
                name='unique_reservation'
            ),
            models.CheckConstraint(
                check=models.Q(duration__gte=1) & models.Q(duration__lte=6),
                name='duration_range_check'
            )
        ]

    def __str__(self) -> str:
        return f"Бронь #{self.id} на {self.date} {self.time} (Столик {self.table.number})"

    def get_end_time(self):
        """Рассчитывает время окончания бронирования"""
        return (datetime.combine(self.date, self.time) + timedelta(hours=self.duration)).time()

    def is_time_slot_available(self):
        """Проверяет, свободен ли столик в выбранный временной промежуток"""
        conflicting = Reservation.objects.filter(
            table=self.table,
            date=self.date,
        ).exclude(id=self.id)
        
        new_start = datetime.combine(self.date, self.time)
        new_end = new_start + timedelta(hours=self.duration)
        
        for reservation in conflicting:
            res_start = datetime.combine(reservation.date, reservation.time)
            res_end = res_start + timedelta(hours=reservation.duration)
            
            if (new_start < res_end) and (new_end > res_start):
                return False
        return True