#!/usr/bin/env python3
"""Render approved website offers from content/site-facts.json. No printing/SMM prices are changed."""
from pathlib import Path
import json,re,subprocess
from html import escape as e
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
FACTS=json.loads((ROOT/'content/site-facts.json').read_text());PRICING=FACTS['pricing'];PACKAGES=[PRICING['launchOffer'],*PRICING['packages'][:3]]
def cards():
 out='<div class="xt-package-grid">'
 for p in PACKAGES:
  message=f"Hi Xclusive Tech, I am interested in {p['name']} at KES {p['priceAmount']:,}. Scope: {p['scope']}. 50% build deposit: KES {p['depositAmount']:,}. Please confirm scope, separate costs and availability."
  out+=f'''<article class="xt-package-card" data-package="{p['id']}"><h3>{e(p['name'])}</h3><p class="xt-package-price">{e(p['price'])}</p><p class="xt-package-deposit">Start with KES {p['depositAmount']:,} · 50% build deposit</p><p class="xt-package-scope">{e(p['scope'])}</p><p class="xt-package-time">Target: {e(p['delivery'])}</p><ul><li>Mobile layout, on-page SEO, contact form and WhatsApp</li><li>Two revision rounds; approved content supplied by you</li>{('<li>CMS handover and analytics/Search Console setup</li>' if p['id']=='growth' else '<li>Standard supported M-Pesa gateway setup</li>' if p['id']=='ecommerce' else '')}<li>{e(p['features'][-1])}</li></ul><a class="xt-package-action" href="https://wa.me/254722753819?text={quote(message)}" target="_blank" rel="noopener noreferrer">Enquire about {e(p['name'])}</a></article>'''
 return out+'</div>'
def terms():
 return f'''<div class="xt-pricing-notes"><p><strong>What the base price covers:</strong> {e(PRICING['scopeBoundaries'])}</p><p><strong>Delivery:</strong> {e(PRICING['deliveryCondition'])}</p><p><strong>Separate running costs:</strong> .co.ke domain registration from KES 1,500/year; hosting from KES 3,000/year. Renewal prices are confirmed in writing before purchase. Optional care from KES 2,000/month covers four hours of updates/support. Payment-provider fees and paid software licences are separate.</p><p><strong>Payment:</strong> {e(PRICING['paymentTerms'])}</p><p><strong>Custom portals and integrations:</strong> Written quote after scope review.</p></div>'''
def extras():
 return '<div class="xt-extra-grid">'+''.join(f'<article><h3>{e(x["name"])}</h3><p><strong>{e(x["price"])}</strong></p><p>{e(x["scope"])}</p></article>' for x in PRICING['extras'])+'</div>'
def offers():
 return [{'@type':'Offer','name':p['name'],'description':p['scope']+'. Two revision rounds; client supplies content. Target '+p['delivery']+' after deposit, content and access. Domain, hosting, extras and provider fees are separate.','price':str(p['priceAmount']),'priceCurrency':'KES','url':'https://www.xclusivetech.co.ke/pricing#packages','priceSpecification':{'@type':'PriceSpecification','price':str(p['priceAmount']),'priceCurrency':'KES','description':'Base build fee for the defined scope; extra work separately quoted.'}} for p in PACKAGES]
def render_county_pricing(name):
 return '<section id="county-pricing" class="buyer-section"><div class="buyer-container"><h2>Website packages for '+e(name)+'</h2>'+cards()+terms()+'</div></section>'
def render():
 p=ROOT/'pricing.html';s=p.read_text();start=s.index('    <!-- Main Pricing Cards -->') if '    <!-- Main Pricing Cards -->' in s else s.index('    <section id=\"packages\"');end=s.index('    <!-- Global Past Works Banner -->',start)
 s=s[:start]+'''    <section id="packages" class="xt-packages-section"><span id="pricing-table" aria-hidden="true"></span><div class="xt-pricing-container"><h2>Choose the scope that fits your business</h2><p class="xt-pricing-intro">Clear starting build prices, a 50% deposit and separately agreed extras. Each package includes the defined scope below.</p>'''+cards()+terms()+'''<h2>Optional extras, agreed before work starts</h2>'''+extras()+'''</div></section>\n'''+s[end:]
 s=s.replace('Ready in 2–3 Weeks (Landing Pages in 2–3 business days)','Landing pages: 2–3 business days · Other packages: see targets below')
 p.write_text(s)
 p=ROOT/'index.html';s=p.read_text();start=s.index('            <!-- Special Offer: Express Lead-Gen') if '            <!-- Special Offer: Express Lead-Gen' in s else s.index('<div class=\"xt-home-packages\"');end=s.index('    <!-- Awards',start) if '    <!-- Awards' in s[start:] else s.index('    <section',s.index('</section>',start)+10)
 # Retain the section/container boundaries and replace the duplicated promo plus large cards/footer.
 close=s.index('    </section>',start)
 s=s[:start]+'<div class="xt-home-packages">'+cards()+terms()+'</div>\n        </div>\n'+s[close:]
 s=s.replace('Calculate Your Exact Website Cost','Estimate Your Website Budget').replace('your transparent pricing, specific deliverables, and guaranteed turnaround time','your build price, deposit, separate running costs and target turnaround').replace('Your Guaranteed Estimate','Your Website Budget Estimate').replace('Total Investment:','Website Build:').replace('Guaranteed Delivery:','Target Delivery:').replace('Balance on Live Approval (50%):','Build Balance on Approval (50%):')
 s=s.replace('100% Risk Reversal:','Clear payment milestones:').replace('The 50% balance is payable ONLY after you test, inspect, and approve your live website. Zero risk.','The remaining build balance is due after review and approval, before launch or file transfer. Domain, hosting and recurring care are separate.')
 for package in PACKAGES:
  pat=rf'(<label class="estimator-pkg-card[^\"]*" data-pkg="{package["id"]}")[\s\S]*?</label>'
  checked=' checked' if package['id']=='express' else ''
  markup=f'''<label class="estimator-pkg-card{' is-selected' if checked else ''}" data-pkg="{package['id']}" data-price="{package['priceAmount']}" data-time="{package['delivery']}" data-name="{e(package['name'])}"><input type="radio" name="estimator-pkg" value="{package['id']}" class="sr-only"{checked}><span class="font-bold text-gray-900">{e(package['name'])}</span><span class="font-extrabold text-blue-600">KES {package['priceAmount']:,}</span><p class="text-xs text-gray-500 mt-1">{e(package['scope'])}. Target: {e(package['delivery'])}.</p></label>'''
  s,count=re.subn(pat,lambda m:markup,s,count=1);assert count,package['id']
 p.write_text(s)
 # Reuse the approved cards/terms wherever they already appear; no numeric search/replace.
 for name in subprocess.check_output(['git','ls-files','*.html'],cwd=ROOT,text=True).splitlines():
  path=ROOT/name;source=path.read_text()
  if 'xt-package-grid' not in source:continue
  source=re.sub(r'<div class="xt-package-grid">[\s\S]*?</div>',lambda m:cards(),source)
  source=re.sub(r'<div class="xt-pricing-notes">[\s\S]*?</div>',lambda m:terms(),source)
  path.write_text(source)
 # Keep the pricing OfferCatalog aligned with its visible cards.
 path=ROOT/'pricing.html';source=path.read_text()
 def catalog(match):
  data=json.loads(match[1])
  def visit(node):
   if isinstance(node,dict):
    if node.get('@type')=='OfferCatalog':node['itemListElement']=offers()
    else:
     for value in node.values():visit(value)
   elif isinstance(node,list):
    for value in node:visit(value)
  visit(data);return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False,indent=2)+'</script>'
 source=re.sub(r'<script type="application/ld\+json">([\s\S]*?)</script>',catalog,source);path.write_text(source)
 # A tiny generated client config makes the estimator use the same approved source.
 config={'packages':{p['id']:{'name':p['name'],'price':p['priceAmount'],'deposit':p['depositAmount'],'delivery':p['delivery'],'scope':p['scope'],'features':p['features']} for p in PACKAGES},'domainAnnual':1500,'hostingAnnual':3000,'careMonthly':2000}
 (ROOT/'js/pricing-data.js').write_text('/* Generated from content/site-facts.json by scripts/sync_website_pricing.py. */\nwindow.XT_PRICING = '+json.dumps(config,ensure_ascii=False,indent=2)+';\n')
 print('Rendered approved package cards, terms, pricing offers and shared calculator data; review editorial copy when changing the policy.')
if __name__=='__main__':render()
