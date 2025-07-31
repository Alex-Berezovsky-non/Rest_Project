from typing import Any
from django.db import models
from django.core.validators import FileExtensionValidator, validate_image_file_extension
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _


class TeamMember(models.Model):
    POSITION_CHOICES = [
        ('CHEF', 'Шеф-повар'),
        ('SOUS_CHEF', 'Су-шеф'),
        ('CHEF_DE_PARTIE', 'Шеф де парти'),
        ('PASTRY_CHEF', 'Кондитер'),
        ('BARMAN', 'Бармен'),
        ('SOMMELIER', 'Сомелье'),
        ('MANAGER', 'Менеджер'),
        ('HOST', 'Администратор'),
        ('WAITER', 'Официант'),
        ('COOK', 'Повар'),
    ]

    name = models.CharField(_('Имя'), max_length=100)
    position = models.CharField(
        _('Должность'),
        max_length=50,
        choices=POSITION_CHOICES
    )
    bio = models.TextField(_('Биография'), blank=True)
    photo = models.ImageField(
        _('Фото'),
        upload_to='team/%Y/%m/%d/',
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_image_file_extension,
        ],
        help_text="Формат: JPG/PNG. Размер: до 2MB"
    )
    is_visible = models.BooleanField(_('Отображать на сайте'), default=True)
    order = models.PositiveIntegerField(_('Порядок сортировки'), default=0)

    class Meta:
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Команда')
        ordering = ['order', 'position', 'name']

    def clean(self) -> None:
        """Валидация данных"""
        if not self.name.strip():
            raise ValidationError(_("Имя не может быть пустым"))
        self.name = escape(self.name)
        self.bio = escape(self.bio) if self.bio else ""

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def get_position_display(self) -> str:
        return dict(self.POSITION_CHOICES).get(self.position, self.position)

    def __str__(self) -> str:
        return f"{self.name} ({self.get_position_display()})"