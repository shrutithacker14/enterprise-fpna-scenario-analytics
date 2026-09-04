# Enterprise FP&A Analytics

![Excel dashboard preview](docs/dashboard_preview.png)

A small FP&A-style analytics case study built from synthetic ERP data. I used Python to generate the data, SQL to validate and analyze it, and Excel to build a simple scenario model. The goal is to show the full path from raw transactions to a business recommendation.

> **Note:** The company, transactions, budgets and vendors in this repository are synthetic. This is a portfolio project, not a real company's financial data.

## What I was trying to answer

- Which departments are on track to exceed their FY2026 budgets?
- How much would FY2026 spend be if the January–July run-rate continued?
- Which areas are contributing most to the projected variance?
- How sensitive is EBITDA to changes in revenue growth and operating-cost inflation?
- What do the same numbers look like in INR?

## Headline FY2026 results

Using January–July 2026 as the YTD period:

- **Full-year budget:** $188.95M / ₹1803.67 crore
- **YTD actual spend:** $118.88M / ₹1134.81 crore
- **Budget consumed:** 62.9%
- **Annualized run-rate:** $203.79M / ₹1945.39 crore (approximately)
- **Projected year-end variance:** +$14.85M

The two clearest run-rate risks are **Engineering** and **Operations**. I would start the review there rather than applying a blanket cost reduction across every department.

## USD to INR

The project stores both currencies in the data files. I use a fixed reference assumption of **₹95.46 per USD**, dated 25-Aug-2026. This keeps the model easy to reproduce and avoids mixing historical transaction FX with a portfolio presentation rate.

If this were an accounting project, I would use a transaction-date FX table instead.

## Repository

```text
enterprise-budget-variance-sensitivity-suite/
├── data/
│   ├── enterprise_erp_general_ledger_50k.csv
│   ├── department_budget_allocations.csv
│   ├── usd_inr_reference_rate.csv
│   └── scenario_outputs.csv
├── docs/
│   └── data_dictionary.md
├── models/
│   └── enterprise_fpna_scenario_model_INR_USD.xlsx
├── reports/
│   └── executive_financial_brief.md
├── scripts/
│   └── generate_enterprise_data.py
├── sql/
│   ├── 01_ddl_and_warehouse_schema.sql
│   ├── 02_data_quality_checks.sql
│   ├── 03_budget_variance_analysis.sql
│   ├── 04_monthly_spend_trend.sql
│   └── 05_executive_metrics.sql
├── requirements.txt
└── README.md
```

## How to run it

### Python

```bash
pip install -r requirements.txt
python scripts/generate_enterprise_data.py
```

The script uses **seed 42** so the synthetic data can be regenerated.

### PostgreSQL

1. Create the three tables with `01_ddl_and_warehouse_schema.sql`.
2. Import the three CSV data files into the matching tables.
3. Run `02_data_quality_checks.sql`. Each check is intended to return zero rows when the data is clean.
4. Run `03_budget_variance_analysis.sql`, `04_monthly_spend_trend.sql`, and `05_executive_metrics.sql`.

The SQL is written for PostgreSQL.

### Excel

Open `models/enterprise_fpna_scenario_model_INR_USD.xlsx`. The workbook contains:

- **Executive Dashboard** — headline KPIs and department run-rate risk
- **Scenario Engine** — Bear/Base/Bull cases and EBITDA sensitivity
- **Department Variance** — department-level USD and INR analysis
- **FX & Assumptions** — model inputs in one place
- **Read Me** — short instructions and assumptions

## Methodology

**Budget burn** = YTD actual spend ÷ full-year budget

**Annualized spend** = YTD actual spend ÷ (7 ÷ 12)

**Projected variance** = annualized spend − full-year budget

Risk labels are deliberately simple:

- `<50%` burn → Underutilized
- `50%–<65%` → On Track
- `65%–100%` → High Risk
- `>100%` → Critical

The run-rate forecast is a straight-line assumption. It does **not** account for seasonality, known contract renewals, or planned one-off spend.

## A note about the scenario model

The Excel scenario model is an **illustrative operating P&L**, separate from the ERP spend ledger. Its purpose is to demonstrate scenario and sensitivity analysis rather than to claim that the synthetic ledger represents a real company's revenue statement.

## What I would do next

If I were extending this for a real FP&A team, I would add monthly budget phasing, actual-vs-plan by month, contract renewal dates, historical FX rates, and a Power BI/Tableau dashboard.

## Tools

Python · Pandas · NumPy · PostgreSQL · SQL · Excel
