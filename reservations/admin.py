from django.contrib import admin
from .models import Table, Reservation

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'seats', 'shape', 'is_vip')
    search_fields = ('number',)
    list_filter = ('is_vip', 'shape')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'customer_name', 'date', 'time', 'is_confirmed')
    list_filter = ('date', 'is_confirmed')
    search_fields = ('customer_name', 'customer_phone')
    date_hierarchy = 'date'