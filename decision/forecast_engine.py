from decision.forecast_confidence import calculate_forecast_confidence
from decision.forecast_scenarios import build_forecast_scenarios
from decision.macro_engine import analyze_macro_environment


def build_summary(forecast):
    regime = forecast.get("market_regime", "Unknown")
    direction = forecast.get("direction", "Unknown")

    reasons = []

    if forecast.get("weekly_bull"):
        reasons.append("weekly trend is bullish")
    if forecast.get("daily_bull"):
        reasons.append("daily trend is bullish")
    if forecast.get("above20") and forecast.get("above50") and forecast.get("above200"):
        reasons.append("price is above the 20, 50, and 200 SMA")
    if forecast.get("bullish_stack"):
        reasons.append("moving averages are stacked bullish")
    if forecast.get("bullish_momentum"):
        reasons.append("momentum confirms the move")
    if forecast.get("strong_volume"):
        reasons.append("volume confirms participation")
    else:
        reasons.append("volume is not confirming yet")

    if not reasons:
        return f"{regime}. Direction: {direction}."

    return f"{regime}. Direction: {direction}. Key reasons: " + "; ".join(reasons) + "."


def detect_market_regime(market):
    price = market.get("price", 0)

    sma20 = market.get("sma20", 0)
    sma50 = market.get("sma50", 0)
    sma200 = market.get("sma200", 0)

    rsi = market.get("rsi", 50)

    macd_data = market.get("macd", {})
    macd = macd_data.get("macd", 0)
    signal = macd_data.get("signal", 0)

    volume = market.get("volume", 0)
    average_volume = market.get("average_volume", volume)

    weekly = market.get("weekly", {})
    daily = market.get("daily", {})
    hour1 = market.get("hour1", {})

    weekly_bull = weekly.get("trend", "Bullish") == "Bullish"
    daily_bull = daily.get("trend", "Bullish") == "Bullish"
    hour_bull = hour1.get("trend", "Bullish") == "Bullish"

    above20 = price > sma20
    above50 = price > sma50
    above200 = price > sma200

    bullish_stack = sma20 > sma50 > sma200
    bearish_stack = sma20 < sma50 < sma200

    bullish_momentum = rsi >= 55 and macd > signal
    bearish_momentum = rsi <= 45 and macd < signal

    strong_volume = volume >= average_volume

    macro = analyze_macro_environment(market)

    if (
        weekly_bull
        and daily_bull
        and above20
        and above50
        and above200
        and bullish_stack
        and bullish_momentum
        and strong_volume
    ):
        regime = "Strong Bull Trend"
        direction = "Bullish Continuation"

    elif above20 and above50 and bullish_stack:
        regime = "Bull Trend"
        direction = "Bullish"

    elif (
        not above20
        and not above50
        and not above200
        and bearish_stack
        and bearish_momentum
        and strong_volume
    ):
        regime = "Strong Bear Trend"
        direction = "Bearish Continuation"

    elif not above20 and not above50 and bearish_stack:
        regime = "Bear Trend"
        direction = "Bearish"

    elif rsi >= 70:
        regime = "Overextended Bull"
        direction = "Bullish but pullback likely"

    elif rsi <= 30:
        regime = "Oversold Bear"
        direction = "Bearish but bounce likely"

    else:
        regime = "Range / Neutral"
        direction = "No Forecast Edge"

    forecast = {
        "market_regime": regime,
        "direction": direction,
        "above20": above20,
        "above50": above50,
        "above200": above200,
        "bullish_stack": bullish_stack,
        "bearish_stack": bearish_stack,
        "bullish_momentum": bullish_momentum,
        "bearish_momentum": bearish_momentum,
        "strong_volume": strong_volume,
        "weekly_bull": weekly_bull,
        "daily_bull": daily_bull,
        "hour_bull": hour_bull,
        "macro": macro,
    }

    forecast["confidence"] = calculate_forecast_confidence(forecast)
    forecast["scenarios"] = build_forecast_scenarios(forecast)
    forecast["summary"] = build_summary(forecast)

    return forecast


def build_forecast(market):
    return detect_market_regime(market)