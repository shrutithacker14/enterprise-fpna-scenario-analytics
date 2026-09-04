from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FX = pd.read_csv(DATA / "usd_inr_reference_rate.csv").iloc[0]["usd_to_inr"]
ledger = pd.read_csv(DATA / "enterprise_erp_general_ledger_50k.csv")
budget = pd.read_csv(DATA / "department_budget_allocations.csv")

checks = {
    "ledger_rows": len(ledger),
    "unique_transaction_ids": ledger.transaction_id.nunique(),
    "budget_rows": len(budget),
    "duplicate_transaction_ids": ledger.transaction_id.duplicated().sum(),
    "negative_usd_values": int((ledger.actual_amount_usd < 0).sum()),
    "fx_mismatches": int(((ledger.actual_amount_inr - ledger.actual_amount_usd * FX).abs() > 0.02).sum()),
    "invalid_quarters": int((~ledger.fiscal_quarter.isin(["Q1","Q2","Q3","Q4"])).sum()),
}

for name, value in checks.items():
    print(f"{name}: {value}")

assert checks["ledger_rows"] == 50000
assert checks["unique_transaction_ids"] == 50000
assert checks["budget_rows"] == 52
assert checks["duplicate_transaction_ids"] == 0
assert checks["negative_usd_values"] == 0
assert checks["fx_mismatches"] == 0
assert checks["invalid_quarters"] == 0
print("\nAll validation checks passed.")
