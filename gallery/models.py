from django.db import models
from django.utils.translation import gettext_lazy as _
from menu.models import Dish
import hashlib
from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from menu.models import Dish

def image_upload_path(instance: 'GalleryItem', filename: str) -> str:
    """Функция для определения пути загрузки изображения."""
    return f'gallery/{hashlib.md5(instance.image.name.encode()).hexdigest()[:10]}/{filename}'

class GalleryItem(models.Model):
    image = models.ImageField(
        _('Изображение'),
        upload_to=image_upload_path,
        help_text=_('Загрузите изображение (до 5MB)')
    )
    title = models.CharField(
        _('Название'),
        max_length=200,
        blank=True
    )
    dishes = models.ManyToManyField(
        Dish,
        verbose_name=_('Связанные блюда'),
        blank=True,
        related_name='gallery_items'
    )
    is_featured = models.BooleanField(
        _('Рекомендуемое'),
        default=False
    )
    created_at = models.DateTimeField(
        _('Дата добавления'),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _('Галерейное изображение')
        verbose_name_plural = _('Галерейные изображения')
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['is_featured']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self) -> str:
        return self.title or f"Изображение #{self.pk}"

    def save(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        if not self.title:
            self.title = f"Фото {self.created_at.strftime('%Y-%m-%d')}"
        super().save(*args, **kwargs)