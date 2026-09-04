SELECT
    fiscal_year,
    DATE_TRUNC('month', posting_date) AS month_start,
    SUM(actual_amount_usd) AS spend_usd,
    SUM(actual_amount_inr) AS spend_inr,
    COUNT(*) AS transactions
FROM fact_erp_general_ledger
GROUP BY 1,2
ORDER BY 1,2;
