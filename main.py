import asyncio
import json
import traceback
from typing import Any

from loguru import logger

from CEX import calc_purchase_amount, buy, sell, get_balance
from finders import OpportunityFinder

logger.add('app.log', format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

config: Any
base_symbol: str
quote_symbol: str


def load_conf():
    logger.info('Loading config...')
    global config, base_symbol, quote_symbol
    with open('config.json') as f:
        config = json.load(f)
        base_symbol, quote_symbol = config['symbol'].split('/')


async def monitor_prices():
    finder = OpportunityFinder(config['symbol'], exchanges=config['exchanges'])

    logger.info('Price monitoring started ...\n')

    while True:
        try:
            opportunity = await finder.find_opportunity()
            purchase_price = opportunity['lowest_ask']['price']
            purchase_exchange = opportunity['lowest_ask']['exchange']
            selling_price = opportunity['highest_bid']['price']
            selling_exchange = opportunity['highest_bid']['exchange']
            price_diff = float(selling_price - purchase_price)

            logger.info(f'{purchase_exchange} price: {format(purchase_price, ".13f")}')
            logger.info(f'{selling_exchange} price:    {format(selling_price, ".13f")}')
            logger.info(f'Price Diff:    {format(price_diff, ".13f")}\n')

            logger.info(f'{purchase_exchange} balance: {await get_balance(purchase_exchange, config["symbol"])}')
            logger.info(f'{selling_exchange} balance: {await get_balance(selling_exchange, config["symbol"])}')
            if price_diff >= config['usd_price_diff']:
                purchase_amount, purchase_price = await calc_purchase_amount(purchase_exchange, config['symbol'],
                                                                             config['usd_amount'])
                await asyncio.wait([buy(purchase_exchange, config['symbol'], purchase_amount, purchase_price),
                                    sell(selling_exchange, config['symbol'], purchase_amount)])

            logger.info(f'{purchase_exchange} balance: {await get_balance(purchase_exchange, config["symbol"])}')
            logger.info(f'{selling_exchange} balance: {await get_balance(selling_exchange, config["symbol"])}')

            await purchase_exchange.close()
            await selling_exchange.close()
            print()
            await asyncio.sleep(config['pause'])
        except Exception as e:
            logger.error(f'Error in monitor_prices(): {e}')
            traceback.print_exc()
            if purchase_exchange and selling_exchange:
                await purchase_exchange.close()
                await selling_exchange.close()


async def main():
    load_conf()
    await monitor_prices()


if __name__ == '__main__':
    asyncio.run(main())
