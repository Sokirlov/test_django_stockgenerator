from django.contrib import admin
from .models import Currency

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'name', 'iso_code', 'exchange_rate', 'symbol', )