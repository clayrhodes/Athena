"""
Athena Thesis Validator

Validates whether the institutional thesis
is strong enough to support a trade.
"""


def validate_thesis(thesis):

    score = 0

    if thesis.get("regime") == "Bull Trend":
        score += 25

    if thesis.get("institutional_bias") != "Bearish":
        score += 20

    if thesis.get("confidence", 0) >= 70:
        score += 20

    if thesis.get("trade_grade") in ["A", "A+", "B"]:
        score += 15

    if thesis.get("forecast") == "Bullish":
        score += 20

    return {
        "score": score,
        "passed": score >= 70,
    }