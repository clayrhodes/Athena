"""
Athena Portfolio Engine

Monitors the entire trading account.
"""


def build_portfolio_report(portfolio=None):

    if portfolio is None:
        portfolio = {}

    account_value = portfolio.get("account_value", 1000)
    cash = portfolio.get("cash", account_value)
    buying_power = portfolio.get("buying_power", cash)
    open_positions = portfolio.get("open_positions", 0)
    daily_pl = portfolio.get("daily_pl", 0)
    total_pl = portfolio.get("total_pl", 0)
    risk_used = portfolio.get("risk_used_percent", 0)

    if open_positions == 0:
        status = "NO OPEN POSITIONS"
    elif risk_used >= 80:
        status = "HEAVILY EXPOSED"
    elif risk_used >= 50:
        status = "MODERATE EXPOSURE"
    else:
        status = "LIGHT EXPOSURE"

    summary = (
        f"Portfolio Status: {status}. "
        f"Account Value: ${account_value}. "
        f"Buying Power: ${buying_power}. "
        f"Open Positions: {open_positions}."
    )

    return {
        "status": status,
        "account_value": account_value,
        "cash": cash,
        "buying_power": buying_power,
        "open_positions": open_positions,
        "daily_pl": daily_pl,
        "total_pl": total_pl,
        "risk_used_percent": risk_used,
        "summary": summary,
    }