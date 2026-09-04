-- Data quality checks: every query should return zero rows unless a problem exists.

-- Duplicate transaction IDs
SELECT transaction_id, COUNT(*) AS row_count
FROM fact_erp_general_ledger
GROUP BY transaction_id
HAVING COUNT(*) > 1;

-- Missing or invalid amounts
SELECT * FROM fact_erp_general_ledger
WHERE actual_amount_usd IS NULL OR actual_amount_usd < 0
   OR actual_amount_inr IS NULL OR actual_amount_inr < 0;

-- FX reconciliation
SELECT * FROM fact_erp_general_ledger
WHERE ABS(actual_amount_inr - actual_amount_usd * (SELECT usd_to_inr FROM dim_fx_rate LIMIT 1)) > 0.02;

-- Invalid fiscal quarter
SELECT * FROM fact_erp_general_ledger
WHERE fiscal_quarter NOT IN ('Q1','Q2','Q3','Q4');

-- Budget duplication at the analytical grain
SELECT fiscal_year, department, expense_category, COUNT(*) AS row_count
FROM dim_department_budget
GROUP BY fiscal_year, department, expense_category
HAVING COUNT(*) > 1;
