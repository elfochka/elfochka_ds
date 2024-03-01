from django.contrib import admin
from .models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'price', 'image']
    ordering = ('-id',)
    readonly_fields = ('pk',)
    fieldsets = [
        ('О товаре', {
            'fields': ('description',)
        }),
        ('Дополнительно', {
            'fields': ('image',)
        }),
        ('Цена', {
            'fields': ('price',)
        }),

    ]


class ItemsInline(admin.TabularInline):
    model = Order.items.through
    verbose_name = 'Товар'
    verbose_name_plural = 'Список товаров'


@admin.register(Discount)
class Discountdmin(admin.ModelAdmin):
    list_display = ['pk', 'amount']


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['pk', 'amount']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ItemsInline, ]
    list_display = ('pk', 'get_display_total_amount', 'created_at')
    ordering = ('-id',)
    readonly_fields = ('get_display_total_amount', 'created_at', 'items', 'pk', 'stripe_payment_id')
    fieldsets = [
        ('Дополнительно', {
            'fields': ('discount', 'tax',)
        }),
        ('Итого', {
            'fields': ('get_display_total_amount',)
        }),
        ('Strip Payment ID', {
            'fields': ('stripe_payment_id',)
        }),

    ]

    def __str__(self, obj):
        return str(obj)
