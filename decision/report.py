from core.athena_core import AthenaCore

from decision.scoring import calculate_scores
from decision.decision_engine import make_decision
from decision.buy_engine import should_buy_now
from decision.entry_engine import calculate_entry
from decision.trade_planner import build_trade_plan
from decision.forecast_engine import build_forecast
from decision.intelligence_engine import build_intelligence_report
from decision.probability_engine import build_probability_report
from decision.conviction_engine import build_conviction_engine
from decision.execution_checklist import build_execution_checklist
from decision.execution_engine import build_execution_report
from decision.trade_management_engine import build_trade_management_report
from decision.position_engine import build_position_report
from decision.risk_manager import build_risk_report
from decision.decision_matrix import evaluate_decision_matrix
from decision.institutional_engine import build_institutional_report
from decision.institutional_thesis_engine import build_institutional_thesis
from decision.narrative_engine import build_market_narrative
from decision.historical_similarity_engine import (
    build_historical_similarity_report,
)
from decision.market_breadth_engine import build_market_breadth_report
from decision.options_flow_engine import build_options_flow_report
from decision.section_builder import build_sections
from decision.report_builder import build_report

from intelligence.market_regime_engine import MarketRegimeEngine

from logs.logger import save_report


def get_level_text(level_data, default_name):
    if not level_data:
        return "None found"

    name = level_data.get("name", default_name)
    price = level_data.get("price", level_data.get("level", "N/A"))

    return f"{name} at {price}"


def generate_mission_brief(market):
    core = AthenaCore()
    core.before_report()

    market = core.enrich_market(market)

    market_report = core.get_market_report()
    market_data = market_report.get("market_data", {})

    for key, value in market_data.items():
        market.setdefault(key, value)

    scores = calculate_scores(market)

    decision = make_decision(scores)
    buy_decision = should_buy_now(scores, decision)

    entry = calculate_entry(market, buy_decision)
    trade_plan = build_trade_plan(market, entry, buy_decision)

    forecast = build_forecast(market)

    probability = build_probability_report(scores, forecast)
    probabilities = probability.get("probabilities", {})

    trend = scores.get("trend", {})
    mtf = scores.get("multi_timeframe", {})
    vwap = scores.get("vwap", {})
    sr = market.get("support_resistance", {})
    environment = scores.get("environment", {})
    price_action = scores.get("price_action", {})
    market_structure = scores.get("market_structure", {})
    momentum = scores.get("momentum", {})
    volume = scores.get("volume", {})
    auction_flow = market_report.get("auction_flow", {})

    market_regime = MarketRegimeEngine().analyze(
        trend_data=trend,
        market_structure=market_structure,
        mtf_data=mtf,
        vwap_data=vwap,
        momentum_data=momentum,
        volume_data=volume,
        price_action=price_action,
        macro_data=market_report,
        fear_greed_data=market_report,
        auction_flow=auction_flow,
    )

    institutional = build_institutional_report(
        trend=trend,
        market_structure=market_structure,
        multi_timeframe=mtf,
        vwap=vwap,
        momentum=momentum,
        volume=volume,
        auction_flow=auction_flow,
        market_regime=market_regime,
    )

    smart_money = scores.get("smart_money", {})
    liquidity = scores.get("liquidity", {})

    first_decision_matrix = evaluate_decision_matrix(scores)

    first_conviction = build_conviction_engine(
        scores,
        forecast,
        probability,
    )

    thesis = build_institutional_thesis(
        market_regime,
        institutional,
        forecast,
        probability,
        first_conviction,
        first_decision_matrix,
    )

    narrative = build_market_narrative(
        thesis,
        market_regime,
        institutional,
    )

    market_breadth = market_report.get("breadth", {})

    if not market_breadth:
        market_breadth = build_market_breadth_report(
            market,
            thesis,
            market_regime,
        )

    options_flow = market_report.get("options_flow", {})

    if not options_flow:
        options_flow = build_options_flow_report(market)

    similarity = build_historical_similarity_report(
        thesis,
        probability,
        first_decision_matrix,
    )

    scores["market_breadth"] = market_breadth
    scores["options_flow"] = options_flow
    scores["historical_similarity"] = {
        "score": similarity.get("estimated_win_rate", 0),
        "quality": similarity.get("quality", "UNKNOWN"),
        "matches_found": similarity.get("matches_found", 0),
    }

    decision_matrix = evaluate_decision_matrix(scores)

    conviction = build_conviction_engine(
        scores,
        forecast,
        probability,
    )

    checklist = build_execution_checklist(
        scores,
        forecast,
        probabilities,
        buy_decision,
    )

    risk = build_risk_report(
        trade_plan,
        probability,
        account_size=1000,
        max_risk_percent=1,
    )

    execution = build_execution_report(
        market_structure=market_structure,
        liquidity=liquidity,
        smart_money=smart_money,
        volume=volume,
        price_action=price_action,
    )

    raw_position = market.get("position", {})
    position = build_position_report(raw_position)

    trade_management = build_trade_management_report(
        active_trade=position,
        market_structure=market_structure,
        smart_money=smart_money,
        liquidity=liquidity,
        volume=volume,
        price_action=price_action,
        probability=probability,
    )

    intelligence = build_intelligence_report(
        scores,
        forecast,
        decision,
        buy_decision,
        entry,
        trade_plan,
    )

    support_text = get_level_text(
        sr.get("nearest_support"),
        "Support",
    )

    resistance_text = get_level_text(
        sr.get("nearest_resistance"),
        "Resistance",
    )

    sections = build_sections(
        intelligence=intelligence,
        decision_matrix=decision_matrix,
        conviction=conviction,
        risk=risk,
        execution=execution,
        position=position,
        trade_management=trade_management,
        probability=probability,
        similarity=similarity,
        smart_money=smart_money,
        liquidity=liquidity,
        market_breadth=market_breadth,
        options_flow=options_flow,
        entry=entry,
        trade_plan=trade_plan,
        buy_decision=buy_decision,
        market_report=market_report,
        environment=environment,
        forecast=forecast,
        trend=trend,
        market_regime=market_regime,
        institutional=institutional,
        thesis=thesis,
        narrative=narrative,
        checklist=checklist,
        price_action=price_action,
        support_text=support_text,
        resistance_text=resistance_text,
        vwap=vwap,
        mtf=mtf,
        decision=decision,
        scores=scores,
    )

    report = build_report(sections)

    print(report)
    save_report(report)

    core.after_report(
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

    return report