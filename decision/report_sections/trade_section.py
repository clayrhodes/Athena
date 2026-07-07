def build_trade_section(buy_decision, entry, trade_plan):

    reason = buy_decision.get("reason", "No reason given")

    # Clean up accidental double periods
    while ".." in reason:
        reason = reason.replace("..", ".")

    return f"""
BUY DECISION:
Should Buy: {buy_decision.get("should_buy", False)}
Reason: {reason}

ENTRY PLAN:
Entry Price: {entry.get("entry_price", "N/A")}
Entry Type: {entry.get("entry_type", "N/A")}
Aggressive Entry: {entry.get("aggressive_entry", "N/A")}
Conservative Entry: {entry.get("conservative_entry", "N/A")}
Stop Reference: {entry.get("stop_reference", "N/A")}
Expected Hold: {entry.get("expected_hold", "N/A")}
Entry Reason: {entry.get("reason", "No entry reason given")}

TRADE PLAN:
Stop Loss: {trade_plan.get("stop_loss", "N/A")}
Target 1: {trade_plan.get("target_1", "N/A")}
Target 2: {trade_plan.get("target_2", "N/A")}
Risk / Reward: {trade_plan.get("risk_reward", "N/A")}
Plan: {trade_plan.get("plan", "No trade plan available")}
"""