from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from account.models import Account


@login_required
def index(request):
    account = Account.objects.get(user=request.user)

    return render(request, 'index.html', {'account': account})

