"""
Athena Narrative Engine V1

Creates Athena's overall market narrative.
"""


def build_market_narrative(
    thesis,
    market_regime,
    institutional,
):

    narrative = []

    if market_regime.get("regime") == "Bull Trend":
        narrative.append(
            "Higher timeframes remain in a confirmed uptrend."
        )

    if institutional.get("score", 0) >= 60:
        narrative.append(
            "Institutional participation supports continuation."
        )
    else:
        narrative.append(
            "Institutional participation is mixed."
        )

    if thesis.get("validated"):
        narrative.append(
            "The institutional thesis currently supports maintaining a bullish bias."
        )
    else:
        narrative.append(
            "The institutional thesis is not yet strong enough for aggressive positioning."
        )

    return {
        "summary": " ".join(narrative)
    }