"""
Athena News Intelligence Engine V3

Live Finnhub news intelligence.

This engine:
- Pulls live headlines from providers/news_provider.py
- Scores news sentiment
- Detects bullish and bearish news pressure
- Feeds the Mission Brief with real market news
"""

from providers.news_provider import NewsProvider
from news.news_sources import NEWS_SOURCES


def get_enabled_sources():
    sources = [s for s in NEWS_SOURCES if s["enabled"]]

    sources.sort(
        key=lambda source: source["priority"],
        reverse=True,
    )

    return sources


def analyze_news(symbol="SPY"):
    provider = NewsProvider()
    news_data = provider.get_news(symbol=symbol, limit=10)

    headlines = news_data.get("headlines", [])

    score = score_headlines(headlines)
    sentiment = sentiment_from_score(score)
    risk_level = risk_from_headlines(headlines)
    bullish_factors = find_bullish_factors(headlines)
    bearish_factors = find_bearish_factors(headlines)
    catalysts = find_major_catalysts(headlines)

    connected = news_data.get("connected", False)

    if connected:
        trade_warning = "Live Finnhub news connected."
        recommendation = build_recommendation(score, risk_level)
        confidence = min(90, 40 + len(headlines) * 5)
        reason = "Live headlines analyzed successfully."
        status = "LIVE"
    else:
        trade_warning = "Live news source not connected or no headlines returned."
        recommendation = "Do not let news affect trade decisions yet."
        confidence = 0
        reason = "Finnhub provider returned no usable live headlines."
        status = "OFFLINE"

    return {
        "engine": "Athena News Intelligence Engine V3",
        "status": status,
        "provider": news_data.get("provider", "Unknown"),
        "sources": get_enabled_sources(),
        "headlines": headlines,
        "sentiment": sentiment,
        "market_news_bias": sentiment,
        "news_risk_level": risk_level,
        "score": score,
        "confidence": confidence,
        "bullish_factors": bullish_factors,
        "bearish_factors": bearish_factors,
        "major_catalysts": catalysts,
        "trade_warning": trade_warning,
        "recommendation": recommendation,
        "reason": reason,
        "provider_errors": news_data.get("errors", []),
    }


def score_headlines(headlines):
    score = 50

    bullish_words = [
        "rally", "surge", "gain", "gains", "higher", "bullish",
        "growth", "beat", "beats", "strong", "optimism",
        "record", "rebound", "recover", "soft landing",
        "rate cut", "rate cuts", "cooling inflation",
    ]

    bearish_words = [
        "selloff", "sell-off", "drop", "drops", "fall", "falls",
        "lower", "bearish", "recession", "miss", "misses",
        "weak", "fear", "inflation", "rate hike", "rate hikes",
        "war", "crisis", "default", "slowdown", "risk-off",
    ]

    text = " ".join(headlines).lower()

    for word in bullish_words:
        if word in text:
            score += 4

    for word in bearish_words:
        if word in text:
            score -= 4

    return max(0, min(100, score))


def sentiment_from_score(score):
    if score >= 65:
        return "Bullish"

    if score <= 35:
        return "Bearish"

    return "Neutral"


def risk_from_headlines(headlines):
    text = " ".join(headlines).lower()

    high_risk_words = [
        "fed", "powell", "cpi", "inflation", "jobs report",
        "fomc", "rate decision", "war", "crisis",
        "tariff", "shutdown",
    ]

    for word in high_risk_words:
        if word in text:
            return "Elevated"

    return "Low"


def find_bullish_factors(headlines):
    factors = []
    text = " ".join(headlines).lower()

    checks = {
        "Positive market momentum in headlines.": ["rally", "surge", "higher", "gain"],
        "Growth or earnings strength mentioned.": ["growth", "beat", "strong"],
        "Rate-cut or soft-landing language detected.": ["rate cut", "soft landing", "cooling inflation"],
    }

    for factor, words in checks.items():
        if any(word in text for word in words):
            factors.append(factor)

    return factors


def find_bearish_factors(headlines):
    factors = []
    text = " ".join(headlines).lower()

    checks = {
        "Risk-off or selloff language detected.": ["selloff", "sell-off", "risk-off"],
        "Inflation or rate-hike pressure detected.": ["inflation", "rate hike", "rate hikes"],
        "Recession, weakness, or slowdown language detected.": ["recession", "weak", "slowdown"],
        "Geopolitical or crisis risk detected.": ["war", "crisis", "shutdown", "default"],
    }

    for factor, words in checks.items():
        if any(word in text for word in words):
            factors.append(factor)

    return factors


def find_major_catalysts(headlines):
    catalysts = []
    text = " ".join(headlines).lower()

    checks = {
        "Federal Reserve": ["fed", "powell", "fomc", "rate decision"],
        "Inflation": ["cpi", "inflation", "ppi"],
        "Labor Market": ["jobs report", "payrolls", "unemployment"],
        "Geopolitical Risk": ["war", "crisis", "tariff"],
        "Government Risk": ["shutdown", "debt ceiling", "default"],
    }

    for catalyst, words in checks.items():
        if any(word in text for word in words):
            catalysts.append(catalyst)

    return catalysts


def build_recommendation(score, risk_level):
    if risk_level == "Elevated":
        return "Use caution. Market-moving news risk is elevated."

    if score >= 65:
        return "News backdrop supports bullish trades."

    if score <= 35:
        return "News backdrop warns against bullish trades."

    return "News backdrop is neutral. Let price action and confirmation lead."


def format_news_section(news):
    lines = []

    lines.append("ATHENA NEWS INTELLIGENCE")
    lines.append("-" * 30)

    lines.append(f"Engine: {news['engine']}")
    lines.append(f"Status: {news['status']}")
    lines.append(f"Provider: {news['provider']}")
    lines.append(f"Sentiment: {news['sentiment']}")
    lines.append(f"Bias: {news['market_news_bias']}")
    lines.append(f"Risk Level: {news['news_risk_level']}")
    lines.append(f"News Score: {news['score']}")
    lines.append(f"Confidence: {news['confidence']}%")

    lines.append("")
    lines.append("Headlines:")

    if news["headlines"]:
        for headline in news["headlines"]:
            lines.append(f"- {headline}")
    else:
        lines.append("- None")

    if news["bullish_factors"]:
        lines.append("")
        lines.append("Bullish News Factors:")
        for factor in news["bullish_factors"]:
            lines.append(f"- {factor}")

    if news["bearish_factors"]:
        lines.append("")
        lines.append("Bearish News Factors:")
        for factor in news["bearish_factors"]:
            lines.append(f"- {factor}")

    if news["major_catalysts"]:
        lines.append("")
        lines.append("Major Catalysts Detected:")
        for catalyst in news["major_catalysts"]:
            lines.append(f"- {catalyst}")

    if news.get("provider_errors"):
        lines.append("")
        lines.append("Provider Errors:")
        for error in news["provider_errors"]:
            lines.append(f"- {error}")

    lines.append("")
    lines.append(news["trade_warning"])
    lines.append("")
    lines.append(news["recommendation"])

    return "\n".join(lines)


def build_news_section(symbol="SPY"):
    news = analyze_news(symbol=symbol)
    return format_news_section(news)