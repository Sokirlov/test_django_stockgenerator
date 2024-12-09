from django.contrib import admin
from .models import Sale, Price, Order, Goods


@admin.action(description="Invert status")
def change_status(model, request, queryset, **kwargs):
    for i in queryset:
        i.is_active = not i.is_active
        i.save()

@admin.register(Sale)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'name', 'min_price', 'max_price', 'create', 'update')
    list_filter = ('is_active', 'create', 'update')
    actions = [change_status, ]
    readonly_fields = ('create_by', 'update_by')

@admin.register(Price)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'base_price', 'create', 'update')
    list_filter = ('is_active', 'create', 'update')
    actions = [change_status,]
    readonly_fields = ('create_by', 'update_by')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'goods', 'price', 'amount', 'order_sum', 'status',
                    'create_by', 'update_by', 'create', 'update')
    list_editable = ('status',)
    readonly_fields = ('create_by', 'update_by')
    search_fields = ('user__last_name', 'user__first_name', 'user__username', 'good__name')
    list_filter = ('status', 'create', 'update', 'goods',)

@admin.register(Goods)
class GoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'create_by', 'update_by', 'create', 'update')
    list_display_links = ('id', 'name')
    readonly_fields = ('create_by', 'update_by',)
