from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    """Категории блюд (паста, пицца, десерты)"""
    name = models.CharField(
        _('Название'),
        max_length=100,
        unique=True,
        help_text=_('Название категории меню (например, "Паста", "Пицца")')
    )
    slug = models.SlugField(
        _('URL-адрес'),
        max_length=100,
        unique=True,
        help_text=_('Уникальная часть URL для этой категории')
    )
    order = models.PositiveIntegerField(
        _('Порядок'),
        default=0,
        help_text=_('Порядок отображения категорий (меньше = выше)')
    )
    image = models.ImageField(
        _('Изображение'),
        upload_to='categories/',
        blank=True,
        null=True,
        help_text=_('Изображение для категории')
    )

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')
        ordering = ['order']
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self) -> str:
        """Строковое представление категории"""
        return str(self.name)

    def get_absolute_url(self) -> str:
        """Получает URL категории"""
        return reverse('menu:category_detail', kwargs={'slug': self.slug})


class Dish(models.Model):
    """Модель блюда с детальным описанием"""
    name = models.CharField(
        _('Название'),
        max_length=200,
        help_text=_('Полное название блюда')
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_('Категория'),
        on_delete=models.PROTECT,
        related_name='dishes',
        help_text=_('К какой категории относится блюдо')
    )
    ingredients = models.TextField(
        _('Ингредиенты'),
        help_text=_('Список ингредиентов через запятую')
    )
    price = models.DecimalField(
        _('Цена'),
        max_digits=8,
        decimal_places=2,
        help_text=_('Цена в рублях')
    )
    weight = models.PositiveIntegerField(
        _('Вес (г)'),
        blank=True,
        null=True,
        help_text=_('Вес порции в граммах')
    )
    is_vegan = models.BooleanField(
        _('Вегетарианское'),
        default=False,
        help_text=_('Отметьте, если блюдо вегетарианское')
    )
    is_spicy = models.BooleanField(
        _('Острое'),
        default=False,
        help_text=_('Отметьте, если блюдо острое')
    )
    is_chefs_choice = models.BooleanField(
        _('Выбор шефа'),
        default=False,
        help_text=_('Отметьте, если это блюдо - выбор шефа')
    )
    image = models.ImageField(
        _('Фото блюда'),
        upload_to='dishes/photos/', 
        blank=True,
        null=True,
        help_text=_('Загрузите фото блюда в формате JPG/PNG')
    )
    slug = models.SlugField(
        _('URL-адрес'),
        max_length=200,
        unique=True,
        help_text=_('Уникальная часть URL для этого блюда')
    )
    created = models.DateTimeField(
        _('Дата добавления'),
        auto_now_add=True,
        help_text=_('Когда блюдо было добавлено в меню')
    )
    updated = models.DateTimeField(
        _('Дата изменения'),
        auto_now=True,
        help_text=_('Когда блюдо было последний раз изменено')
    )
    is_active = models.BooleanField(
        _('Активно'),
        default=True,
        help_text=_('Показывать ли блюдо в меню')
    )

    class Meta:
        verbose_name = _('Блюдо')
        verbose_name_plural = _('Блюда')
        ordering = ['-is_chefs_choice', 'category__order', 'name']
        db_table = 'menu_dish' 
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_chefs_choice']),
            models.Index(fields=['is_active']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gt=0),
                name='price_positive'
            ),
        ]

    def __str__(self) -> str:
        """Строковое представление блюда"""
        return f"{str(self.name)} ({float(self.price):.2f}₽)"

    def get_absolute_url(self) -> str:
        """Получает URL для детального просмотра блюда"""
        return reverse('menu:dish_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """Дополнительная обработка перед сохранением"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)