from django.contrib.auth.models import User

from account.models import Account

test1 = User.objects.create_user('test1', password='test1')
test1.is_superuser = False
test1.is_staff = True
test1.save()

test2 = User.objects.create_user('test2', password='test2')
test2.is_superuser = False
test2.is_staff = True
test2.save()

test3 = User.objects.create_user('test3', password='test3')
test3.is_superuser = False
test3.is_staff = True
test3.save()

admin = User.objects.create_user('admin', password='admin')
admin.is_superuser = True
admin.is_staff = True
admin.save()

account = Account(user=test1, usd=1000, eur=2000, ltc=10, btc=20, created_by=test1)
account.save()
account = Account(user=test2, usd=1000, eur=2000, ltc=10, btc=20, created_by=test2)
account.save()
account = Account(user=test3, usd=1000, eur=60000, ltc=10, btc=20, created_by=test3)
account.save()
account = Account(user=admin, usd=1000, eur=2000, ltc=10, btc=20, created_by=admin)
account.save()

from order.models import Order
from common.constants import ACTIVE, SELL, BTC, EUR, BUY

order = Order(user=test1, order_type=SELL, what=BTC, amount=10, price=1000, trade_currency=EUR, status=ACTIVE, created_by=test1)
order.save()
order = Order(user=test2, order_type=SELL, what=BTC, amount=20, price=1500, trade_currency=EUR, status=ACTIVE, created_by=test1)
order.save()
order = Order(user=test1, order_type=SELL, what=BTC, amount=30, price=2000, trade_currency=EUR, status=ACTIVE, created_by=test1)
order.save()
order = Order(user=test3, order_type=BUY, what=BTC, amount=15, price=1540, trade_currency=EUR, status=ACTIVE, created_by=test2)
order.save()

from common.functions import try_limit_order
from order.models import Order

order = Order.objects.get(id=3)
try_limit_order(order)
