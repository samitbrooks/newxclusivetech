/* Product-specific printing briefs; no public prices or automatic production approval. */
(() => {
 const form=document.getElementById('printing-quote-form');if(!form)return;
 const $=id=>document.getElementById(id);
 const product=$('print-product'),fileInput=$('print-artwork'),status=$('print-upload-status'),remove=$('print-remove-artwork'),feedback=$('print-quote-feedback');
 const label=id=>{const e=$(id);return e?.selectedOptions?.[0]?.textContent.trim()||e?.value.trim()||'Please advise'};
 let current='tab-publications';
 const groups={
 'tab-publications':[['pub-size','Finished size'],['pub-pages','Inner pages (excluding cover)'],['pub-qty','Quantity'],['pub-sides','Printed sides'],['pub-colour','Print colour'],['pub-paper','Inner paper'],['pub-cover-stock','Cover'],['pub-lamination','Cover finish'],['pub-binding','Binding']],
 'tab-stationery':[['stationery-type','Stationery product'],['stationery-qty','Quantity (pieces / sheets / books)'],['stationery-size','Finished size'],['stationery-sides','Printed sides'],['stationery-stock','Paper / card'],['stationery-finish','Finish']],
 'tab-banners':[['display-type','Display product'],['display-qty','Quantity'],['display-width','Width (cm)'],['display-height','Height (cm)'],['display-material','Material'],['display-mount','Mounting / hardware'],['display-use','Use']]
 };
 const common=[['pub-speed','Production preference'],['pub-zone','Collection / delivery'],['delivery-town','Destination town / area'],['print-date','Requested arrival date (subject to confirmation)'],['artwork-help','Artwork readiness'],['order-type','Project type'],['previous-reference','Previous reference'],['repeat-changes','Repeat changes'],['company','Organisation'],['billing-tax','Tax / KRA PIN reference'],['purchase-order','Purchase-order reference'],['billing-address','Billing address']];
 function specifications(){
  const custom=product.value==='Other / help me choose';
  const fields=custom?[]:[...groups[current]];
  if(!custom&&current==='tab-stationery'&&$('stationery-type').value==='ncr')fields.push(['ncr-parts','Parts per set'],['ncr-sets','Sets per book'],['ncr-numbering','Numbering']);
  const lines=[`Product: ${product.value}`,custom?'Please recommend a specification based on my project notes.':'',...fields.map(([id,title])=>`${title}: ${label(id)}`),...common.filter(([id])=>!$(id).disabled&&$(id).value).map(([id,title])=>`${title}: ${label(id)}`)];
  const extras=['add-proof','add-prepress','add-spotuv','add-shrinkwrap'].filter(id=>$(id).checked).map(id=>$(id).nextElementSibling.textContent.trim());
  if(extras.length)lines.push('Optional services: '+extras.join('; '));
  return lines.filter(Boolean).join('\n');
 }
 function refresh(){
  const custom=product.value==='Other / help me choose';
  document.querySelectorAll('.tab-pane').forEach(p=>{p.hidden=custom||p.id!==current;p.classList.toggle('hidden',p.hidden);p.querySelectorAll('input,select').forEach(e=>e.disabled=p.hidden)});
  const ncr=!custom&&current==='tab-stationery'&&$('stationery-type').value==='ncr';$('ncr-options').hidden=!ncr;$('ncr-options').querySelectorAll('input,select').forEach(e=>e.disabled=!ncr);
  const repeat=$('order-type').value==='repeat';for(const id of ['previous-reference','repeat-changes']){$(id).disabled=!repeat;$(id).closest('label').hidden=!repeat}
  $('delivery-town').required=$('pub-zone').value==='delivery';
  document.querySelectorAll('.tab-btn').forEach(b=>{const on=!custom&&b.dataset.target===current;b.classList.toggle('active-tab',on);b.setAttribute('aria-pressed',String(on))});
  let issue='';
  if(!custom){
   const enabled=$(current).querySelectorAll('input,select');
   if([...enabled].some(e=>!e.disabled&&!e.checkValidity()))issue='Please check the quantities and dimensions. Use whole copies and page counts; leave unknown values blank.';
   if(current==='tab-publications'&&$('pub-binding').value==='saddle'){
    if($('pub-pages').value&&Number($('pub-pages').value)%4!==0)issue='Saddle-stitched inner pages must be a multiple of four (for example 28 or 32). Other binding choices do not have this restriction.';
    if($('pub-sides').value==='one')issue='Saddle-stitched booklets use double-sided pages. Choose double-sided, Help me choose, or another binding.';
   }
   if(current==='tab-banners'&&Boolean($('display-width').value)!==Boolean($('display-height').value))issue='Enter both display dimensions, or leave both blank for advice.';
  }
  $('calculator').dataset.valid=String(!issue);$('print-validation').textContent=issue;
  const specs=specifications();$('print-spec-summary').textContent=specs;$('print-live-summary').textContent=specs;
  const wa=$('btn-whatsapp-quote');
  if(!issue){wa.href='https://wa.me/254722753819?text='+encodeURIComponent('Hi Xclusive Tech Printing Desk, please quote for:\n\n'+specs+($('print-notes').value?'\n\nProject notes: '+$('print-notes').value:'')+'\n\nPlease confirm current pricing, VAT, stock, artwork requirements, production timing, delivery and quote validity.');wa.removeAttribute('aria-disabled')}
  else{wa.removeAttribute('href');wa.setAttribute('aria-disabled','true')}
 }
 function setFamily(value,scroll){
  product.value=value;
  if(value!=='Other / help me choose')current=value==='Business stationery'?'tab-stationery':value==='Events & display'?'tab-banners':'tab-publications';
  if(value==='Reports & training materials')$('pub-binding').value='wireo';
  refresh();if(scroll)$('calculator').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
 }
 document.querySelectorAll('[data-print-family]').forEach(b=>b.addEventListener('click',()=>setFamily(b.dataset.printFamily,true)));
 product.addEventListener('change',()=>setFamily(product.value,false));
 document.querySelectorAll('.tab-btn').forEach(b=>b.addEventListener('click',()=>{current=b.dataset.target;product.value=current==='tab-stationery'?'Business stationery':current==='tab-banners'?'Events & display':'Books & publications';refresh()}));
 $('stationery-type').addEventListener('change',()=>{
  const presets={cards:['card','350','two','matt'],folders:['a4','350','two','matt'],letterheads:['a4','100','one','none'],flyers:['a5','135','two','none'],ncr:['a5','ncr','one','none'],certificates:['a4','300','one','none']};
  const values=presets[$('stationery-type').value];if(values)['stationery-size','stationery-stock','stationery-sides','stationery-finish'].forEach((id,i)=>$(id).value=values[i]);refresh();
 });
 $('calculator').addEventListener('input',refresh);$('calculator').addEventListener('change',refresh);form.addEventListener('input',refresh);form.addEventListener('change',refresh);
 $('print-date').min=new Date(Date.now()+10800000).toISOString().slice(0,10);
 let receipt=null,uploadedFile=null,sending=false;
 function mime(file){return file.type||({pdf:'application/pdf',png:'image/png',jpg:'image/jpeg',jpeg:'image/jpeg'}[file.name.split('.').pop().toLowerCase()])}
 function validFile(file){if(!['application/pdf','image/png','image/jpeg'].includes(mime(file))){status.textContent='Please choose a PDF, JPG or PNG, or share a link below for other formats.';return false}if(file.size>10*1024*1024){status.textContent='This file exceeds 10 MB. Share an artwork link below or choose a smaller file.';return false}return true}
 function chosen(){receipt=null;uploadedFile=null;const file=fileInput.files[0];remove.hidden=!file;status.textContent=file&&validFile(file)?`${file.name} · ${(file.size/1024/1024).toFixed(2)} MB · ready to upload with your quote request.`:file?status.textContent:''}
 fileInput.disabled=false;fileInput.addEventListener('change',chosen);remove.addEventListener('click',()=>{fileInput.value='';chosen()});
 const drop=document.getElementById('artwork-dropzone');for(const type of ['dragenter','dragover'])drop.addEventListener(type,e=>{e.preventDefault();drop.classList.add('is-dragging')});for(const type of ['dragleave','drop'])drop.addEventListener(type,e=>{e.preventDefault();drop.classList.remove('is-dragging')});drop.addEventListener('drop',e=>{if(sending||!e.dataTransfer.files.length)return;const data=new DataTransfer();data.items.add(e.dataTransfer.files[0]);fileInput.files=data.files;chosen()});
 form.addEventListener('submit',async e=>{
  e.preventDefault();e.stopPropagation();if(sending||!form.reportValidity())return;
  refresh();if($('calculator').dataset.valid!=='true'){feedback.textContent=$('print-validation').textContent;feedback.focus();return}
  const file=fileInput.files[0];if(file&&!validFile(file)){feedback.textContent='Please choose a supported file, remove it to send artwork later, or share an artwork link.';feedback.focus();return}
  sending=true;const button=form.querySelector('[type=submit]');button.disabled=true;fileInput.disabled=true;remove.disabled=true;button.textContent=file?'Uploading artwork…':'Saving quote request…';feedback.textContent='';
  try{
   if(file&&uploadedFile!==file){const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),60000);try{const response=await fetch('/api/leads/artwork',{method:'POST',headers:{'Content-Type':mime(file),'X-File-Name':encodeURIComponent(file.name)},body:file,signal:controller.signal});const result=await response.json();if(!response.ok||result.success!==true||!result.receipt)throw Error(result.error||'Artwork could not be saved.');receipt=result.receipt;uploadedFile=file;status.textContent=`${file.name} uploaded. Saving your quote request…`;}finally{clearTimeout(timer)}}
   button.textContent='Saving quote request…';
   const values=Object.fromEntries(new FormData(form));
   const message=[specifications(),values.requested_date?`Requested delivery date: ${values.requested_date} (subject to confirmation)`:'',values.artwork_link?`Artwork link: ${values.artwork_link}`:'',values.message?`Project notes: ${values.message}`:'',file?'Artwork attached to this enquiry.':'Artwork: link supplied or to follow.'].filter(Boolean).join('\n\n');
   const result=await window.XTLeadAPI.submit({name:values.name,phone:values.phone,email:values.email,company:values.company,service:`Printing: ${product.value}`,message,_honey:values._honey,artwork_receipt:receipt||undefined},'printing-quote-form');
   feedback.textContent=`Thank you. Your print quote request is saved. Reference: ${result.reference}. ${file?'Your uploaded artwork is linked to the enquiry. ':''}We will contact you to confirm the details before production.`;feedback.style.color='#065f46';button.textContent='Print quote request saved';if(file)status.textContent=`${file.name} saved with your enquiry.`;feedback.focus();
  }catch(error){feedback.textContent=`${error.name==='AbortError'?'The upload timed out.':error.message||'We could not confirm the request was saved.'} Your details are still here. Retry, remove the file and share a link, or contact us on WhatsApp.`;feedback.style.color='#991b1b';button.disabled=false;button.textContent='Retry print quote request';feedback.focus();}
  finally{sending=false;fileInput.disabled=false;remove.disabled=false}
 });
 // CSS sticky supplies the scroll effect without scroll listeners or transforms.
 // Tall briefs pin at their bottom so every line and action stays reachable.
 const followers=document.querySelectorAll('.print-builder-grid > .print-estimate,.print-quote-grid > .print-brief');
 const header=document.querySelector('.print-navbar');
 let followFrame=0;
 function sizeFollowers(){
  cancelAnimationFrame(followFrame);
  followFrame=requestAnimationFrame(()=>{
   const inset=(header?.getBoundingClientRect().height||88)+24;
   followers.forEach(panel=>panel.style.setProperty('--print-follow-top',Math.min(inset,window.innerHeight-panel.offsetHeight-24)+'px'));
  });
 }
 const followObserver=new ResizeObserver(sizeFollowers);
 followers.forEach(panel=>followObserver.observe(panel));if(header)followObserver.observe(header);
 window.addEventListener('resize',sizeFollowers,{passive:true});
 refresh();sizeFollowers();
})();
