
from pathlib import Path
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

load_dotenv()

url = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME")
)

engine = create_engine(url)

datasets = {
    "financial_events": "data/processed/financial_events_validated.csv",
    "financial_metrics": "data/final/financial_metrics.csv",
    "valuation_scenarios": "data/final/valuation_scenarios.csv",
    "profitability_scenarios": "data/final/profitability_scenarios.csv"
}

with engine.begin() as conn:
    for table, file_path in datasets.items():
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(path)

        df = pd.read_csv(path)

        conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY"))

        df.to_sql(
            table,
            con=conn,
            if_exists="append",
            index=False,
            method="multi"
        )

        count = conn.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        ).scalar_one()

        if count != len(df):
            raise ValueError(f"Row mismatch in {table}")

        print(f"{table}: {count} rows loaded")

print("\nALL DATASETS LOADED SUCCESSFULLY")
