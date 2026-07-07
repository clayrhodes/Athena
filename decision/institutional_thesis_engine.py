"""
Athena Institutional Thesis Engine V4

Creates Athena's institutional market thesis.
"""

from decision.thesis_validator import validate_thesis


def build_institutional_thesis(
    market_regime,
    institutional,
    forecast,
    probability,
    conviction,
    decision_matrix,
):

    readiness = decision_matrix.get("readiness", 0)

    confidence = round(
        (
            market_regime.get("confidence", 0)
            + conviction.get("score", 0)
            + readiness
        ) / 3
    )

    bull_probability = probability.get(
        "probabilities",
        {},
    ).get(
        "Bullish Continuation",
        0,
    )

    evidence = []

    if market_regime.get("regime") == "Bull Trend":
        evidence.append(
            "Higher timeframes remain in a confirmed bull trend."
        )

    if institutional.get("score", 0) >= 60:
        evidence.append(
            "Institutional participation supports continuation."
        )
    else:
        evidence.append(
            "Institutional participation remains mixed."
        )

    if bull_probability >= 45:
        evidence.append(
            "Bullish continuation remains the highest probability path."
        )

    if readiness >= 85:
        evidence.append(
            "Decision Matrix has reached trading readiness."
        )
    else:
        evidence.append(
            "Decision Matrix still requires additional confirmation."
        )

    risks = []

    if readiness < 85:
        risks.append(
            "Trade readiness has not reached Athena's threshold."
        )

    if conviction.get("score", 0) < 85:
        risks.append(
            "Conviction is solid but not yet elite."
        )

    thesis = {
        "title": "Institutional Market Thesis",
        "regime": market_regime.get(
            "regime",
            "Unknown",
        ),
        "confidence": confidence,
        "conviction": conviction.get(
            "verdict",
            "Unknown",
        ),
        "trade_grade": "B",
        "institutional_bias": institutional.get(
            "bias",
            "Neutral",
        ),
        "forecast": forecast.get(
            "direction",
            "Unknown",
        ),
        "primary_scenario": probability.get(
            "most_likely",
            "Unknown",
        ),
        "bull_probability": bull_probability,
        "evidence": evidence,
        "risks": risks,
        "summary": " ".join(evidence),
    }

    validation = validate_thesis(thesis)

    thesis["validation_score"] = validation["score"]
    thesis["validated"] = validation["passed"]

    return thesis