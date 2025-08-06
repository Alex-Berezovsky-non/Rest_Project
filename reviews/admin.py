from django.contrib import admin
from django.http import HttpRequest
from django.db.models import QuerySet
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Настройки списка отзывов
    list_display = ('id', 'author_name', 'rating_stars', 'created_at', 'is_published')
    list_display_links = ('id', 'author_name')
    list_filter = ('rating', 'is_published', 'created_at')
    list_editable = ('is_published',)
    list_per_page = 20
    search_fields = ('author_name', 'text')
    date_hierarchy = 'created_at'
    actions = ['publish_selected', 'unpublish_selected']
    
    # Русские названия
    @admin.display(description='Рейтинг')
    def rating_stars(self, obj):
        return f"{'★' * obj.rating}{'☆' * (5 - obj.rating)} ({obj.rating}/5)"
    
    # Групповые действия
    @admin.action(description="Опубликовать выбранные отзывы")
    def publish_selected(self, request: HttpRequest, queryset: QuerySet[Review]) -> None:
        updated = queryset.update(is_published=True)
        self.message_user(request, f"Опубликовано {updated} отзыв(ов)")

    @admin.action(description="Снять с публикации выбранные отзывы")
    def unpublish_selected(self, request: HttpRequest, queryset: QuerySet[Review]) -> None:
        updated = queryset.update(is_published=False)
        self.message_user(request, f"Снято с публикации {updated} отзыв(ов)")

    # Настройки формы редактирования
    fieldsets = (
        (None, {
            'fields': ('author', 'author_name', 'rating', 'text')
        }),
        ('Модерация', {
            'fields': ('is_published', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)
    
    # Мета-данные для админки
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    # Русские названия в заголовке
    def get_model_perms(self, request):
        return {
            'add': self.has_add_permission(request),
            'change': self.has_change_permission(request),
            'delete': self.has_delete_permission(request),
            'view': self.has_view_permission(request),
        }