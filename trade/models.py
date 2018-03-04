from common.models import Skeleton
from django.db import models
from common.constants import order_choices, what_choices, trade_currency_choices, status_choices, BTC, LTC, BUY, SELL, EUR, USD

class Trade(Skeleton):
    order_type = models.CharField(max_length=4, choices=order_choices, null=False, blank=False)