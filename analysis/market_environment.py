def detect_market_environment(market, scores):
    price = market.get("price", 0)
    sma20 = market.get("sma20", 0)
    sma50 = market.get("sma50", 0)
    sma200 = market.get("sma200", 0)
    rsi = market.get("rsi", 50)

    trend_score = scores.get("trend", {}).get("score", 0)
    momentum_score = scores.get("momentum", {}).get("score", 0)
    volume_score = scores.get("volume", {}).get("score", 0)
    structure_score = scores.get("structure", {}).get("score", 0)
    vwap_score = scores.get("vwap", {}).get("score", 0)

    reasons = []

    bias = "Neutral"
    trend = "Mixed"
    condition = "Choppy"
    strategy = "Be patient. Wait for cleaner confirmation."

    if price > sma20 > sma50 > sma200 and trend_score >= 80:
        bias = "Bullish"
        trend = "Strong Uptrend"
        condition = "Trend Continuation"
        strategy = "Favor calls on pullbacks or clean breakout-retests."
        reasons.append("Price is above the 20, 50, and 200 SMA.")
        reasons.append("Moving averages are stacked bullish.")
        reasons.append("Trend score is strong.")

    elif price < sma20 < sma50 < sma200 and trend_score <= 30:
        bias = "Bearish"
        trend = "Strong Downtrend"
        condition = "Trend Continuation Lower"
        strategy = "Favor puts on failed bounces or clean breakdown-retests."
        reasons.append("Price is below the 20, 50, and 200 SMA.")
        reasons.append("Moving averages are stacked bearish.")
        reasons.append("Trend score is weak.")

    elif rsi > 70:
        bias = "Bullish but Extended"
        trend = "Uptrend"
        condition = "Overbought / Pullback Risk"
        strategy = "Do not chase. Wait for pullback or consolidation."
        reasons.append("RSI is overbought.")

    elif rsi < 30:
        bias = "Bearish but Oversold"
        trend = "Downtrend"
        condition = "Oversold / Bounce Risk"
        strategy = "Do not chase puts. Wait for reversal confirmation."
        reasons.append("RSI is oversold.")

    elif trend_score >= 70 and momentum_score < 60:
        bias = "Cautiously Bullish"
        trend = "Bullish Trend With Weak Momentum"
        condition = "Needs Momentum Confirmation"
        strategy = "Wait for momentum confirmation before buying."
        reasons.append("Trend is bullish.")
        reasons.append("Momentum is not confirming yet.")

    elif structure_score >= 80 and volume_score < 50:
        bias = "Cautiously Bullish"
        trend = "Bullish Structure With Weak Participation"
        condition = "Needs Volume Confirmation"
        strategy = "Wait for volume confirmation before entering."
        reasons.append("Market structure is strong.")
        reasons.append("Volume is weak.")

    elif vwap_score >= 75 and trend_score >= 70:
        bias = "Bullish"
        trend = "Above VWAP With Bullish Trend"
        condition = "Bullish Intraday Control"
        strategy = "Look for pullback to VWAP or breakout continuation."
        reasons.append("Price is above VWAP.")
        reasons.append("Trend is bullish.")

    return {
        "bias": bias,
        "trend": trend,
        "condition": condition,
        "strategy": strategy,
        "reasons": reasons,
    }