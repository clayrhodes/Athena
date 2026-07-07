"""
Athena Memory Engine V3

Creates and saves a memory record for every Athena Mission Brief.
"""

from datetime import datetime

from memory.trade_database import save_memory_record


def build_memory_record(
    market,
    scores,
    decision,
    buy_decision,
    entry,
    trade_plan,
    forecast,
    probability,
    conviction,
    risk,
):
    now = datetime.now()

    record = {
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),

        "ticker": market.get("ticker", "SPY"),
        "current_price": market.get(
            "current_price",
            market.get("price", "Unknown")
        ),

        "decision": decision,
        "should_buy": buy_decision.get("should_buy", False),
        "buy_reason": buy_decision.get("reason", ""),

        "overall_score": scores.get("overall_score"),
        "trade_grade": scores.get("trade_grade"),
        "confidence": scores.get("confidence"),

        "trend_score": scores.get("trend", {}).get("score"),
        "market_structure_score": scores.get("market_structure", {}).get("score"),
        "weekly_score": scores.get("multi_timeframe", {}).get("weekly_score"),
        "daily_score": scores.get("multi_timeframe", {}).get("daily_score"),
        "one_hour_score": scores.get("multi_timeframe", {}).get("one_hour_score"),
        "vwap_score": scores.get("vwap", {}).get("score"),
        "price_action_score": scores.get("price_action", {}).get("score"),
        "momentum_score": scores.get("momentum", {}).get("score"),
        "volume_score": scores.get("volume", {}).get("score"),

        "forecast": forecast,
        "probability": probability,
        "conviction": conviction,
        "risk": risk,

        "entry": entry,
        "trade_plan": trade_plan,

        "market_intelligence": market.get("market_intelligence", {}),

        "outcome": None,
    }

    return record


def save_analysis(
    market,
    scores,
    decision,
    buy_decision,
    entry,
    trade_plan,
    forecast,
    probability,
    conviction,
    risk,
):
    record = build_memory_record(
        market,
        scores,
        decision,
        buy_decision,
        entry,
        trade_plan,
        forecast,
        probability,
        conviction,
        risk,
    )

    return save_memory_record(record)