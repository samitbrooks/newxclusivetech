import { artworkNote } from './artwork.mjs';
const MAX_BYTES = 32768;
const JSON_HEADERS = { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store', 'x-content-type-options': 'nosniff' };
const respond = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: JSON_HEADERS });
class RequestError extends Error { constructor(message, status = 422) { super(message); this.status = status; } }
function text(value, max, required = false) {
    if (value == null && !required) return '';
    if (typeof value !== 'string') throw new RequestError('Please check the enquiry fields.');
    const clean = value.trim();
    if ((required && !clean) || clean.length > max) throw new RequestError('Please check the enquiry fields and shorten any long notes.');
    return clean;
}
export function normalizeLead(body, request) {
    if (!body || typeof body !== 'object' || Array.isArray(body)) throw new RequestError('Please check the enquiry fields.');
    if (body._honey) throw new RequestError('Please retry your enquiry or contact us by WhatsApp.');
    const newsletter = body.form_id === 'newsletter-form';
    const name = text(newsletter ? 'Newsletter subscription request' : body.name, 120, true).replace(/[\r\n\t]+/g, ' ');
    let phone = newsletter ? '' : text(body.phone, 40, true);
    if (!newsletter && !/^[+0-9 ().-]+$/.test(phone)) throw new RequestError('Please enter a phone number we can reach you on.');
    phone = phone.replace(/[ ().-]/g, '');
    if (/^0\d{9}$/.test(phone)) phone = '+254' + phone.slice(1);
    else if (/^[17]\d{8}$/.test(phone)) phone = '+254' + phone;
    else if (/^254\d{9}$/.test(phone)) phone = '+' + phone;
    if (!newsletter && !/^\+?\d{7,15}$/.test(phone)) throw new RequestError('Please enter a phone number we can reach you on.');
    const email = text(body.email, 254, newsletter);
    if (email && (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || /[\r\n]/.test(email))) throw new RequestError('Please check the email address, or leave it blank.');
    const formId = text(body.form_id || 'website-enquiry', 80);
    if (!/^[a-z0-9_-]+$/i.test(formId)) throw new RequestError('Please retry your enquiry.');
    let message = text(body.message ?? body.project_details, 8000);
    if (formId === 'printing-quote-form' && body.product) {
        const product = text(body.product, 120);
        const requested = text(body.requested_date, 20);
        const artworkLink = text(body.artwork_link, 700);
        if (artworkLink) {
            try { if (!['https:', 'http:'].includes(new URL(artworkLink).protocol)) throw Error(); }
            catch { throw new RequestError('Please enter a valid artwork download link.'); }
        }
        message = [`Product: ${product}`, requested ? `Requested date: ${requested} (subject to confirmation)` : '', artworkLink ? `Artwork link: ${artworkLink}` : '', message].filter(Boolean).join('\n\n');
    }
    let path = '/';
    try { const page = new URL(body.page_path || request.headers.get('referer') || '/', request.url); if (page.origin === new URL(request.url).origin) path = page.pathname.slice(0, 250); } catch {}
    return { name, phone, email, company: text(body.company, 200), service: text(body.service, 200), budget: text(body.budget, 160), message, county: text(body.county, 80), form_id: formId, page_path: path };
}
async function hmac(secret, value) {
    const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
    return [...new Uint8Array(await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(value)))].map(b => b.toString(16).padStart(2, '0')).join('');
}
async function readBody(request) {
    const reader = request.body?.getReader();
    if (!reader) throw new RequestError('Please enter your enquiry details.');
    const chunks = []; let size = 0;
    while (true) {
        const { value, done } = await reader.read(); if (done) break;
        size += value.byteLength;
        if (size > MAX_BYTES) { await reader.cancel(); throw new RequestError('Please shorten the enquiry and try again.', 413); }
        chunks.push(value);
    }
    const all = new Uint8Array(size); let offset = 0;
    for (const chunk of chunks) { all.set(chunk, offset); offset += chunk.byteLength; }
    const raw = new TextDecoder().decode(all);
    const type = (request.headers.get('content-type') || '').split(';')[0].trim();
    if (type === 'application/json') {
        try { return JSON.parse(raw); } catch { throw new RequestError('Please retry your enquiry.', 400); }
    }
    if (type === 'application/x-www-form-urlencoded') return Object.fromEntries(new URLSearchParams(raw));
    // Native enquiry forms use urlencoded data, not files or multipart uploads.
    throw new RequestError('This form could not be read. Please retry or use WhatsApp.', 415);
}
function configured(env) { return Boolean(env.LEADS_DB && env.EMAIL && env.NOTIFICATION_TO && env.SENDER_EMAIL && env.IP_HASH_KEY); }
async function rateLimit(env, request, now) {
    const ip = request.headers.get('CF-Connecting-IP') || 'unknown';
    const digest = await hmac(env.IP_HASH_KEY, ip);
    for (const [seconds, limit] of [[60, 8], [3600, 60]]) {
        const key = `${digest}:${seconds}:${Math.floor(now / seconds)}`;
        const row = await env.LEADS_DB.prepare('INSERT INTO rate_buckets(bucket_key,hits,expires_at) VALUES(?,1,?) ON CONFLICT(bucket_key) DO UPDATE SET hits=hits+1 RETURNING hits').bind(key, now + seconds * 2).first();
        if (row.hits > limit) throw new RequestError('Too many requests. Please wait a moment or contact us by WhatsApp.', 429);
    }
}
export async function handleRequest(request, env, context, sendNotification) {
    const url = new URL(request.url);
    if (url.pathname === '/api/leads/health' && request.method === 'GET') {
        if (!configured(env)) return respond({ ready: false }, 503);
        try { await env.LEADS_DB.prepare('SELECT id FROM leads LIMIT 1').first(); return respond({ ready: true, storage: true }); }
        catch { return respond({ ready: false }, 503); }
    }
    if (url.pathname !== '/api/leads' && url.pathname !== '/api/leads/') return respond({ error: 'Not found.' }, 404);
    if (request.method !== 'POST') return new Response('Method not allowed', { status: 405, headers: { ...JSON_HEADERS, allow: 'POST' } });
    if (!configured(env)) return respond({ success: false, error: 'Please retry shortly or contact us by WhatsApp.' }, 503);
    const allowed = (env.ALLOWED_ORIGINS || 'https://www.xclusivetech.co.ke').split(',').map(x => x.trim());
    if (!allowed.includes(request.headers.get('origin'))) return respond({ success: false, error: 'This submission is not allowed.' }, 403);
    try {
        const body = await readBody(request); const lead = normalizeLead(body, request);
        try { lead.message += await artworkNote(body.artwork_receipt, env); } catch { throw new RequestError('Please upload your artwork again, or send the enquiry without a file.'); }
        const key = body.client_request_id || request.headers.get('Idempotency-Key') || crypto.randomUUID();
        if (typeof key !== 'string' || !/^[a-z0-9_-]{16,80}$/i.test(key)) throw new RequestError('Please retry your enquiry.', 400);
        const hash = await hmac(env.IP_HASH_KEY, JSON.stringify(lead));
        // A replay of a successfully saved request does not consume more write quota or send a second notification.
        const existing = await env.LEADS_DB.prepare('SELECT id,reference,payload_hash FROM leads WHERE client_request_id=?').bind(key).first();
        if (existing) {
            if (existing.payload_hash !== hash) throw new RequestError('Your details changed. Please retry the enquiry.', 409);
            return savedResponse(request, existing.reference);
        }
        const now = Math.floor(Date.now() / 1000); await rateLimit(env, request, now);
        const id = crypto.randomUUID(); const reference = `XT-${new Date(Date.now() + 10800000).toISOString().slice(0, 10).replaceAll('-', '')}-${id.replaceAll('-', '').slice(0, 12).toUpperCase()}`;
        const values = [id, reference, key, hash, lead.name, lead.phone, lead.email, lead.company, lead.service, lead.budget, lead.message, lead.county, lead.form_id, lead.page_path, now];
        // D1 batch is atomic: the lead and durable outbox entry are committed together.
        await env.LEADS_DB.batch([
            env.LEADS_DB.prepare('INSERT INTO leads(id,reference,client_request_id,payload_hash,name,phone,email,company,service,budget,message,county,form_id,page_path,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(client_request_id) DO NOTHING').bind(...values),
            env.LEADS_DB.prepare("INSERT OR IGNORE INTO lead_notifications(lead_id,state,next_attempt_at) SELECT id,'pending',? FROM leads WHERE client_request_id=? AND payload_hash=?").bind(now, key, hash)
        ]);
        const saved = await env.LEADS_DB.prepare('SELECT id,reference,payload_hash FROM leads WHERE client_request_id=?').bind(key).first();
        if (!saved || saved.payload_hash !== hash) throw new RequestError('Your details changed. Please retry the enquiry.', 409);
        // The response confirms storage only. Email is asynchronous and can be retried independently.
        context.waitUntil(deliverOne(env, saved.id, sendNotification));
        return savedResponse(request, saved.reference, 201);
    } catch (error) {
        const status = error instanceof RequestError ? error.status : 503;
        if (!(error instanceof RequestError)) console.error(JSON.stringify({event: 'lead_storage_request_failed'}));
        return respond({ success: false, error: error instanceof RequestError ? error.message : 'We could not save the enquiry. Please retry or contact us by WhatsApp.' }, status);
    }
}
function savedResponse(request, reference, status = 200) {
    if (!(request.headers.get('content-type') || '').includes('application/json') && !(request.headers.get('accept') || '').includes('application/json')) {
        return new Response(null, { status: 303, headers: { 'cache-control': 'no-store', location: `https://www.xclusivetech.co.ke/contact?success=true&reference=${encodeURIComponent(reference)}` } });
    }
    return respond({ success: true, status: 'saved', reference }, status);
}
export async function deliverOne(env, leadId, sendNotification) {
    const now = Math.floor(Date.now() / 1000);
    try {
        const lease = await env.LEADS_DB.prepare("UPDATE lead_notifications SET state='sending',attempts=attempts+1,locked_until=? WHERE lead_id=? AND state!='sent' AND next_attempt_at<=? AND locked_until<=? RETURNING attempts").bind(now + 300, leadId, now, now).first();
        if (!lease) return;
        const lead = await env.LEADS_DB.prepare('SELECT * FROM leads WHERE id=?').bind(leadId).first();
        await sendNotification(lead, env);
        await env.LEADS_DB.prepare("UPDATE lead_notifications SET state='sent',sent_at=?,locked_until=0,last_error=NULL WHERE lead_id=?").bind(Math.floor(Date.now() / 1000), leadId).run();
    } catch {
        // No PII or mail address is put in public errors or console logs.
        console.error(JSON.stringify({event: 'lead_notification_pending_retry'}));
        try {
            const record = await env.LEADS_DB.prepare('SELECT attempts FROM lead_notifications WHERE lead_id=?').bind(leadId).first();
            const delay = Math.min(86400, 60 * 2 ** Math.min(record?.attempts || 1, 10));
            await env.LEADS_DB.prepare("UPDATE lead_notifications SET state='pending',locked_until=0,next_attempt_at=?,last_error='EMAIL_SEND_FAILED' WHERE lead_id=?").bind(now + delay, leadId).run();
        } catch { console.error(JSON.stringify({event: 'lead_notification_retry_state_failed'})); }
    }
}
export async function retryPending(env, sendNotification) {
    if (!configured(env)) return;
    const now = Math.floor(Date.now() / 1000);
    const due = await env.LEADS_DB.prepare("SELECT lead_id FROM lead_notifications WHERE state!='sent' AND next_attempt_at<=? AND locked_until<=? ORDER BY next_attempt_at LIMIT 20").bind(now, now).all();
    for (const item of due.results) await deliverOne(env, item.lead_id, sendNotification);
    await env.LEADS_DB.prepare('DELETE FROM rate_buckets WHERE expires_at<?').bind(now).run();
}
