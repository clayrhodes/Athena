def calculate_scenario_probabilities(forecast):
    """
    Athena Scenario Probability Engine

    Converts market evidence into scenario probabilities.
    """

    score = 50

    if forecast["weekly_bull"]:
        score += 10

    if forecast["daily_bull"]:
        score += 10

    if forecast["above20"]:
        score += 5

    if forecast["above50"]:
        score += 5

    if forecast["above200"]:
        score += 5

    if forecast["bullish_stack"]:
        score += 5

    if forecast["bullish_momentum"]:
        score += 5

    if forecast["strong_volume"]:
        score += 5

    score = max(0, min(score, 95))

    primary = score

    remaining = 100 - primary

    secondary = int(remaining * 0.65)
    failure = remaining - secondary

    return {
        "primary": primary,
        "secondary": secondary,
        "failure": failure,
    }