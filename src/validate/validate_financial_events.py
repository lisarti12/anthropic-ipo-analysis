
from pathlib import Path
import pandas as pd

RAW = Path("data/raw/financial_events.csv")
OUTPUT = Path("data/processed/financial_events_validated.csv")

df = pd.read_csv(RAW)

required = [
    "metric_date", "metric_name", "value", "unit",
    "metric_type", "source_id", "value_qualifier", "notes"
]

assert all(col in df.columns for col in required), "Missing columns"
assert not df[required[:-1]].isna().any().any(), "Missing required values"

df["metric_date"] = pd.to_datetime(df["metric_date"], errors="raise")
df["value"] = pd.to_numeric(df["value"], errors="raise")

assert (df["value"] >= 0).all(), "Negative values detected"
assert df["unit"].eq("USD_bn").all(), "Unexpected currency or unit"
assert df["metric_type"].isin(
    ["ACTUAL", "RUN_RATE", "VALUATION", "FORECAST", "MODELED"]
).all(), "Invalid metric type"
assert df["value_qualifier"].isin(
    ["EXACT", "APPROXIMATE", "LOWER_BOUND", "UPPER_BOUND"]
).all(), "Invalid qualifier"

assert not df.duplicated(
    ["metric_date", "metric_name", "source_id"]
).any(), "Duplicate observations"

assert df.loc[
    df["metric_name"].eq("revenue_run_rate"),
    "metric_type"
].eq("RUN_RATE").all(), "Run-rate classification error"

assert df.loc[
    df["metric_name"].eq("post_money_valuation"),
    "metric_type"
].eq("VALUATION").all(), "Valuation classification error"

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.sort_values(["metric_date", "metric_name"]).to_csv(OUTPUT, index=False)

print("VALIDATION PASSED")
print("Rows:", len(df))
print("Sources:", df["source_id"].nunique())
print("Duplicate observations: 0")
print("Missing required values: 0")
print("\nMetric types:")
print(df["metric_type"].value_counts().to_string())
