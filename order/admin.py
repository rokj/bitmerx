from django.contrib import admin

from order.models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.get_fields()]

admin.site.register(Order, OrderAdmin)
