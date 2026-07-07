"""
Athena Macro Score Engine V1

Converts macroeconomic conditions into a
single score for the Decision Engine.
"""


class MacroScoreEngine:

    def calculate(
        self,
        sentiment_report,
        market_report,
    ):

        score = 50

        reasons = []

        vix = sentiment_report.get("vix")
        dxy = sentiment_report.get("dxy")
        treasury = sentiment_report.get("treasury_10y")

        if vix is not None:

            if vix < 15:
                score += 10
                reasons.append("Low VIX supports risk assets.")

            elif vix > 22:
                score -= 15
                reasons.append("Elevated VIX increases risk.")

        if dxy is not None:

            if dxy < 103:
                score += 5
                reasons.append("Weak dollar supports equities.")

            elif dxy > 106:
                score -= 10
                reasons.append("Strong dollar pressures equities.")

        if treasury is not None:

            if treasury < 45:
                score += 5
                reasons.append("Treasury yields are supportive.")

            elif treasury > 48:
                score -= 10
                reasons.append("Treasury yields remain restrictive.")

        score = max(0, min(100, score))

        return {
            "score": score,
            "reasons": reasons,
        }