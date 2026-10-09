
from pathlib import Path
import pandas as pd

INPUT = Path("data/final/valuation_scenarios.csv")
OUTPUT = Path("data/final/profitability_scenarios.csv")

valuation_df = pd.read_csv(INPUT)

revenue_scenarios = (
    valuation_df[["scenario", "year", "revenue_usd_bn"]]
    .drop_duplicates()
)

operating_margins = [-0.20, -0.10, 0.00, 0.10, 0.20]

rows = []

for _, scenario in revenue_scenarios.iterrows():
    revenue = float(scenario["revenue_usd_bn"])

    for margin in operating_margins:
        operating_profit = revenue * margin

        rows.append({
            "scenario": scenario["scenario"],
            "year": int(scenario["year"]),
            "revenue_usd_bn": revenue,
            "operating_margin_pct": margin * 100,
            "operating_profit_usd_bn": round(operating_profit, 2),
            "profitability_status": (
                "Profit" if operating_profit > 0
                else "Loss" if operating_profit < 0
                else "Break-even"
            ),
            "assumption_type": "MODELED"
        })

df = pd.DataFrame(rows)

assert len(df) == 20
assert not df.duplicated(
    ["scenario", "year", "operating_margin_pct"]
).any()

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT, index=False)

print("PROFITABILITY MODEL COMPLETE")
print("Rows:", len(df))
print("\nOperating profit / loss (USD billions):")

pivot = df.pivot(
    index="scenario",
    columns="operating_margin_pct",
    values="operating_profit_usd_bn"
)

print(pivot.to_string())
print(f"\nSaved: {OUTPUT}")
