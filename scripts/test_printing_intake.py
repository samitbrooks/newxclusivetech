"""UI checks only: all uploads and enquiries intercepted, no notifications sent."""
import asyncio,os,json
from playwright.async_api import async_playwright
BASE=os.getenv('XT_TEST_BASE_URL','http://localhost:8766').rstrip('/')
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
  page=await b.new_page(viewport={'width':1440,'height':1000},service_workers='block');errors=[];page.on('pageerror',lambda e:errors.append(str(e)));calls=[];uploads=[]
  await page.route('**/api/leads/artwork',lambda r:(uploads.append(r.request.post_data_buffer),r.fulfill(status=201,content_type='application/json',body='{"success":true,"receipt":"local-test-receipt","name":"design.pdf"}'))[-1])
  async def fail(r):calls.append(r.request.post_data_json);await r.fulfill(status=503,content_type='application/json',body='{"success":false}')
  async def saved(r):calls.append(r.request.post_data_json);await r.fulfill(status=201,content_type='application/json',body='{"success":true,"status":"saved","reference":"XT-20261031-ABCDEF123456"}')
  await page.route('**/api/leads',fail)
  await page.goto(BASE+'/printing',wait_until='domcontentloaded');assert await page.locator('nav').get_by_text('Launch Calculator',exact=True).count()==0;assert await page.locator('nav a[href="#calculator"]').count()==2
  assert await page.locator('.print-product img').count()==4
  for img in await page.locator('.print-product img').all():await img.scroll_into_view_if_needed();await page.wait_for_function('(e)=>e.complete&&e.naturalWidth>0',arg=await img.element_handle())
  assert not await page.locator('#mobile-menu-btn').is_visible()
  await page.locator('[data-print-family="Reports & training materials"]').click();assert await page.locator('#pub-binding').input_value()=='wireo';assert 'Reports & training materials' in await page.locator('#print-spec-summary').inner_text()
  await page.locator('#pub-qty').fill('250');await page.locator('#pub-qty').dispatch_event('input');assert 'Quantity: 250' in await page.locator('#print-spec-summary').inner_text()
  await page.locator('#print-product').select_option(label='Other / help me choose');assert await page.locator('#print-product').input_value()=='Other / help me choose'
  await page.locator('#print-product').select_option(label='Books & publications')
  await page.locator('#print-name').fill('Local printing QA');await page.locator('#print-phone').fill('0700000000')
  await page.locator('#print-artwork').set_input_files({'name':'bad.exe','mimeType':'application/octet-stream','buffer':b'not artwork'});await page.locator('.print-submit').click();assert len(calls)==0;assert 'supported file' in await page.locator('#print-quote-feedback').inner_text()
  await page.locator('#print-artwork').set_input_files({'name':'design.pdf','mimeType':'application/pdf','buffer':b'%PDF-1.4\nLocal UI test only'})
  await page.locator('.print-submit').click();await page.wait_for_function("document.querySelector('#print-quote-feedback').textContent.includes('Your details are still here')")
  assert await page.locator('#print-name').input_value()=='Local printing QA';assert len(uploads)==1;assert calls[0]['artwork_receipt']=='local-test-receipt';assert 'Quantity: 250' in calls[0]['message'];assert await page.locator('.print-submit').is_enabled()
  await page.unroute('**/api/leads');await page.route('**/api/leads',saved);await page.locator('.print-submit').click();await page.wait_for_function("document.querySelector('#print-quote-feedback').textContent.includes('XT-20261031')")
  assert len(uploads)==1;assert calls[0]['client_request_id']==calls[1]['client_request_id']
  await page.set_viewport_size({'width':390,'height':844});await page.reload(wait_until='domcontentloaded');assert await page.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth+1');await page.locator('#mobile-menu-btn').click();await page.wait_for_timeout(200);assert await page.locator('#mobile-menu').is_visible()
  await page.locator('#mobile-menu-btn').click();await page.locator('.print-product').first.screenshot(path='/tmp/printing-product-mobile.png')
  await page.set_viewport_size({'width':1440,'height':1000});await page.goto(BASE+'/printing',wait_until='domcontentloaded');await page.locator('#print-quote').screenshot(path='/tmp/printing-artwork-desktop.png');assert not errors,errors
  print('PASS: navbar link, original mockups, product-to-calculator presets, spec summary, custom product, file validation, upload/quote retry and idempotency, mobile layout/menu; no browser errors or real submissions')
  await b.close()
asyncio.run(main())
