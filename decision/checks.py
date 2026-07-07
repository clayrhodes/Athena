def run_checks(scores):

    checks = []

    def add_check(name, passed, waiting_for, weight):
        checks.append({
            "name": name,
            "passed": passed,
            "waiting_for": waiting_for,
            "weight": weight
        })

    add_check(
        "Weekly Trend",
        scores["multi_timeframe"]["Weekly"]["score"] >= 75,
        "Weekly trend confirmation",
        18,
    )

    add_check(
        "Daily Trend",
        scores["multi_timeframe"]["Daily"]["score"] >= 75,
        "Daily trend confirmation",
        15,
    )

    add_check(
        "Trend",
        scores["trend"]["score"] >= 80,
        "Trend strength above 80",
        13,
    )

    add_check(
        "Market Structure",
        scores["structure"]["score"] >= 80,
        "Clear market structure",
        13,
    )

    add_check(
        "Price Action",
        scores["price_action"]["score"] >= 65,
        "Better price action confirmation",
        12,
    )

    add_check(
        "VWAP",
        scores["vwap"]["score"] >= 75,
        "VWAP confirmation",
        10,
    )

    add_check(
        "Momentum",
        scores["momentum"]["score"] >= 70,
        "Momentum confirmation",
        10,
    )

    add_check(
        "Volume",
        scores["volume"]["score"] >= 60,
        "Above-average volume",
        7,
    )

    add_check(
        "Smart Money",
        scores["smart_money"]["passed"],
        "Institutional activity not confirmed",
        7,
    )

    add_check(
        "Liquidity",
        scores["liquidity"]["score"] >= 60,
        "Liquidity sweep not confirmed",
        6,
    )

    add_check(
        "Historical Similarity",
        scores["historical_similarity"]["score"] >= 60,
        "Historical match too weak",
        4,
    )

    add_check(
        "1 Hour Trend",
        scores["multi_timeframe"]["1 Hour"]["score"] >= 75,
        "1-hour trend confirmation",
        2,
    )

    return checks