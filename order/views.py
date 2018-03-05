from decimal import Decimal

from django.shortcuts import render
from django.db import transaction
from django.contrib.auth.decorators import login_required

from account.models import Account
from common.constants import ACTIVE
from order.models import Order
from common.functions import try_limit_order


@login_required
@transaction.atomic
def order(request):
    account = Account.objects.get(user=request.user)

    if request.method == 'POST':
        order = Order(
            user=request.user,
            order_type=request.POST['order_type'],
            what=request.POST['what'],
            amount=Decimal(request.POST['amount']),
            price=Decimal(request.POST['price']),
            trade_currency=request.POST['trade_currency'],
            created_by=request.user,
            status=ACTIVE
        )
        order.save()

        if order.id:
            try_limit_order(order)

    return render(request, 'order.html', {'account': account})


@login_required
def my_orders(request):
    account = Account.objects.get(user=request.user)
    orders = Order.objects.filter(user=request.user)

    return render(request, 'orders.html', {'orders': orders, 'account': account})


@login_required
def order_book(request):
    account = Account.objects.get(user=request.user)
    orders = Order.objects.filter(status=ACTIVE)

    return render(request, 'order-book.html', {'orders': orders, 'account': account, 'user': request.user})
