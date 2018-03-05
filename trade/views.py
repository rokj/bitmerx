from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from account.models import Account
from trade.models import Trade


@login_required
def my_trades(request):
    account = Account.objects.get(user=request.user)
    trades = Trade.objects.filter(Q(order__user=request.user) | Q(candidate__user=request.user))

    return render(request, 'trades.html', {'trades': trades, 'account': account, 'user': request.user})
