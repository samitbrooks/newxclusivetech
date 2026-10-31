"""Browser checks intercept all submissions; never send customer enquiries."""
import asyncio,json,os
from playwright.async_api import async_playwright
BASE=os.getenv('XT_TEST_BASE_URL','http://localhost:8766').rstrip('/')
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
  page=await b.new_page(viewport={'width':390,'height':844},service_workers='block');errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  requests=[]
  async def fail(route):
   requests.append(route.request.post_data_json)
   await route.fulfill(status=503,content_type='application/json',body='{"success":false}')
  async def saved(route):
   requests.append(route.request.post_data_json)
   await route.fulfill(status=201,content_type='application/json',body='{"success":true,"status":"saved","reference":"XT-20261031-ABCDEF123456"}')
  await page.route('**/api/leads',fail)
  await page.goto(BASE+'/locations/web-design-bungoma',wait_until='domcontentloaded')
  f=page.locator('#county-quote-form');await f.locator('[name=name]').fill('Local QA');await f.locator('[name=phone]').fill('0700000000');await f.locator('button').click()
  await page.wait_for_function("document.querySelector('[data-lead-feedback]').textContent.includes('could not confirm')")
  assert await f.locator('[name=name]').input_value()=='Local QA';assert await f.locator('button').is_enabled()
  await page.unroute('**/api/leads');await page.route('**/api/leads',saved);await f.locator('button').click()
  await page.wait_for_function("document.querySelector('[data-lead-feedback]').textContent.includes('XT-')")
  assert requests[0]['client_request_id']==requests[1]['client_request_id'];assert requests[1]['county']=='Bungoma'
  assert await page.evaluate('dataLayer.some(e=>e.event==="lead_saved")')
  await page.goto(BASE+'/contact',wait_until='domcontentloaded');await page.evaluate('openSmartExitIntent()');await page.locator('#xt-exit-name').fill('Local QA');await page.locator('#xt-exit-phone').fill('0700000000')
  terms=page.locator('#xt-exit-terms')
  if await terms.count():await terms.check()
  await page.locator('#xt-exit-submit-btn').click();await page.locator('#xt-exit-success').wait_for(state='visible');assert 'XT-20261031' in await page.locator('.xt-success-desc').inner_text()
  await page.goto(BASE+'/contact',wait_until='domcontentloaded');f=page.locator('#contact-form');await f.locator('[name=name]').fill('Local QA');await f.locator('[name=phone]').fill('0700000000');await f.locator('button[type=submit]').click();await page.wait_for_function("document.querySelector('[data-lead-feedback]').textContent.includes('XT-')")
  newsletter=page.locator('#newsletter-form');await newsletter.locator('[name=email]').fill('owner@example.test');await newsletter.locator('[type=submit]').click();await page.wait_for_function("document.querySelector('#newsletter-form [data-lead-feedback]').textContent.includes('XT-')")
  assert requests[-1]['form_id']=='newsletter-form'
  assert not errors,errors
  await page.goto(BASE+'/printing',wait_until='domcontentloaded');assert await page.locator('h1').count()==1
  total=await page.locator('#grand-total').inner_text();await page.locator('#pub-qty').fill('200');await page.locator('#pub-qty').dispatch_event('input');assert await page.locator('#grand-total').inner_text()!=total
  await page.locator('#pub-pages').fill('9');await page.locator('#pub-pages').dispatch_event('input');assert await page.locator('#btn-print-proforma').is_disabled();assert await page.locator('#btn-whatsapp-quote').get_attribute('href') is None
  await page.locator('#pub-pages').fill('52');await page.locator('#pub-pages').dispatch_event('input');assert await page.locator('#pub-binding').input_value()=='perfect';assert await page.locator('#btn-print-proforma').is_enabled()
  assert await page.locator('body').evaluate('(e)=>e.scrollWidth <= innerWidth+1')
  await page.locator('#btn-print-proforma').click();await page.locator('#proforma-modal').wait_for(state='visible');await page.locator('#close-proforma').click()
  await page.set_viewport_size({'width':1440,'height':1000});await page.goto(BASE+'/printing',wait_until='domcontentloaded');await page.screenshot(path='/tmp/printing-desktop.png',full_page=True)
  assert not errors,errors
  print('PASS: county/contact/smart forms, failure preserves fields, stable retry ID, saved reference, accurate events; printing estimates, invalid-input guards, binding threshold, mobile width and proforma; no browser errors.')
  await b.close()
asyncio.run(main())
