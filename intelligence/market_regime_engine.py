# intelligence/market_regime_engine.py

"""
Athena Market Regime Engine V2

Purpose:
Detects the current market regime and the market behavior type.

Primary Regime:
- Bull Trend
- Bear Trend
- Range / Chop
- High Volatility / Danger
- Bullish Breakout Attempt
- Bearish Breakdown Attempt
- No Clear Regime

Behavior Type:
- Clean Trend Day
- Weak Trend Day
- Balanced Auction
- Low Volume Drift
- Momentum Breakout Attempt
- Exhaustion Risk
- Confirmation Still Needed
"""


class MarketRegimeEngine:
    def __init__(self):
        self.name = "Athena Market Regime Engine V2"

    def analyze(
        self,
        trend_data=None,
        market_structure=None,
        mtf_data=None,
        vwap_data=None,
        momentum_data=None,
        volume_data=None,
        price_action=None,
        macro_data=None,
        fear_greed_data=None,
        auction_flow=None,
    ):
        trend_data = trend_data or {}
        market_structure = market_structure or {}
        mtf_data = mtf_data or {}
        vwap_data = vwap_data or {}
        momentum_data = momentum_data or {}
        volume_data = volume_data or {}
        price_action = price_action or {}
        macro_data = macro_data or {}
        fear_greed_data = fear_greed_data or {}
        auction_flow = auction_flow or {}

        bull_score = 0
        bear_score = 0
        chop_score = 0
        danger_score = 0
        notes = []
        warnings = []

        trend_score = self._get_score(trend_data)
        trend_text = self._get_text(trend_data)

        if trend_score >= 80 and self._has_any(trend_text, ["bull", "uptrend"]):
            bull_score += 30
            notes.append("Trend is strongly bullish.")
        elif trend_score >= 80 and self._has_any(trend_text, ["bear", "downtrend"]):
            bear_score += 30
            notes.append("Trend is strongly bearish.")
        elif trend_score >= 60:
            chop_score += 5
            notes.append("Trend is positive but not fully decisive.")
        else:
            chop_score += 10
            warnings.append("Trend is weak or unclear.")

        structure_score = self._get_score(market_structure)
        structure_text = self._get_text(market_structure)

        if structure_score >= 80 and not self._has_any(structure_text, ["bear", "lower low", "lower high"]):
            bull_score += 25
            notes.append("Market structure strongly supports bulls.")
        elif structure_score >= 80:
            bear_score += 25
            notes.append("Market structure strongly supports bears.")
        elif structure_score >= 60:
            chop_score += 5
            notes.append("Market structure is constructive but not dominant.")
        else:
            chop_score += 5

        weekly_score = self._find_number(mtf_data, ["weekly", "week"])
        daily_score = self._find_number(mtf_data, ["daily", "day"])
        hourly_score = self._find_number(mtf_data, ["hour", "1 hour", "one_hour", "1h"])

        if weekly_score >= 80 and daily_score >= 80:
            bull_score += 25
            notes.append("Weekly and daily timeframes are bullish.")
        elif weekly_score > 0 and daily_score > 0 and weekly_score <= 40 and daily_score <= 40:
            bear_score += 25
            notes.append("Weekly and daily timeframes are bearish.")
        elif weekly_score > 0 and daily_score > 0:
            chop_score += 10
            warnings.append("Higher timeframes are mixed.")

        if hourly_score > 0 and hourly_score < 70:
            chop_score += 10
            warnings.append("1 Hour confirmation is still weak, so entry timing matters.")

        vwap_score = self._get_score(vwap_data)

        if vwap_score >= 80:
            bull_score += 10
            notes.append("VWAP supports bullish control.")
        elif vwap_score > 0 and vwap_score <= 40:
            bear_score += 10
            notes.append("VWAP supports bearish control.")
        else:
            chop_score += 5

        momentum_score = self._get_score(momentum_data)

        if momentum_score >= 70:
            bull_score += 10
            notes.append("Momentum confirms participation.")
        elif momentum_score > 0 and momentum_score < 70:
            chop_score += 10
            warnings.append("Momentum is not strong enough yet.")

        volume_score = self._get_score(volume_data)

        if volume_score >= 70:
            bull_score += 10
            notes.append("Volume confirms the move.")
        elif volume_score > 0 and volume_score < 70:
            chop_score += 15
            warnings.append("Volume is not confirming yet.")

        price_action_score = self._get_score(price_action)

        if price_action_score >= 80:
            bull_score += 10
            notes.append("Price action supports continuation.")
        elif price_action_score > 0 and price_action_score <= 40:
            bear_score += 5
            warnings.append("Price action is weak.")

        auction_score = self._get_score(auction_flow)
        auction_text = self._get_text(auction_flow)

        auction_balanced = False

        if auction_score >= 70 and self._has_any(auction_text, ["bull", "accumulation"]):
            bull_score += 10
            notes.append("Auction flow confirms bullish imbalance.")
        elif auction_score >= 70 and self._has_any(auction_text, ["bear", "distribution"]):
            bear_score += 10
            notes.append("Auction flow confirms bearish imbalance.")
        elif self._has_any(auction_text, ["balanced", "rotation", "undecided"]):
            auction_balanced = True
            chop_score += 10
            warnings.append("Auction flow is balanced.")
        elif auction_score > 0 and auction_score < 70:
            chop_score += 5
            warnings.append("Auction flow is not confirming trend yet.")

        macro_score = self._find_number(macro_data, ["macro_score"])
        sentiment_score = self._find_number(macro_data, ["sentiment_score"])
        fear_greed_value = self._find_number(fear_greed_data, ["fear_greed"])

        if macro_score > 0 and macro_score < 40:
            danger_score += 15
            warnings.append("Macro score is risk-off.")

        if sentiment_score > 0 and sentiment_score < 40:
            danger_score += 10
            warnings.append("Sentiment is risk-off.")

        if fear_greed_value > 0 and (fear_greed_value >= 80 or fear_greed_value <= 20):
            danger_score += 10
            warnings.append("Fear & Greed is at an extreme.")

        regime = self._classify_primary_regime(
            bull_score,
            bear_score,
            chop_score,
            danger_score,
        )

        confidence = self._calculate_confidence(
            regime,
            bull_score,
            bear_score,
            chop_score,
            danger_score,
        )

        behavior = self._classify_behavior(
            regime,
            bull_score,
            bear_score,
            chop_score,
            danger_score,
            hourly_score,
            momentum_score,
            volume_score,
            price_action_score,
            auction_balanced,
        )

        strategy = self._strategy_for_regime(regime, behavior)

        return {
            "engine": self.name,
            "regime": regime,
            "behavior": behavior,
            "confidence": confidence,
            "bull_score": bull_score,
            "bear_score": bear_score,
            "chop_score": chop_score,
            "danger_score": danger_score,
            "summary": f"Market Regime: {regime}. Behavior: {behavior}. Confidence: {confidence}%.",
            "strategy": strategy,
            "notes": notes,
            "warnings": warnings,
        }

    def _classify_primary_regime(self, bull_score, bear_score, chop_score, danger_score):
        if danger_score >= 25:
            return "High Volatility / Danger"

        if bull_score >= 75 and bull_score >= bear_score + 20:
            return "Bull Trend"

        if bear_score >= 75 and bear_score >= bull_score + 20:
            return "Bear Trend"

        if chop_score >= 45 and bull_score < 75 and bear_score < 75:
            return "Range / Chop"

        if bull_score >= 55 and bull_score > bear_score:
            return "Bullish Breakout Attempt"

        if bear_score >= 55 and bear_score > bull_score:
            return "Bearish Breakdown Attempt"

        return "No Clear Regime"

    def _calculate_confidence(self, regime, bull_score, bear_score, chop_score, danger_score):
        if regime == "High Volatility / Danger":
            return min(95, 60 + danger_score)

        if regime == "Bull Trend":
            return min(95, bull_score)

        if regime == "Bear Trend":
            return min(95, bear_score)

        if regime == "Range / Chop":
            return min(90, 50 + chop_score)

        if "Breakout" in regime or "Breakdown" in regime:
            return min(85, max(bull_score, bear_score))

        return 50

    def _classify_behavior(
        self,
        regime,
        bull_score,
        bear_score,
        chop_score,
        danger_score,
        hourly_score,
        momentum_score,
        volume_score,
        price_action_score,
        auction_balanced,
    ):
        if danger_score >= 25:
            return "Risk-Off / Danger Tape"

        if auction_balanced:
            return "Balanced Auction"

        if regime in ["Bull Trend", "Bear Trend"]:
            if hourly_score >= 70 and momentum_score >= 70 and volume_score >= 70:
                return "Clean Trend Day"

            if price_action_score >= 80 and (momentum_score < 70 or volume_score < 70):
                return "Weak Trend Day / Confirmation Needed"

            return "Trend Continuation With Entry Timing Risk"

        if regime == "Range / Chop":
            if volume_score < 50:
                return "Low Volume Drift"

            return "Choppy Two-Way Trade"

        if regime == "Bullish Breakout Attempt":
            if momentum_score >= 70 and volume_score >= 70:
                return "Momentum Breakout Attempt"

            return "Breakout Attempt Needs Confirmation"

        if regime == "Bearish Breakdown Attempt":
            if momentum_score >= 70 and volume_score >= 70:
                return "Momentum Breakdown Attempt"

            return "Breakdown Attempt Needs Confirmation"

        if chop_score >= 45:
            return "Confirmation Still Needed"

        return "Unclear Tape"

    def _strategy_for_regime(self, regime, behavior):
        if regime == "Bull Trend":
            if "Clean Trend" in behavior:
                return "Favor calls on pullbacks, breakout-retests, or VWAP holds. Avoid fading strength."
            return "Favor calls only after confirmation. Wait for 1 Hour, momentum, or volume to improve."

        if regime == "Bear Trend":
            if "Clean Trend" in behavior:
                return "Favor puts on failed bounces, rejection retests, or VWAP loses. Avoid fighting downside momentum."
            return "Favor puts only after confirmation. Wait for bearish momentum and volume to confirm."

        if regime == "Range / Chop":
            return "Avoid chasing. Favor patience, smaller size, or no trade until range breaks cleanly."

        if regime == "High Volatility / Danger":
            return "Protect capital. Avoid new trades unless setup is exceptional and risk is tightly controlled."

        if "Breakout" in regime:
            return "Wait for breakout confirmation, retest, and volume before entering."

        if "Breakdown" in regime:
            return "Wait for breakdown confirmation, failed retest, and volume before entering."

        return "No clear edge. Wait for cleaner confirmation."

    def _get_score(self, data):
        if not isinstance(data, dict):
            return 0

        for key in ["score", "overall_score", "trend_score"]:
            if key in data:
                return self._safe_number(data.get(key))

        for value in data.values():
            if isinstance(value, dict):
                nested_score = self._get_score(value)
                if nested_score > 0:
                    return nested_score

        return 0

    def _find_number(self, data, keywords):
        if not isinstance(data, dict):
            return 0

        for key, value in data.items():
            key_text = str(key).lower()

            if any(keyword in key_text for keyword in keywords):
                if isinstance(value, dict):
                    score = self._get_score(value)
                    if score > 0:
                        return score
                else:
                    number = self._safe_number(value)
                    if number > 0:
                        return number

        for value in data.values():
            if isinstance(value, dict):
                found = self._find_number(value, keywords)
                if found > 0:
                    return found

        return 0

    def _safe_number(self, value):
        try:
            if value is None:
                return 0
            return float(value)
        except (TypeError, ValueError):
            return 0

    def _get_text(self, data):
        if not isinstance(data, dict):
            return ""

        parts = []

        for value in data.values():
            if isinstance(value, dict):
                parts.append(self._get_text(value))
            else:
                parts.append(str(value).lower())

        return " ".join(parts)

    def _has_any(self, text, keywords):
        text = str(text).lower()
        return any(keyword in text for keyword in keywords)