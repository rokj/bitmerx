from django.shortcuts import render

from order.models import Order


def index(request):
    return render(request, 'index.html')


def order(request):
    if request.method == 'POST':
        order = Order(
            order_type=request.POST['order_type'],
            what=request.POST['what'],
            amount=request.POST['amount'],
            price=request.POST['price'],
            _for=request.POST['for']
        )
        order.save()

    return render(request, 'order.html')

