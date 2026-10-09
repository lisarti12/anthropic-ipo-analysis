
CREATE TABLE IF NOT EXISTS financial_events (
    id BIGSERIAL PRIMARY KEY,
    metric_date DATE NOT NULL,
    metric_name VARCHAR(100) NOT NULL,
    value NUMERIC(18,4) NOT NULL,
    unit VARCHAR(20) NOT NULL,
    metric_type VARCHAR(30) NOT NULL,
    source_id VARCHAR(20) NOT NULL,
    value_qualifier VARCHAR(30) NOT NULL,
    notes TEXT,
    UNIQUE (metric_date, metric_name, source_id)
);

CREATE TABLE IF NOT EXISTS financial_metrics (
    metric_name VARCHAR(150) PRIMARY KEY,
    value NUMERIC(18,4) NOT NULL,
    unit VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS valuation_scenarios (
    scenario VARCHAR(30) NOT NULL,
    year INTEGER NOT NULL,
    revenue_usd_bn NUMERIC(18,4) NOT NULL,
    revenue_multiple NUMERIC(10,2) NOT NULL,
    implied_valuation_usd_bn NUMERIC(18,4) NOT NULL,
    target_valuation_usd_bn NUMERIC(18,4) NOT NULL,
    required_multiple_for_target NUMERIC(10,4) NOT NULL,
    valuation_gap_usd_bn NUMERIC(18,4) NOT NULL,
    assumption_type VARCHAR(30) NOT NULL,
    PRIMARY KEY (scenario, year, revenue_multiple)
);

CREATE TABLE IF NOT EXISTS profitability_scenarios (
    scenario VARCHAR(30) NOT NULL,
    year INTEGER NOT NULL,
    revenue_usd_bn NUMERIC(18,4) NOT NULL,
    operating_margin_pct NUMERIC(10,2) NOT NULL,
    operating_profit_usd_bn NUMERIC(18,4) NOT NULL,
    profitability_status VARCHAR(30) NOT NULL,
    assumption_type VARCHAR(30) NOT NULL,
    PRIMARY KEY (scenario, year, operating_margin_pct)
);
