-- Enterprise FP&A Analytics Suite
-- PostgreSQL-compatible schema
-- Currency conversion assumption: 1 USD = INR 95.46 as of 2026-08-25.

DROP TABLE IF EXISTS fact_erp_general_ledger;
DROP TABLE IF EXISTS dim_department_budget;
DROP TABLE IF EXISTS dim_fx_rate;

CREATE TABLE dim_fx_rate (
    fx_date DATE PRIMARY KEY,
    usd_to_inr NUMERIC(12,4) NOT NULL,
    source VARCHAR(120) NOT NULL,
    note VARCHAR(255)
);

CREATE TABLE dim_department_budget (
    budget_id VARCHAR(32) PRIMARY KEY,
    fiscal_year INT NOT NULL,
    cost_center VARCHAR(10) NOT NULL,
    department VARCHAR(50) NOT NULL,
    expense_category VARCHAR(60) NOT NULL,
    allocated_budget_usd NUMERIC(18,2) NOT NULL CHECK (allocated_budget_usd >= 0),
    allocated_budget_inr NUMERIC(20,2) NOT NULL CHECK (allocated_budget_inr >= 0),
    budget_owner VARCHAR(100)
);

CREATE TABLE fact_erp_general_ledger (
    transaction_id VARCHAR(20) PRIMARY KEY,
    posting_date DATE NOT NULL,
    fiscal_year INT NOT NULL,
    fiscal_quarter VARCHAR(5) NOT NULL,
    cost_center VARCHAR(10) NOT NULL,
    department VARCHAR(50) NOT NULL,
    expense_category VARCHAR(60) NOT NULL,
    vendor_name VARCHAR(120) NOT NULL,
    actual_amount_usd NUMERIC(18,2) NOT NULL CHECK (actual_amount_usd >= 0),
    actual_amount_inr NUMERIC(20,2) NOT NULL CHECK (actual_amount_inr >= 0),
    payment_status VARCHAR(20) NOT NULL
);

CREATE INDEX idx_ledger_dept_year ON fact_erp_general_ledger (fiscal_year, department);
CREATE INDEX idx_ledger_posting_date ON fact_erp_general_ledger (posting_date);
CREATE INDEX idx_budget_lookup ON dim_department_budget (fiscal_year, department, expense_category);
