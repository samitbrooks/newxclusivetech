#!/usr/bin/env python3
"""County buying guidance and short native enquiry forms."""
from html import escape as e
from pathlib import Path
import re
from implement_buyer_improvements import section,install,LEAD
from normalize_site_assets import normalize_html
PROFILES=[
 (('tourism','safari','hotel','resort','hospitality','beach','holiday'), 'Tourism and accommodation', 'Present rooms, itineraries or experiences with clear availability and cancellation information. Agree whether enquiries, booking requests or a paid reservation flow are needed.', '/services#ecommerce'),
 (('agri','farm','livestock','dairy','produce','horticulture','tea','sugar','coffee','irrigation'), 'Agriculture and produce suppliers', 'Show product specifications, seasonal availability, quantities and delivery coverage. Collect the buyer’s required volume and destination in a wholesale enquiry.', '/solutions#industries'),
 (('logistic','port','transport','trade','border','cargo','freight'), 'Trade, transport and distribution', 'Explain routes and service areas, required shipment details and the quotation process. Publish capability information buyers can check before making contact.', '/services'),
 (('manufactur','industrial','textile','quarry','cement','contract','construction','mineral'), 'Manufacturing and contractor websites', 'Organise capabilities, product specifications and permitted project photographs. Link to current company documents and collect structured requests for quotation.', '/portfolio'),
 (('health','hospital','medical','clinic'), 'Healthcare providers', 'Explain services, opening hours and appointment options. Agree a suitable appointment workflow and keep sensitive health information out of public enquiry forms.', '/services'),
 (('school','educat','universit','training'), 'Schools and training providers', 'Make programmes, entry requirements, fee information and admission dates easy to find. Provide accessible downloads and a prospectus or admissions enquiry route.', '/portfolio#healthcare-wellness-medical-education'),
 (('retail','shop','commerce','market'), 'Retail and online catalogues', 'Create clear categories, product information, delivery costs and returns information. Choose enquiry checkout or online payment according to the actual sales process.', '/services#ecommerce'),
 (('ngo','conservation','community','aid'), 'Community and conservation organisations', 'Describe programmes with dated evidence, named contacts and accessible reports. Confirm consent before publishing beneficiary photographs or personal stories.', '/portfolio#ngos-development-community'),
 (('finance','insurance','legal','professional','bank'), 'Professional services', 'Explain specialisations, who the service is for, the enquiry process and the information needed to assess a project. Use verifiable credentials and approved case examples.', '/services')
]

def improve_county_conversion(source,c):
 name=c['name'];focus=c['economic_focus'].lower()
 if name!='Bungoma':
  selected=[]
  for keywords,title,body,href in PROFILES:
   hits=[focus.find(k) for k in keywords if k in focus]
   if hits:selected.append((min(hits),title,body,href))
  selected.sort(key=lambda x:x[0]);selected=selected[:3]
  while len(selected)<3:
   fallback=[('Business service information','Show what you offer, the towns you serve and a clear path to a quote or appointment.','/services'),('Launch planning','Prepare approved content, project priorities and account access so the written scope and delivery schedule can be agreed.','/project-guide')][len(selected)%2]
   selected.append((100,*fallback))
  cards=''.join(f'<article class="county-brief-card"><h3>{e(title)}</h3><p>{e(body)}</p><p><a href="{href}">Explore the relevant scope</a></p></article>' for _,title,body,href in selected)
  source=re.sub(r'(<div class="county-brief-grid">)[\s\S]*?(</div><div class="county-brief-next">)',lambda m:m[1]+cards+m[2],source,count=1)
 form=f'''<p>Leave your name and phone number. Project notes are optional; we can discuss the scope together.</p><form id="county-quote-form" data-lead-form="true" data-county="{e(name,quote=True)}" action="https://formsubmit.co/hello@xclusivetech.co.ke" method="POST" class="buyer-quote-form"><input type="hidden" name="_subject" value="Website quote enquiry — {e(name,quote=True)} County"><input type="hidden" name="_next" value="https://www.xclusivetech.co.ke/contact?success=true"><input type="hidden" name="_captcha" value="false"><input type="hidden" name="county" value="{e(name,quote=True)}"><input name="_honey" type="text" tabindex="-1" hidden><div class="buyer-fields"><label>Your name<input name="name" autocomplete="name" required maxlength="100"></label><label>Phone / WhatsApp<input name="phone" type="tel" autocomplete="tel" required maxlength="40"></label></div><label>Project notes (optional)<textarea name="message" rows="3" maxlength="1500" placeholder="What should the website help your customers do?"></textarea></label><p><button class="nav-cta-btn" type="submit">Request a written quote</button></p><p class="buyer-note">We use these details to respond to your enquiry. <a href="/privacy">Privacy policy</a>. Prefer a call? <a href="tel:+254722753819">+254 722 753 819</a>.</p></form>'''
 source=install(source,'county-quick-quote',section('county-quick-quote',f'Get a website quote for {e(name)}',form))
 source=install(source,'your-project-lead',LEAD)
 guide=section('county-buying-questions',f'Before you choose a developer in {e(name)}','''<details><summary>Can I redesign the site and keep my existing domain?</summary><p>Start with a review of the current site, domain access and integrations. Agree which pages and URLs will be retained or redirected before moving anything.</p></details><details><summary>What happens after the website launches?</summary><p>Your quote sets the included launch support and handover. The optional care plan starts at KES 2,000/month; larger features are scoped separately. <a href="/project-guide#support-and-ownership">Compare support and ownership details</a>.</p></details><p><a href="/project-guide">Read the full project guide</a> · <a href="/project-guide#project-terms">Check deposit, revision and cancellation terms</a></p>''')
 source=install(source,'county-buying-questions',guide)
 # Mark the primary quote label for a controlled experiment once reporting is configured.
 source=re.sub(r'(<a\b[^>]*class="[^"]*inline-flex[^"]*"[^>]*>\s*)<span>Get a Free Quote on WhatsApp</span>',r'\1<span data-quote-label="county-primary">Get a written quote on WhatsApp</span>',source,count=1)
 return normalize_html(source)

if __name__=='__main__':
 from generate_county_pages import COUNTIES
 for c in COUNTIES:
  p=Path('locations')/(c['slug']+'.html');p.write_text(improve_county_conversion(p.read_text(),c))
 print('Updated buying guidance, two-required-field quote forms and project-lead profiles for all 47 counties')
