from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.http import HttpRequest
from django import forms
from typing import Any, Optional, Dict, Type
from .models import TeamMember


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'name', 'position', 'is_visible', 'order')
    list_editable = ('is_visible', 'order')
    list_filter = ('position', 'is_visible')
    search_fields = ('name', 'bio', 'position')
    fieldsets = (
        (None, {
            'fields': ('name', 'position', 'bio')
        }),
        (_('Изображение'), {
            'fields': ('photo',)
        }),
        (_('Настройки отображения'), {
            'fields': ('is_visible', 'order')
        }),
    )
    
    def photo_preview(self, obj: TeamMember) -> str:
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height:50px;max-width:50px;" />', 
                obj.photo.url
            )
        return "-"
    
    photo_preview.short_description = _('Фото')  # type: ignore[attr-defined]
    
    def get_changeform_initial_data(self, request: HttpRequest) -> Dict[str, str]:
        return {'order': str(TeamMember.objects.count() + 1)}
    
    def get_form(
        self,
        request: HttpRequest,
        obj: Optional[TeamMember] = None,
        change: bool = False,
        **kwargs: Any
    ) -> Type[forms.ModelForm]:
        form = super().get_form(request, obj, change, **kwargs)
        
        if hasattr(form, 'base_fields') and 'bio' in form.base_fields:
            form.base_fields['bio'].help_text = _("Краткое описание опыта и достижений")
        
        return form