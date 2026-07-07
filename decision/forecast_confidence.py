def calculate_forecast_confidence(forecast):
    """
    Athena Forecast Confidence Engine

    Scores how trustworthy the forecast is.
    """

    score = 0

    if forecast["above20"]:
        score += 10

    if forecast["above50"]:
        score += 15

    if forecast["above200"]:
        score += 20

    if forecast["bullish_stack"]:
        score += 15

    if forecast["bearish_stack"]:
        score += 15

    if forecast["bullish_momentum"]:
        score += 10

    if forecast["bearish_momentum"]:
        score += 10

    if forecast["strong_volume"]:
        score += 10

    if forecast["weekly_bull"]:
        score += 5

    if forecast["daily_bull"]:
        score += 5

    if score > 100:
        score = 100

    return score