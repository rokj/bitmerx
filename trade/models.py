from common.models import Skeleton
from django.db import models
from order.models import Order


class Trade(Skeleton):
    # order_type = models.CharField(max_length=4, choices=order_choices, null=False, blank=False)
    order = models.ForeignKey(Order, related_name='%(app_label)s_%(class)s_order', on_delete=models.DO_NOTHING)
    candidate = models.ForeignKey(Order, related_name='%(app_label)s_%(class)s_candidate', on_delete=models.DO_NOTHING)
    amount = models.DecimalField('Amount', max_digits=16, decimal_places=8, null=False, blank=False, default=0)
    price = models.DecimalField('Price', max_digits=10, decimal_places=4, null=False, blank=False, default=0)
    total = models.DecimalField('Amount', max_digits=10, decimal_places=4, null=False, blank=False, default=0)