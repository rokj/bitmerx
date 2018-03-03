from django.db import models
from django.contrib.auth.models import User


class Skeleton(models.Model):
    datetime_created = models.DateTimeField(auto_now=False, auto_now_add=True, null=False, blank=False)
    datetime_updated = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    datetime_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class SkeletonU(Skeleton):
    """
    Skeleton model with Users included.
    """
    created_by = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_created_by', null=False, on_delete=models.DO_NOTHING)
    updated_by = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_updated_by', null=True, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True
