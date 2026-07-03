def determine_bias(market):

    price = market["price"]
    sma20 = market["sma20"]
    sma50 = market["sma50"]

    if price > sma20 and sma20 > sma50:
        return "Strong Bullish"

    elif price > sma20:
        return "Bullish"

    elif price < sma20 and sma20 < sma50:
        return "Strong Bearish"

    elif price < sma20:
        return "Bearish"

    else:
        return "Neutral"