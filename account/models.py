from django.db import models
from django.contrib.auth.models import User

from common.models import SkeletonU


class Account(SkeletonU):
    user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_user', on_delete=models.DO_NOTHING)
    usd = models.DecimalField('USD', max_digits=16, decimal_places=4, null=False, blank=False, default=0)
    eur = models.DecimalField('EUR', max_digits=16, decimal_places=4, null=False, blank=False, default=0)
