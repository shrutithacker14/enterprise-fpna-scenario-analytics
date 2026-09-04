import numpy as np
import pandas as pd
from pathlib import Path

# Reproducible synthetic ERP generator for the Enterprise FP&A portfolio project.
SEED = 42
FX_RATE = 95.46
FX_DATE = "2026-08-25"
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
rng = np.random.default_rng(SEED)

departments = {
"Engineering": ("CC-100","Director of Engineering", {"Cloud Infrastructure":.28,"Salaries & Contractors":.38,"DevOps Tooling":.22,"Hardware & Peripherals":.12}),
"Marketing": ("CC-200","Director of Marketing", {"Paid Performance Ads":.42,"Events & Sponsorships":.22,"Content & SEO Agencies":.20,"Brand & Creative Assets":.16}),
"Sales": ("CC-300","VP Sales", {"Travel & Entertainment":.20,"Commissions & Incentives":.46,"CRM & Enablement Software":.22,"Client Hospitality":.12}),
"Operations": ("CC-400","VP Operations", {"SaaS Licenses & ERP":.35,"Office Facilities & Lease":.28,"Logistics & Shipping":.17,"Professional Services":.20}),
"Finance & Legal": ("CC-500","CFO", {"External Audit & Tax":.34,"Legal Counsel & Retainers":.30,"Treasury & Bank Fees":.16,"Payroll Processing":.20}),
"Product & Design": ("CC-600","VP Product", {"UX Research & UserTesting":.36,"Prototyping Software":.28,"Design Contractors":.36}),
"Customer Success": ("CC-700","VP Customer Success", {"Ticketing & Support Tools":.48,"Customer Advisory Board":.22,"Retention Swag & Gifting":.30})}
base = {"Engineering":46_500_000,"Marketing":30_000_000,"Sales":27_000_000,"Operations":22_000_000,"Finance & Legal":16_000_000,"Product & Design":18_000_000,"Customer Success":20_000_000}
growth = {"Engineering":.07,"Marketing":.04,"Sales":.05,"Operations":.06,"Finance & Legal":.04,"Product & Design":.06,"Customer Success":.03}
burn25={"Engineering":.94,"Marketing":.92,"Sales":.96,"Operations":.91,"Finance & Legal":.95,"Product & Design":.93,"Customer Success":.90}
burn26={"Engineering":.73,"Marketing":.57,"Sales":.60,"Operations":.69,"Finance & Legal":.55,"Product & Design":.63,"Customer Success":.52}
vendors = {
"Cloud Infrastructure":["AWS","Google Cloud","Microsoft Azure"], "Salaries & Contractors":["Adecco Staffing","Robert Half","Contractor Payroll"], "DevOps Tooling":["Datadog","GitHub Enterprise","Atlassian"], "Hardware & Peripherals":["Dell Technologies","Lenovo","CDW"], "Paid Performance Ads":["Google Ads","Meta Ads","LinkedIn Ads"], "Events & Sponsorships":["Web Summit","SaaStr Events","Regional Expo Group"], "Content & SEO Agencies":["GrowthCraft Agency","SearchLab","ContentWorks"], "Brand & Creative Assets":["Adobe","Canva Enterprise","Creative Studio Partners"], "Travel & Entertainment":["American Airlines","Marriott","Uber for Business"], "Commissions & Incentives":["Sales Incentive Pool","Xactly","Direct Commission Disbursal"], "CRM & Enablement Software":["Salesforce","HubSpot","Gong"], "Client Hospitality":["Four Seasons Hotels","Hilton","Client Dining Partners"], "SaaS Licenses & ERP":["SAP","Oracle NetSuite","ServiceNow"], "Office Facilities & Lease":["WeWork","CBRE","Regus"], "Logistics & Shipping":["FedEx","DHL","UPS"], "Professional Services":["Deloitte Advisory","PwC","KPMG"], "External Audit & Tax":["Deloitte Tax","EY","KPMG Tax"], "Legal Counsel & Retainers":["Baker McKenzie","Clifford Chance","Regional Counsel"], "Treasury & Bank Fees":["JPMorgan Chase","HSBC","Bank Processing Network"], "Payroll Processing":["ADP","Workday Payroll","Paychex"], "UX Research & UserTesting":["UserTesting","Maze","Qualtrics"], "Prototyping Software":["Figma","Miro","Adobe XD"], "Design Contractors":["Toptal","Design Contractor Pool","Fiverr Business"], "Ticketing & Support Tools":["Zendesk","Intercom","Freshworks"], "Customer Advisory Board":["Four Seasons Hotels","Customer Research Partners","Eventbrite"], "Retention Swag & Gifting":["Sendoso","Snappy","Corporate Gifting Co."]}

cat_mult={"Cloud Infrastructure":1.10,"Salaries & Contractors":1.02,"DevOps Tooling":1.04,"Hardware & Peripherals":.96,"Paid Performance Ads":.96,"Events & Sponsorships":.88,"Content & SEO Agencies":.93,"Brand & Creative Assets":.91,"Travel & Entertainment":.92,"Commissions & Incentives":1.02,"CRM & Enablement Software":1.04,"Client Hospitality":.90,"SaaS Licenses & ERP":1.12,"Office Facilities & Lease":1.00,"Logistics & Shipping":.97,"Professional Services":.98,"External Audit & Tax":.99,"Legal Counsel & Retainers":1.03,"Treasury & Bank Fees":.95,"Payroll Processing":.98,"UX Research & UserTesting":.96,"Prototyping Software":1.01,"Design Contractors":1.03,"Ticketing & Support Tools":.98,"Customer Advisory Board":.91,"Retention Swag & Gifting":.89}

budget=[]
for year in [2025,2026]:
  for dept,(cc,owner,cats) in departments.items():
    total=base[dept] if year==2025 else base[dept]*(1+growth[dept])
    for cat,share in cats.items():
      budget.append([f"BUD-{year}-{len(budget)+1:04d}",year,cc,dept,cat,round(total*share,2),owner])
budget=pd.DataFrame(budget,columns=["budget_id","fiscal_year","cost_center","department","expense_category","allocated_budget_usd","budget_owner"])
budget["allocated_budget_inr"]=budget.allocated_budget_usd*FX_RATE

def make_year(year,n,burn):
  b=budget[budget.fiscal_year.eq(year)].copy()
  b["target"]=b.apply(lambda r:r.allocated_budget_usd*burn[r.department]*cat_mult[r.expense_category],axis=1)
  raw=b.target/b.target.sum()*n
  counts=np.maximum(np.floor(raw).astype(int),80)
  diff=n-counts.sum()
  for idx in np.argsort(-raw.values)[:abs(diff)]: counts.iloc[idx]+=1 if diff>0 else -1
  out=[]; counter=1
  for _,r in b.iterrows():
    cnt=int(counts.loc[r.name]); start=pd.Timestamp(f"{year}-01-01"); end=pd.Timestamp(f"{year}-12-31" if year==2025 else f"{year}-07-31")
    dates=start+pd.to_timedelta(rng.integers(0,(end-start).days+1,size=cnt),unit="D")
    x=rng.gamma(2.2,1,cnt); x=x/x.sum()*r.target; x=np.round(x,2); x[-1]=round(x[-1]+(r.target-x.sum()),2)
    for i in range(cnt):
      out.append([f"TXN-{year}{counter:06d}",dates[i].date().isoformat(),year,f"Q{((dates[i].month-1)//3)+1}",r.cost_center,r.department,r.expense_category,rng.choice(vendors[r.expense_category]),x[i],round(x[i]*FX_RATE,2),rng.choice(["Settled","Cleared","Pending"],p=[.70,.25,.05])]); counter+=1
  return pd.DataFrame(out,columns=["transaction_id","posting_date","fiscal_year","fiscal_quarter","cost_center","department","expense_category","vendor_name","actual_amount_usd","actual_amount_inr","payment_status"])

ledger=pd.concat([make_year(2025,25000,burn25),make_year(2026,25000,burn26)],ignore_index=True).sort_values("posting_date")
budget.to_csv(DATA/"department_budget_allocations.csv",index=False)
ledger.to_csv(DATA/"enterprise_erp_general_ledger_50k.csv",index=False)
pd.DataFrame([{"fx_date":FX_DATE,"usd_to_inr":FX_RATE,"source":"Portfolio reference rate","note":"Fixed conversion assumption; not historical transaction-date FX."}]).to_csv(DATA/"usd_inr_reference_rate.csv",index=False)
print(f"Generated {len(ledger):,} ledger rows and {len(budget):,} budget rows.")
print(f"USD to INR: ₹{FX_RATE:.2f}")

# Scenario outputs for quick validation / downstream Excel use.
# This is a separate illustrative operating P&L, not a reconstruction of the ERP ledger.
base_revenue_start=220_000_000
scenario_growth={"Bear":.02,"Base":.10,"Bull":.20}
cogs_pct={"Bear":.266,"Base":.239,"Bull":.213}
opex_pct={"Bear":.585,"Base":.571,"Bull":.566}
tax_interest={"Bear":10_500_000,"Base":11_500_000,"Bull":13_000_000}
rows=[]
for name in ["Bear","Base","Bull"]:
    revenue=base_revenue_start*(1+scenario_growth[name])
    cogs=revenue*cogs_pct[name]
    gross=revenue-cogs
    opex=revenue*opex_pct[name]
    ebitda=gross-opex
    dep=5_000_000 if name!="Bull" else 5_500_000
    net_income=ebitda-dep-tax_interest[name]
    rows.append([name,revenue,cogs,gross,gross/revenue,opex,ebitda,ebitda/revenue,net_income,revenue*FX_RATE,ebitda*FX_RATE,net_income*FX_RATE])
pd.DataFrame(rows,columns=["Scenario","Revenue_USD","COGS_USD","GrossProfit_USD","GrossMargin","OPEX_USD","EBITDA_USD","EBITDA_Margin","NetIncome_USD","Revenue_INR","EBITDA_INR","NetIncome_INR"]).to_csv(DATA/"scenario_outputs.csv",index=False)
