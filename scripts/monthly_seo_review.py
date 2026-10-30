#!/usr/bin/env python3
"""Generate a private monthly Search Console action queue; never auto-publish claims."""
import argparse,calendar,json,sys
from pathlib import Path
from datetime import date,timedelta
from search_console import get_access_token,get_search_analytics,inspect_url

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--month',required=True,help='Complete calendar month, YYYY-MM')
parser.add_argument('--output-dir',default=str(Path.home()/'seo-audits'/'monthly'))
args=parser.parse_args()
year,month=map(int,args.month.split('-'));start=date(year,month,1);end=date(year,month,calendar.monthrange(year,month)[1]);previous_end=start-timedelta(days=1);previous_start=previous_end.replace(day=1)
if end>=date.today():raise SystemExit('Choose a completed month so the report does not imply a complete current-month result.')
token=get_access_token();site='sc-domain:xclusivetech.co.ke';data={'property':site,'month':args.month,'period':{'start':str(start),'end':str(end)},'previous_period':{'start':str(previous_start),'end':str(previous_end)}}
for period,a,b in [('current',start,end),('previous',previous_start,previous_end)]:
 data[period]={}
 for dimension in ['page','query']:
  status,result=get_search_analytics(token,site,dimension,str(a),str(b),25000)
  if status!=200:raise SystemExit(f'Google returned HTTP {status}; no complete review was generated.')
  data[period][dimension]=result.get('rows',[])
actions=[]
previous={r['keys'][0]:r for r in data['previous']['page']}
for row in data['current']['page']:
 url=row['keys'][0];before=previous.get(url,{});action=None
 if row['impressions']>=20 and row['clicks']==0:action='Review title, description and buyer intent. Check indexing before editing.'
 elif before.get('clicks',0)>row['clicks']:action='Compare query mix and current content; do not infer that one edit caused the change.'
 if action:actions.append({'url':url,'clicks':row['clicks'],'impressions':row['impressions'],'ctr':row['ctr'],'position':row['position'],'action':action})
data['action_queue']=sorted(actions,key=lambda r:r['impressions'],reverse=True)
root=Path(args.output_dir);root.mkdir(parents=True,exist_ok=True);(root/f'{args.month}.json').write_text(json.dumps(data,indent=2))
lines=[f'# Monthly SEO review — {args.month}','',f'Property: {site}. Current month: {start}–{end}. Comparison: {previous_start}–{previous_end}.','', 'Page and query rows may not reconcile because Google anonymizes some queries. No edits are published automatically.','', '| Page | Clicks | Impressions | Review action |','|---|---:|---:|---|']
lines.extend(f'| {r["url"]} | {r["clicks"]} | {r["impressions"]} | {r["action"]} |' for r in data['action_queue'])
lines+=['','## Manual review','', '- Inspect any unindexed priority URL in Search Console.','- Compare real enquiries, accepted submissions and qualified leads separately from clicks.','- Recheck form delivery and mobile performance.','- Add only evidence-backed customer examples or approved feedback.','- Record the content change and revisit it after Google has recrawled.']
(root/f'{args.month}.md').write_text('\n'.join(lines)+'\n')
print(f'Private monthly review written to {root/args.month}.md; {len(actions)} page actions, no automatic content changes')
