import asyncio

import ccxt.async_support as ccxt


class OpportunityFinder:

    def __init__(self, market_name, exchanges: list[dict]):
        """
        An object of type OpportunityFinder finds the largest price disparity between exchanges for a given
        cryptocurrency market by finding the exchange with the lowest market ask price and the exchange with the
        highest market bid price.
        """
        exchanges = [getattr(ccxt, exchange['name'])({
            'apiKey': exchange['apiKey'],
            'secret': exchange['secret'],
            'timeout': 60000
        }) for exchange in exchanges]

        self.exchange_list = exchanges
        self.market_name = market_name
        self.highest_bid = {'exchange': None, 'price': -1}
        self.lowest_ask = {'exchange': None, 'price': float('Inf')}

    async def _test_bid_and_ask(self, exchange: ccxt.Exchange):
        """
        Retrieves the bid and ask for self.market_name on self.exchange_name. If the retrieved bid > self.highest_bid,
        sets self.highest_bid to the retrieved bid. If retrieved ask < self.lowest ask, sets self.lowest_ask to the
        retrieved ask.
        """
        if not isinstance(exchange, ccxt.Exchange):
            raise ValueError("exchange is not a ccxt Exchange instance.")

        exchange.open()
        # try:
        orderbook = await exchange.fetch_order_book(self.market_name, 5)
        # A KeyError or ExchangeError occurs when the exchange does not have a market named self.market_name.
        # Any ccxt BaseError is because of ccxt, not this code.
        # except (KeyError, ccxt.ExchangeError, ccxt.BaseError):
        #     await exchange.close()
        #     return

        ask = orderbook['asks'][0][0]
        bid = orderbook['bids'][0][0]
        if self.highest_bid['price'] < bid:
            self.highest_bid['price'] = bid
            self.highest_bid['exchange'] = exchange
        if ask < self.lowest_ask['price']:
            self.lowest_ask['price'] = ask
            self.lowest_ask['exchange'] = exchange

    async def find_opportunity(self):
        tasks = [self._test_bid_and_ask(exchange_name) for exchange_name in self.exchange_list]
        await asyncio.wait(tasks)

        return {'highest_bid': self.highest_bid,
                'lowest_ask': self.lowest_ask,
                'ticker': self.market_name}
