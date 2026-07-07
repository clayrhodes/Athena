import yfinance as yf

from data.indicators import calculate_rsi
from data.indicators import calculate_macd
from data.indicators import calculate_atr
from analysis.vwap import calculate_vwap
from analysis.support_resistance import find_support_resistance
from strategy.price_action_engine_v2 import run_price_action_engine_v2


def _flatten_columns(data):
    if hasattr(data.columns, "nlevels") and data.columns.nlevels > 1:
        data.columns = data.columns.get_level_values(0)
    return data


def _build_candles(data, limit=250):
    candles = []

    recent = data.tail(limit)

    for index, row in recent.iterrows():
        candles.append({
            "time": str(index),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),
        })

    return candles


def get_market_data():
    daily = yf.download(
        "SPY",
        period="1y",
        interval="1d",
        auto_adjust=True
    )

    intraday = yf.download(
        "SPY",
        period="5d",
        interval="5m",
        auto_adjust=True
    )

    daily = _flatten_columns(daily)
    intraday = _flatten_columns(intraday)

    close = daily["Close"]
    volume = daily["Volume"]

    latest_daily = daily.iloc[-1]

    price = float(close.iloc[-1])
    open_price = float(latest_daily["Open"])
    high_price = float(latest_daily["High"])
    low_price = float(latest_daily["Low"])
    previous_close = float(close.iloc[-2])

    sma20 = float(close.rolling(20).mean().iloc[-1])
    sma50 = float(close.rolling(50).mean().iloc[-1])
    sma200 = float(close.rolling(200).mean().iloc[-1])

    rsi = calculate_rsi(close)
    macd = calculate_macd(close)
    atr = calculate_atr(daily)
    vwap = calculate_vwap(intraday)

    current_volume = int(volume.iloc[-1])
    average_volume = int(volume.rolling(20).mean().iloc[-1])

    daily_candles = _build_candles(daily, limit=250)
    intraday_candles = _build_candles(intraday, limit=300)

    price_action_v2_report, price_action_v2_data = run_price_action_engine_v2(daily)

    market = {
        "symbol": "SPY",

        "price": price,
        "current_price": price,

        "open": open_price,
        "high": high_price,
        "low": low_price,
        "previous_close": previous_close,

        "sma20": sma20,
        "sma50": sma50,
        "sma200": sma200,

        "rsi": rsi,
        "macd": macd,
        "atr": atr,
        "vwap": vwap,

        "current_volume": current_volume,
        "average_volume": average_volume,

        "candles": daily_candles,
        "daily_candles": daily_candles,
        "intraday_candles": intraday_candles,
        "ohlc": daily_candles,
        "history": daily_candles,

        "price_action_v2": price_action_v2_report,
        "price_action_v2_score": price_action_v2_report["price_action_score"],
        "price_action_v2_bias": price_action_v2_report["price_action_bias"],
    }

    market["support_resistance"] = find_support_resistance(market)

    return market