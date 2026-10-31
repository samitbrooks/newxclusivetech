/* Printing quote intake: estimate and artwork accompany a durably saved enquiry. */
(() => {
 const form=document.getElementById('printing-quote-form');if(!form)return;
 const product=document.getElementById('print-product'),fileInput=document.getElementById('print-artwork'),status=document.getElementById('print-upload-status'),remove=document.getElementById('print-remove-artwork'),feedback=document.getElementById('print-quote-feedback');
 const label=id=>{const e=document.getElementById(id);return e?.selectedOptions?.[0]?.textContent.trim()||e?.value||''};
 const text=id=>document.getElementById(id)?.textContent.trim()||'';
 const active=()=>document.querySelector('.tab-pane:not(.hidden)')?.id;
 function specifications(){
  if(product.value==='Other / help me choose')return 'Custom print project. Please describe sizes, quantities and finishes in your project notes.';
  if(active()==='tab-publications')return [`Product: ${product.value}`,`Format: ${label('pub-size')}`,`Inner pages: ${label('pub-pages')}`,`Quantity: ${label('pub-qty')}`,`Print: ${document.querySelector('.color-toggle.active')?.textContent.trim()||'Full colour'}`,`Paper: ${label('pub-paper')}`,`Cover: ${label('pub-cover-stock')}`,`Lamination: ${label('pub-lamination')}`,`Binding: ${label('pub-binding')}`,`Turnaround: ${label('pub-speed')}`,`Delivery: ${label('pub-zone')}`,`Finishing / add-ons: ${['add-proof','add-prepress','add-spotuv','add-shrinkwrap'].filter(id=>document.getElementById(id)?.checked).map(id=>document.getElementById(id).closest('label')?.innerText.trim().replace(/\s+/g,' ')).filter(Boolean).join('; ')||'None selected'}`,`Indicative estimate: ${text('grand-total')} (${document.getElementById('include-vat').checked?'including VAT estimate':'excluding VAT'})`].join('\n');
  if(active()==='tab-stationery')return ['Product: Business stationery',...['card-qty','folder-qty','letterhead-qty'].map((id,i)=>`${['Business cards','Presentation folders','Letterheads'][i]}: ${label(id)}`),`Spot UV: ${document.getElementById('card-spotuv')?.checked?'Requested, quoted separately':'Not requested'}`, 'Final quote confirms finishing, delivery and tax.'].join('\n');
  return 'Product: Events & display. Include item type, dimensions, quantities and event date in your project notes. Display prices are indicative; the written quote confirms the complete scope.';
 }
 function refresh(){document.getElementById('print-spec-summary').textContent=specifications();const total=['card-qty','folder-qty','letterhead-qty'].reduce((n,id)=>n+Number(document.getElementById(id)?.value||0),0);document.getElementById('stationery-estimate').textContent=`Configured stationery base: KES ${total.toLocaleString()}. Finishing, delivery and tax are confirmed separately.`}
 document.querySelectorAll('[name="print-speed-choice"]').forEach(radio=>radio.addEventListener('change',()=>{const select=document.getElementById('pub-speed');select.value=radio.value;select.dispatchEvent(new Event('change',{bubbles:true}))}));
 function setFamily(value,scroll){
  product.value=value;if(value==='Other / help me choose'){refresh();return}const target=value==='Business stationery'?'tab-stationery':value==='Events & display'?'tab-banners':'tab-publications';
  document.querySelector(`.tab-btn[data-target="${target}"]`)?.click();
  if(value==='Reports & training materials'){document.getElementById('pub-binding').value='wireo';document.getElementById('pub-binding').dispatchEvent(new Event('change',{bubbles:true}))}
  refresh();if(scroll)document.getElementById('calculator').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
 }
 document.querySelectorAll('[data-print-family]').forEach(button=>button.addEventListener('click',()=>setFamily(button.dataset.printFamily,true)));
 product.addEventListener('change',()=>setFamily(product.value,false));
 document.querySelectorAll('.tab-btn').forEach(button=>button.addEventListener('click',()=>{const target=button.dataset.target;if(target==='tab-stationery')product.value='Business stationery';else if(target==='tab-banners')product.value='Events & display';else if(!['Books & publications','Reports & training materials'].includes(product.value))product.value='Books & publications';refresh()}));
 document.getElementById('calculator').addEventListener('input',refresh);document.getElementById('calculator').addEventListener('change',refresh);document.getElementById('calculator').addEventListener('click',()=>requestAnimationFrame(refresh));
 document.getElementById('print-date').min=new Date(Date.now()+10800000).toISOString().slice(0,10);
 let receipt=null,uploadedFile=null,sending=false;
 function mime(file){return file.type||({pdf:'application/pdf',png:'image/png',jpg:'image/jpeg',jpeg:'image/jpeg'}[file.name.split('.').pop().toLowerCase()])}
 function validFile(file){if(!['application/pdf','image/png','image/jpeg'].includes(mime(file))){status.textContent='Please choose a PDF, JPG or PNG, or share a link below for other formats.';return false}if(file.size>10*1024*1024){status.textContent='This file exceeds 10 MB. Share an artwork link below or choose a smaller file.';return false}return true}
 function chosen(){receipt=null;uploadedFile=null;const file=fileInput.files[0];remove.hidden=!file;status.textContent=file&&validFile(file)?`${file.name} · ${(file.size/1024/1024).toFixed(2)} MB · ready to upload with your quote request.`:file?status.textContent:''}
 fileInput.disabled=false;fileInput.addEventListener('change',chosen);remove.addEventListener('click',()=>{fileInput.value='';chosen()});
 const drop=document.getElementById('artwork-dropzone');for(const type of ['dragenter','dragover'])drop.addEventListener(type,e=>{e.preventDefault();drop.classList.add('is-dragging')});for(const type of ['dragleave','drop'])drop.addEventListener(type,e=>{e.preventDefault();drop.classList.remove('is-dragging')});drop.addEventListener('drop',e=>{if(sending||!e.dataTransfer.files.length)return;const data=new DataTransfer();data.items.add(e.dataTransfer.files[0]);fileInput.files=data.files;chosen()});
 form.addEventListener('submit',async e=>{
  e.preventDefault();e.stopPropagation();if(sending||!form.reportValidity())return;
  if(product.value!=='Other / help me choose'&&active()==='tab-publications'&&document.getElementById('btn-print-proforma').disabled){feedback.textContent='Please correct the page count and quantity in the calculator before submitting.';feedback.focus();return}
  const file=fileInput.files[0];if(file&&!validFile(file)){feedback.textContent='Please choose a supported file, remove it to send artwork later, or share an artwork link.';feedback.focus();return}
  sending=true;const button=form.querySelector('[type=submit]');button.disabled=true;fileInput.disabled=true;remove.disabled=true;button.textContent=file?'Uploading artwork…':'Saving quote request…';feedback.textContent='';
  try{
   if(file&&uploadedFile!==file){const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),60000);try{const response=await fetch('/api/leads/artwork',{method:'POST',headers:{'Content-Type':mime(file),'X-File-Name':encodeURIComponent(file.name)},body:file,signal:controller.signal});const result=await response.json();if(!response.ok||result.success!==true||!result.receipt)throw Error(result.error||'Artwork could not be saved.');receipt=result.receipt;uploadedFile=file;status.textContent=`${file.name} uploaded. Saving your quote request…`;}finally{clearTimeout(timer)}}
   button.textContent='Saving quote request…';
   const values=Object.fromEntries(new FormData(form));
   const message=[specifications(),values.requested_date?`Requested delivery date: ${values.requested_date} (subject to confirmation)`:'',values.artwork_link?`Artwork link: ${values.artwork_link}`:'',values.message?`Project notes: ${values.message}`:'',file?'Artwork attached to this enquiry.':'Artwork: link supplied or to follow.'].filter(Boolean).join('\n\n');
   const result=await window.XTLeadAPI.submit({name:values.name,phone:values.phone,email:values.email,service:`Printing: ${product.value}`,message,_honey:values._honey,artwork_receipt:receipt||undefined},'printing-quote-form');
   feedback.textContent=`Thank you. Your print quote request is saved. Reference: ${result.reference}. ${file?'Your uploaded artwork is linked to the enquiry. ':''}We will contact you to confirm the details before production.`;feedback.style.color='#065f46';button.textContent='Print quote request saved';if(file)status.textContent=`${file.name} saved with your enquiry.`;feedback.focus();
  }catch(error){feedback.textContent=`${error.name==='AbortError'?'The upload timed out.':error.message||'We could not confirm the request was saved.'} Your details are still here. Retry, remove the file and share a link, or contact us on WhatsApp.`;feedback.style.color='#991b1b';button.disabled=false;button.textContent='Retry print quote request';feedback.focus();}
  finally{sending=false;fileInput.disabled=false;remove.disabled=false}
 });
 refresh();
})();
