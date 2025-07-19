from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserProfile(AbstractUser):    
    # Персональные данные
    phone = models.CharField(
        _('Телефон'),
        max_length=20,
        blank=True,
        help_text=_('Номер телефона для связи')
    )
    
    birth_date = models.DateField(
        _('Дата рождения'),
        null=True,
        blank=True,
        help_text=_('Дата в формате ГГГГ-ММ-ДД')
    )
    
    avatar = models.ImageField(
        _('Аватар'),
        upload_to='users/avatars/%Y/%m/%d/',
        blank=True,
        help_text=_('Изображение профиля пользователя')
    )

    # Права доступа и группы
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('Группы'),
        blank=True,
        help_text=_('Группы, к которым принадлежит пользователь'),
        related_name="custom_user_set",
        related_query_name="user",
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('Права пользователя'),
        blank=True,
        help_text=_('Конкретные права для этого пользователя'),
        related_name="custom_user_set", 
        related_query_name="user",
    )

    class Meta:
        verbose_name = _('Профиль пользователя')
        verbose_name_plural = _('Профили пользователей')
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        """Строковое представление для админки и логирования"""
        return f"{self.get_full_name()} ({self.username})" if self.get_full_name() else self.username

    def get_short_name(self):
        """Короткое имя для email-рассылок"""
        return self.first_name or self.username

    @property
    def profile_completion(self):
        """Процент заполненности профиля"""
        fields = [self.phone, self.birth_date, self.avatar, self.first_name, self.last_name]
        return int((sum(1 for field in fields if field) / len(fields)) * 100)