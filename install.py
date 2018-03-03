from django.contrib.auth.models import User

user = User.objects.create_user('test1', password='test1')
user.is_superuser = False
user.is_staff = True
user.save()
user = User.objects.create_user('test2', password='test2')
user.is_superuser = False
user.is_staff = True
user.save()
user = User.objects.create_user('test3', password='test3')
user.is_superuser = False
user.is_staff = True
user.save()

user = User.objects.create_user('admin', password='admin')
user.is_superuser = True
user.is_staff = True
user.save()

from order.models import Order
from common.functions import try_limit_order

order = Order.objects.get(id=4)
try_limit_order(order)

