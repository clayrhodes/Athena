"""
Athena Sentiment Engine V2

Uses live market-wide data from the Provider Layer.

Inputs:
- VIX
- DXY
- 10-Year Treasury Yield

Output:
A simple market sentiment score.
"""

from providers.provider_manager import ProviderManager


class SentimentEngine:

    def __init__(self):
        self.providers = ProviderManager()

    def analyze(self):
        market_data = self.providers.get_market_data()

        vix = market_data.get("vix")
        dxy = market_data.get("dxy")
        treasury_10y = market_data.get("treasury_10y")

        score = 50
        warnings = []
        bullish_factors = []
        bearish_factors = []

        if vix is not None:
            if vix < 15:
                score += 10
                bullish_factors.append("VIX is low.")
            elif vix > 22:
                score -= 15
                bearish_factors.append("VIX is elevated.")
                warnings.append("Higher volatility risk.")

        if dxy is not None:
            if dxy < 103:
                score += 5
                bullish_factors.append("Dollar index is not pressuring equities.")
            elif dxy > 106:
                score -= 10
                bearish_factors.append("Strong dollar may pressure equities.")

        if treasury_10y is not None:
            if treasury_10y < 45:
                score += 5
                bullish_factors.append("10-year yield is not highly restrictive.")
            elif treasury_10y > 48:
                score -= 10
                bearish_factors.append("10-year yield is elevated.")

        score = max(0, min(100, score))

        if score >= 70:
            overall = "Bullish"
        elif score <= 35:
            overall = "Bearish"
        else:
            overall = "Neutral"

        return {
            "overall_sentiment": overall,
            "score": score,
            "vix": vix,
            "dxy": dxy,
            "treasury_10y": treasury_10y,
            "fear_greed": market_data.get("fear_greed"),
            "bullish_factors": bullish_factors,
            "bearish_factors": bearish_factors,
            "warnings": warnings,
            "provider_connected": market_data.get("connected", False),
        }