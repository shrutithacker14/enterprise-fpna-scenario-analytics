-- Compact KPI layer for a dashboard or executive report.
-- FY2026 actuals are YTD through the cutoff used in the variance query.
WITH params AS (SELECT DATE '2026-07-31' AS ytd_cutoff),
dept AS (
    SELECT
        b.fiscal_year, b.department,
        SUM(b.allocated_budget_usd) AS budget_usd,
        SUM(COALESCE(a.actual_usd,0)) AS actual_usd
    FROM dim_department_budget b
    LEFT JOIN (
        SELECT fiscal_year, department, SUM(actual_amount_usd) actual_usd
        FROM fact_erp_general_ledger
        GROUP BY 1,2
    ) a USING (fiscal_year, department)
    GROUP BY 1,2
)
SELECT
    d.fiscal_year,
    p.ytd_cutoff,
    SUM(d.budget_usd) AS total_budget_usd,
    SUM(d.actual_usd) AS ytd_actual_usd,
    SUM(d.actual_usd)-SUM(d.budget_usd) AS ytd_vs_full_year_budget_usd,
    100.0*SUM(d.actual_usd)/NULLIF(SUM(d.budget_usd),0) AS ytd_budget_burn_pct
FROM dept d
CROSS JOIN params p
GROUP BY d.fiscal_year, p.ytd_cutoff
ORDER BY d.fiscal_year;
