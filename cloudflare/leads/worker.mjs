import { EmailMessage } from 'cloudflare:email';
import { handleRequest, retryPending } from './service.mjs';

async function notify(lead, env) {
    // Only the fixed, verified site-owner destination can receive notifications.
    const text = `New website enquiry — ${lead.reference}\n\nName: ${lead.name}\nPhone: ${lead.phone}\nEmail: ${lead.email || 'Not provided'}\nCompany: ${lead.company}\nService: ${lead.service}\nBudget: ${lead.budget}\nCounty: ${lead.county}\nForm: ${lead.form_id}\nPage: ${lead.page_path}\n\nProject notes:\n${lead.message}\n\nThis enquiry is safely stored in the Xclusive Tech leads database. Reference: ${lead.reference}`;
    const encoded = btoa(Array.from(new TextEncoder().encode(text), b => String.fromCharCode(b)).join('')).match(/.{1,76}/g).join('\r\n');
    const headers = [`From: Xclusive Tech <${env.SENDER_EMAIL}>`, `To: ${env.NOTIFICATION_TO}`, `Subject: Website enquiry ${lead.reference}`, `Date: ${new Date().toUTCString()}`, `Message-ID: <${lead.id}@xclusivetech.co.ke>`, 'MIME-Version: 1.0', 'Content-Type: text/plain; charset=UTF-8', 'Content-Transfer-Encoding: base64'];
    if (lead.email) headers.push(`Reply-To: ${lead.email}`);
    await env.EMAIL.send(new EmailMessage(env.SENDER_EMAIL, env.NOTIFICATION_TO, headers.join('\r\n') + '\r\n\r\n' + encoded));
}
export default {
    fetch(request, env, ctx) { return handleRequest(request, env, ctx, notify); },
    scheduled(controller, env, ctx) { ctx.waitUntil(retryPending(env, notify)); }
};
