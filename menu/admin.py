from typing import Optional, cast
from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from django.http import HttpRequest
from django.db.models import QuerySet
from .models import Category, Dish


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'size': 50, 'placeholder': 'Введите название категории'}),
            'slug': forms.TextInput(attrs={'size': 50, 'placeholder': 'Автозаполнение после ввода названия'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
        help_texts = {
            'name': 'Название категории меню (например, "Паста", "Пицца")',
            'slug': 'Уникальная часть URL для этой категории (латинские буквы, цифры, дефисы)',
            'order': 'Порядок отображения категорий (меньше = выше)',
            'image': 'Рекомендуемый размер: 800x600px, формат JPG/PNG',
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('name', 'order', 'image_preview', 'active_dishes_count')
    list_display_links = ('name',)
    list_editable = ('order',)
    list_filter = ('order',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_preview',)
    actions = ['activate_categories', 'deactivate_categories']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'order', 'image', 'image_preview')
        }),
    )
    
    def image_preview(self, obj: Optional[Category]) -> str:
        if obj and obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "—"
    image_preview.short_description = 'Превью'
    
    def active_dishes_count(self, obj: Category) -> int:
        return obj.dishes.filter(is_active=True).count()
    active_dishes_count.short_description = 'Активных блюд'
    
    @admin.action(description='Активировать выбранные категории')
    def activate_categories(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активировано {updated} категорий.')
    
    @admin.action(description='Деактивировать выбранные категории')
    def deactivate_categories(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Деактивировано {updated} категорий.')


class DishAdminForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'size': 50, 'placeholder': 'Полное название блюда'}),
            'ingredients': forms.Textarea(attrs={
                'rows': 3, 
                'cols': 50,
                'placeholder': 'Список ингредиентов через запятую'
            }),
            'price': forms.NumberInput(attrs={'step': 0.01, 'min': 0}),
            'weight': forms.NumberInput(attrs={'min': 0}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
        help_texts = {
            'name': 'Полное название блюда',
            'category': 'Выберите категорию из списка',
            'ingredients': 'Список ингредиентов через запятую',
            'price': 'Цена в рублях (например: 350.00)',
            'weight': 'Вес порции в граммах (необязательно)',
            'image': 'Рекомендуемый размер: 800x600px, формат JPG/PNG',
            'is_vegan': 'Отметьте, если блюдо вегетарианское',
            'is_spicy': 'Отметьте, если блюдо острое',
            'is_chefs_choice': 'Отметьте, если это блюдо - выбор шефа',
            'is_active': 'Показывать ли блюдо в меню',
        }


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    form = DishAdminForm
    list_display = (
        'name', 
        'category', 
        'price', 
        'weight', 
        'is_vegan', 
        'is_spicy', 
        'is_chefs_choice',
        'is_active',
        'image_preview',
        'created_short',
    )
    list_display_links = ('name',)
    list_editable = (
        'price', 
        'weight', 
        'is_vegan', 
        'is_spicy', 
        'is_chefs_choice',
        'is_active'
    )
    list_filter = (
        'category', 
        'is_vegan', 
        'is_spicy', 
        'is_chefs_choice',
        'is_active',
        'created',
    )
    search_fields = ('name', 'ingredients')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_preview', 'created', 'updated')
    date_hierarchy = 'created'
    list_per_page = 25
    save_on_top = True
    actions = ['activate_dishes', 'deactivate_dishes', 'mark_as_chefs_choice']
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'name', 
                'slug', 
                'category', 
                'ingredients',
                ('price', 'weight'),
                'image',
                'image_preview',
            )
        }),
        ('Дополнительные параметры', {
            'fields': (
                ('is_vegan', 'is_spicy', 'is_chefs_choice'),
                'is_active',
            )
        }),
        ('Даты', {
            'fields': (
                ('created', 'updated'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj: Optional[Dish]) -> str:
        if obj and obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "—"
    image_preview.short_description = 'Превью'
    
    def created_short(self, obj: Dish) -> str:
        return obj.created.strftime('%d.%m.%Y')
    created_short.short_description = 'Добавлено'
    created_short.admin_order_field = 'created'
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Dish]:
        return cast(QuerySet[Dish], 
            super().get_queryset(request).select_related('category')
        )
    
    @admin.action(description='Активировать выбранные блюда')
    def activate_dishes(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'Активировано {updated} блюд.')
    
    @admin.action(description='Деактивировать выбранные блюда')
    def deactivate_dishes(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Деактивировано {updated} блюд.')
    
    @admin.action(description='Отметить как "Выбор шефа"')
    def mark_as_chefs_choice(self, request, queryset):
        updated = queryset.update(is_chefs_choice=True)
        self.message_user(request, f'{updated} блюд отмечены как "Выбор шефа".')
