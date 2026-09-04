# Executive FP&A Financial Brief — Enterprise Budget Variance & Scenario Analysis

**Purpose:** A portfolio case study showing how synthetic ERP transactions can be turned into a budget-risk view and a simple operating scenario model.

**Data period:** FY2025 full year and FY2026 January–July 2026.

**FX convention:** 1 USD = ₹95.46, fixed for presentation. This is not historical transaction-date FX.

## 1. Executive summary

FY2026 has a full-year department budget of **$188.95M (₹1803.67 crore)**. Through July, actual spend is **$118.88M (₹1134.81 crore)**, or **62.9% of the full-year budget**.

If the January–July run-rate continues for the remaining five months, projected FY2026 spend is about **$203.79M**, which is approximately **$14.85M (₹141.72 crore) above budget**. This is a simple linear forecast, not a seasonally adjusted forecast.

## 2. Department run-rate

| Department | Annual Budget | YTD Actual | Burn | Annualized Spend | Projected Variance | Risk |
|---|---:|---:|---:|---:|---:|---|
| Engineering | $49.76M | $37.76M | 75.9% | $64.73M | $14.98M | HIGH RISK |
| Operations | $23.32M | $16.62M | 71.3% | $28.49M | $5.17M | HIGH RISK |
| Product & Design | $19.08M | $12.01M | 62.9% | $20.59M | $1.51M | ON TRACK |
| Sales | $28.35M | $16.84M | 59.4% | $28.87M | $0.52M | ON TRACK |
| Finance & Legal | $16.64M | $9.09M | 54.6% | $15.59M | $-1.05M | ON TRACK |
| Marketing | $31.20M | $16.51M | 52.9% | $28.30M | $-2.90M | ON TRACK |
| Customer Success | $20.60M | $10.04M | 48.8% | $17.22M | $-3.38M | UNDERUTILIZED |

## 3. What stands out

1. **Engineering is the largest run-rate risk**, followed by Operations. Their current seven-month burn rates are already above the 65% high-risk threshold.

2. **Product & Design is close to the risk threshold**. It is not labelled high risk in this model, but it is worth watching because a straight-line forecast still points to a modest year-end overrun.

3. **Marketing and Customer Success are below the model's 50%/65% risk bands**, so I would avoid assuming that every department needs the same cost action.

4. The largest projected variance is a **run-rate signal**, not proof that a department will actually finish over budget. A real forecast should include seasonality and known commitments.

## 4. Scenario model

The scenario workbook is intentionally separate from the transaction ledger. It is an illustrative operating P&L used to demonstrate scenario and sensitivity analysis at an enterprise scale.

| Scenario | Revenue | EBITDA | EBITDA Margin | Net Income |
|---|---:|---:|---:|---:|
| Bear | $224.4M | $33.4M | 14.9% | $17.9M |
| Base | $242.0M | $46.0M | 19.0% | $29.5M |
| Bull | $264.0M | $58.3M | 22.1% | $39.8M |

## 5. Recommended actions

- **Engineering / FinOps:** review cloud commitments, unused resources and the largest infrastructure vendors first.

- **Operations:** review SaaS and ERP licences for unused seats, overlapping tools and renewal timing.

- **Forecasting:** move from a single linear run-rate to monthly budget phasing if this were used with real finance data.

- **Scenario monitoring:** use the sensitivity grid to see how quickly EBITDA margin changes when growth slows or operating costs rise.

## 6. Caveats

- ERP transactions, budgets and vendors are synthetic.
- INR is a fixed presentation conversion, not historical accounting FX.
- The run-rate forecast assumes the first seven months are representative of the final five months.
- Scenario revenue and margin assumptions are illustrative and are not derived from the synthetic ERP ledger.
