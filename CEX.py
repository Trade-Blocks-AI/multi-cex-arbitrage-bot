import ccxt.async_support as ccxt
from loguru import logger


async def get_balance(exchange: ccxt.Exchange, symbol: str):
    balance = await exchange.fetch_free_balance()
    base_symbol, quote_symbol = symbol.split('/')
    return {base_symbol: balance[base_symbol], quote_symbol: balance[quote_symbol]}


async def get_order_book(exchange: ccxt.Exchange, symbol):
    return await exchange.fetch_order_book(symbol, 10)


async def calc_selling_price(exchange: ccxt.Exchange, symbol: str, amount):
    """
    Calculates selling price for given token amount
    :returns: sale price
    """
    bids = (await exchange.fetch_order_book(symbol, 10))['bids']
    amount_to_sell = amount
    for i in range(len(bids)):
        if amount_to_sell == 0:
            return bids[i + 3][0]
        if bids[i][1] > amount_to_sell:
            amount_to_sell = 0
        else:
            amount_to_sell -= bids[i][1]


async def calc_purchase_amount(exchange: ccxt.Exchange, symbol: str, usd_amount):
    """
    Calculates what amount of token can be bought for given usd_amount
    :returns: tuple(amount to buy, starting buy price)
    """
    asks = (await exchange.fetch_order_book(symbol, 10))['asks']
    amount_to_buy = 0
    for i in range(len(asks)):
        if usd_amount == 0:
            return round(amount_to_buy, 5), asks[i + 3][0]
        if asks[i][1] * asks[i][0] > usd_amount:  # quantity * price > buy_usd_amount
            amount_to_buy += usd_amount / asks[i][0]
            usd_amount = 0
        else:
            amount_to_buy += asks[i][1]
            usd_amount -= asks[i][1] * asks[i][0]


async def buy(exchange, symbol, amount, price):
    logger.info(f'Buy {symbol} on {exchange}, amount: {amount} with price: {price}')
    return await exchange.create_limit_buy_order(symbol, amount, price)


async def sell(exchange, symbol, amount):
    price = await calc_selling_price(exchange, symbol, amount)
    logger.info(f'Sell {symbol} on {exchange}, amount: {amount} with price: {price}')
    return await exchange.create_limit_sell_order(symbol, amount, price)
