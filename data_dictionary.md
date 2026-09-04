# Data Dictionary

## `enterprise_erp_general_ledger_50k.csv`

| Field | Meaning |
|---|---|
| `transaction_id` | Unique synthetic ERP transaction ID |
| `posting_date` | Transaction posting date |
| `fiscal_year` | Fiscal year derived from posting date |
| `fiscal_quarter` | Quarter derived from posting month |
| `cost_center` | Synthetic cost-center code |
| `department` | Department responsible for the spend |
| `expense_category` | Spend category |
| `vendor_name` | Synthetic vendor name |
| `actual_amount_usd` | Actual spend in USD |
| `actual_amount_inr` | Same spend converted using the fixed portfolio FX rate |
| `payment_status` | Synthetic payment status |

## `department_budget_allocations.csv`

| Field | Meaning |
|---|---|
| `budget_id` | Unique budget line ID |
| `fiscal_year` | Budget year |
| `cost_center` | Cost-center code |
| `department` | Budget-owning department |
| `expense_category` | Budget category |
| `allocated_budget_usd` | Full-year budget in USD |
| `allocated_budget_inr` | Full-year budget converted at the fixed FX rate |
| `budget_owner` | Synthetic budget owner title |

## FX convention

`1 USD = ₹95.46` is a fixed presentation assumption dated 25-Aug-2026. It is not a transaction-date accounting translation.
