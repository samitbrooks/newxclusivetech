"""Approved pricing/scope consistency and real calculator arithmetic. No enquiries are submitted."""
import asyncio,json,re,os,subprocess
from pathlib import Path
from urllib.parse import unquote_plus
from playwright.async_api import async_playwright
BASE=os.getenv('XT_TEST_BASE_URL','http://localhost:8766').rstrip('/')
facts=json.loads(Path('content/site-facts.json').read_text())['pricing'];packages=[facts['launchOffer'],*facts['packages'][:3]]
async def main():
 # Protect independent service prices: printing and social media were not repriced.
 baseline=subprocess.check_output(['git','show','HEAD:services.html'],text=True)
 old=re.search(r'<section id="social-media-management"[\s\S]*?</section>',baseline)[0]
 new=re.search(r'<section id="social-media-management"[\s\S]*?</section>',Path('services.html').read_text())[0];assert old==new
 assert subprocess.check_output(['git','show','HEAD:printing.html'],text=True)==Path('printing.html').read_text()
 counties=list(Path('locations').glob('web-design-*.html'));assert len(counties)==47
 for p in counties:
  src=p.read_text();assert src.count('class="xt-package-card"')==4,p
  for package in packages:assert f'Start with KES {package["depositAmount"]:,}' in src,p
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome');page=await b.new_page(viewport={'width':1440,'height':1000},service_workers='block');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto(BASE+'/',wait_until='domcontentloaded')
  for package in packages:
   await page.locator(f'[data-pkg="{package["id"]}"]').click()
   assert await page.locator('#estimator-total').inner_text()==f'KES {package["priceAmount"]:,}'
   assert await page.locator('#estimator-deposit').inner_text()==f'KES {package["depositAmount"]:,}'
   assert await page.locator('#estimator-timeline').inner_text()==package['delivery']
   msg=unquote_plus(await page.locator('#estimator-whatsapp-btn').get_attribute('href'));assert package['delivery'] in msg;assert f'Build deposit (50%): KES {package["depositAmount"]:,}' in msg
  await page.locator('[data-pkg="express"]').click()
  for field in ['addon-domain','addon-hosting','addon-maintenance']:await page.locator('#'+field).check()
  assert await page.locator('#estimator-total').inner_text()=='KES 10,000'
  assert await page.locator('#estimator-deposit').inner_text()=='KES 5,000'
  assert await page.locator('#estimator-balance').inner_text()=='KES 5,000'
  assert await page.locator('#estimator-annual').inner_text()=='KES 4,500/year selected'
  assert await page.locator('#estimator-care').inner_text()=='KES 2,000/month'
  assert await page.locator('#estimator-due-now').inner_text()=='KES 9,500'
  assert await page.locator('#estimator-first-year').inner_text()=='KES 38,500'
  await page.goto(BASE+'/pricing',wait_until='domcontentloaded');assert await page.locator('#packages .xt-package-card').count()==4;assert await page.locator('#pricing-table table').count()==0
  assert 'KES 25,000' in await page.locator('[data-package=ecommerce] .xt-package-deposit').inner_text()
  # Structured offers agree with visible cards, not obsolete ranges.
  schemas=await page.locator('script[type="application/ld+json"]').all_text_contents();data=[json.loads(s) for s in schemas]
  def offers(x):
   if isinstance(x,dict):
    if x.get('@type')=='OfferCatalog':return x['itemListElement']
    for v in x.values():
     found=offers(v)
     if found:return found
   elif isinstance(x,list):
    for v in x:
     found=offers(v)
     if found:return found
  assert [int(x['price']) for x in offers(data)]==[10000,20000,35000,50000]
  await page.locator('#packages').screenshot(path='/tmp/approved-pricing-desktop.png')
  for width in [390,768,1440]:
   await page.set_viewport_size({'width':width,'height':900})
   for route in ['/pricing','/','/locations/web-design-bungoma','/blog/how-much-does-a-website-cost-in-kenya']:
    await page.goto(BASE+route,wait_until='domcontentloaded');assert await page.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth+1'),(width,route)
  assert not errors,errors
  print('PASS: 4 packages/50% deposits/targets, annual and monthly arithmetic, WhatsApp amounts, matching structured offers, all 47 county packages, responsive layouts; printing and social-media prices unchanged')
  await b.close()
asyncio.run(main())
