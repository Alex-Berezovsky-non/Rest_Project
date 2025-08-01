from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_active', 'is_upcoming')
    list_filter = ('is_active', 'date')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'