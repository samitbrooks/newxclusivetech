#!/usr/bin/env python3
"""Build a follow-up sitemap from URL Inspection results, limited to current canonical pages.
A sitemap submission requests discovery/crawling; it never proves or guarantees indexing.
Run with --audit pointing to a private, complete URL Inspection JSON export.
"""
import argparse,json,re,xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
NS='http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('',NS)
def prepare(audit_file,output):
 audit=json.loads(Path(audit_file).read_text());by_url={r['url']:r for r in audit}
 main=ET.parse(ROOT/'sitemap.xml').getroot();target=ET.Element(f'{{{NS}}}urlset');pending=[]
 for entry in main.findall(f'{{{NS}}}url'):
  url=entry.find(f'{{{NS}}}loc').text;row=by_url.get(url)
  if not row or row.get('http')!=200 or 'verdict' not in row:raise ValueError(f'Missing or failed URL Inspection result: {url}')
  path=urlparse(url).path.strip('/');source=ROOT/(path or 'index.html')
  if source.is_dir():source=source/'index.html'
  elif not source.suffix:source=Path(str(source)+'.html')
  if not source.is_file():raise ValueError(f'Obsolete or missing page must be reconciled in main sitemap first: {url}')
  html=source.read_text()
  if re.search(r'<meta[^>]*name=["\'](?:robots|googlebot)["\'][^>]*content=["\'][^"\']*noindex',html,re.I):raise ValueError(f'Page is currently noindex: {url}')
  if row['verdict']=='PASS':continue
  child=ET.SubElement(target,f'{{{NS}}}url');ET.SubElement(child,f'{{{NS}}}loc').text=url
  lastmod=entry.find(f'{{{NS}}}lastmod')
  if lastmod is not None:ET.SubElement(child,f'{{{NS}}}lastmod').text=lastmod.text
  pending.append(url)
 ET.indent(target,space='  ');ET.ElementTree(target).write(output,encoding='UTF-8',xml_declaration=True)
 return pending
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--audit',required=True);args=parser.parse_args()
 pending=prepare(args.audit,ROOT/'sitemap-recheck.xml')
 print(f'Prepared {len(pending)} current canonical URLs for recheck. Existing indexed pages retained in main sitemap. No pages deleted; no indexing guarantee implied.')
