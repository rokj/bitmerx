from django.contrib import admin

from account.models import Account


class AccountAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Account._meta.get_fields()]

admin.site.register(Account, AccountAdmin)
