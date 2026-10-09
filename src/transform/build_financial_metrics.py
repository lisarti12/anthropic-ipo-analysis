
from pathlib import Path
import pandas as pd

INPUT = Path("data/processed/financial_events_validated.csv")
OUTPUT = Path("data/final/financial_metrics.csv")

df = pd.read_csv(INPUT, parse_dates=["metric_date"])

def get_value(metric, date):
    rows = df[
        (df["metric_name"] == metric)
        & (df["metric_date"] == pd.Timestamp(date))
    ]
    if len(rows) != 1:
        raise ValueError(f"Expected one observation: {metric}, {date}")
    return float(rows.iloc[0]["value"])

revenue_2024 = get_value("annual_revenue", "2024-12-31")
revenue_2025 = get_value("annual_revenue", "2025-12-31")
operating_loss_2024 = get_value("operating_loss", "2024-12-31")
operating_loss_2025 = get_value("operating_loss", "2025-12-31")
compute_2025 = get_value("compute_infrastructure_spending", "2025-12-31")
opex_2025 = get_value("operating_expenses", "2025-12-31")

valuation_e = get_value("post_money_valuation", "2025-03-03")
valuation_f = get_value("post_money_valuation", "2025-09-02")
valuation_g = get_value("post_money_valuation", "2026-02-12")
valuation_h = get_value("post_money_valuation", "2026-05-28")

metrics = [
    ("revenue_growth_2025_pct",
     (revenue_2025 / revenue_2024 - 1) * 100, "pct"),

    ("operating_loss_to_revenue_2024_pct",
     operating_loss_2024 / revenue_2024 * 100, "pct"),

    ("operating_loss_to_revenue_2025_pct",
     operating_loss_2025 / revenue_2025 * 100, "pct"),

    ("compute_to_revenue_2025_pct",
     compute_2025 / revenue_2025 * 100, "pct"),

    ("operating_expenses_to_revenue_2025_pct",
     opex_2025 / revenue_2025 * 100, "pct"),

    ("series_e_to_f_valuation_growth_pct",
     (valuation_f / valuation_e - 1) * 100, "pct"),

    ("series_f_to_g_valuation_growth_pct",
     (valuation_g / valuation_f - 1) * 100, "pct"),

    ("series_g_to_h_valuation_growth_pct",
     (valuation_h / valuation_g - 1) * 100, "pct"),

    ("series_e_to_h_valuation_growth_pct",
     (valuation_h / valuation_e - 1) * 100, "pct"),

    ("series_h_to_fy2025_revenue_multiple",
     valuation_h / revenue_2025, "x"),
]

result = pd.DataFrame(
    metrics,
    columns=["metric_name", "value", "unit"]
)

result["value"] = result["value"].round(2)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT, index=False)

print(result.to_string(index=False))
print(f"\nSaved: {OUTPUT}")
