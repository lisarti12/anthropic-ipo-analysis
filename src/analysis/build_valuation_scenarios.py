
from pathlib import Path
import pandas as pd

OUTPUT = Path("data/final/valuation_scenarios.csv")

target_valuation = 2000.0

scenarios = {
    "Bear": 100.0,
    "Base": 150.0,
    "Bull": 200.0,
    "Upside": 250.0
}

multiples = [5, 8, 10, 12, 15, 20]

rows = []

for scenario, revenue in scenarios.items():
    required_multiple = target_valuation / revenue

    for multiple in multiples:
        implied_valuation = revenue * multiple

        rows.append({
            "scenario": scenario,
            "year": 2028,
            "revenue_usd_bn": revenue,
            "revenue_multiple": multiple,
            "implied_valuation_usd_bn": implied_valuation,
            "target_valuation_usd_bn": target_valuation,
            "required_multiple_for_target": required_multiple,
            "valuation_gap_usd_bn": implied_valuation - target_valuation,
            "assumption_type": "MODELED"
        })

df = pd.DataFrame(rows)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT, index=False)

print("SCENARIO MODEL COMPLETE")
print("Rows:", len(df))
print("\nRequired multiples for $2T valuation:")
print(
    df.groupby("scenario", sort=False)
      .first()[["revenue_usd_bn", "required_multiple_for_target"]]
      .to_string()
)
print(f"\nSaved: {OUTPUT}")
