"""
Athena Market Intelligence Engine V8

Now uses Athena DataHub as the central provider data source.
"""

from core.data_hub import AthenaDataHub

from intelligence.sentiment_engine import SentimentEngine
from intelligence.macro_score import MacroScoreEngine

from market_intelligence.fear_greed import FearGreedEngine
from market_intelligence.market_breadth import MarketBreadthEngine
from market_intelligence.options_flow import OptionsFlowEngine
from market_intelligence.institutional_flow import InstitutionalFlowEngine
from market_intelligence.sector_rotation import SectorRotationEngine
from market_intelligence.auction_flow import AuctionFlowEngine

from providers.economic_provider import EconomicProvider


class MarketIntelligence:

    def __init__(self):

        self.data_hub = AthenaDataHub()
        self.economic_provider = EconomicProvider()

        self.sentiment = SentimentEngine()
        self.macro_score = MacroScoreEngine()

        self.fear_greed = FearGreedEngine()
        self.breadth = MarketBreadthEngine()
        self.options_flow = OptionsFlowEngine()
        self.institutional_flow = InstitutionalFlowEngine()
        self.sector_rotation = SectorRotationEngine()
        self.auction_flow = AuctionFlowEngine()

    def analyze(self):

        data = self.data_hub.collect()

        market_data = data.get("market", {})
        calendar = data.get("calendar", {})
        news = data.get("news", {})
        breadth_data = data.get("breadth", {})
        options_data = data.get("options_flow", {})

        fred_macro = self.economic_provider.get_macro_data()

        sentiment = self.sentiment.analyze()

        macro_score = self.macro_score.calculate(
            sentiment,
            market_data,
        )

        fear_greed = self.fear_greed.analyze()

        breadth = self.breadth.analyze(breadth_data)

        options_flow = self.options_flow.analyze(
            options_data.get("trades", [])
        )

        institutional_flow = self.institutional_flow.analyze()
        sector_rotation = self.sector_rotation.analyze()
        auction_flow = self.auction_flow.analyze(market_data)

        return {
            "market_data": market_data,
            "calendar": calendar,
            "news": news,
            "fred_macro": fred_macro,
            "sentiment": sentiment,
            "macro_score": macro_score,
            "fear_greed": fear_greed,
            "breadth": breadth,
            "options_flow": options_flow,
            "institutional_flow": institutional_flow,
            "sector_rotation": sector_rotation,
            "auction_flow": auction_flow,
            "data_hub": data,
        }


def format_market_intelligence_section(report):

    sentiment = report.get("sentiment", {})
    market_data = report.get("market_data", {})
    macro_score = report.get("macro_score", {})
    fred_macro = report.get("fred_macro", {})
    fear_greed = report.get("fear_greed", {})
    breadth = report.get("breadth", {})
    options_flow = report.get("options_flow", {})
    institutional_flow = report.get("institutional_flow", {})
    sector_rotation = report.get("sector_rotation", {})
    auction_flow = report.get("auction_flow", {})

    fred_data = fred_macro.get("data", {})

    lines = []

    lines.append("ATHENA MARKET INTELLIGENCE")
    lines.append("-" * 30)

    lines.append(f"Provider Connected: {market_data.get('connected', False)}")
    lines.append(f"FRED Connected: {fred_macro.get('connected', False)}")

    lines.append("")
    lines.append(f"VIX: {market_data.get('vix')}")
    lines.append(f"DXY: {market_data.get('dxy')}")
    lines.append(f"10Y Treasury Yield: {market_data.get('treasury_10y')}")
    lines.append(f"Fear & Greed: {fear_greed.get('value')}")

    lines.append("")
    lines.append("FRED MACRO DATA:")
    lines.append(_format_fred_line("Fed Funds Rate", fred_data.get("fed_funds_rate")))
    lines.append(_format_fred_line("CPI", fred_data.get("cpi")))
    lines.append(_format_fred_line("Unemployment Rate", fred_data.get("unemployment_rate")))
    lines.append(_format_fred_line("Nonfarm Payrolls", fred_data.get("nonfarm_payrolls")))
    lines.append(_format_fred_line("Consumer Sentiment", fred_data.get("consumer_sentiment")))
    lines.append(_format_fred_line("10Y-2Y Yield Curve", fred_data.get("yield_curve_10y_2y")))

    lines.append("")
    lines.append(f"Overall Sentiment: {sentiment.get('overall_sentiment')}")
    lines.append(f"Sentiment Score: {sentiment.get('score')} / 100")
    lines.append(f"Macro Score: {macro_score.get('score')} / 100")

    lines.append("")
    lines.append("Auction Flow:")
    lines.append(f"- Status: {auction_flow.get('status', 'UNKNOWN')}")
    lines.append(f"- Bias: {auction_flow.get('bias', 'UNKNOWN')}")
    lines.append(f"- Score: {auction_flow.get('score', 50)} / 100")
    lines.append(f"- Summary: {auction_flow.get('summary', 'No auction flow summary available.')}")

    _append_list(lines, "Auction Bullish Signals", auction_flow.get("bullish_signals", []))
    _append_list(lines, "Auction Bearish Signals", auction_flow.get("bearish_signals", []))
    _append_list(lines, "Auction Warnings", auction_flow.get("warnings", []))

    lines.append("")
    lines.append("Market Breadth:")
    lines.append(f"- Status: {breadth.get('status', 'UNKNOWN')}")
    lines.append(f"- Breadth: {breadth.get('breadth', 'Unknown')}")
    lines.append(f"- Score: {breadth.get('score', 50)} / 100")
    lines.append(f"- Summary: {breadth.get('summary', 'No breadth summary available.')}")

    _append_list(lines, "Breadth Bullish Signals", breadth.get("bullish_signals", []))
    _append_list(lines, "Breadth Bearish Signals", breadth.get("bearish_signals", []))
    _append_list(lines, "Breadth Warnings", breadth.get("warnings", []))

    lines.append("")
    lines.append("Options Flow:")
    lines.append(f"- Status: {options_flow.get('status', 'UNKNOWN')}")
    lines.append(f"- Bias: {options_flow.get('bias', 'NEUTRAL')}")
    lines.append(f"- Score: {options_flow.get('score', 50)} / 100")
    lines.append(f"- Summary: {options_flow.get('summary', 'No options flow summary available.')}")

    _append_list(lines, "Options Bullish Signals", options_flow.get("bullish_signals", []))
    _append_list(lines, "Options Bearish Signals", options_flow.get("bearish_signals", []))
    _append_list(lines, "Options Warnings", options_flow.get("warnings", []))

    lines.append("")
    lines.append("Institutional Flow:")
    lines.append(f"- Score: {institutional_flow.get('score')} / 100")
    lines.append(f"- Summary: {institutional_flow.get('summary')}")

    lines.append("")
    lines.append("Sector Rotation:")
    lines.append(f"- Leading Sector: {sector_rotation.get('leading_sector')}")
    lines.append(f"- Lagging Sector: {sector_rotation.get('lagging_sector')}")
    lines.append(f"- Score: {sector_rotation.get('score')} / 100")

    reasons = macro_score.get("reasons", [])

    lines.append("")
    lines.append("Macro Factors:")

    if reasons:
        for reason in reasons:
            lines.append(f"- {reason}")
    else:
        lines.append("- None")

    bullish = sentiment.get("bullish_factors", [])

    lines.append("")
    lines.append("Bullish Factors:")

    if bullish:
        for factor in bullish:
            lines.append(f"- {factor}")
    else:
        lines.append("- None")

    bearish = sentiment.get("bearish_factors", [])

    lines.append("")
    lines.append("Bearish Factors:")

    if bearish:
        for factor in bearish:
            lines.append(f"- {factor}")
    else:
        lines.append("- None")

    warnings = sentiment.get("warnings", [])

    lines.append("")
    lines.append("Warnings:")

    if warnings:
        for warning in warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- None")

    return "\n".join(lines)


def _append_list(lines, title, items):
    lines.append("")
    lines.append(f"{title}:")

    if items:
        for item in items:
            lines.append(f"- {item}")
    else:
        lines.append("- None")


def _format_fred_line(label, item):
    if not item:
        return f"- {label}: Unavailable"

    return f"- {label}: {item.get('value')} as of {item.get('date')}"