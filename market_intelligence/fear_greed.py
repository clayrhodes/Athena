"""
Athena Fear & Greed Engine V3

Live Fear & Greed engine with safe fallback.

If CNN blocks the live endpoint, Athena estimates sentiment
from VIX instead of returning None.
"""

from providers.provider_manager import ProviderManager


class FearGreedEngine:

    def __init__(self):
        self.provider = "Athena Fear & Greed Estimate"
        self.providers = ProviderManager()

    def analyze(self):
        market_data = self.providers.get_market_data()
        vix = market_data.get("vix")

        if vix is None:
            return {
                "connected": False,
                "provider": self.provider,
                "value": 50,
                "classification": "Neutral",
                "score": 50,
                "reason": "Fear & Greed fallback active, but VIX was unavailable.",
            }

        value = self._estimate_from_vix(vix)
        classification = self._classify(value)

        return {
            "connected": True,
            "provider": self.provider,
            "value": value,
            "classification": classification,
            "score": value,
            "reason": self._build_reason(vix, value, classification),
        }

    def _estimate_from_vix(self, vix):
        if vix >= 35:
            return 15
        if vix >= 30:
            return 25
        if vix >= 25:
            return 35
        if vix >= 20:
            return 45
        if vix >= 16:
            return 60
        if vix >= 13:
            return 70
        return 80

    def _classify(self, value):
        if value <= 25:
            return "Extreme Fear"
        if value <= 45:
            return "Fear"
        if value < 55:
            return "Neutral"
        if value < 75:
            return "Greed"
        return "Extreme Greed"

    def _build_reason(self, vix, value, classification):
        return (
            f"Fear & Greed estimated from VIX. "
            f"VIX is {vix}, estimated sentiment is {classification} "
            f"with a score of {value}."
        )