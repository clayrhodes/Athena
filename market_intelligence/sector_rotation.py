"""
Athena Sector Rotation Engine V3

Live sector rotation using Yahoo Finance sector ETFs.

Fixes newer yfinance MultiIndex Close column format.
"""

import yfinance as yf


class SectorRotationEngine:

    def __init__(self):
        self.provider = "Yahoo Finance Sector ETFs"

        self.sectors = {
            "XLK": "Technology",
            "XLF": "Financials",
            "XLY": "Consumer Discretionary",
            "XLI": "Industrials",
            "XLE": "Energy",
            "XLV": "Healthcare",
            "XLP": "Consumer Staples",
            "XLU": "Utilities",
            "XLB": "Materials",
            "XLRE": "Real Estate",
            "XLC": "Communication Services",
        }

        self.risk_on = ["XLK", "XLF", "XLY", "XLI", "XLC"]
        self.risk_off = ["XLV", "XLP", "XLU"]

    def analyze(self):
        performances = {}

        for ticker, name in self.sectors.items():
            performance = self._get_performance(ticker)

            if performance is not None:
                performances[ticker] = {
                    "sector": name,
                    "performance": performance,
                }

        if not performances:
            return {
                "connected": False,
                "provider": self.provider,
                "leading_sector": None,
                "lagging_sector": None,
                "score": 50,
                "market_tone": "Unknown",
                "summary": "Sector rotation unavailable.",
                "sector_performance": {},
            }

        leader = max(
            performances.items(),
            key=lambda item: item[1]["performance"],
        )

        laggard = min(
            performances.items(),
            key=lambda item: item[1]["performance"],
        )

        score = self._score_rotation(performances)
        market_tone = self._market_tone(score)

        return {
            "connected": True,
            "provider": self.provider,
            "leading_sector": leader[1]["sector"],
            "leading_ticker": leader[0],
            "lagging_sector": laggard[1]["sector"],
            "lagging_ticker": laggard[0],
            "score": score,
            "market_tone": market_tone,
            "summary": self._summary(leader, laggard, score, market_tone),
            "sector_performance": performances,
        }

    def _get_performance(self, ticker):
        try:
            data = yf.download(
                ticker,
                period="1mo",
                interval="1d",
                progress=False,
                auto_adjust=True,
                threads=False,
            )

            if data is None or data.empty or len(data) < 2:
                return None

            close = self._get_close_series(data, ticker)

            if close is None or len(close) < 2:
                return None

            first_close = float(close.iloc[0])
            last_close = float(close.iloc[-1])

            return round(((last_close - first_close) / first_close) * 100, 2)

        except Exception:
            return None

    def _get_close_series(self, data, ticker):
        try:
            if "Close" not in data.columns:
                return None

            close = data["Close"]

            if hasattr(close, "columns"):
                if ticker in close.columns:
                    close = close[ticker]
                else:
                    close = close.iloc[:, 0]

            close = close.dropna()

            return close

        except Exception:
            return None

    def _score_rotation(self, performances):
        risk_on_scores = []
        risk_off_scores = []

        for ticker, data in performances.items():
            if ticker in self.risk_on:
                risk_on_scores.append(data["performance"])

            if ticker in self.risk_off:
                risk_off_scores.append(data["performance"])

        if not risk_on_scores or not risk_off_scores:
            return 50

        risk_on_avg = sum(risk_on_scores) / len(risk_on_scores)
        risk_off_avg = sum(risk_off_scores) / len(risk_off_scores)

        spread = risk_on_avg - risk_off_avg
        score = 50 + (spread * 10)

        return max(0, min(100, round(score, 2)))

    def _market_tone(self, score):
        if score >= 65:
            return "Risk-On"

        if score <= 35:
            return "Risk-Off"

        return "Mixed"

    def _summary(self, leader, laggard, score, market_tone):
        return (
            f"{market_tone} sector rotation. "
            f"Leading sector: {leader[1]['sector']} ({leader[0]}) "
            f"at {leader[1]['performance']}%. "
            f"Lagging sector: {laggard[1]['sector']} ({laggard[0]}) "
            f"at {laggard[1]['performance']}%. "
            f"Sector rotation score: {score}/100."
        )