#!/usr/bin/env python3
"""Read Google URL Inspection status for current sitemap URLs; save results privately.
This does not submit indexing requests. Pair a complete audit with prepare_indexing_recheck.py.
"""
import argparse,json,time,concurrent.futures
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import xml.etree.ElementTree as ET
from search_console import get_access_token,inspect_url
ROOT=Path(__file__).resolve().parents[1]
NS={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
def audit_urls(urls,token,site,workers=4):
 def inspect(url):
  for attempt in range(3):
   try:
    status,response=inspect_url(token,site,url)
    if status in [429,500,502,503,504] and attempt<2:time.sleep(attempt+1);continue
    detail=response.get('inspectionResult',{}).get('indexStatusResult',{})
    return {'url':url,'http':status,**detail,'error':response.get('error')}
   except Exception as error:
    if attempt<2:time.sleep(attempt+1);continue
    return {'url':url,'http':None,'error':type(error).__name__}
 results=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
  for row in pool.map(inspect,urls):
   results.append(row)
   if len(results)%20==0:print(f'Inspected {len(results)}/{len(urls)} URLs',flush=True)
 return results

def main():
 today=datetime.now(ZoneInfo('Africa/Nairobi')).date().isoformat()
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--sitemap',type=Path,default=ROOT/'sitemap.xml')
 parser.add_argument('--site-url',default='sc-domain:xclusivetech.co.ke')
 parser.add_argument('--output',type=Path,default=Path.home()/'seo-audits'/f'xclusivetech-{today}'/'url-inspection.json')
 args=parser.parse_args()
 # Search Console exports are private operational data, never deploy them with website assets.
 output=args.output.expanduser().resolve()
 if output.is_relative_to(ROOT):parser.error('Choose a private output path outside the website repository.')
 urls=[x.text for x in ET.parse(args.sitemap).findall('s:url/s:loc',NS)]
 if not urls or len(urls)!=len(set(urls)):parser.error('Sitemap is empty or contains duplicate URLs.')
 print(f'Inspecting {len(urls)} current canonical URLs for {args.site_url}',flush=True)
 results=audit_urls(urls,get_access_token(),args.site_url)
 output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(results,indent=2)+'\n')
 summary=Counter(r.get('coverageState','Inspection error')for r in results)
 print(json.dumps(dict(summary),indent=2));print(f'Private audit saved: {output}')
 failures=[r for r in results if r.get('http')!=200 or not r.get('verdict')]
 if failures:raise SystemExit(f'{len(failures)} inspection calls failed; do not treat those URLs as confirmed non-indexed. Retry the audit.')
if __name__=='__main__':main()
