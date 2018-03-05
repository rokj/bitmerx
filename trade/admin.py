from django.contrib import admin

from trade.models import Trade


class TradeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Trade._meta.get_fields()]


admin.site.register(Trade, TradeAdmin)
