from django.contrib import admin

from order.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_type', 'what', 'amount', 'amount_completed', 'price', 'trade_currency', 'status']


admin.site.register(Order, OrderAdmin)
