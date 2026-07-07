from news.news_engine import analyze_news


def analyze_macro_environment(market):
    """
    Athena Macro Engine V2

    Combines macro conditions with news sentiment.
    """

    news = analyze_news()

    vix = market.get("vix", 18)
    trend = market.get("trend", "Bullish")

    reasons = []

    score = 50

    # -------------------------
    # Trend
    # -------------------------

    if trend == "Bullish":
        score += 20
        reasons.append("Higher-timeframe trend is bullish.")

    elif trend == "Bearish":
        score -= 20
        reasons.append("Higher-timeframe trend is bearish.")

    # -------------------------
    # VIX
    # -------------------------

    if vix < 18:
        score += 15
        reasons.append("Low volatility supports risk assets.")

    elif vix > 25:
        score -= 20
        reasons.append("High volatility increases uncertainty.")

    # -------------------------
    # News
    # -------------------------

    if news["sentiment"] == "Bullish":
        score += 10
        reasons.append("News sentiment is bullish.")

    elif news["sentiment"] == "Bearish":
        score -= 10
        reasons.append("News sentiment is bearish.")

    score = max(0, min(score, 100))

    if score >= 75:
        environment = "Risk-On"

    elif score <= 35:
        environment = "Risk-Off"

    else:
        environment = "Neutral"

    return {
        "environment": environment,
        "score": score,
        "reasons": reasons,
        "news": news,
    }