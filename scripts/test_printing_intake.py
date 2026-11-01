"""Printing UI checks: all uploads/enquiries intercepted; no client notifications sent."""
import asyncio,os,json,xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote
from playwright.async_api import async_playwright
BASE=os.getenv('XT_TEST_BASE_URL','http://localhost:8766').rstrip('/')
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
  page=await b.new_page(viewport={'width':1440,'height':1000},service_workers='block');errors=[];page.on('pageerror',lambda e:errors.append(str(e)));calls=[];uploads=[]
  await page.route('**/api/leads/artwork',lambda r:(uploads.append(r.request.post_data_buffer),r.fulfill(status=201,content_type='application/json',body='{"success":true,"receipt":"local-test-receipt","name":"design.pdf"}'))[-1])
  async def fail(r):calls.append(r.request.post_data_json);await r.fulfill(status=503,content_type='application/json',body='{"success":false}')
  async def saved(r):calls.append(r.request.post_data_json);await r.fulfill(status=201,content_type='application/json',body='{"success":true,"status":"saved","reference":"XT-20261101-ABCDEF123456"}')
  await page.route('**/api/leads',fail)
  await page.goto(BASE+'/printing',wait_until='domcontentloaded')
  assert await page.locator('nav').get_by_text('Launch Calculator',exact=True).count()==0
  assert await page.locator('.print-product img').count()==4
  for img in await page.locator('.print-product img').all():
   await img.scroll_into_view_if_needed();await page.wait_for_function('(e)=>e.complete&&e.naturalWidth>0',arg=await img.element_handle())
  assert not await page.locator('#mobile-menu-btn').is_visible()
  await page.locator('[data-print-family="Reports & training materials"]').click();assert await page.locator('#pub-binding').input_value()=='wireo'
  await page.locator('#pub-paper').select_option('art-135');await page.locator('#pub-pages').fill('30');await page.locator('#pub-qty').fill('250')
  assert await page.locator('#calculator').get_attribute('data-valid')=='true'
  assert '135gsm' in await page.locator('#print-spec-summary').inner_text()
  await page.locator('#pub-binding').select_option('saddle');assert await page.locator('#calculator').get_attribute('data-valid')=='false';assert await page.locator('#btn-whatsapp-quote').get_attribute('href') is None
  await page.locator('#pub-binding').select_option('perfect');assert await page.locator('#calculator').get_attribute('data-valid')=='true'
  await page.locator('#pub-pages').fill('');await page.locator('#pub-paper').select_option('help');assert 'Please advise' in await page.locator('#print-live-summary').inner_text()
  await page.locator('[data-target="tab-stationery"]').click();await page.locator('#stationery-type').select_option('ncr');await page.locator('#stationery-qty').fill('30');await page.locator('#ncr-parts').select_option('three')
  brief=await page.locator('#print-spec-summary').inner_text();assert 'Triplicate' in brief and 'Sets per book: 50' in brief and 'Inner pages' not in brief
  await page.locator('#stationery-type').select_option('letterheads');assert await page.locator('#stationery-stock').input_value()=='100';assert not await page.locator('#ncr-options').is_visible()
  await page.locator('[data-target="tab-banners"]').click();await page.locator('#display-width').fill('300');await page.locator('#display-height').fill('225');await page.locator('#display-mount').select_option('eyelets')
  assert 'Width (cm): 300' in await page.locator('#print-spec-summary').inner_text()
  await page.locator('#display-width').fill('');assert await page.locator('#calculator').get_attribute('data-valid')=='false'
  await page.locator('#print-product').select_option(label='Other / help me choose');assert await page.locator('#calculator').get_attribute('data-valid')=='true'
  await page.locator('#print-product').select_option(label='Books & publications');await page.locator('#pub-pages').fill('60');await page.locator('#pub-paper').select_option('art-135')
  await page.locator('#pub-zone').select_option('delivery');assert await page.locator('#delivery-town').get_attribute('required') is not None
  await page.locator('#delivery-town').fill('Kisumu, Milimani');await page.locator('#order-type').select_option('repeat');await page.locator('#previous-reference').fill('XT-PREVIOUS-123');await page.locator('#repeat-changes').fill('Same artwork, 250 copies')
  await page.locator('details.print-form-group summary').click();await page.locator('#company').fill('Local QA organisation');await page.locator('#purchase-order').fill('PO-QA-123');await page.locator('#billing-tax').fill('TEST-PIN')
  await page.locator('#print-name').fill('Local printing QA');await page.locator('#print-phone').fill('0700000000')
  await page.locator('#print-artwork').set_input_files({'name':'bad.exe','mimeType':'application/octet-stream','buffer':b'not artwork'});await page.locator('.print-quote-form .print-submit').click();assert len(calls)==0;assert 'supported file' in await page.locator('#print-quote-feedback').inner_text()
  await page.locator('#print-artwork').set_input_files({'name':'design.pdf','mimeType':'application/pdf','buffer':b'%PDF-1.4\nLocal UI test only'})
  await page.locator('.print-quote-form .print-submit').click();await page.wait_for_function("document.querySelector('#print-quote-feedback').textContent.includes('Your details are still here')")
  assert len(uploads)==1 and calls[0]['artwork_receipt']=='local-test-receipt'
  for value in ['Quantity: 250','135gsm','Kisumu, Milimani','XT-PREVIOUS-123','PO-QA-123']:assert value in calls[0]['message'],value
  assert calls[0]['company']=='Local QA organisation'
  assert await page.locator('#print-name').input_value()=='Local printing QA'
  await page.unroute('**/api/leads');await page.route('**/api/leads',saved);await page.locator('.print-quote-form .print-submit').click();await page.wait_for_function("document.querySelector('#print-quote-feedback').textContent.includes('XT-20261101')")
  assert len(uploads)==1 and calls[0]['client_request_id']==calls[1]['client_request_id']
  wa=unquote(await page.locator('#btn-whatsapp-quote').get_attribute('href'));assert 'Kisumu' in wa and 'PO-QA-123' in wa and 'KES' not in wa
  for link in await page.locator('#print-templates a[download]').all():
   response=await page.request.get(BASE+(await link.get_attribute('href')));assert response.status==200;svg=ET.fromstring(await response.text());assert svg.attrib['width'].endswith('mm');assert 'Guides-DELETE-BEFORE-EXPORT' in await response.text()
  for width in [390,768,1024,1440]:
   await page.set_viewport_size({'width':width,'height':1000});assert await page.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth+1'),width
  await page.set_viewport_size({'width':390,'height':844});await page.reload(wait_until='domcontentloaded');await page.locator('#mobile-menu-btn').click();assert await page.locator('#mobile-menu').is_visible();await page.locator('#mobile-menu-btn').click();await page.wait_for_timeout(400);assert not await page.locator('#mobile-menu').is_visible()
  await page.locator('#calculator').screenshot(path='/tmp/printing-builder-mobile.png');await page.locator('.print-product').first.screenshot(path='/tmp/printing-product-mobile.png')
  await page.set_viewport_size({'width':1440,'height':1000});await page.goto(BASE+'/printing',wait_until='domcontentloaded');await page.locator('#calculator').screenshot(path='/tmp/printing-builder-desktop.png');await page.locator('#print-quote').screenshot(path='/tmp/printing-artwork-desktop.png');await page.locator('#print-products').screenshot(path='/tmp/printing-products-desktop.png')
  assert 'KES' not in await page.locator('main').inner_text() if await page.locator('main').count() else True
  assert not errors,errors
  await b.close()
  print('PASS: all product families, advice options, 135gsm, binding validation, delivery, repeats, organisations, upload retry/idempotency, templates, WhatsApp brief, responsive widths and images; no real submissions')
asyncio.run(main())
