import csv,json
from pathlib import Path
from decimal import Decimal
from collections import defaultdict
root=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((root/'data/processed/observations.csv').open(encoding='utf-8')))
sources={s['source_id'] for s in json.loads((root/'data/metadata/sources.json').read_text())}
keys=set(); groups=defaultdict(list); checks=defaultdict(dict)
for r in rows:
 assert r['source_id'] in sources
 key=tuple(r[k] for k in ('source_id','source_location','fiscal_year','status','metric','unit'))
 assert key not in keys,key
 keys.add(key)
 v=float(r['value']); assert abs(v-float(r['reported_value'])/(1000 if r['reported_unit']=='KES_million' else 1))<1e-8
 groups[(r['fiscal_year'],r['status'],r['metric'],r['unit'])].append(r)
 checks[(r['source_id'],r['source_location'],r['fiscal_year'],r['status'])][r['metric']]=v
issues=[]
for k,rs in groups.items():
 if len({float(r['value']) for r in rs})>1: issues.append({'type':'different_observations','key':k,'observations':[{a:r[a] for a in ('source_id','source_location','value')} for r in rs]})
for k,d in checks.items():
 for total,parts in [('public_debt',['domestic_debt','external_debt']),('net_financing',['net_domestic_financing','net_external_financing']),('primary_balance',['revenue_and_grants','primary_expenditure']),('gross_financing',['fiscal_deficit','total_principal']),('total_interest',['domestic_interest','external_interest']),('total_debt_service',['domestic_debt_service','external_debt_service'])]:
  if total in d and all(p in d for p in parts):
   expected=d[parts[0]]-d[parts[1]] if total=='primary_balance' else sum(d[p] for p in parts)
   if abs(d[total]-expected)>0.11: issues.append({'type':'identity_variance','key':k,'metric':total,'reported':d[total],'expected':expected})
# Validate the transcribed column in its published unit. The sum of three
# independently rounded whole-million figures can differ by one million.
debt_metrics = {"public_debt", "domestic_debt", "external_debt"}
early = [r for r in rows if r["source_id"] == "dm22" and r["fiscal_year"] == "2021/22"
         and r["metric"] in debt_metrics]
if (len(early) != 3 or {r["metric"] for r in early} != debt_metrics
        or any(r["reported_unit"] != "KES_million" or r["status"] != "provisional_actual"
               for r in early)):
    raise ValueError("Expected three provisional FY 2021/22 debt stocks in KES million")
amounts = {r["metric"]: Decimal(r["reported_value"]) for r in early}
if abs(amounts["public_debt"] - amounts["domestic_debt"] - amounts["external_debt"]) > 1:
    raise ValueError("FY 2021/22 debt identity exceeds the KES 1 million rounding tolerance")

# Compare the same metrics across vintages even when publication statuses differ.
later = {r["metric"]: r for r in rows if r["source_id"] == "dm26"
         and r["fiscal_year"] == "2021/22" and r["metric"] in debt_metrics}
for row in early:
    comparator = later[row["metric"]]
    if row["unit"] != comparator["unit"]:
        raise ValueError("Cannot compare debt vintages with different normalized units")
    if Decimal(row["value"]) != Decimal(comparator["value"]):
        issues.append({
            "type": "publication_vintage_difference",
            "key": [row["fiscal_year"], row["metric"], row["unit"]],
            "observations": [
                {field: observation[field] for field in ("source_id", "source_location", "status", "value")}
                for observation in (row, comparator)
            ],
        })
(root/'data/metadata/discrepancies.json').write_text(json.dumps(issues,indent=2))
print(f'PASS: {len(rows)} rows, {len(keys)} unique source keys; {len(issues)} review flags (not automatically corrected)')
