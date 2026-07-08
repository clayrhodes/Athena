"""
Athena Report Sections

Builds every report section before
the report is assembled.
"""

from decision.report_sections.executive_summary import build_executive_summary
from decision.report_sections.intelligence_section import build_intelligence_section
from decision.report_sections.decision_matrix_section import build_decision_matrix_section
from decision.report_sections.conviction_section import build_conviction_section
from decision.report_sections.risk_section import build_risk_section
from decision.report_sections.execution_section import build_execution_section
from decision.report_sections.position_section import build_position_section
from decision.report_sections.trade_management_section import build_trade_management_section
from decision.report_sections.checklist_section import build_checklist_section
from decision.report_sections.probability_section import build_probability_section
from decision.report_sections.forecast_section import build_forecast_section
from decision.report_sections.trend_section import build_trend_section
from decision.report_sections.trade_section import build_trade_section
from decision.report_sections.market_section import build_market_section
from decision.report_sections.market_regime_section import build_market_regime_section
from decision.report_sections.institutional_section import build_institutional_section
from decision.report_sections.institutional_thesis_section import (
    build_institutional_thesis_section,
)
from decision.report_sections.narrative_section import (
    build_narrative_section,
)
from decision.report_sections.historical_similarity_section import (
    build_historical_similarity_section,
)
from decision.report_sections.smart_money_section import (
    build_smart_money_section,
)
from decision.report_sections.liquidity_section import (
    build_liquidity_section,
)
from decision.report_sections.market_breadth_section import (
    build_market_breadth_section,
)
from decision.report_sections.options_flow_section import (
    build_options_flow_section,
)

from intelligence.market_intelligence import (
    format_market_intelligence_section,
)

from news.news_engine import build_news_section
from news.economic_calendar import build_economic_calendar_section


def build_sections(
    intelligence,
    decision_matrix,
    conviction,
    risk,
    execution,
    position,
    trade_management,
    probability,
    similarity,
    smart_money,
    liquidity,
    market_breadth,
    options_flow,
    entry,
    trade_plan,
    buy_decision,
    market_report,
    environment,
    forecast,
    trend,
    market_regime,
    institutional,
    thesis,
    narrative,
    checklist,
    price_action,
    support_text,
    resistance_text,
    vwap,
    mtf,
    decision,
    scores,
):

    executive_summary = build_executive_summary(
        intelligence,
        decision_matrix,
        conviction,
        risk,
        probability,
        entry,
        trade_plan,
        buy_decision,
    )

    return {
        "executive_summary": executive_summary,
        "market_intelligence": format_market_intelligence_section(
            market_report
        ),
        "intelligence": build_intelligence_section(
            intelligence
        ),
        "narrative": build_narrative_section(
            narrative
        ),
        "historical_similarity": build_historical_similarity_section(
            similarity
        ),
        "smart_money": build_smart_money_section(
            smart_money
        ),
        "liquidity": build_liquidity_section(
            liquidity
        ),
        "market_breadth": build_market_breadth_section(
            market_breadth
        ),
        "options_flow": build_options_flow_section(
            options_flow
        ),
        "news": build_news_section(),
        "economic_calendar": build_economic_calendar_section(),
        "decision_matrix": build_decision_matrix_section(
            decision_matrix
        ),
        "conviction": build_conviction_section(
            conviction
        ),
        "risk": build_risk_section(
            risk
        ),
        "execution": build_execution_section(
            execution
        ),
        "position": build_position_section(
            position
        ),
        "trade_management": build_trade_management_section(
            trade_management
        ),
        "checklist": build_checklist_section(
            checklist
        ),
        "probability": build_probability_section(
            probability
        ),
        "market_regime": build_market_regime_section(
            market_regime
        ),
        "institutional": build_institutional_section(
            institutional
        ),
        "institutional_thesis": build_institutional_thesis_section(
            thesis
        ),
        "forecast": build_forecast_section(
            environment,
            forecast,
        ),
        "trend": build_trend_section(
            trend
        ),
        "trade": build_trade_section(
            buy_decision,
            entry,
            trade_plan,
        ),
        "market": build_market_section(
            price_action,
            support_text,
            resistance_text,
            vwap,
            mtf,
            decision,
            scores,
            decision_matrix,
        ),
    }