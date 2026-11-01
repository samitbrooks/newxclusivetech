"""Contact-link checks; no emails, calls, WhatsApp messages or leads are sent."""
import asyncio,sys,re,os
from pathlib import Path
sys.path.insert(0,'scripts')
from link_site_contacts import Contacts
from playwright.async_api import async_playwright
# Parser edits preserve JSON-LD, existing links and non-contact text.
source='<p>WhatsApp <strong>+254 722 753 819</strong> or email hello@xclusivetech.co.ke.</p><script>{"email":"hello@xclusivetech.co.ke"}</script><a href="tel:+254722753819">+254722753819</a>'
p=Contacts(source);p.feed(source);out=p.result();assert 'href="https://wa.me/254722753819"' in out and out.count('mailto:')==1 and '<script>{"email":"hello@xclusivetech.co.ke"}</script>' in out
p2=Contacts(out);p2.feed(out);assert not p2.edits
BASE=os.getenv("XT_TEST_BASE_URL","http://localhost:8766").rstrip("/")
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');page=await b.new_page(viewport={'width':1440,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto(BASE+'/printing');assert await page.locator('#print-project-guide a[href="mailto:hello@xclusivetech.co.ke"]').count()==1
  assert await page.locator('#print-project-guide a[href="https://wa.me/254722753819"]').count()==1
  await page.evaluate('''()=>{const p=document.createElement('p');p.id='contact-qa';p.textContent='Please call +254 722 753 819 or use WhatsApp. Email hello@xclusivetech.co.ke.';document.body.append(p)}''')
  await page.wait_for_function("document.querySelectorAll('#contact-qa a').length===3")
  links=await page.locator('#contact-qa a').evaluate_all('(els)=>els.map(e=>e.getAttribute("href"))');assert links==['tel:+254722753819','https://wa.me/254722753819','mailto:hello@xclusivetech.co.ke'],links
  await page.evaluate("document.getElementById('contact-qa').textContent='WhatsApp +254 722 753 819'")
  await page.wait_for_function("document.querySelector('#contact-qa a')?.href==='https://wa.me/254722753819'")
  assert await page.locator('a a').count()==0
  for width in [390,1440]:
   await page.set_viewport_size({'width':width,'height':1000});assert await page.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth+1')
  await page.goto(BASE+'/privacy');assert await page.get_by_role('link',name='+254722753819',exact=True).count()>=1
  assert not errors,errors;await b.close();print('PASS: static links, safe/idempotent markup, dynamic email/call/WhatsApp feedback, no nested anchors, mobile width and no browser errors')
asyncio.run(main())
