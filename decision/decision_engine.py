def make_decision(scores):

    overall = scores["overall_score"]

    if overall >= 90:
        return {
            "bias": "Very Strong Bullish",
            "trade_grade": "A+",
            "confidence": overall,
            "risk": "Low"
        }

    elif overall >= 80:
        return {
            "bias": "Strong Bullish",
            "trade_grade": "A",
            "confidence": overall,
            "risk": "Low"
        }

    elif overall >= 70:
        return {
            "bias": "Bullish",
            "trade_grade": "A-",
            "confidence": overall,
            "risk": "Medium"
        }

    elif overall >= 60:
        return {
            "bias": "Neutral Bullish",
            "trade_grade": "B",
            "confidence": overall,
            "risk": "Medium"
        }

    elif overall >= 45:
        return {
            "bias": "Neutral",
            "trade_grade": "C",
            "confidence": overall,
            "risk": "Medium"
        }

    elif overall >= 30:
        return {
            "bias": "Bearish",
            "trade_grade": "B",
            "confidence": 100 - overall,
            "risk": "Medium"
        }

    else:
        return {
            "bias": "Strong Bearish",
            "trade_grade": "A",
            "confidence": 100 - overall,
            "risk": "Low"
        }