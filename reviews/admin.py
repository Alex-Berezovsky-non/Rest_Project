from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_name', 'rating', 'created_at', 'is_published')
    list_filter = ('rating', 'is_published')
    list_editable = ('is_published',) 
    actions = ['publish_selected', 'unpublish_selected']

    def publish_selected(self, request: HttpRequest, queryset: QuerySet[Review]) -> None:
        """Действие для публикации выбранных отзывов"""
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} отзыв(ов) опубликовано")
    publish_selected.short_description = "Опубликовать выбранные отзывы"  # type: ignore

    def unpublish_selected(self, request: HttpRequest, queryset: QuerySet[Review]) -> None:
        """Действие для снятия с публикации"""
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} отзыв(ов) снято с публикации")
    unpublish_selected.short_description = "Снять с публикации"  # type: ignore