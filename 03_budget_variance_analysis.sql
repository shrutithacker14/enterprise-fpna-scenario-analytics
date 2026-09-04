-- FY2026 budget variance and run-rate analysis
-- The cutoff and completed-month count are defined once in params so the model is easy to update.

WITH params AS (
    SELECT DATE '2026-07-31' AS ytd_cutoff,
           7.0 AS completed_months,
           12.0 AS months_in_year
),
actuals AS (
    SELECT
        fiscal_year, cost_center, department, expense_category,
        SUM(actual_amount_usd) AS actual_spend_usd,
        SUM(actual_amount_inr) AS actual_spend_inr,
        COUNT(*) AS transaction_count
    FROM fact_erp_general_ledger
    GROUP BY 1,2,3,4
),
joined AS (
    SELECT
        b.fiscal_year, b.cost_center, b.department, b.expense_category,
        b.budget_owner, b.allocated_budget_usd, b.allocated_budget_inr,
        COALESCE(a.actual_spend_usd,0) AS actual_spend_usd,
        COALESCE(a.actual_spend_inr,0) AS actual_spend_inr,
        COALESCE(a.transaction_count,0) AS transaction_count
    FROM dim_department_budget b
    LEFT JOIN actuals a
      ON a.fiscal_year=b.fiscal_year
     AND a.cost_center=b.cost_center
     AND a.department=b.department
     AND a.expense_category=b.expense_category
),
calc AS (
    SELECT j.*, p.ytd_cutoff,
        actual_spend_usd-allocated_budget_usd AS variance_usd,
        actual_spend_inr-allocated_budget_inr AS variance_inr,
        100.0*actual_spend_usd/NULLIF(allocated_budget_usd,0) AS budget_burn_pct,
        CASE WHEN fiscal_year=2026 THEN actual_spend_usd/(p.completed_months/p.months_in_year) ELSE actual_spend_usd END AS annualized_spend_usd
    FROM joined j
    CROSS JOIN params p
)
SELECT *,
       annualized_spend_usd-allocated_budget_usd AS projected_year_end_variance_usd,
       CASE
         WHEN budget_burn_pct > 100 THEN 'CRITICAL'
         WHEN budget_burn_pct >= 65 THEN 'HIGH RISK'
         WHEN budget_burn_pct >= 50 THEN 'ON TRACK'
         ELSE 'UNDERUTILIZED'
       END AS risk_status
FROM calc
ORDER BY fiscal_year DESC, budget_burn_pct DESC;

-- Department roll-up for FY2026
WITH params AS (SELECT 7.0 AS completed_months, 12.0 AS months_in_year),
actuals AS (
    SELECT fiscal_year, department, SUM(actual_amount_usd) AS actual_usd
    FROM fact_erp_general_ledger
    GROUP BY 1,2
)
SELECT
    b.department,
    SUM(b.allocated_budget_usd) AS budget_usd,
    SUM(COALESCE(a.actual_usd,0)) AS ytd_actual_usd,
    100.0*SUM(COALESCE(a.actual_usd,0))/NULLIF(SUM(b.allocated_budget_usd),0) AS burn_pct,
    SUM(COALESCE(a.actual_usd,0))/(p.completed_months/p.months_in_year) AS annualized_spend_usd,
    SUM(COALESCE(a.actual_usd,0))/(p.completed_months/p.months_in_year)-SUM(b.allocated_budget_usd) AS projected_variance_usd
FROM dim_department_budget b
LEFT JOIN actuals a ON a.fiscal_year=b.fiscal_year AND a.department=b.department
CROSS JOIN params p
WHERE b.fiscal_year=2026
GROUP BY b.department, p.completed_months, p.months_in_year
ORDER BY projected_variance_usd DESC;
