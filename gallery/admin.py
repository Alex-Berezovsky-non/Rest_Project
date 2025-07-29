from django.contrib import admin
from django.db import models
from .models import GalleryItem

class DishInline(admin.TabularInline):  # type: ignore
    model = GalleryItem.dishes.through  # type: ignore
    extra = 1
    verbose_name = "Связанное блюдо"

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):  # type: ignore
    list_display = ('title', 'created_at', 'is_featured')
    list_filter = ('is_featured', 'dishes')
    search_fields = ('title', 'dishes__name')
    inlines = [DishInline]
    exclude = ('dishes',)
    readonly_fields = ('created_at',)