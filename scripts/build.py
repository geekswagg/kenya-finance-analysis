from pathlib import Path
import csv,json
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'data/processed'
rows=[]
def add(domain,source,loc,year,status,metrics,unit='KES_billion',notes=''):
 for metric,value in metrics.items():
  if value is None: continue
  v=Decimal(str(value)); normalized=v/1000 if unit=='KES_million' else v
  rows.append(dict(domain=domain,source_id=source,source_location=loc,fiscal_year=year,period_end=f'{int(year[:4])+1}-06-30',status=status,metric=metric,reported_value=str(v),reported_unit=unit,value=float(normalized),unit='KES_billion' if unit=='KES_million' else unit,notes=notes))
years=[f'{y}/{str(y+1)[-2:]}' for y in range(2021,2027)]
for idx,(total,dom,ext,pct,loc) in enumerate([(1024,664,360,8.1,'printed p.3'),(862.92,582.19,280.73,6.2,'printed pp.1–2'),(861.3,449.2,412.15,5.3,'printed p.3 §3.1'),(768.6,413.1,355.5,4.3,'printed p.7 §3.2'),(901,613.6,287.4,4.7,'printed p.5 §3.2'),(1145.2,898,247.2,5.5,'printed p.5 §3.2')]):
 s=f'abp{21+idx}'; y=years[idx]; add('borrowing',s,loc,y,'published_plan',dict(net_financing=total,net_domestic_financing=dom,net_external_financing=ext)); add('borrowing',s,loc,y,'published_plan',dict(deficit_to_gdp=pct),'percent')
keys='revenue_and_grants primary_expenditure primary_balance domestic_interest external_interest total_interest fiscal_deficit domestic_principal external_principal total_principal gross_financing'.split()
for s,y,vals,loc,status in [('abp24',years[2],[2724699,2814818,-90119,622544,218188,840732,930851,284973,537783,822756,1753607],'Table 2, printed p.7','prior_year_comparator'),('abp24',years[3],[3112254,2870947,241307,749970,259907,1009877,768570,569893,330711,900604,1669174],'Table 2, printed p.7','published_plan'),('abp25',years[4],[3368882,3172179,196703,851421,246268,1097689,900986,306161,340190,646351,1547337],'Table 2, printed p.4','published_plan'),('abp26',years[5],[3674175,3565129,109047,986726,267512,1254238,1145191,438408,412870,851278,1996469],'Table 2, printed p.5','published_plan')]:
 add('fiscal',s,loc,y,status,dict(zip(keys,vals)),'KES_million','Deficit, principal and gross needs shown as positive magnitudes; principal excludes T-bill redemptions.')
add('fiscal','abp21','printed p.3',years[0],'published_plan',dict(revenue=2125,grants=66,total_expenditure=3215,fiscal_deficit=1024))
add('fiscal','abp22','Table 1, printed p.1',years[1],'published_plan',dict(revenue=2462.36,grants=33.32,total_expenditure=3358.60,fiscal_deficit=862.92))
for metric,vals in {'public_debt':[8761418,10278879,10580455,11814474,13120868],'external_debt':[4334791,5446561,5171704,5488465,5793666],'domestic_debt':[4426627,4832318,5408751,6326009,7327202],'nominal_gdp':[12752164,14274419,15826415,17434534,18642472]}.items():
 for j,v in enumerate(vals): add('debt','dm26','Table 3, printed p.13',years[j],'provisional_actual' if j==4 else 'actual',{metric:v},'KES_million')
for metric,vals in {'debt_to_gdp':[68.7,72,66.9,67.8,70.4],'pv_debt_to_gdp':[63.1,64.4,64.4,63.7,65.6],'real_gdp_growth':[4.8,5.3,5.6,4.9,5.1]}.items():
 for j,v in enumerate(vals): add('debt','dm26','Table 3, printed p.13',years[j],'provisional_actual' if j==4 else 'actual',{metric:v},'percent')
for metric,vals in {'total_debt_service':[917778,1202075,1580766,1722104,1872138],'total_interest':[577979,689327,843846,987495,1071589],'external_debt_service':[305666,405004,773406,579042,716104],'external_principal':[184536,248776,552104,367804,504344],'external_interest':[121130,156229,221302,211238,211760],'domestic_debt_service':[612112,797071,807360,1143062,1156034],'domestic_interest':[456849,533098,622544,776257,859829],'domestic_principal':[155263,263973,184816,366805,296205],'ordinary_revenue':[1917911,2041119,2288921,2420174,2588401]}.items():
 for j,v in enumerate(vals): add('debt_service','dm26','Table 4, printed pp.15–16',years[j],'actual',{metric:v},'KES_million','Domestic principal excludes T-bill redemptions.')
for metric,vals in {'debt_service_to_ordinary_revenue':[47.9,58.9,69.1,71.2,72.3],'interest_to_ordinary_revenue':[30.1,33.8,36.9,40.8,41.4]}.items():
 for j,v in enumerate(vals): add('debt_service','dm26','Table 4, printed p.15',years[j],'actual',{metric:v},'percent')
for s,y,vals,target in [('abp25',years[3],[1032.8,853.4,178.9],[1012.3,825.8,186.5]),('abp26',years[4],[1252.5,985.2,267.3],[1357.7,973.6,384]),('dm26',years[3],[1034.2,None,179.7],[1012.3,None,186.5]),('dm26',years[4],[1251.1,None,267.4],[1357.7,None,384])]:
 for status,vs in [('actual',vals),('revised_target',target)]: add('borrowing',s,'Table 2, printed p.10' if s=='dm26' else '§2 Review of prior plan',y,status,dict(zip(['net_financing','net_domestic_financing','net_external_financing'],vs)))
add('debt','abp26','§1.4 printed p.3',years[4],'actual',dict(public_debt=13013.2,domestic_debt=7328.5,external_debt=5684.7))
add('debt','abp23','§1.2 printed p.1',years[1],'provisional_actual',dict(public_debt=10278.67,domestic_debt=4832.11,external_debt=5446.56))
for metric,vals in {'bilateral':[1105737,1257498,1092689,1032812,990065],'multilateral':[1923444,2654934,2786948,3045391,3180402],'commercial':[1113256,1349052,1178364,1312602,1538663],'suppliers_credit':[12154,14848,13537,14419,14139],'guaranteed_bilateral':[67532,82005,71026,73551,60688],'guaranteed_commercial':[83712,88224,29139,9690,9710],'external_debt_total':[4305835,5446561,5171703,5488465,5793666]}.items():
 for j,v in enumerate(vals): add('creditors','dm26','Table 10, printed p.31',years[j],'actual',{metric:v},'KES_million')
for metric,vals in {'real_gdp_growth':[4.6,4.8,5,5.1,5.2,5.3],'gdp_deflator':[3.1,4.9,6.1,5.8,5.4,5.4],'inflation':[4.3,4.7,5.5,5.2,4.8,4.8],'fiscal_balance_to_gdp':[-5.9,-6.8,-5.5,-3.9,-3.6,-3.4]}.items():
 for j,v in enumerate(vals): add('macro','abp26','Table 1, printed p.2',f'{2024+j}/{str(2025+j)[-2:]}','preliminary_actual' if j<2 else 'projection',{metric:v},'percent')
for status,vals in [('revised_target',[11.9,7.5,5.1]),('actual',[12.7,9.7,6.2])]: add('risk','dm26','Table 1, printed p.6',years[4],status,dict(zip(['debt_maturing_1yr_share','debt_maturing_1yr_to_gdp','interest_to_gdp'],vals)),'percent')
add('risk','dm26','Executive summary p.xvi',years[4],'actual',{'debt_maturing_1yr_share':12.5},'percent')
add('risk','dm26','Executive summary p.xvi',years[4],'actual',{'average_time_to_maturity':8.6},'years')
# Printed page 10 uses the provisional June 2022 column.
for metric, label, value in (
    ("public_debt", "GRAND TOTAL", 8588281),
    ("domestic_debt", "Total Gross Domestic", 4288333),
    ("external_debt", "Total External debt", 4299948),
):
    add("debt", "dm22", f"Table 4.0-1, printed p.10, {label}, Jun-2022*",
        "2021/22", "provisional_actual", {metric: value}, "KES_million",
        "External debt includes publicly guaranteed debt.")

for name,subset in [('observations',rows)]+[(d,[r for r in rows if r['domain']==d]) for d in sorted({r['domain'] for r in rows})]:
 with (OUT/f'{name}.csv').open('w',newline='',encoding='utf-8') as f: w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(subset)
 (OUT/f'{name}.json').write_text(json.dumps(subset,indent=2),encoding='utf-8')
print(f'{len(rows)} observations')
