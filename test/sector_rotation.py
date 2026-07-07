from market_intelligence.sector_rotation import SectorRotationEngine


engine = SectorRotationEngine()
result = engine.analyze()

print("\n================ ATHENA SECTOR ROTATION TEST ================\n")
print("Connected:", result["connected"])
print("Provider:", result["provider"])
print("Leading Sector:", result["leading_sector"])
print("Lagging Sector:", result["lagging_sector"])
print("Score:", result["score"])
print("Market Tone:", result.get("market_tone"))
print("Summary:", result.get("summary"))

print("\nErrors:")
for error in result.get("errors", []):
    print("-", error)

print("\nSector Performance:")
for ticker, data in result.get("sector_performance", {}).items():
    print(f"{ticker} | {data['sector']} | {data['performance']}%")