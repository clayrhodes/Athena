def build_risk_section(risk):
    """
    Athena Risk Manager Report Section
    """

    return f"""
RISK MANAGER:
Account Size: ${risk.get("account_size", "N/A")}
Max Risk Percent: {risk.get("max_risk_percent", "N/A")}%
Max Dollar Risk: ${risk.get("max_dollar_risk", "N/A")}
Risk Per Share: ${risk.get("risk_per_share", "N/A")}
Reward Per Share: ${risk.get("reward_per_share", "N/A")}
Shares Allowed: {risk.get("shares_allowed", "N/A")}
Win Probability: {risk.get("win_probability", "N/A")}%
Expected Value: ${risk.get("expected_value", "N/A")}
Risk Rating: {risk.get("risk_rating", "N/A")}
Risk Recommendation: {risk.get("recommendation", "N/A")}
"""