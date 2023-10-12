# Multi CEX Arbitrage Bot

Robust and efficient trading bot designed to identify and capitalize on arbitrage opportunities across multiple
centralized exchanges for specific trading pairs.

![Trade Blocks AI](https://tradeblocks.ai/static/media/logo.a2830001108d66fe70fb.png)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Support and Contact](#support-and-contact)
- [License](#license)

## Introduction

Arbitrage refers to the process of buying an asset at a lower price on one exchange and selling it at a higher price on
another, capturing the price differential as profit. With numerous centralized exchanges having slight variations in
supply and demand, arbitrage opportunities are frequent but often short-lived. Multi CEX Arbitrage Bot constantly
monitors selected exchanges and trading pairs, acting swiftly to seize these opportunities.

Visit our website: [TradeBlocks.ai](https://tradeblocks.ai)

## Features

- **Real-time Monitoring**: The bot continuously fetches order book data from multiple exchanges to identify profitable
  opportunities.
- **Flexibility**: Easily configure which trading pairs and on which exchanges the bot should monitor and trade.
- **Fast Execution**: Once an opportunity is identified, the bot acts swiftly to execute the necessary trades.

## Supported Exchanges

The current version supports arbitrage for the following centralized exchanges:

- **Binance**
- **Kraken**
- **Bittrex**
- **Bitget**
- **And more...**

## Getting Started

Follow these instructions to get your trading bot up and running.

### Prerequisites

Before setting up and running the bot, ensure you meet the following prerequisites:

- **Python 3.8+**
- **API keys**: To enable the bot's interaction with different exchanges, you'll need API keys from those exchanges.
Ensure you have them ready before configuration.

### Installation

```bash
# Clone the repository
git clone https://github.com/Trade-Blocks-AI/multi-cex-arbitrage-bot.git

# Change directory
cd multi-cex-arbitrage-bot/

# Create python virtual environment and activate it
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

The **config.json** file steers the bot's operation. Here's a quick rundown:

- **symbol**: Specifies the trading pair, e.g., "BTC/USDT".
- **exchanges**: List of exchanges for arbitrage. For each:
    - **name**: Exchange identifier.
    - **apiKey**: Your exchange-specific API key.
    - **secret**: Your secret key for the exchange.
- **usd_amount**: Amount in USD for each arbitrage action.
- **usd_price_diff**: Minimum price difference in USD to trigger an arbitrage opportunity.
- **pause**: Delay in seconds after each operation to prevent rate limits or other issues.

Ensure to populate **apiKey** and **secret** appropriately for each exchange.

### Usage

To run the bot and start monitoring for arbitrage opportunities:

```bash
# Run the bot
python main.py
```

### Important Notice

The bot showcased in this repository is a streamlined variant of our comprehensive trading solution. If you find value
in this tool and wish to explore our advanced, feature-rich offering or need bespoke trading solutions, please don't
hesitate to contact us.

### Support And Contact

This project is open source, if you need up and running bots please contact us.

Website : https://tradeblocks.ai
Email: info@tradeblocks.ai
Telegram: https://t.me/mirhamzahasan &
https://t.me/chain_chakra
Twitter : https://twitter.com/TradeBlocksAI

### License

This project is licensed under the MIT License - see the LICENSE file for details.


