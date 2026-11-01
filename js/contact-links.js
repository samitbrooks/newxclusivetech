/* Keep contact details actionable in static content and live enquiry feedback. */
(() => {
 const pattern=/[A-Z0-9._%+-]+@xclusivetech\.co\.ke|(?<!\d)(?:\+?254[\s.-]*|0)?722[\s.-]*753[\s.-]*819(?!\d)|(?:use)\s+WhatsApp/gi;
 const excluded='a,script,style,textarea,pre,code,option,button,[contenteditable],#print-spec-summary';
 function enhance(node){
  if(node.nodeType!==Node.TEXT_NODE||!node.parentElement||node.parentElement.closest(excluded))return;
  const value=node.nodeValue;pattern.lastIndex=0;const matches=[...value.matchAll(pattern)];if(!matches.length)return;
  const fragment=document.createDocumentFragment();let end=0;
  for(const match of matches){
   fragment.append(document.createTextNode(value.slice(end,match.index)));
   const link=document.createElement('a'),contact=match[0];link.className='contact-inline-link';link.textContent=contact;
   if(contact.includes('@'))link.href='mailto:'+contact.replace(/^info@/i,'hello@');
   else{
    const context=(node.parentElement.textContent.slice(0,node.parentElement.textContent.indexOf(value))+value.slice(0,match.index)).slice(-140);
    const labels=context.match(/whatsapp|phone|call|tel(?:ephone)?/gi)||[];
    const whatsapp=/use\s+WhatsApp/i.test(contact)||labels.at(-1)?.toLowerCase()==='whatsapp';
    link.href=whatsapp?'https://wa.me/254722753819':'tel:+254722753819';
    if(whatsapp){link.target='_blank';link.rel='noopener noreferrer'}
   }
   fragment.append(link);end=match.index+contact.length;
  }
  fragment.append(document.createTextNode(value.slice(end)));node.replaceWith(fragment);
 }
 function scan(root){
  if(root.nodeType===Node.TEXT_NODE){enhance(root);return}
  if(root.nodeType!==Node.ELEMENT_NODE||root.closest(excluded))return;
  const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);const texts=[];while(walker.nextNode())texts.push(walker.currentNode);texts.forEach(enhance);
 }
 function start(){
  scan(document.body);
  const observer=new MutationObserver(records=>{for(const record of records){if(record.type==='characterData')enhance(record.target);else record.addedNodes.forEach(scan)}});
  observer.observe(document.body,{childList:true,subtree:true,characterData:true});
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
