#!/usr/bin/env python3
"""Check crawlable URLs, canonical tags, schemas, SVG icons and shared assets."""
from pathlib import Path
import json,re,xml.etree.ElementTree as ET
from normalize_site_assets import EMOJI
ROOT=Path(__file__).resolve().parents[1]
BASE='https://www.xclusivetech.co.ke'
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
urls=[x.text for x in ET.parse(ROOT/'sitemap.xml').findall('.//s:loc',ns)]
assert len(urls)==len(set(urls)), 'Duplicate sitemap URLs'
titles=set();counties=0
for url in urls:
 path=url.removeprefix(BASE).strip('/')
 file=ROOT/(path or 'index.html')
 if file.is_dir():file=file/'index.html'
 elif not file.suffix:file=Path(str(file)+'.html')
 assert file.exists(),url
 source=file.read_text()
 assert not re.search(r'<meta[^>]*name="robots"[^>]*content="[^\"]*noindex',source,re.I),url
 canonical=re.search(r'<link rel="canonical" href="([^"]+)"',source)
 assert canonical and canonical[1]==url,(url,'canonical mismatch')
 ids=re.findall(r'\bid=[\"\']([^\"\']+)[\"\']',source)
 assert len(ids)==len(set(ids)),(url,'duplicate element IDs')
 title=re.search(r'<title>(.*?)</title>',source,re.S)[1]
 assert title not in titles,(url,'duplicate title')
 titles.add(title)
 assert len(re.findall(r'<h1\b',source))==1,(url,'expected one H1')
 assert not EMOJI.search(source),(url,'emoji remains')
 assert 'cdn.tailwindcss.com' not in source,(url,'runtime CSS remains')
 for block in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>',source):json.loads(block)
 if '/locations/web-design-' in url:
  counties+=1
  for marker in ['id="county-service-summary"','id="county-website-brief"','id="mobile-menu-btn"','id="mobile-menu"']:
   assert marker in source,(url,marker)
  assert source.index('<!-- CTA Row -->') < source.index('<!-- Key Towns List -->'),url
assert counties==47,counties
assert 'noindex,follow' in (ROOT/'404.html').read_text()
print(f'PASS: {len(urls)} unique indexable sitemap URLs; 47 county pages; valid canonicals, JSON-LD, H1s, SVG-only icons, static CSS and repaired county navigation')
