def find_support_resistance(market):

    price = market["price"]
    sma20 = market["sma20"]
    sma50 = market["sma50"]
    sma200 = market["sma200"]
    vwap = market["vwap"]["vwap"]

    support_levels = []
    resistance_levels = []

    levels = [
        ("VWAP", vwap),
        ("20 SMA", sma20),
        ("50 SMA", sma50),
        ("200 SMA", sma200)
    ]

    for name, level in levels:
        if level < price:
            support_levels.append({
                "name": name,
                "level": round(level, 2),
                "distance": round(price - level, 2)
            })
        elif level > price:
            resistance_levels.append({
                "name": name,
                "level": round(level, 2),
                "distance": round(level - price, 2)
            })

    support_levels = sorted(support_levels, key=lambda x: x["distance"])
    resistance_levels = sorted(resistance_levels, key=lambda x: x["distance"])

    nearest_support = support_levels[0] if support_levels else None
    nearest_resistance = resistance_levels[0] if resistance_levels else None

    return {
        "nearest_support": nearest_support,
        "nearest_resistance": nearest_resistance,
        "support_levels": support_levels,
        "resistance_levels": resistance_levels
    }