def get_score(scores, category):
    if category == "weekly":
        return scores.get("multi_timeframe", {}).get("Weekly", {}).get("score", 0)

    if category == "daily":
        return scores.get("multi_timeframe", {}).get("Daily", {}).get("score", 0)

    if category == "hourly":
        return scores.get("multi_timeframe", {}).get("1 Hour", {}).get("score", 0)

    return scores.get(category, {}).get("score", 0)


def _get_report_score(scores, key):
    value = scores.get(key, {})

    if isinstance(value, dict):
        return value.get("score", 0)

    return 0


DECISION_RULES = {
    "trend": {"label": "Trend", "weight": 14, "minimum": 70},
    "structure": {"label": "Market Structure", "weight": 12, "minimum": 70},
    "weekly": {"label": "Weekly Timeframe", "weight": 10, "minimum": 70},
    "daily": {"label": "Daily Timeframe", "weight": 8, "minimum": 70},
    "hourly": {"label": "1 Hour Confirmation", "weight": 8, "minimum": 70},
    "vwap": {"label": "VWAP", "weight": 7, "minimum": 70},
    "price_action": {"label": "Price Action", "weight": 7, "minimum": 70},
    "auction_flow": {"label": "Auction Flow", "weight": 5, "minimum": 70},
    "momentum": {"label": "Momentum", "weight": 3, "minimum": 70},
    "volume": {"label": "Volume", "weight": 2, "minimum": 70},

    # Institutional decision inputs
    "smart_money": {"label": "Smart Money", "weight": 5, "minimum": 60},
    "liquidity": {"label": "Liquidity", "weight": 4, "minimum": 60},
    "market_breadth": {"label": "Market Breadth", "weight": 5, "minimum": 55},
    "options_flow": {"label": "Options Flow", "weight": 5, "minimum": 55},
    "historical_similarity": {"label": "Historical Similarity", "weight": 3, "minimum": 55},
}


def evaluate_decision_matrix(scores):
    rows = []
    earned_weight = 0
    total_weight = 0

    report_score_keys = [
        "smart_money",
        "liquidity",
        "market_breadth",
        "options_flow",
        "historical_similarity",
    ]

    for key, rule in DECISION_RULES.items():
        if key in report_score_keys:
            score = _get_report_score(scores, key)
        else:
            score = get_score(scores, key)

        weight = rule["weight"]
        minimum = rule["minimum"]
        passed = score >= minimum

        total_weight += weight

        if passed:
            earned_weight += weight

        rows.append({
            "key": key,
            "label": rule["label"],
            "score": score,
            "minimum": minimum,
            "weight": weight,
            "passed": passed,
        })

    readiness = round((earned_weight / total_weight) * 100) if total_weight > 0 else 0

    failed = [row for row in rows if not row["passed"]]
    passed = [row for row in rows if row["passed"]]

    hard_blocks = []

    hourly_score = get_score(scores, "hourly")
    momentum_score = get_score(scores, "momentum")
    volume_score = get_score(scores, "volume")

    smart_money = scores.get("smart_money", {})
    liquidity = scores.get("liquidity", {})
    market_breadth = scores.get("market_breadth", {})
    options_flow = scores.get("options_flow", {})
    historical = scores.get("historical_similarity", {})

    smart_money_bias = smart_money.get("bias", "NEUTRAL")
    liquidity_condition = liquidity.get("condition", "BALANCED")
    breadth_condition = market_breadth.get("condition", "UNKNOWN")
    options_condition = options_flow.get("condition", "UNKNOWN")
    historical_quality = historical.get("quality", "UNKNOWN")

    if hourly_score < 70:
        hard_blocks.append("1 Hour Confirmation is not ready.")

    if momentum_score < 70:
        hard_blocks.append("Momentum is not strong enough.")

    if volume_score < 70:
        hard_blocks.append("Volume is not confirming the move.")

    if smart_money_bias == "DISTRIBUTION":
        hard_blocks.append("Smart Money shows distribution.")

    if liquidity_condition == "ACTIVE LIQUIDITY SWEEP":
        hard_blocks.append("Liquidity sweep detected. Wait for confirmation.")

    if breadth_condition == "WEAK PARTICIPATION":
        hard_blocks.append("Market breadth shows weak participation.")

    if breadth_condition == "INTERNAL DIVERGENCE":
        hard_blocks.append("Market breadth shows internal divergence.")

    if options_condition == "BEARISH INSTITUTIONAL FLOW":
        hard_blocks.append("Options flow is bearish.")

    if options_condition == "UNUSUAL MIXED FLOW":
        hard_blocks.append("Options flow is mixed. Wait for confirmation.")

    if historical_quality == "WEAK HISTORICAL PROFILE":
        hard_blocks.append("Historical similarity is weak.")

    if readiness >= 90 and not hard_blocks:
        action = "BUY NOW"
    elif readiness >= 70:
        action = "WAIT FOR ENTRY"
    else:
        action = "NO TRADE"

    return {
        "rows": rows,
        "passed": passed,
        "failed": failed,
        "readiness": readiness,
        "action": action,
        "earned_weight": earned_weight,
        "total_weight": total_weight,
        "hard_blocks": hard_blocks,
    }