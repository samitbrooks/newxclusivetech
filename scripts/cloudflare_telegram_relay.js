/**
 * ============================================================================
 * Cloudflare Worker — Zero-Exposure Telegram Notification Relay
 * ============================================================================
 * 
 * Why use this?
 * - Keeps your Telegram Bot Token 100% hidden on Cloudflare servers.
 * - Visitors never see your bot token in their browser Network tab or JavaScript.
 * - GitHub Secret Scanning will never flag your repository.
 * - Completely free on Cloudflare's free tier (up to 100,000 requests/day).
 *
 * How to deploy in 2 minutes:
 * 1. Log in to your Cloudflare Dashboard -> "Workers & Pages" -> "Create Application" -> "Create Worker".
 * 2. Paste this entire code into the Worker editor.
 * 3. Go to Worker "Settings" -> "Variables" -> "Environment Variables", and add:
 *    - TELEGRAM_BOT_TOKEN : <Your Bot Token from @BotFather>
 *    - TELEGRAM_CHAT_ID   : 8642131404
 * 4. Click "Deploy". Your worker will give you a URL like:
 *    https://telegram-relay.your-subdomain.workers.dev
 * 5. (Optional) In Cloudflare DNS/Workers Routes, you can route it to:
 *    https://xclusivetech.co.ke/api/track
 * ============================================================================
 */

export default {
    async fetch(request, env) {
        // Handle CORS preflight
        if (request.method === 'OPTIONS') {
            return new Response(null, {
                status: 204,
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                }
            });
        }

        if (request.method !== 'POST') {
            return new Response(JSON.stringify({ error: 'Method not allowed' }), {
                status: 405,
                headers: { 'Content-Type': 'application/json' }
            });
        }

        try {
            const body = await request.json();
            const message = body.text || body.message;

            if (!message) {
                return new Response(JSON.stringify({ error: 'Message text required' }), {
                    status: 400,
                    headers: { 'Content-Type': 'application/json' }
                });
            }

            const token = env.TELEGRAM_BOT_TOKEN;
            const chatId = env.TELEGRAM_CHAT_ID || '8642131404';

            if (!token) {
                return new Response(JSON.stringify({ error: 'TELEGRAM_BOT_TOKEN not configured on Worker' }), {
                    status: 500,
                    headers: { 'Content-Type': 'application/json' }
                });
            }

            const telegramRes = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    chat_id: chatId,
                    text: message,
                    parse_mode: 'HTML',
                    disable_web_page_preview: true
                })
            });

            const data = await telegramRes.json();

            return new Response(JSON.stringify(data), {
                status: telegramRes.status,
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            });
        } catch (err) {
            return new Response(JSON.stringify({ error: err.message }), {
                status: 500,
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            });
        }
    }
};
