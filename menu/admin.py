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
            'name': forms.TextInput(attrs={'size': 50}),
            'slug': forms.TextInput(attrs={'size': 50}),
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('name', 'order', 'image_preview', 'active_dishes_count')
    list_editable = ('order',)
    list_filter = ('order',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj: Optional[Category]) -> str:
        if obj and obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "—"
    image_preview.short_description = 'Превью'  # type: ignore[attr-defined]
    
    def active_dishes_count(self, obj: Category) -> int:
        dishes: QuerySet[Dish] = obj.dishes.all()  # type: ignore[attr-defined]
        return dishes.filter(is_active=True).count() # type: ignore
    active_dishes_count.short_description = 'Активных блюд'  # type: ignore[attr-defined]


class DishAdminForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'size': 50}),
            'ingredients': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            'price': forms.NumberInput(attrs={'step': 0.01}),
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
        'image_preview'
    )
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
    image_preview.short_description = 'Превью'  # type: ignore[attr-defined]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Dish]:
        queryset = super().get_queryset(request)
        return cast(QuerySet[Dish], queryset.select_related('category'))