from data.market_data import get_market_data
from decision.report import generate_mission_brief


def main():
    print()
    print("Connecting to market...")
    print()

    market = get_market_data()

    generate_mission_brief(market)


if __name__ == "__main__":
    main()