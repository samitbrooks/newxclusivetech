import asyncio,json,re
from pathlib import Path
from playwright.async_api import async_playwright
import os
BASE=os.environ.get('XT_TEST_BASE_URL','http://localhost:8766/').rstrip('/')+'/'
ARTIFACTS=Path('/tmp/xclusive-buyer-tests');ARTIFACTS.mkdir(parents=True,exist_ok=True)
async def main():
 async with async_playwright() as p:
  chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
  b=await p.chromium.launch(**({'executable_path':str(chrome)} if chrome.exists() else {}))
  page=await b.new_page(viewport={'width':1440,'height':1000},service_workers='block');errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
  await page.goto(BASE+'project-guide',wait_until='domcontentloaded')
  form=page.locator('.ownership-calculator');assert await form.count()==1
  await form.locator('[name="hosting"]').fill('3000');await form.locator('[name="care"]').fill('2000')
  assert '43,500' in await form.locator('output').inner_text()
  assert await page.locator('.buyer-faqs details').count()==8
  height=await page.locator('body').evaluate('(e)=>e.scrollHeight')
  for offset in range(0,height,800):
   await page.evaluate('(y)=>window.scrollTo(0,y)',offset);await page.wait_for_timeout(650)
  await page.evaluate('window.scrollTo(0,0)');await page.wait_for_timeout(200)
  close=page.locator('#xt-exit-close-btn')
  if await close.count() and await close.is_visible():await close.click();await page.wait_for_timeout(250)
  await page.screenshot(path=str(ARTIFACTS/'project-guide-desktop.png'),full_page=True)
  assert await page.evaluate('window.XT_MEASUREMENT_CONFIG.ga4MeasurementId') is None
  assert not await page.locator('script[src*="googletagmanager.com"]').count()
  await page.set_viewport_size({'width':390,'height':844})
  await page.goto(BASE+'locations/web-design-bungoma',wait_until='domcontentloaded')
  quote=page.locator('#county-quote-form');assert await quote.locator('[required]').count()==2
  assert await page.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth+1')
  await quote.locator('[name="name"]').fill('Local QA');await quote.locator('[name="phone"]').fill('0712345678')
  await page.route('https://formsubmit.co/**',lambda route:route.fulfill(status=200,content_type='text/html',body='<p>Local interception only</p>'))
  async with page.expect_request('https://formsubmit.co/**') as outgoing:await quote.locator('button').click()
  sent=await outgoing.value;assert 'Bungoma' in sent.post_data
  await page.goto(BASE+'contact?success=true',wait_until='domcontentloaded')
  await page.wait_for_timeout(100)
  assert await page.evaluate('dataLayer.some(e=>e.event==="lead_provider_return")')
  await page.reload(wait_until='domcontentloaded')
  assert not await page.evaluate('dataLayer.some(e=>e.event==="lead_provider_return")')
  # Explicit negative and positive provider responses: do not send real enquiries.
  await page.set_viewport_size({'width':1440,'height':1000})
  await page.goto(BASE+'contact',wait_until='domcontentloaded');await page.evaluate('window.openSmartExitIntent()')
  await page.locator('#xt-exit-name').fill('Local QA');await page.locator('#xt-exit-phone').fill('0712345678')
  terms=page.locator('#xt-exit-terms')
  if await terms.count():await terms.check()
  await page.route('https://formsubmit.co/ajax/**',lambda route:route.fulfill(status=500,content_type='application/json',body='{"success":false}'))
  await page.locator('#xt-exit-submit-btn').click();await page.locator('#xt-exit-feedback').wait_for(state='visible')
  assert not await page.locator('#xt-exit-success').is_visible()
  assert await page.locator('#xt-exit-submit-btn').is_enabled()
  assert not await page.evaluate('dataLayer.some(e=>e.event==="lead_provider_accepted")')
  await page.unroute('https://formsubmit.co/ajax/**')
  await page.route('https://formsubmit.co/ajax/**',lambda route:route.fulfill(status=200,content_type='application/json',body='{"success":"true"}'))
  await page.locator('#xt-exit-submit-btn').click();await page.locator('#xt-exit-success').wait_for(state='visible')
  assert await page.evaluate('dataLayer.filter(e=>e.event==="lead_provider_accepted").length')==1
  # A/B wiring is tested with a local analytics stub; no real property is invented.
  await page.route('**/js/measurement-config.js*',lambda route:route.fulfill(content_type='application/javascript',body='window.__qaEvents=[];window.gtag=(...args)=>__qaEvents.push(args);window.XT_MEASUREMENT_CONFIG={ga4MeasurementId:null,ctaExperimentEnabled:true,ctaExperimentId:"qa-county-label"};'))
  await page.goto(BASE+'locations/web-design-bungoma',wait_until='domcontentloaded')
  label=page.locator('[data-quote-label]');variant=await label.inner_text()
  assert variant in ['Get a written quote on WhatsApp','Discuss my website on WhatsApp']
  await page.reload(wait_until='domcontentloaded');assert await label.inner_text()==variant
  assert await page.evaluate('__qaEvents.some(e=>e[1]==="quote_cta_exposure")')
  await page.unroute('**/js/measurement-config.js*')
  await page.goto(BASE+'portfolio',wait_until='domcontentloaded')
  assert await page.locator('[class~="group"][class~="overflow-hidden"]').count()==61
  pata=page.locator('a[href="https://patamaps.com"]');assert await pata.count()==1;assert 'Problem' not in await pata.inner_text()
  assert await page.locator('source[srcset*="-400.webp"]').count()==61
  await page.goto(BASE,wait_until='domcontentloaded')
  await page.locator('[data-pkg="growth"]').click()
  assert '3–5 weeks' in await page.locator('#estimator-timeline').inner_text()
  await page.locator('[data-pkg="ecommerce"]').click()
  assert '5–7 weeks' in await page.locator('#estimator-timeline').inner_text()
  assert '5–7 weeks' in __import__('urllib.parse',fromlist=['unquote']).unquote(await page.locator('#estimator-whatsapp-btn').get_attribute('href'))
  assert not errors,errors
  print('PASS: budget arithmetic, buyer FAQs, mobile layout, two-field native quotes, matching/deduplicated provider returns, failed-submission retry, positive acknowledgement event, stable A/B variant with local stub, 61 responsive portfolio cards and simple PataMaps; no browser errors')
  await b.close()
asyncio.run(main())
