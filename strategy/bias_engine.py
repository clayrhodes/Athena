def determine_bias(market):

    score = 0

    price = market["price"]
    sma20 = market["sma20"]
    sma50 = market["sma50"]
    sma200 = market["sma200"]
    rsi = market["rsi"]
    macd = market["macd"]
    current_volume = market["current_volume"]
    average_volume = market["average_volume"]

    if price > sma20:
        score += 15
    else:
        score -= 15

    if price > sma50:
        score += 20
    else:
        score -= 20

    if price > sma200:
        score += 25
    else:
        score -= 25

    if sma20 > sma50:
        score += 15
    else:
        score -= 15

    if rsi > 70:
        score -= 5
    elif rsi > 55:
        score += 10
    elif rsi < 30:
        score += 5
    elif rsi < 45:
        score -= 10

    if macd["histogram"] > 0:
        score += 10
    else:
        score -= 10

    if current_volume > average_volume:
        score += 5
    else:
        score -= 5

    if score >= 70:
        bias = "Strong Bullish"
    elif score >= 35:
        bias = "Bullish"
    elif score <= -70:
        bias = "Strong Bearish"
    elif score <= -35:
        bias = "Bearish"
    else:
        bias = "Neutral"

    return bias, score


def detect_market_regime(market):

    price = market["price"]
    sma20 = market["sma20"]
    sma50 = market["sma50"]
    sma200 = market["sma200"]
    rsi = market["rsi"]
    macd = market["macd"]

    if price > sma20 and sma20 > sma50 and sma50 > sma200:
        return "Bullish Trend"

    if price < sma20 and sma20 < sma50 and sma50 < sma200:
        return "Bearish Trend"

    if rsi > 70:
        return "Overbought / Pullback Risk"

    if rsi < 30:
        return "Oversold / Bounce Risk"

    if abs(macd["histogram"]) < 0.25:
        return "Momentum Cooling / Range Risk"

    return "Mixed / Neutral"


def calculate_confidence(score):

    confidence = abs(score)

    if confidence > 100:
        confidence = 100

    return confidence


def grade_trade(score, market):

    rsi = market["rsi"]
    macd = market["macd"]
    current_volume = market["current_volume"]
    average_volume = market["average_volume"]

    grade_score = abs(score)

    if rsi > 70 or rsi < 30:
        grade_score -= 10

    if macd["histogram"] < 0:
        grade_score -= 5

    if current_volume < average_volume:
        grade_score -= 5

    if grade_score >= 90:
        return "A+"

    if grade_score >= 80:
        return "A"

    if grade_score >= 70:
        return "A-"

    if grade_score >= 60:
        return "B"

    if grade_score >= 50:
        return "C"

    return "No Trade"


def calculate_risk_level(market):

    rsi = market["rsi"]
    current_volume = market["current_volume"]
    average_volume = market["average_volume"]
    macd = market["macd"]

    risk_points = 0

    if rsi > 70 or rsi < 30:
        risk_points += 1

    if current_volume < average_volume:
        risk_points += 1

    if macd["histogram"] < 0:
        risk_points += 1

    if risk_points >= 3:
        return "High"

    if risk_points == 2:
        return "Medium"

    return "Low"