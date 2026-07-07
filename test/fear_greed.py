from market_intelligence.fear_greed import FearGreedEngine


engine = FearGreedEngine()
result = engine.analyze()

print("\n================ ATHENA FEAR & GREED TEST ================\n")
print("Connected:", result["connected"])
print("Provider:", result["provider"])
print("Value:", result["value"])
print("Classification:", result["classification"])
print("Score:", result["score"])
print("Reason:", result["reason"])