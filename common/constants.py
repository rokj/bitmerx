BUY = 'buy'
SELL = 'sell'
ACTIVE = 'active'
DONE = 'done'

BTC = 'BTC'
LTC = 'LTC'
EUR = 'EUR'
USD = 'USD'

order_choices = (
    (BUY, 'Buy'),
    (SELL, 'Sell')
)

what_choices = (
    (BTC, 'BTC'),
    (LTC, 'LTC')
)

trade_currency_choices = (
    (EUR, 'EUR'),
    (USD, 'USD')
)

status_choices = (
    (ACTIVE, 'Active'),
    (DONE, 'Done')
)