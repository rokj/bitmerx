from django.db.models import Q

from order.models import Order, BUY, ACTIVE, SELL, DONE


def get_candidate(order):
    if order.order_type == BUY:
        candidate = Order.objects\
            .filter(Q(what=order.what) & Q(trade_currency=order.trade_currency) & Q(order_type=SELL) & Q(status=ACTIVE) & Q(price__leq=order.price))\
            .order_by("datetime_created")[:1]
    else:
        candidate = Order.objects \
            .filter(Q(what=order.what) & Q(trade_currency=order.trade_currency) & Q(order_type=BUY) & Q(status=ACTIVE) & Q(price__geq=order.price)) \
            .order_by("datetime_created")[:1]

    if not candidate:
        return False

    return candidate[0]


def try_limit_order(order):
    candidate = get_candidate(order)

    while candidate and order.status == ACTIVE:
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

        if order.status == ACTIVE:
            candidate = get_candidate(order)
