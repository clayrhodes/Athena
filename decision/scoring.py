from analysis.trend import analyze_trend
from analysis.momentum import analyze_momentum
from analysis.volume import analyze_volume
from analysis.volatility import analyze_volatility
from analysis.market_structure import analyze_market_structure
from analysis.multi_timeframe import analyze_multi_timeframe
from analysis.market_environment import detect_market_environment
from analysis.price_action import analyze_price_action
from analysis.institutional_structure import analyze_institutional_structure
from analysis.market_structure_v2 import analyze_market_structure_v2
from analysis.order_block_engine import analyze_order_blocks

from decision.smart_money_engine import build_smart_money_report
from decision.liquidity_engine import build_liquidity_report


def get_trade_grade(score):
    if score >= 90:
        return "A+"
    if score >= 85:
        return "A"
    if score >= 80:
        return "B+"
    if score >= 75:
        return "B"
    if score >= 70:
        return "C"
    return "NO TRADE"


def get_confidence(score):
    if score >= 90:
        return "Very High"
    if score >= 85:
        return "High"
    if score >= 80:
        return "Medium-High"
    if score >= 75:
        return "Medium"
    if score >= 70:
        return "Low"
    return "Very Low"


def _merge_price_action(price_action, institutional_structure, structure_v2, order_blocks):
    merged = dict(price_action)

    keys_to_copy = [
        "broke_support",
        "reclaimed_support",
        "broke_resistance",
        "rejected_resistance",
        "long_lower_wick",
        "long_upper_wick",
        "near_support",
        "near_resistance",
        "above_vwap",
        "below_vwap",
    ]

    for key in keys_to_copy:
        merged[key] = institutional_structure.get(key, merged.get(key, False))

    merged["bos_bullish"] = structure_v2.get("bos_bullish", False)
    merged["bos_bearish"] = structure_v2.get("bos_bearish", False)
    merged["choch_bullish"] = structure_v2.get("choch_bullish", False)
    merged["choch_bearish"] = structure_v2.get("choch_bearish", False)

    merged["last_swing_high"] = structure_v2.get("last_swing_high")
    merged["last_swing_low"] = structure_v2.get("last_swing_low")

    merged["order_block_score"] = order_blocks.get("score", 50)
    merged["order_block_bias"] = order_blocks.get("bias", "neutral")
    merged["nearest_bullish_order_block"] = order_blocks.get("nearest_bullish_block")
    merged["nearest_bearish_order_block"] = order_blocks.get("nearest_bearish_block")

    merged["institutional_structure_score"] = institutional_structure.get("score", 50)
    merged["institutional_structure_bias"] = institutional_structure.get("bias", "neutral")
    merged["institutional_structure_signals"] = institutional_structure.get("signals", [])

    merged["market_structure_v2_score"] = structure_v2.get("score", 50)
    merged["market_structure_v2_bias"] = structure_v2.get("bias", "neutral")
    merged["market_structure_v2_signals"] = structure_v2.get("signals", [])

    return merged


def _merge_structure(structure, structure_v2, order_blocks):
    merged = dict(structure)

    merged["structure_v2_score"] = structure_v2.get("score", 50)
    merged["structure_v2_bias"] = structure_v2.get("bias", "neutral")
    merged["structure_v2_trend"] = structure_v2.get("trend", "neutral")

    merged["bos_bullish"] = structure_v2.get("bos_bullish", False)
    merged["bos_bearish"] = structure_v2.get("bos_bearish", False)
    merged["choch_bullish"] = structure_v2.get("choch_bullish", False)
    merged["choch_bearish"] = structure_v2.get("choch_bearish", False)

    merged["last_swing_high"] = structure_v2.get("last_swing_high")
    merged["last_swing_low"] = structure_v2.get("last_swing_low")
    merged["buy_side_liquidity"] = structure_v2.get("buy_side_liquidity")
    merged["sell_side_liquidity"] = structure_v2.get("sell_side_liquidity")

    merged["order_block_score"] = order_blocks.get("score", 50)
    merged["order_block_bias"] = order_blocks.get("bias", "neutral")
    merged["nearest_bullish_order_block"] = order_blocks.get("nearest_bullish_block")
    merged["nearest_bearish_order_block"] = order_blocks.get("nearest_bearish_block")

    return merged


def calculate_scores(market):
    trend = analyze_trend(market)
    momentum = analyze_momentum(market)
    volume = analyze_volume(market)
    volatility = analyze_volatility(market)

    structure_base = analyze_market_structure(market)
    structure_v2 = analyze_market_structure_v2(market)
    order_blocks = analyze_order_blocks(market)

    structure = _merge_structure(
        structure_base,
        structure_v2,
        order_blocks,
    )

    multi_timeframe = analyze_multi_timeframe()
    vwap = market["vwap"]

    price_action_base = analyze_price_action(market)
    institutional_structure = analyze_institutional_structure(market)

    price_action = _merge_price_action(
        price_action_base,
        institutional_structure,
        structure_v2,
        order_blocks,
    )

    auction_flow = market.get("auction_flow", {
        "connected": False,
        "status": "OFFLINE",
        "bias": "UNKNOWN",
        "score": 50,
        "summary": "Auction flow not available.",
        "bullish_signals": [],
        "bearish_signals": [],
        "warnings": ["Auction flow was not provided by Athena Core."],
    })

    liquidity = build_liquidity_report(
        price_action=price_action,
        market_structure=structure,
        volume=volume,
    )

    historical_similarity = market.get("historical_similarity", {
        "score": 50,
        "bias": "neutral",
        "matches": [],
        "summary": "Historical similarity not available yet.",
    })

    smart_money = build_smart_money_report(
        market_structure=structure,
        volume=volume,
        price_action=price_action,
        liquidity=liquidity,
    )

    scores_so_far = {
        "trend": trend,
        "momentum": momentum,
        "volume": volume,
        "volatility": volatility,
        "structure": structure,
        "structure_v2": structure_v2,
        "order_blocks": order_blocks,
        "vwap": vwap,
        "multi_timeframe": multi_timeframe,
        "price_action": price_action,
        "institutional_structure": institutional_structure,
        "auction_flow": auction_flow,
        "liquidity": liquidity,
        "historical_similarity": historical_similarity,
        "smart_money": smart_money,
    }

    environment = detect_market_environment(market, scores_so_far)

    overall_score = (
        trend["score"] * 0.13 +
        momentum["score"] * 0.09 +
        volume["score"] * 0.07 +
        volatility["score"] * 0.05 +
        structure["score"] * 0.09 +
        structure_v2["score"] * 0.06 +
        order_blocks["score"] * 0.05 +
        vwap["score"] * 0.07 +
        price_action["score"] * 0.08 +
        institutional_structure["score"] * 0.05 +
        smart_money["score"] * 0.10 +
        liquidity["score"] * 0.06 +
        historical_similarity["score"] * 0.04 +
        auction_flow["score"] * 0.04 +
        multi_timeframe["Weekly"]["score"] * 0.10 +
        multi_timeframe["Daily"]["score"] * 0.03 +
        multi_timeframe["1 Hour"]["score"] * 0.01
    )

    overall_score = round(overall_score)
    trade_grade = get_trade_grade(overall_score)
    confidence = get_confidence(overall_score)

    return {
        "trend": trend,
        "momentum": momentum,
        "volume": volume,
        "volatility": volatility,
        "structure": structure,
        "structure_v2": structure_v2,
        "order_blocks": order_blocks,
        "vwap": vwap,
        "price_action": price_action,
        "institutional_structure": institutional_structure,
        "auction_flow": auction_flow,
        "liquidity": liquidity,
        "historical_similarity": historical_similarity,
        "smart_money": smart_money,
        "multi_timeframe": multi_timeframe,
        "environment": environment,
        "overall_score": overall_score,
        "trade_grade": trade_grade,
        "confidence": confidence,
    }