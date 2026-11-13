(() => {
 const root=document.querySelector('[data-solution-catalogue]');if(!root)return;
 const input=root.querySelector('#solution-search'), buttons=[...root.querySelectorAll('[data-category]')],cards=[...root.querySelectorAll('[data-solution-card]')],count=root.querySelector('#solution-count'),empty=root.querySelector('#solution-empty');
 let category='All';
 function update(){const q=input.value.toLowerCase().trim();let visible=0;cards.forEach(card=>{const show=(category==='All'||card.dataset.group===category)&&card.dataset.search.includes(q);card.hidden=!show;if(show)visible++;});count.textContent=`${visible} of ${cards.length} packages${category==='All'?'':' in '+category}`;empty.hidden=visible!==0;}
 buttons.forEach(button=>button.addEventListener('click',()=>{category=button.dataset.category;buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));update();}));input.addEventListener('input',update);
 root.querySelector('#solution-reset').addEventListener('click',()=>{input.value='';category='All';buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.category==='All')));update();input.focus();});update();
})();
