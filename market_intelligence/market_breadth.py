"""
Athena Market Breadth Engine V3

Purpose:
- Analyze market breadth from the Provider Manager.
- Keep Athena stable when live breadth data is not connected.
- Prepare Athena for advance/decline, new highs/lows,
  and moving-average participation data.
"""


class MarketBreadthEngine:

    def analyze(self, breadth_data=None):

        if not breadth_data or not breadth_data.get("connected", False):
            return {
                "connected": False,
                "status": "OFFLINE",
                "breadth": "Unknown",
                "score": 50,
                "advancers": 0,
                "decliners": 0,
                "advance_decline_ratio": None,
                "new_highs": 0,
                "new_lows": 0,
                "new_high_low_ratio": None,
                "percent_above_20_sma": None,
                "percent_above_50_sma": None,
                "percent_above_200_sma": None,
                "summary": "Live market breadth not connected.",
                "bullish_signals": [],
                "bearish_signals": [],
                "warnings": [
                    "Athena is treating market breadth as neutral until live breadth is connected."
                ],
            }

        advancers = breadth_data.get("advancers", 0)
        decliners = breadth_data.get("decliners", 0)
        new_highs = breadth_data.get("new_highs", 0)
        new_lows = breadth_data.get("new_lows", 0)

        percent_above_20 = breadth_data.get("percent_above_20_sma")
        percent_above_50 = breadth_data.get("percent_above_50_sma")
        percent_above_200 = breadth_data.get("percent_above_200_sma")

        total_ad = advancers + decliners
        total_hl = new_highs + new_lows

        ad_ratio = advancers / total_ad if total_ad > 0 else 0.5
        high_low_ratio = new_highs / total_hl if total_hl > 0 else 0.5

        score = 50
        bullish_signals = []
        bearish_signals = []
        warnings = []

        if ad_ratio >= 0.70:
            score += 25
            bullish_signals.append(
                f"Strong breadth thrust: {ad_ratio:.0%} of tracked stocks are advancing."
            )
        elif ad_ratio >= 0.60:
            score += 15
            bullish_signals.append(
                f"Positive participation: {ad_ratio:.0%} of tracked stocks are advancing."
            )
        elif ad_ratio <= 0.30:
            score -= 25
            bearish_signals.append(
                f"Severe weak participation: only {ad_ratio:.0%} of tracked stocks are advancing."
            )
        elif ad_ratio <= 0.40:
            score -= 15
            bearish_signals.append(
                f"Weak participation: only {ad_ratio:.0%} of tracked stocks are advancing."
            )
        else:
            warnings.append("Advance/decline participation is mixed.")

        if high_low_ratio >= 0.70:
            score += 15
            bullish_signals.append(
                f"New highs strongly lead new lows: {high_low_ratio:.0%} positive high/low ratio."
            )
        elif high_low_ratio >= 0.60:
            score += 8
            bullish_signals.append(
                f"New highs are leading new lows: {high_low_ratio:.0%} positive high/low ratio."
            )
        elif high_low_ratio <= 0.30:
            score -= 15
            bearish_signals.append(
                f"New lows strongly outweigh new highs: {high_low_ratio:.0%} positive high/low ratio."
            )
        elif high_low_ratio <= 0.40:
            score -= 8
            bearish_signals.append(
                f"New lows are outweighing new highs: {high_low_ratio:.0%} positive high/low ratio."
            )
        else:
            warnings.append("New highs versus new lows are mixed.")

        if percent_above_20 is not None:
            if percent_above_20 >= 65:
                score += 8
                bullish_signals.append(
                    f"{percent_above_20}% of stocks are above the 20-day SMA."
                )
            elif percent_above_20 <= 40:
                score -= 8
                bearish_signals.append(
                    f"Only {percent_above_20}% of stocks are above the 20-day SMA."
                )

        if percent_above_50 is not None:
            if percent_above_50 >= 65:
                score += 10
                bullish_signals.append(
                    f"{percent_above_50}% of stocks are above the 50-day SMA."
                )
            elif percent_above_50 <= 40:
                score -= 10
                bearish_signals.append(
                    f"Only {percent_above_50}% of stocks are above the 50-day SMA."
                )

        if percent_above_200 is not None:
            if percent_above_200 >= 60:
                score += 7
                bullish_signals.append(
                    f"{percent_above_200}% of stocks are above the 200-day SMA."
                )
            elif percent_above_200 <= 40:
                score -= 7
                bearish_signals.append(
                    f"Only {percent_above_200}% of stocks are above the 200-day SMA."
                )

        score = max(0, min(100, int(score)))

        if score >= 80:
            breadth = "Strong Bullish"
            summary = "Market breadth shows strong broad participation."
        elif score >= 70:
            breadth = "Bullish"
            summary = "Market breadth supports upside participation."
        elif score <= 30:
            breadth = "Strong Bearish"
            summary = "Market breadth shows broad downside participation."
        elif score <= 40:
            breadth = "Bearish"
            summary = "Market breadth is weak and warns of downside risk."
        else:
            breadth = "Neutral"
            summary = "Market breadth is mixed or neutral."

        return {
            "connected": True,
            "status": "ACTIVE",
            "breadth": breadth,
            "score": score,
            "advancers": advancers,
            "decliners": decliners,
            "advance_decline_ratio": ad_ratio,
            "new_highs": new_highs,
            "new_lows": new_lows,
            "new_high_low_ratio": high_low_ratio,
            "percent_above_20_sma": percent_above_20,
            "percent_above_50_sma": percent_above_50,
            "percent_above_200_sma": percent_above_200,
            "summary": summary,
            "bullish_signals": bullish_signals,
            "bearish_signals": bearish_signals,
            "warnings": warnings,
        }