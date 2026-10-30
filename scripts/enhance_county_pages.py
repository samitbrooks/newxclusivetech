#!/usr/bin/env python3
"""Improve service intent, truthful coverage and lead paths on county pages."""
from pathlib import Path
import re,json
from html import escape
from normalize_site_assets import normalize_html

def enhance_county_html(source,c):
 name=c['name'];towns=', '.join(c['towns'][:4]);canonical=f'https://www.xclusivetech.co.ke/locations/{c["slug"]}'
 title=f'Web Design in {name} County — From KES 15,000 | Xclusive Tech'
 description=f'Website design for businesses in {towns}, {name} County. Landing pages from KES 15,000, business sites from KES 25,000. View work and get a quote.'
 source=re.sub(r'<title>[^<]+</title>',f'<title>{escape(title)}</title>',source,count=1)
 for key in ['description','og:description','twitter:description']:
  source=re.sub(r'(<meta (?:name|property)="'+key+r'" content=")[^"]*(">)',lambda m:m[1]+escape(description,quote=True)+m[2],source)
 for key in ['og:title','twitter:title']:
  source=re.sub(r'(<meta (?:name|property)="'+key+r'" content=")[^"]*(">)',lambda m:m[1]+escape(title,quote=True)+m[2],source)
 source=source.replace('Website Design &amp; Digital Engineering in','Website Design in')
 if 'id="county-service-summary"' not in source:
  summary=f'''<p id="county-service-summary" class="county-service-summary">Xclusive Tech designs business websites and M-Pesa online stores for {escape(name)} County. We are based in Nairobi and serve {escape(towns)} remotely. A landing page starts at <strong>KES 15,000</strong>; multi-page websites start at <strong>KES 25,000</strong>. <a href="/pricing">Compare packages</a> or <a href="/contact">request a written quote</a>.</p>'''
  source=re.sub(r'(</h1>)',lambda m:m[0]+'\n'+summary,source,count=1)
 # Keep the main contact action close to the heading on a small screen.
 short_summary=f'<p id="county-service-summary" class="county-service-summary">Xclusive Tech builds business websites for {escape(name)} County. Landing pages from <strong>KES 15,000</strong>; multi-page sites from <strong>KES 25,000</strong>. Our Nairobi-based team works remotely. Domain and hosting costs are separate. <a href="/portfolio">View our work</a>.</p>'
 source=re.sub(r'<p id="county-service-summary"[^>]*>[\s\S]*?</p>',lambda m:short_summary,source,count=1)
 cta=re.search(r'<!-- CTA Row -->\s*<div class="pt-4 flex flex-col sm:flex-row gap-4">[\s\S]*?</div>',source)
 if cta and cta.start() > source.find('<!-- Key Towns List -->'):
  block=cta[0];source=source.replace(block,'',1);source=source.replace(short_summary,short_summary+'\n'+block,1)
 source=source.replace('Sub-1.5s Load Times:','Mobile-first Performance:').replace('Optimized for mobile visitors on Safaricom 4G/5G and Airtel Kenya networks','Designed for clear navigation and fast-loading pages on Kenyan mobile networks')
 source=re.sub(r'Dominate local search in [^<]+',f'Help search engines understand your business and services in {escape(name)}',source)
 source=source.replace('class="nav-cta"','class="nav-cta-btn"')
 # Keep the desktop county CTA legible against the dark header.
 source=re.sub(r'(<a\b[^>]*class=")([^"\n]*)("[^>]*>\s*<span>WhatsApp Us</span>)',lambda m:m[1]+m[2]+' nav-cta-btn'+m[3] if 'nav-cta-btn' not in m[2] else m[0],source)
 if 'id="county-website-brief"' not in source:
  focus=c['economic_focus'].rstrip('.')
  if name=='Bungoma':
   needs=[('Produce suppliers and cooperatives','Show available produce, packing options, delivery areas and a clear wholesale enquiry form for buyers in Bungoma Town and Chwele.'),('Webuye manufacturers and contractors','Publish service capabilities, project photographs, downloadable company profiles and quote requests.'),('Shops and service businesses','Create a mobile catalogue, show opening hours and location, and offer WhatsApp enquiries or M-Pesa checkout where required.')]
  else:
   needs=[(f'Business websites for {c["seat"]}','Present your services, contact details, operating hours and an enquiry form that collects the information you need to quote.'),(f'Catalogues and online payments in {name}','Show products or service packages with clear prices and delivery terms. Add M-Pesa checkout when customers need to pay online.'),(f'Service coverage across {c["towns"][1] if len(c["towns"])>1 else name}','Explain the towns you serve, delivery or appointment arrangements, and the next step for a customer who wants to contact you.')]
  cards=''.join(f'<article class="county-brief-card"><h3>{escape(h)}</h3><p>{escape(t)}</p></article>' for h,t in needs)
  section=f'''<section id="county-website-brief" class="county-brief-section"><div class="county-brief-container"><h2>Plan a website for your {escape(name)} business</h2><p>Local business context: {escape(focus)}. Choose features around what your customers need to do, rather than adding pages for their own sake.</p><div class="county-brief-grid">{cards}</div><div class="county-brief-next"><h3>See our work before you enquire</h3><p>Browse <a href="/portfolio">live client websites</a>, compare <a href="/pricing">published packages</a>, or read our <a href="/blog/how-much-does-a-website-cost-in-kenya">website cost guide</a>. These are examples from our wider portfolio, not claims of an office or completed project in {escape(name)}.</p><h3>A clear brief gets you a clearer quote</h3><p>Send your business name, services or products, preferred launch date and budget. We confirm the scope, delivery schedule, domain and hosting costs before work starts. Reviews and approval are handled remotely; you do not need to travel to Nairobi.</p><a class="nav-cta-btn" href="/contact?county={escape(name,quote=True)}">Request a {escape(name)} website quote</a><a class="county-phone-link" href="tel:+254722753819">Call +254 722 753 819</a></div></div></section>'''
  source=source.replace('</main>',section+'\n</main>')
 def schema(m):
  d=json.loads(m[1])
  for item in d.get('@graph',[]):
   if item.get('@type')=='Service':
    item['name']=f'Website Design in {name} County';item['url']=canonical
    item['provider']['@id']='https://www.xclusivetech.co.ke/#organization'
    item['areaServed']=list(dict.fromkeys(item.get('areaServed',[])))
    item['description']=f'Business website design, M-Pesa e-commerce and on-page SEO for {name} County. Nairobi-based team serving {towns} remotely.'
   if item.get('@type')=='FAQPage':
    for q in item.get('mainEntity',[]):
     if 'cost' in q.get('name','').lower():q['acceptedAnswer']['text']=f'Landing pages start at KES 15,000. Multi-page business websites start at KES 25,000 and e-commerce starts at KES 72,000. Domain registration and hosting are separate. Request a written quote for the agreed scope.'
  return '<script type="application/ld+json">\n'+json.dumps(d,indent=2,ensure_ascii=False)+'\n</script>'
 source=re.sub(r'<script type="application/ld\+json">([\s\S]*?)</script>',schema,source)
 return normalize_html(source)

if __name__=='__main__':
 from generate_county_pages import COUNTIES
 for c in COUNTIES:
  p=Path('locations')/(c['slug']+'.html');p.write_text(enhance_county_html(p.read_text(),c))
 print('Enhanced all 47 county service pages')
