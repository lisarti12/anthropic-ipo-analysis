
CREATE OR REPLACE VIEW vw_financial_timeline AS
SELECT
    metric_date,
    EXTRACT(YEAR FROM metric_date)::INTEGER AS year,
    metric_name,
    value AS value_usd_bn,
    metric_type,
    value_qualifier,
    source_id,
    notes
FROM financial_events
ORDER BY metric_date;


CREATE OR REPLACE VIEW vw_valuation_sensitivity AS
SELECT
    scenario,
    year,
    revenue_usd_bn,
    revenue_multiple,
    implied_valuation_usd_bn,
    target_valuation_usd_bn,
    required_multiple_for_target,
    valuation_gap_usd_bn,
    ROUND(
        implied_valuation_usd_bn
        / NULLIF(target_valuation_usd_bn, 0) * 100,
        2
    ) AS target_achievement_pct,
    CASE
        WHEN implied_valuation_usd_bn >= target_valuation_usd_bn
            THEN 'At or Above Target'
        ELSE 'Below Target'
    END AS valuation_status,
    assumption_type
FROM valuation_scenarios;


CREATE OR REPLACE VIEW vw_profitability_sensitivity AS
SELECT
    scenario,
    year,
    revenue_usd_bn,
    operating_margin_pct,
    operating_profit_usd_bn,
    profitability_status,
    ROUND(
        operating_profit_usd_bn
        / NULLIF(revenue_usd_bn, 0) * 100,
        2
    ) AS calculated_margin_pct,
    assumption_type
FROM profitability_scenarios;
