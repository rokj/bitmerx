from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render

from order.models import Order, ACTIVE

from common.functions import try_limit_order


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
@transaction.atomic
def order(request):
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

    return render(request, 'order.html')

