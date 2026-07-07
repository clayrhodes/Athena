"""
Athena Auction Flow Engine V3

Purpose:
- Read price behavior like an auction.
- Detect buyer control, seller control, balance, acceptance, and rejection.
- Safely handles VWAP whether it is a number or a dictionary.
"""


class AuctionFlowEngine:

    def analyze(self, market=None):
        if not market:
            return self._offline_report()

        current_price = market.get("current_price") or market.get("spy")
        vwap_value = self._extract_vwap_value(market.get("vwap"))
        previous_close = market.get("previous_close")
        day_high = market.get("day_high")
        day_low = market.get("day_low")

        score = 50
        bullish_signals = []
        bearish_signals = []
        warnings = []

        if current_price is None:
            return self._offline_report("Current price unavailable.")

        if previous_close is not None:
            if current_price > previous_close:
                score += 10
                bullish_signals.append("Price is trading above previous close.")
            elif current_price < previous_close:
                score -= 10
                bearish_signals.append("Price is trading below previous close.")

        if vwap_value is not None:
            if current_price > vwap_value:
                score += 15
                bullish_signals.append("Price is accepted above VWAP.")
            elif current_price < vwap_value:
                score -= 15
                bearish_signals.append("Price is accepted below VWAP.")
            else:
                warnings.append("Price is sitting directly on VWAP.")
        else:
            warnings.append("VWAP unavailable for auction confirmation.")

        if day_high is not None and day_low is not None:
            day_range = day_high - day_low

            if day_range > 0:
                position_in_range = (current_price - day_low) / day_range

                if position_in_range >= 0.70:
                    score += 10
                    bullish_signals.append("Price is holding in the upper part of the daily range.")
                elif position_in_range <= 0.30:
                    score -= 10
                    bearish_signals.append("Price is holding in the lower part of the daily range.")
                else:
                    warnings.append("Price is near the middle of the daily range.")
        else:
            warnings.append("Daily high/low unavailable for auction range analysis.")

        score = max(0, min(100, score))

        if score >= 70:
            bias = "BULLISH AUCTION"
            summary = "Auction behavior favors buyers."
        elif score <= 30:
            bias = "BEARISH AUCTION"
            summary = "Auction behavior favors sellers."
        else:
            bias = "BALANCED AUCTION"
            summary = "Auction behavior is balanced or undecided."

        return {
            "connected": True,
            "status": "ACTIVE",
            "bias": bias,
            "score": score,
            "summary": summary,
            "bullish_signals": bullish_signals,
            "bearish_signals": bearish_signals,
            "warnings": warnings,
        }

    def _extract_vwap_value(self, vwap):
        if vwap is None:
            return None

        if isinstance(vwap, (int, float)):
            return float(vwap)

        if isinstance(vwap, dict):
            for key in ["value", "price", "level", "vwap"]:
                if key in vwap and vwap.get(key) is not None:
                    try:
                        return float(vwap.get(key))
                    except Exception:
                        return None

        return None

    def _offline_report(self, reason="Market data unavailable."):
        return {
            "connected": False,
            "status": "OFFLINE",
            "bias": "UNKNOWN",
            "score": 50,
            "summary": "Auction flow not available.",
            "bullish_signals": [],
            "bearish_signals": [],
            "warnings": [reason],
        }