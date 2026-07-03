from config.settings import APP_NAME
from config.settings import VERSION
from config.settings import DEFAULT_SYMBOL

from data.market_data import get_market_snapshot
from strategy.bias_engine import determine_bias

market = get_market_snapshot(DEFAULT_SYMBOL)
bias = determine_bias(market)

print("=" * 40)
print(APP_NAME)
print(f"Version: {VERSION}")
print("=" * 40)

print(f"Symbol: {market['symbol']}")
print(f"Price: ${market['price']}")
print(f"Trend: {market['trend']}")
print(f"20 Day SMA: ${market['sma20']}")
print(f"50 Day SMA: ${market['sma50']}")
print(f"Source: {market['source']}")

print(f"Athena Bias: {bias}")

print("=" * 40)