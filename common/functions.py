from django.db.models import Q

from account.models import Account
from order.models import Order, BUY, ACTIVE, SELL, DONE, BTC, LTC, USD, EUR


def get_candidate(order):
    if order.order_type == BUY:
        candidate = Order.objects\
            .filter(Q(what=order.what) & Q(trade_currency=order.trade_currency) & Q(order_type=SELL) & Q(status=ACTIVE) & Q(price__lte=order.price))\
            .order_by("datetime_created")[:1]
    else:
        candidate = Order.objects \
            .filter(Q(what=order.what) & Q(trade_currency=order.trade_currency) & Q(order_type=BUY) & Q(status=ACTIVE) & Q(price__gte   =order.price)) \
            .order_by("datetime_created")[:1]

    if not candidate:
        return False

    return candidate[0]


def try_limit_order(order):
    candidate = get_candidate(order)

    while candidate and order.status == ACTIVE:
        initial_order_amount_completed = order.amount_completed
        initial_candidate_amount_completed = candidate.amount_completed

        amount_needed = order.amount - order.amount_completed
        amount_available = candidate.amount - candidate.amount_completed

        if amount_needed >= amount_available:
            order.amount_completed = order.amount_completed + amount_available
            candidate.amount_completed = candidate.amount
            candidate.status = DONE
        else:
            order.amount_completed = order.amount
            order.status = DONE
            candidate.amount_completed = candidate.amount_completed + amount_needed

        if order.amount == order.amount_completed:
            order.status = DONE

        order.save()
        candidate.save()

        if order.have_enough_funds():
            account_order = Account.objects.get(user=order.user)
            account_candidate = Account.objects.get(user=candidate.user)

            if order.what == BTC and order.order_type == BUY:
                account_order.btc = account_order.btc + (order.amount_completed - initial_order_amount_completed)
                account_candidate.btc = account_candidate.btc - (candidate.amount_completed - initial_candidate_amount_completed)
            elif order.what == LTC and order.order_type == BUY:
                account_order.ltc = account_order.ltc + (order.amount_completed - initial_order_amount_completed)
                account_candidate.ltc = account_candidate.ltc - (candidate.amount_completed - initial_candidate_amount_completed)
            if order.what == BTC and order.order_type == SELL:
                account_order.btc = account_order.btc - (order.amount_completed - initial_order_amount_completed)
                account_candidate.btc = account_candidate.btc + (candidate.amount_completed - initial_candidate_amount_completed)
            if order.what == LTC and order.order_type == SELL:
                account_order.ltc = account_order.ltc - (order.amount_completed - initial_order_amount_completed)
                account_candidate.ltc = account_candidate.ltc + (candidate.amount_completed - initial_candidate_amount_completed)

        if order.status == ACTIVE:
            candidate = get_candidate(order)
