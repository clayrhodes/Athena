"""
Athena Adaptive Confidence Engine V1

Adjusts Athena's confidence using
historical performance.
"""


def build_adaptive_confidence(
    thesis,
    similarity,
):

    confidence = thesis.get(
        "confidence",
        0,
    )

    confidence += similarity.get(
        "confidence_adjustment",
        0,
    )

    confidence = max(
        0,
        min(
            100,
            confidence,
        ),
    )

    if confidence >= 90:
        rating = "ELITE"

    elif confidence >= 80:
        rating = "HIGH"

    elif confidence >= 70:
        rating = "GOOD"

    elif confidence >= 60:
        rating = "MODERATE"

    else:
        rating = "LOW"

    return {
        "confidence": confidence,
        "rating": rating,
    }