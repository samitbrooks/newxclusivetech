const MAX = 10 * 1024 * 1024;
const TTL = 30 * 86400;
const encoder = new TextEncoder();
const json = (body, status=200) => new Response(JSON.stringify(body),{status,headers:{'content-type':'application/json','cache-control':'no-store','x-content-type-options':'nosniff'}});
async function key(env){return crypto.subtle.importKey('raw',encoder.encode(env.IP_HASH_KEY),{name:'HMAC',hash:'SHA-256'},false,['sign','verify'])}
const hex = bytes => [...new Uint8Array(bytes)].map(b=>b.toString(16).padStart(2,'0')).join('');
async function sign(env,text){return hex(await crypto.subtle.sign('HMAC',await key(env),encoder.encode(text)))}
async function verify(env,text,signature){if(!/^[a-f0-9]{64}$/.test(signature||''))return false;return crypto.subtle.verify('HMAC',await key(env),Uint8Array.from(signature.match(/../g),x=>parseInt(x,16)),encoder.encode(text))}
function encode(value){return btoa(String.fromCharCode(...encoder.encode(JSON.stringify(value)))).replaceAll('+','-').replaceAll('/','_').replaceAll('=','')}
function decode(value){const raw=value.replaceAll('-','+').replaceAll('_','/');return JSON.parse(new TextDecoder().decode(Uint8Array.from(atob(raw),c=>c.charCodeAt(0))))}
export async function artworkNote(receipt,env){
 if(!receipt)return '';
 if(typeof receipt!=='string'||receipt.length>2000)throw Error('Invalid artwork receipt');
 const [payload,signature,...rest]=receipt.split('.');
 if(rest.length||!await verify(env,payload,signature))throw Error('Invalid artwork receipt');
 const data=decode(payload);
 if(data.expires<Math.floor(Date.now()/1000)||!/^[-a-f0-9]{36}$/.test(data.id))throw Error('Artwork receipt expired');
 const token=await sign(env,`download:${data.id}:${data.expires}`);
 return `\n\nUploaded artwork: ${data.name} (${data.size} bytes)\nPrivate download (expires after 30 days): https://www.xclusivetech.co.ke/api/leads/artwork/${data.id}?expires=${data.expires}&token=${token}`;
}
export async function artworkRequest(request,env){
 const url=new URL(request.url);const path=url.pathname;
 if(!path.startsWith('/api/leads/artwork'))return null;
 if(!env.PRINT_ARTWORK||!env.IP_HASH_KEY)return json({error:'Artwork upload is temporarily unavailable. Send a file link or use WhatsApp instead.'},503);
 if(path.startsWith('/api/leads/artwork/')&&request.method==='GET'){
  const id=path.split('/').pop(),expires=Number(url.searchParams.get('expires'));
  if(!/^[-a-f0-9]{36}$/.test(id)||!Number.isInteger(expires)||!await verify(env,`download:${id}:${expires}`,url.searchParams.get('token')))return json({error:'Invalid download link.'},403);
  if(expires<Math.floor(Date.now()/1000))return json({error:'This artwork link expired. Ask the sender to share the file again.'},410);
  let result;try{result=await env.PRINT_ARTWORK.getWithMetadata(id,{type:'arrayBuffer',cacheTtl:30})}catch{return json({error:'Artwork download is temporarily unavailable. Please retry shortly.'},503)}
  if(!result.value)return new Response('The file may still be becoming available. Please retry in one minute, or ask the sender to share it again.',{status:503,headers:{'retry-after':'60','cache-control':'no-store','content-type':'text/plain'}});
  return new Response(result.value,{headers:{'content-type':'application/octet-stream','content-disposition':`attachment; filename="artwork.${result.metadata.extension}"; filename*=UTF-8''${encodeURIComponent(result.metadata.name).replaceAll("'",'%27')}`,'cache-control':'private, no-store','x-content-type-options':'nosniff','content-security-policy':"default-src 'none'; sandbox",'referrer-policy':'no-referrer'}});
 }
 if(path!=='/api/leads/artwork'||request.method!=='POST')return json({error:'Not found.'},404);
 if(!(env.ALLOWED_ORIGINS||'https://www.xclusivetech.co.ke').split(',').includes(request.headers.get('origin')))return json({error:'This upload is not allowed.'},403);
 try{
  const now=Math.floor(Date.now()/1000);
  const digest=await sign(env,'artwork-ip:'+(request.headers.get('CF-Connecting-IP')||'unknown'));
  const rate=await env.LEADS_DB.prepare('INSERT INTO rate_buckets(bucket_key,hits,expires_at) VALUES(?,1,?) ON CONFLICT(bucket_key) DO UPDATE SET hits=hits+1 RETURNING hits').bind(`artwork:${digest}:${Math.floor(now/3600)}`,now+7200).first();
  if(rate.hits>8)return json({error:'Please wait before uploading again, or share an artwork link.'},429);
  const mime=(request.headers.get('content-type')||'').split(';')[0];
  const extension={'application/pdf':'pdf','image/png':'png','image/jpeg':'jpg'}[mime];
  if(!extension)return json({error:'Upload a PDF, JPG or PNG. Share a link for other formats.'},415);
  let name;try{name=decodeURIComponent(request.headers.get('x-file-name')||`artwork.${extension}`)}catch{return json({error:'Please rename the file and retry.'},422)}
  name=name.split(/[\\/]/).pop().replace(/[\x00-\x1f\x7f]/g,'').slice(0,120);
  if(!name)return json({error:'Please name the file and retry.'},422);
  const chunks=[];let size=0;const reader=request.body?.getReader();
  if(!reader)return json({error:'Choose a file to upload.'},422);
  while(true){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;if(size>MAX){await reader.cancel();return json({error:'Maximum file size is 10 MB. Share a file link instead.'},413)}chunks.push(value)}
  const bytes=new Uint8Array(size);let offset=0;for(const c of chunks){bytes.set(c,offset);offset+=c.byteLength}
  const valid=extension==='pdf'?new TextDecoder().decode(bytes.slice(0,5))==='%PDF-':extension==='png'?hex(bytes.slice(0,8))==='89504e470d0a1a0a':hex(bytes.slice(0,3))==='ffd8ff';
  if(!valid)return json({error:'The file contents do not match a supported PDF, JPG or PNG.'},422);
  const id=crypto.randomUUID(),expires=now+TTL;
  await env.PRINT_ARTWORK.put(id,bytes.buffer,{expiration:expires,metadata:{name,mime,extension,size}});
  const payload=encode({id,name,size,expires});
  return json({success:true,receipt:payload+'.'+await sign(env,payload),name,size},201);
 }catch{console.error(JSON.stringify({event:'artwork_upload_failed'}));return json({error:'The upload could not be saved. Retry, share a file link, or send the artwork later on WhatsApp.'},503)}
}
