"""
Athena Market Provider V4

Live market-wide intelligence using Yahoo Finance.

Tracks:
- SPY current price
- SPY previous close
- SPY day high
- SPY day low
- VIX
- DXY
- 10-Year Treasury Yield
"""

import yfinance as yf


class MarketProvider:

    def __init__(self):
        self.connected = True
        self.provider_name = "Yahoo Finance"

    def status(self):
        return {
            "connected": self.connected,
            "provider": self.provider_name,
        }

    def get_last_price(self, symbol):
        try:
            data = yf.Ticker(symbol).history(period="5d", interval="1d")

            if data.empty:
                return None

            return round(float(data["Close"].iloc[-1]), 2)

        except Exception:
            return None

    def get_spy_context(self):
        try:
            data = yf.Ticker("SPY").history(period="5d", interval="1d")

            if data.empty:
                return {
                    "spy": None,
                    "current_price": None,
                    "previous_close": None,
                    "day_high": None,
                    "day_low": None,
                }

            current_row = data.iloc[-1]
            previous_row = data.iloc[-2] if len(data) >= 2 else current_row

            current_price = round(float(current_row["Close"]), 2)
            previous_close = round(float(previous_row["Close"]), 2)
            day_high = round(float(current_row["High"]), 2)
            day_low = round(float(current_row["Low"]), 2)

            return {
                "spy": current_price,
                "current_price": current_price,
                "previous_close": previous_close,
                "day_high": day_high,
                "day_low": day_low,
            }

        except Exception:
            return {
                "spy": None,
                "current_price": None,
                "previous_close": None,
                "day_high": None,
                "day_low": None,
            }

    def get_market_data(self):

        spy_context = self.get_spy_context()

        vix = self.get_last_price("^VIX")
        dxy = self.get_last_price("DX-Y.NYB")
        treasury_10y = self.get_last_price("^TNX")

        spy = spy_context.get("spy")

        connected = any(
            value is not None
            for value in [spy, vix, dxy, treasury_10y]
        )

        return {
            "connected": connected,
            "provider": self.provider_name,

            "spy": spy_context.get("spy"),
            "current_price": spy_context.get("current_price"),
            "previous_close": spy_context.get("previous_close"),
            "day_high": spy_context.get("day_high"),
            "day_low": spy_context.get("day_low"),

            "vix": vix,
            "dxy": dxy,
            "treasury_10y": treasury_10y,

            "fear_greed": None,
        }