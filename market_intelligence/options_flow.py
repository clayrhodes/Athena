"""
Athena Options Flow Engine V2

Purpose:
- Safely analyze options-flow style data when available.
- Keep Athena stable when live options flow is not connected.
- Return a clean score, bias, summary, signals, and warnings.

Future live inputs:
- Call premium
- Put premium
- Sweep orders
- Large block trades
- Ask-side buying
- Bid-side selling
- Expiration date
- Strike price
- Open interest
- Volume
"""


class OptionsFlowEngine:

    def analyze(self, options_data=None):

        if not options_data:
            return {
                "connected": False,
                "status": "OFFLINE",
                "bias": "NEUTRAL",
                "bullish_flow": 0,
                "bearish_flow": 0,
                "call_premium": 0,
                "put_premium": 0,
                "call_ratio": 0,
                "put_ratio": 0,
                "score": 50,
                "summary": "Live options flow not connected.",
                "bullish_signals": [],
                "bearish_signals": [],
                "warnings": [
                    "Options flow provider is not connected yet.",
                    "Athena is treating options flow as neutral."
                ],
            }

        call_premium = 0
        put_premium = 0
        bullish_trades = 0
        bearish_trades = 0
        sweep_count = 0
        block_count = 0

        for trade in options_data:
            option_type = str(trade.get("type", "")).lower()
            side = str(trade.get("side", "")).lower()
            trade_type = str(trade.get("trade_type", "")).lower()
            premium = float(trade.get("premium", 0))

            if trade_type == "sweep":
                sweep_count += 1

            if trade_type == "block":
                block_count += 1

            if option_type == "call":
                call_premium += premium

                if side in ["ask", "buy", "bought"]:
                    bullish_trades += 1

            elif option_type == "put":
                put_premium += premium

                if side in ["ask", "buy", "bought"]:
                    bearish_trades += 1

        total_premium = call_premium + put_premium

        if total_premium <= 0:
            return {
                "connected": True,
                "status": "WEAK",
                "bias": "NEUTRAL",
                "bullish_flow": 0,
                "bearish_flow": 0,
                "call_premium": call_premium,
                "put_premium": put_premium,
                "call_ratio": 0,
                "put_ratio": 0,
                "score": 50,
                "summary": "Options flow was too weak to matter.",
                "bullish_signals": [],
                "bearish_signals": [],
                "warnings": [
                    "No meaningful premium was detected.",
                    "Athena will not overweight this signal."
                ],
            }

        call_ratio = call_premium / total_premium
        put_ratio = put_premium / total_premium

        bullish_signals = []
        bearish_signals = []
        warnings = []

        if call_ratio >= 0.65:
            bias = "BULLISH"
            score = 75
            bullish_signals.append(
                f"Call premium controls {call_ratio:.0%} of total detected premium."
            )
        elif put_ratio >= 0.65:
            bias = "BEARISH"
            score = 25
            bearish_signals.append(
                f"Put premium controls {put_ratio:.0%} of total detected premium."
            )
        else:
            bias = "MIXED"
            score = 50
            warnings.append("Call and put premium are mixed.")

        if bullish_trades > bearish_trades:
            bullish_signals.append(
                f"More bullish ask-side call activity detected: {bullish_trades} bullish trades."
            )
            score += 5

        if bearish_trades > bullish_trades:
            bearish_signals.append(
                f"More bearish ask-side put activity detected: {bearish_trades} bearish trades."
            )
            score -= 5

        if sweep_count > 0:
            bullish_signals.append(
                f"{sweep_count} sweep order(s) detected. Sweeps can show urgency."
            )

        if block_count > 0:
            warnings.append(
                f"{block_count} block trade(s) detected. Blocks may be hedges, not pure direction."
            )

        score = max(0, min(100, score))

        if bias == "BULLISH":
            summary = "Options flow is leaning bullish."
        elif bias == "BEARISH":
            summary = "Options flow is leaning bearish."
        elif bias == "MIXED":
            summary = "Options flow is mixed."
        else:
            summary = "Options flow is neutral."

        return {
            "connected": True,
            "status": "ACTIVE",
            "bias": bias,
            "bullish_flow": bullish_trades,
            "bearish_flow": bearish_trades,
            "call_premium": call_premium,
            "put_premium": put_premium,
            "call_ratio": call_ratio,
            "put_ratio": put_ratio,
            "score": score,
            "summary": summary,
            "bullish_signals": bullish_signals,
            "bearish_signals": bearish_signals,
            "warnings": warnings,
        }