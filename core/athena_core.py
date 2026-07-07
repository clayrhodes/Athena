"""
Athena Core V6

Central orchestrator for Athena.
Now passes completed current market setup into the
Pattern Recognition / Historical Similarity Engine.
"""

from intelligence.market_intelligence import MarketIntelligence
from intelligence.macro_intelligence import MacroIntelligence
from intelligence.sentiment_engine import SentimentEngine

from memory.memory_engine import save_analysis
from memory.pattern_engine import (
    analyze_patterns,
    format_pattern_report,
)
from memory.history import (
    build_history_summary,
    format_history_summary,
)


class AthenaCore:

    def __init__(self):

        self.market_intelligence = MarketIntelligence()
        self.macro = MacroIntelligence()
        self.sentiment = SentimentEngine()

        self.market_report = {}
        self.macro_report = {}
        self.sentiment_report = {}

        self.pattern_results = {}
        self.history_summary = {}

    def before_report(self):

        self.market_report = self.market_intelligence.analyze()
        self.macro_report = self.macro.analyze()
        self.sentiment_report = self.sentiment.analyze()

        self.pattern_results = analyze_patterns()
        self.history_summary = build_history_summary()

    def enrich_market(self, market):
        """
        Injects live intelligence into the market dictionary.
        """

        market["market_intelligence"] = self.market_report

        market_data = self.market_report.get("market_data", {})
        auction_flow = self.market_report.get("auction_flow", {})

        for key, value in market_data.items():
            if key not in market:
                market[key] = value

        market["auction_flow"] = auction_flow

        return market

    def build_current_record(
        self,
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
        """
        Builds today's completed setup so the Pattern Engine
        can compare it against saved historical setups.
        """

        return {
            "market_environment": {
                "bias": market.get("bias", "Unknown"),
                "trend": market.get("trend", "Unknown"),
                "condition": market.get("condition", "Unknown"),
            },
            "forecast": forecast,
            "probability": probability,
            "conviction": conviction,
            "risk": risk,
            "scores": scores,
            "decision": decision,
            "buy_decision": buy_decision,
            "entry": entry,
            "trade_plan": trade_plan,
            "should_buy": buy_decision.get("should_buy", False),
            "overall_score": scores.get("overall_score", 0),
            "regime": {
                "regime": market.get("regime", market.get("market_regime", "Unknown"))
            },
        }

    def after_report(
        self,
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

        current_record = self.build_current_record(
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

        self.pattern_results = analyze_patterns(current_record=current_record)

        save_analysis(
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

    def get_market_report(self):
        return self.market_report

    def get_macro_report(self):
        return self.macro_report

    def get_sentiment_report(self):
        return self.sentiment_report

    def get_pattern_results(self):
        return self.pattern_results

    def get_history_summary(self):
        return self.history_summary

    def print_system_summary(self):

        print()
        print(format_history_summary(self.history_summary))
        print()
        print(format_pattern_report(self.pattern_results))
        print()