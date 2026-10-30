#!/usr/bin/env python3
"""Render approved buyer information without inventing client results or terms."""
from pathlib import Path
from html import escape as e
import json,re
from normalize_site_assets import normalize_html
ROOT=Path(__file__).resolve().parents[1]
FACTS=json.loads((ROOT/'content/site-facts.json').read_text())
EVIDENCE=json.loads((ROOT/'content/client-evidence.json').read_text())

def section(identifier,title,body):
 return f'<section id="{identifier}" class="buyer-section"><div class="buyer-container"><h2>{title}</h2>{body}</div></section>'

def install(source,identifier,markup,before='</main>'):
 pattern=rf'<section id="{identifier}"[\s\S]*?</section>'
 if re.search(pattern,source):return re.sub(pattern,lambda m:markup,source,count=1)
 if before in source:return source.replace(before,markup+'\n'+before,1)
 # Some legacy landing pages use sections directly under body.
 marker=re.search(r'\n\s*<footer\b',source)
 if marker:return source[:marker.start()]+markup+source[marker.start():]
 raise ValueError('No content insertion point')

def reviewer_cards(reviews):
 return '<div class="buyer-grid">'+''.join(f'<figure class="buyer-card"><blockquote>“{e(r["quote"])}”</blockquote><figcaption><strong>{e(r["name"])}</strong><br>{e(r["role"])} · {e(r["location"])}</figcaption></figure>' for r in reviews)+'</div>'

LEAD=section('your-project-lead','Know who will build your website', '''<div class="buyer-lead"><img src="/assets/images/samuel-headshot.png" alt="Samuel Kidemi, lead designer and engineer at Xclusive Tech" width="160" height="160" loading="lazy" decoding="async"><div><h3>Samuel Kidemi</h3><p>Lead designer and engineer, Xclusive Tech. Speak directly about the features, budget and launch schedule your project needs. Our Nairobi-based team serves businesses remotely across Kenya.</p><p><a href="/founder">Meet Samuel and see his work</a> · <a href="tel:+254722753819">Call +254 722 753 819</a></p></div></div>''')
PACKAGES=[('Express landing page','KES 15,000','3–5 business days','One focused page with five conversion sections, a WhatsApp contact route and enquiry form.'),('Starter Site','KES 25,000–45,500','2–3 weeks','Up to five pages, custom mobile-first design, on-page SEO, contact form and WhatsApp integration. One month of launch support.'),('Business Growth','KES 49,000–62,000','3–5 weeks','Up to 15 pages, content management for news or a blog, on-page SEO and analytics setup. Three months of launch support.'),('E-commerce Pro','KES 72,000–85,000','5–7 weeks','Product catalogue, customer accounts, stock management and M-Pesa checkout integration. Six months of priority launch support.')]
PACKAGE_HTML='<div class="buyer-grid">'+''.join(f'<article class="buyer-card"><h3>{e(n)}</h3><p><strong>{e(p)}</strong> · {e(t)}</p><p>{e(d)}</p></article>' for n,p,t,d in PACKAGES)+'</div><p>These scopes are starting points. The signed-off quote specifies integrations, included revision rounds, content responsibilities and acceptance criteria. Domain registration, hosting, payment-provider fees and third-party licences are separate unless your quote includes them.</p>'
COSTS='''<div class="buyer-grid"><article class="buyer-card"><h3>Build cost</h3><p>One-off project fee from KES 15,000. Your written quote fixes the agreed scope and payment milestones.</p></article><article class="buyer-card"><h3>Domain and hosting</h3><p>.co.ke registration starts at KES 1,500/year; .com from KES 1,800/year. Hosting is quoted separately. Ask for both the first-year price and renewal price.</p></article><article class="buyer-card"><h3>Ongoing support</h3><p>The optional care plan starts at KES 2,000/month and covers four hours of support and updates per month. Confirm the tasks included in your agreement.</p></article></div>
<form class="ownership-calculator buyer-card" aria-label="Estimate first-year website costs"><h3>Estimate your first-year budget</h3><p>Enter the figures from your quote. This estimate is not a binding quote; any unentered cost remains excluded.</p><div class="buyer-fields"><label>Build fee (KES)<input name="build" type="number" min="0" value="15000" required></label><label>Annual domain cost (KES)<input name="domain" type="number" min="0" value="1500" required></label><label>Annual hosting quote (KES)<input name="hosting" type="number" min="0" placeholder="Enter your hosting quote"></label><label>Monthly care plan (KES, optional)<input name="care" type="number" min="0" value="0"></label></div><p><output aria-live="polite">Enter the costs above to calculate your estimate.</output></p><p class="buyer-note">Payment fees, extra licences, content production and any other unlisted costs are excluded. Without JavaScript, add build + annual domain + annual hosting + 12 × monthly care.</p></form>'''
PROCESS='''<ol class="buyer-steps"><li><strong>Scope and written quote.</strong> Agree pages, integrations, content, timetable, revision rounds and payment milestones.</li><li><strong>Deposit and project inputs.</strong> The existing terms require a 50% deposit before work begins. Supply approved content, brand assets and any required account access.</li><li><strong>Design review.</strong> Review the proposed layout and consolidate feedback within the agreed revision rounds.</li><li><strong>Development and testing.</strong> Check mobile layouts, forms, content and any payment integrations against the agreed acceptance criteria.</li><li><strong>Approval and handover.</strong> Review the completed work, settle the remaining balance under the agreed terms, then launch or receive the files and access details.</li></ol><p>Typical delivery is 3–5 business days for a landing page, 2–3 weeks for Starter, 3–5 weeks for Growth and 5–7 weeks for e-commerce. The confirmed schedule depends on scope, content readiness and approval turnaround.</p>'''
SUPPORT='''<div class="buyer-grid"><article class="buyer-card"><h3>Included launch support</h3><p>Starter includes one month, Growth three months and e-commerce six months of support. Your quote sets the scope of fixes and assistance included.</p></article><article class="buyer-card"><h3>Care after launch</h3><p>Choose an optional care plan from KES 2,000/month for four hours of updates and support. Request a separate quote for larger changes or new functionality.</p></article><article class="buyer-card"><h3>Ownership and access</h3><p>On full payment, receive the agreed project files and access details. Third-party software, fonts, stock assets and reusable tools remain subject to their licences and the agreed terms.</p></article></div>'''
TERMS='''<ul class="buyer-list"><li><strong>Payment:</strong> 50% deposit before work; the remaining balance is due on delivery, before publication or file transfer, under the current terms.</li><li><strong>Revisions:</strong> Included rounds are specified in the quote. Changes outside the agreed scope are quoted separately.</li><li><strong>Cancellation:</strong> Work completed is invoiced; the deposit is non-refundable once design work begins, as set out in the existing terms.</li><li><strong>Ownership:</strong> The project agreement distinguishes your delivered work from third-party licences and reusable tools.</li></ul><p><a href="/terms">Read the full terms</a> before accepting a quote. Ask us to clarify anything your project agreement needs to cover.</p>'''
FAQS=[('Can you redesign my existing website?','Yes. Start with a review of your current pages, domain, forms and integrations. We agree what will be retained, replaced and redirected before migration.'),('Can I keep my domain and hosting?','Bring your existing details to the project review. We confirm access, compatibility and any migration work before recommending changes; you do not have to buy a new domain just to discuss a redesign.'),('What is needed for M-Pesa integration?','We review your merchant account, the payment flow and the appropriate API access with you. Merchant approval and payment-provider fees are separate from the website build.'),('Who supplies the words and photographs?','Your quote states whether you provide approved content and licensed images or whether content production is included as a separate service. Content readiness affects the launch schedule.'),('Can I update the website after launch?','For projects that include a CMS, handover covers the agreed editing workflow. Confirm any training, maintenance or ongoing editing requirement in the scope.'),('Do you guarantee first-page rankings or sales?','No. On-page SEO helps search engines access and understand a site, but indexing, rankings, enquiries and sales depend on factors beyond a website build. We agree measurable work and review actual performance.'),('How do I compare two website quotes?','Compare page count, integrations, revision rounds, content responsibilities, domain and hosting renewals, support, ownership and acceptance criteria—not only the headline price.'),('What happens if I want more features later?','Agree a separate scope and quote before extra work begins. Ask whether an existing upgrade offer applies to your project; do not assume that every new feature is included in the original fee.')]
FAQ_HTML='<div class="buyer-faqs">'+''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in FAQS)+'</div>'


def build():
 # Existing public reviews are replaced by the exact owner-approved text, without fabricated star ratings.
 p=ROOT/'index.html';s=p.read_text();review_section=section('approved-client-feedback','Client feedback',reviewer_cards(EVIDENCE['reviews'])+'<p><a href="'+e(FACTS['company']['googleBusinessProfile'],quote=True)+'" target="_blank" rel="noopener noreferrer">Visit our Google Business Profile for independent reviews</a></p>')
 if '<!-- Client Testimonials & Verifiable Reviews -->' in s:s=re.sub(r'<!-- Client Testimonials & Verifiable Reviews -->[\s\S]*?</section>',lambda m:review_section,s,count=1)
 else:s=install(s,'approved-client-feedback',review_section)
 s=install(s,'your-project-lead',LEAD);p.write_text(s)
 for name in ['pricing.html','services.html','contact.html']:
  p=ROOT/name;s=p.read_text();s=install(s,'your-project-lead',LEAD)
  guide=section('plan-your-project','Plan your website before requesting a quote','<p>Understand the scope, launch process, ongoing costs and support before you choose a package.</p><p><a href="/project-guide">Read the website project guide</a> · <a href="/project-guide#ownership-costs">Estimate first-year costs</a> · <a href="/project-guide#project-questions">Common project questions</a></p>')
  s=install(s,'plan-your-project',guide)
  if name=='pricing.html':
   for ident,title,body in [('ownership-costs','Budget for the full cost of your website',COSTS),('project-terms','Know the terms before you commit',TERMS)]:s=install(s,ident,section(ident,title,body))
  p.write_text(s)
 # Build a focused guide with an independent title, canonical and WebPage schema.
 source=(ROOT/'pricing.html').read_text();head,rest=source.split('<body',1);body='<body'+rest
 header=body[:body.index('<main')]
 footer=body[body.index('</main>')+len('</main>'):]
 title='Website Project Guide: Costs, Process & Support | Xclusive Tech';description='Plan your website with clear package scopes, first-year costs, delivery steps, support, ownership and answers to common buying questions.'
 head=re.sub(r'<script type="application/ld\+json">[\s\S]*?</script>','',head)
 head=re.sub(r'<title>[\s\S]*?</title>',f'<title>{title}</title>',head)
 head=re.sub(r'(<meta name="keywords" content=")[^"]*',lambda m:m[1]+'website project planning, website ownership costs, website delivery process, website support Kenya',head)
 head=re.sub(r'(<meta (?:name|property)="(?:description|og:description|twitter:description)" content=")[^"]*',lambda m:m[1]+description,head)
 head=re.sub(r'(<meta (?:property|name)="(?:og:title|twitter:title)" content=")[^"]*',lambda m:m[1]+title,head)
 head=head.replace('https://www.xclusivetech.co.ke/pricing','https://www.xclusivetech.co.ke/project-guide')
 schema={'@context':'https://schema.org','@type':'WebPage','@id':'https://www.xclusivetech.co.ke/project-guide#webpage','url':'https://www.xclusivetech.co.ke/project-guide','name':title,'description':description,'about':{'@id':'https://www.xclusivetech.co.ke/#organization'}}
 head=head.replace('</head>','<script type="application/ld+json">'+json.dumps(schema)+'</script>\n</head>')
 header=header.replace('nav-link active','nav-link').replace(' aria-current="page"','')
 hero='<main id="main-content"><section class="buyer-section buyer-guide-hero"><div class="buyer-container"><p><a href="/">Home</a> / Website project guide</p><h1>Know what you are buying before you build</h1><p>'+description+'</p><nav class="buyer-jump" aria-label="Guide sections"><a href="#package-deliverables">Deliverables</a><a href="#ownership-costs">Costs</a><a href="#delivery-process">Process</a><a href="#support-and-ownership">Support</a><a href="#project-terms">Terms</a><a href="#project-questions">Questions</a></nav></div></section>'
 guide=hero+''.join(section(i,t,b) for i,t,b in [('package-deliverables','Choose the right scope',PACKAGE_HTML),('ownership-costs','Understand the first-year and ongoing costs',COSTS),('delivery-process','From brief to handover',PROCESS),('support-and-ownership','What happens after launch?',SUPPORT),('project-terms','Agree the terms before work starts',TERMS),('project-questions','Questions to ask before choosing a developer',FAQ_HTML)])+LEAD+section('ready-for-a-quote','Get a written scope and quote','<p>Tell us what your business does, what customers need to do on the site and your preferred launch date.</p><a class="nav-cta-btn" href="/contact">Get a written quote</a>')+'</main>'
 (ROOT/'project-guide.html').write_text(normalize_html(head+header+guide+footer))
 # Add inspectable delivery notes without making the simple portfolio cards wordier.
 notes=''
 for project in EVIDENCE['projects']:
  notes+=f'<details><summary>{e(project["name"])} — {e(project["focus"])}</summary><p>{e(project["implementation"])}</p><p>{e(project["resultEvidence"])}</p><p><a href="{e(project["url"],quote=True)}" target="_blank" rel="noopener noreferrer">Inspect the live website</a></p></details>'
 p=ROOT/'portfolio.html';source=p.read_text();source=install(source,'project-evidence',section('project-evidence','Project implementation notes','<p>Inspect the features relevant to your business. These notes describe delivered presentation and enquiry paths, not measured lead or revenue increases.</p><div class="buyer-faqs">'+notes+'</div><p><a href="/project-guide">See how scope, testing and handover work</a></p>'));p.write_text(source)
 # A source-backed local project reference, not a claim of a branch office.
 p=ROOT/'locations/web-design-kisumu.html';s=p.read_text();s=install(s,'related-kisumu-work',section('related-kisumu-work','Related education website work','<p>Our portfolio includes the <a href="https://gluksdbs.org/" target="_blank" rel="noopener noreferrer">GLUK School of Dentistry &amp; Biomedical Sciences website</a>. The school’s public website identifies its main campus in Kisumu. Explore its programme information and prospectus enquiry route, then <a href="/portfolio">compare other work in our portfolio</a>.</p>'));p.write_text(s)
 # Only associate reviews with locations explicitly supplied by the owner.
 for county in ['Nairobi','Uasin Gishu','Kiambu']:
  slug=county.lower().replace(' ','-');p=ROOT/f'locations/web-design-{slug}.html';s=p.read_text()
  reviews=[r for r in EVIDENCE['reviews'] if r['county']==county]
  s=install(s,'local-client-feedback',section('local-client-feedback',f'Client feedback from {e(county)}',reviewer_cards(reviews)));p.write_text(s)
 print('Rendered buyer scopes, costs, lead identity, approved reviews, project evidence and the project guide')

if __name__=='__main__':build()
