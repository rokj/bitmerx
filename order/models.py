from django.contrib.auth.models import User
from django.db import models

order_choices = (
    ('buy', 'Buy'),
    ('sell', 'Sell')
)

what_choices = (
    ('BTC', 'BTC'),
    ('LTC', 'LTC')
)

for_choices = (
    ('EUR', 'EUR'),
    ('USD', 'USD')
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    order_type = models.CharField(max_length=4, choices=order_choices, null=False, blank=False)
    what = models.CharField(max_length=3, choices=what_choices, null=False, blank=False)
    amount = models.DecimalField(_('Amount'), max_digits=16, decimal_places=8, null=False, blank=False)
    amount_completed = models.DecimalField(_('Amount completed'), max_digits=16, decimal_places=8, null=False, blank=False)
    price = models.DecimalField(_('Buy or sell at price'), max_digits=10, decimal_places=5, null=False, blank=False)
    _for = models.CharField(max_length=3, choices=for_choices, null=False, blank=False)


