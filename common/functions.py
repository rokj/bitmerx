from django.db.models import Q

from account.models import Account
from order.models import Order

from common.constants import BUY, ACTIVE, SELL, DONE, BTC, LTC, USD, EUR
from trade.models import Trade


def get_candidate(order):
    if order.order_type == BUY:
        candidate = Order.objects\
            .filter(~Q(user=order.user) & Q(what=order.what) & Q(trade_currency=order.trade_currency) & Q(order_type=SELL) & Q(status=ACTIVE) & Q(price__lte=order.price))\
            .order_by("datetime_created")[:1]
    else:
        candidate = Order.objects \
            .filter(~Q(user=order.user) & Q(what=order.what) & Q(trade_currency=order.trade_currency) & Q(order_type=BUY) & Q(status=ACTIVE) & Q(price__gte=order.price)) \
            .order_by("datetime_created")[:1]

    if not candidate:
        return False

    return candidate[0]


def balance_accounts(order, candidate, initial_order_amount_completed, initial_candidate_amount_completed):
    account_order = Account.objects.get(user=order.user)
    account_candidate = Account.objects.get(user=candidate.user)

    order_amount_completed = order.amount_completed - initial_order_amount_completed
    candidate_amount_completed = candidate.amount_completed - initial_candidate_amount_completed

    if order_amount_completed != candidate_amount_completed:
        raise RuntimeError('Amounts should be the same!')

    # todo: check again for prices
    if order.what == BTC and order.order_type == BUY:
        account_order.btc = account_order.btc + order_amount_completed
        account_candidate.btc = account_candidate.btc - candidate_amount_completed
    elif order.what == LTC and order.order_type == BUY:
        account_order.ltc = account_order.ltc + order_amount_completed
        account_candidate.ltc = account_candidate.ltc - candidate_amount_completed
    elif order.what == BTC and order.order_type == SELL:
        account_order.btc = account_order.btc - order_amount_completed
        account_candidate.btc = account_candidate.btc + candidate_amount_completed
    elif order.what == LTC and order.order_type == SELL:
        account_order.ltc = account_order.ltc - order_amount_completed
        account_candidate.ltc = account_candidate.ltc + candidate_amount_completed

    for_how_much = None
    price = None

    if order.order_type == BUY:
        # important that we use candidates price
        for_how_much = order_amount_completed * candidate.price
        price = candidate.price

        if order.trade_currency == EUR:
            account_order.eur = account_order.eur - for_how_much
            account_candidate.eur = account_candidate.eur + for_how_much
        elif order.trade_currency == USD:
            account_order.usd = account_order.usd - for_how_much
            account_candidate.usd = account_candidate.usd + for_how_much
    elif order.order_type == SELL:
        # important that we use order price
        for_how_much = order_amount_completed * order.price
        price = order.price

        if order.trade_currency == EUR:
            account_order.eur = account_order.eur + for_how_much
            account_candidate.eur = account_candidate.eur - for_how_much
        elif order.trade_currency == USD:
            account_order.usd = account_order.usd + for_how_much
            account_candidate.usd = account_candidate.usd - for_how_much

    account_order.save()
    account_candidate.save()

    trade = Trade(
        order=order,
        candidate=candidate,
        amount=order_amount_completed,
        price=price,
        total=for_how_much
    )
    trade.save()


def try_limit_order(order):
    candidate = get_candidate(order)

    while candidate and order.status == ACTIVE:
        initial_order_amount_completed = order.amount_completed
        initial_candidate_amount_completed = candidate.amount_completed

        amount_needed = order.amount-order.amount_completed
        amount_available = candidate.amount-candidate.amount_completed

        if amount_needed >= amount_available:
            order.amount_completed = order.amount_completed + amount_available
            candidate.amount_completed = candidate.amount
            candidate.status = DONE
        elif amount_needed < amount_available:
            order.amount_completed = order.amount
            candidate.amount_completed = candidate.amount_completed + amount_needed
            order.status = DONE

        if order.amount == order.amount_completed:
            order.status = DONE

        order.save()
        candidate.save()

        if order.have_enough_funds():
            balance_accounts(order, candidate, initial_order_amount_completed, initial_candidate_amount_completed)

        if order.status == ACTIVE:
            candidate = get_candidate(order)
