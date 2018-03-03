from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from order.models import Order

from common.functions import try_limit_order


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def order(request):
    if request.method == 'POST':
        order = Order(
            user=request.user,
            order_type=request.POST['order_type'],
            what=request.POST['what'],
            amount=request.POST['amount'],
            price=request.POST['price'],
            trade_currency=request.POST['trade_currency'],
            created_by=request.user
        )
        order.save()

        try_limit_order(order)

    return render(request, 'order.html')

