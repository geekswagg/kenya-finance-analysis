import csv,json
from pathlib import Path
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
(root/'data/metadata/discrepancies.json').write_text(json.dumps(issues,indent=2))
print(f'PASS: {len(rows)} rows, {len(keys)} unique source keys; {len(issues)} review flags (not automatically corrected)')
