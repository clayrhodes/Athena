from strategy.bias_engine import detect_market_regime
from strategy.bias_engine import calculate_confidence
from strategy.bias_engine import grade_trade
from strategy.bias_engine import calculate_risk_level


def build_report(market, bias, score):

    regime = detect_market_regime(market)
    confidence = calculate_confidence(score)
    trade_grade = grade_trade(score, market)
    risk_level = calculate_risk_level(market)

    print("==============================")
    print("ATHENA MISSION BRIEF")
    print("==============================")
    print()
    print("MARKET REGIME")
    print("------------------------------")
    print(regime)
    print()
    print("ATHENA DECISION")
    print("------------------------------")
    print(f"Bias: {bias}")
    print(f"Score: {score} / 100")
    print(f"Confidence: {confidence}%")
    print(f"Trade Grade: {trade_grade}")
    print(f"Risk Level: {risk_level}")
    print()
    print("TRADE GUIDANCE")
    print("------------------------------")

    if trade_grade in ["A+", "A", "A-"]:
        print("Setup Quality: Strong")
        print("Plan: Look for a clean entry confirmation.")
        print("Avoid: Chasing extended candles.")
    elif trade_grade == "B":
        print("Setup Quality: Decent but not perfect")
        print("Plan: Wait for a better pullback, retest, or confirmation.")
    else:
        print("Setup Quality: Not good enough")
        print("Plan: No trade unless conditions improve.")