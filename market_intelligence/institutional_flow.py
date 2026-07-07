"""
Athena Institutional Flow Engine V2

Live institutional flow proxy using Yahoo Finance.

No new API key needed.

This estimates institutional pressure using:
- SPY price movement
- Current volume
- Average volume
- Dollar volume
- Volume expansion
"""

import yfinance as yf


class InstitutionalFlowEngine:

    def __init__(self):
        self.provider = "Yahoo Finance Institutional Flow Proxy"
        self.symbol = "SPY"

    def analyze(self):
        try:
            data = yf.download(
                self.symbol,
                period="1mo",
                interval="1d",
                progress=False,
                auto_adjust=True,
                threads=False,
            )

            if data is None or data.empty or len(data) < 10:
                return self._offline("Not enough SPY data returned.")

            close = self._get_series(data, "Close")
            volume = self._get_series(data, "Volume")

            if close is None or volume is None:
                return self._offline("Close or Volume data unavailable.")

            latest_close = float(close.iloc[-1])
            previous_close = float(close.iloc[-2])
            latest_volume = float(volume.iloc[-1])
            average_volume = float(volume.tail(20).mean())

            price_change = ((latest_close - previous_close) / previous_close) * 100
            volume_ratio = latest_volume / average_volume if average_volume else 1
            dollar_volume = latest_close * latest_volume

            score = self._score_flow(price_change, volume_ratio)
            bias = self._bias(score)

            return {
                "connected": True,
                "provider": self.provider,
                "symbol": self.symbol,
                "score": score,
                "bias": bias,
                "price_change_percent": round(price_change, 2),
                "volume_ratio": round(volume_ratio, 2),
                "latest_volume": int(latest_volume),
                "average_volume": int(average_volume),
                "dollar_volume": round(dollar_volume, 2),
                "summary": self._summary(score, bias, price_change, volume_ratio),
            }

        except Exception as error:
            return self._offline(str(error))

    def _get_series(self, data, column):
        try:
            if column not in data.columns:
                return None

            series = data[column]

            if hasattr(series, "columns"):
                series = series.iloc[:, 0]

            return series.dropna()

        except Exception:
            return None

    def _score_flow(self, price_change, volume_ratio):
        score = 50

        if price_change > 0:
            score += 10
        elif price_change < 0:
            score -= 10

        if volume_ratio >= 1.5:
            if price_change > 0:
                score += 25
            elif price_change < 0:
                score -= 25

        elif volume_ratio >= 1.2:
            if price_change > 0:
                score += 15
            elif price_change < 0:
                score -= 15

        elif volume_ratio < 0.8:
            score -= 5

        return max(0, min(100, round(score, 2)))

    def _bias(self, score):
        if score >= 70:
            return "Institutional Buying"
        if score <= 30:
            return "Institutional Selling"
        return "Neutral / Mixed"

    def _summary(self, score, bias, price_change, volume_ratio):
        return (
            f"{bias}. SPY changed {round(price_change, 2)}% with volume "
            f"{round(volume_ratio, 2)}x its 20-day average. "
            f"Institutional flow proxy score: {score}/100."
        )

    def _offline(self, reason):
        return {
            "connected": False,
            "provider": self.provider,
            "score": 50,
            "bias": "Unknown",
            "summary": f"Institutional flow unavailable. {reason}",
        }