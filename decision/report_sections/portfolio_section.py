"""
Athena Portfolio Report Section
"""


def build_portfolio_section(portfolio):

    report = []

    report.append("")
    report.append("=======================================================")
    report.append("ATHENA PORTFOLIO MANAGER")
    report.append("=======================================================")
    report.append("")

    report.append(f"Status: {portfolio.get('status', 'UNKNOWN')}")
    report.append(f"Account Value: ${portfolio.get('account_value', 0)}")
    report.append(f"Cash: ${portfolio.get('cash', 0)}")
    report.append(f"Buying Power: ${portfolio.get('buying_power', 0)}")
    report.append(f"Open Positions: {portfolio.get('open_positions', 0)}")
    report.append(f"Daily P/L: ${portfolio.get('daily_pl', 0)}")
    report.append(f"Total P/L: ${portfolio.get('total_pl', 0)}")
    report.append(f"Risk Used: {portfolio.get('risk_used_percent', 0)}%")

    report.append("")
    report.append("Summary:")
    report.append(portfolio.get("summary", ""))
    report.append("")
    report.append("=======================================================")

    return "\n".join(report)