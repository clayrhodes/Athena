from providers.economic_provider import EconomicProvider


provider = EconomicProvider()

print("\n================ ATHENA FRED TEST ================\n")

print("Status:")
print(provider.status())

print("\nMacro Data:")
macro = provider.get_macro_data()

print("Connected:", macro["connected"])
print("Provider:", macro["provider"])

for name, item in macro["data"].items():
    if item:
        print(f"{name}: {item['value']} as of {item['date']}")
    else:
        print(f"{name}: None")