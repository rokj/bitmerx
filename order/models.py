from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.db import models

from account.models import Account
from common.models import SkeletonU

BUY = 'buy'
SELL = 'sell'
ACTIVE = 'active'
DONE = 'done'

BTC = 'BTC'
LTC = 'LTC'
EUR = 'EUR'
USD = 'USD'

order_choices = (
    (BUY, 'Buy'),
    (SELL, 'Sell')
)

what_choices = (
    (BTC, 'BTC'),
    (LTC, 'LTC')
)

trade_currency_choices = (
    (EUR, 'EUR'),
    (USD, 'USD')
)

status_choices = (
    (ACTIVE, 'Active'),
    (DONE, 'Done')
)


class Order(SkeletonU):
    user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_user', on_delete=models.DO_NOTHING)
    order_type = models.CharField(max_length=4, choices=order_choices, null=False, blank=False)
    what = models.CharField(max_length=3, choices=what_choices, null=False, blank=False)
    amount = models.DecimalField(_('Amount'), max_digits=16, decimal_places=8, null=False, blank=False)
    amount_completed = models.DecimalField(_('Amount completed'), max_digits=16, decimal_places=8, null=False, blank=False, default=0)
    price = models.DecimalField(_('Buy or sell at price'), max_digits=10, decimal_places=5, null=False, blank=False)
    trade_currency = models.CharField(max_length=3, choices=trade_currency_choices, null=False, blank=False)
    status = models.CharField(max_length=6, choices=status_choices, null=False, blank=False, default='ACTIVE')

    def have_enough_funds(self):
        account = Account.objects.get(user=self.user)

        if self.order_type == SELL:
            if self.what == BTC and account.btc >= self.amount:
                return True
            elif self.what == LTC and account.ltc >= self.amount:
                return True
        elif self.order_type == BUY:
            if self.trade_currency == EUR and account.eur >= self.amount*self.price:
                return True
            elif self.trade_currency == USD and account.usd >= self.amount * self.price:
                return True

        return False

    def save(self, force_insert=False, force_update=False):
        if self.have_enough_funds():
            super(Order, self).save(force_insert, force_update)

    def __str__(self):
        return "%s: %s %s %s %s %s %s" % (self.user.id, self.order_type, self.what, self.amount, self.amount_completed, self.price, self.trade_currency)


