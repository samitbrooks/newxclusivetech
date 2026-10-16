/**
 * ============================================================================
 * Xclusive Tech — Instant Telegram Visitor & Lead Notifier
 * ============================================================================
 * Sends real-time alerts to your Telegram chat whenever a visitor lands on
 * your site, visits key conversion pages (pricing, contact), or submits a lead form.
 *
 * Setup (Takes 1-2 minutes):
 * 1. Open Telegram, search for @BotFather and send: /newbot
 * 2. Follow instructions and copy the HTTP API Token (e.g. "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ")
 * 3. Search for @userinfobot on Telegram, send /start to get your numeric ID (e.g. "987654321")
 * 4. Paste both in TELEGRAM_CONFIG below (or set via window.TelegramTracker.setConfig).
 * ============================================================================
 */

(function () {
    'use strict';

    // CONFIGURATION — Enter your Bot Token and Chat ID here
    const TELEGRAM_CONFIG = {
        botToken: '8817153493:AAGqxeH8zDv_r_mVWxjonYXIdKlrooBLWYM',
        chatId: '8642131404',
        enabled: true,

        // Notification triggers
        notifyOnFirstVisit: true,            // Alert when a new visitor session starts
        notifyOnKeyPages: true,              // Alert when visitor views high-intent pages
        notifyOnFormSubmit: true,            // Alert instantly when contact form is submitted

        // Key high-intent paths that trigger a follow-up alert if viewed
        keyPages: ['/pricing', '/contact', '/frostwoodcrm', '/services', '/solutions'],

        // Cooldown between general session alerts (in minutes) to prevent notification fatigue
        sessionCooldownMinutes: 30,

        // Don't track site owner/admin visits
        ignoreAdmin: true,

        // Debug logging in console
        debug: false
    };

    // Storage keys
    const SESSION_KEY = 'xt_visitor_session';
    const KEY_PAGES_NOTIFIED_KEY = 'xt_keypages_notified';
    const ADMIN_FLAG_KEY = 'xclusive_admin_session';

    // Helper: Escape HTML special chars for Telegram HTML parse_mode
    function escapeHtml(str) {
        if (!str) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    // Helper: Detect Device & Browser
    function getDeviceInfo() {
        const ua = navigator.userAgent || '';
        let device = '💻 Desktop';
        let os = 'Unknown OS';
        let browser = 'Unknown Browser';

        if (/mobile/i.test(ua)) device = '📱 Mobile';
        if (/tablet|ipad/i.test(ua)) device = '📟 Tablet';

        if (/iPhone/i.test(ua)) os = 'iOS (iPhone)';
        else if (/iPad/i.test(ua)) os = 'iPadOS';
        else if (/Android/i.test(ua)) os = 'Android';
        else if (/Macintosh|Mac OS X/i.test(ua)) os = 'macOS';
        else if (/Windows NT/i.test(ua)) os = 'Windows';
        else if (/Linux/i.test(ua)) os = 'Linux';

        if (/Edg\//i.test(ua)) browser = 'Edge';
        else if (/Chrome\//i.test(ua) && !/Chromium|Edg/i.test(ua)) browser = 'Chrome';
        else if (/Safari\//i.test(ua) && !/Chrome/i.test(ua)) browser = 'Safari';
        else if (/Firefox\//i.test(ua)) browser = 'Firefox';

        const screenRes = `${window.screen.width}×${window.screen.height}`;
        return { device, os, browser, screenRes, summary: `${device} (${os} • ${browser})` };
    }

    // Helper: Categorize Referrer / Traffic Source
    function getTrafficSource() {
        const ref = document.referrer;
        if (!ref) return 'Direct / Bookmark / WhatsApp link';

        try {
            const refUrl = new URL(ref);
            const host = refUrl.hostname.toLowerCase();

            // Self navigation
            if (host === window.location.hostname) return 'Internal navigation';

            // Search engines
            if (host.includes('google')) return `🔍 Google Search (${host})`;
            if (host.includes('bing')) return `🔍 Bing Search (${host})`;
            if (host.includes('yahoo')) return `🔍 Yahoo Search`;
            if (host.includes('duckduckgo')) return `🔍 DuckDuckGo`;

            // Social media
            if (host.includes('facebook') || host.includes('fb.com')) return `📘 Facebook`;
            if (host.includes('instagram')) return `📸 Instagram`;
            if (host.includes('tiktok')) return `🎵 TikTok`;
            if (host.includes('linkedin')) return `💼 LinkedIn`;
            if (host.includes('t.co') || host.includes('twitter') || host.includes('x.com')) return `🐦 X / Twitter`;
            if (host.includes('youtube')) return `▶️ YouTube`;
            if (host.includes('whatsapp') || host.includes('wa.me')) return `💬 WhatsApp`;

            return `🌐 ${refUrl.hostname}`;
        } catch (e) {
            return ref.slice(0, 100);
        }
    }

    // Helper: Formatted local time
    function getFormattedTime() {
        try {
            const now = new Date();
            return now.toLocaleString('en-KE', {
                timeZone: 'Africa/Nairobi',
                dateStyle: 'medium',
                timeStyle: 'short'
            }) + ' EAT';
        } catch (e) {
            return new Date().toLocaleTimeString();
        }
    }

    // Helper: Fast IP Geo lookup with fallback and 2.5s strict timeout
    async function getGeoLocation() {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 2500);

        try {
            const res = await fetch('https://ipwho.is/', {
                signal: controller.signal,
                cache: 'no-cache'
            });
            clearTimeout(timeoutId);

            if (res.ok) {
                const data = await res.json();
                if (data && data.success) {
                    const city = data.city || '';
                    const region = data.region || '';
                    const country = data.country || '';
                    const flag = data.country_code ? getFlagEmoji(data.country_code) : '🌍';
                    const isp = data.connection && data.connection.isp ? data.connection.isp : (data.isp || '');

                    const locParts = [city, region, country].filter(Boolean);
                    const locationStr = locParts.length ? locParts.join(', ') : 'Unknown location';
                    return {
                        summary: `${flag} ${locationStr}${isp ? ` (${isp})` : ''}`,
                        city,
                        country,
                        ip: data.ip
                    };
                }
            }
        } catch (e) {
            // Timeout or network blocked
        }

        // Fallback: Browser language + timezone
        try {
            const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
            const lang = navigator.language || '';
            return { summary: `🌍 TimeZone: ${tz} (Lang: ${lang})` };
        } catch (e) {
            return { summary: '🌍 Location unavailable' };
        }
    }

    // Flag emoji converter
    function getFlagEmoji(countryCode) {
        if (!countryCode || countryCode.length !== 2) return '🌍';
        const codePoints = countryCode
            .toUpperCase()
            .split('')
            .map(char => 127397 + char.charCodeAt(0));
        return String.fromCodePoint(...codePoints);
    }

    // Send Telegram API request
    async function sendTelegramAlert(htmlMessage) {
        if (!TELEGRAM_CONFIG.enabled) return { success: false, error: 'Telegram notifications are disabled in settings' };

        const token = TELEGRAM_CONFIG.botToken;
        const chatId = TELEGRAM_CONFIG.chatId;

        if (!token || !chatId || token === 'YOUR_TELEGRAM_BOT_TOKEN' || chatId === 'YOUR_TELEGRAM_CHAT_ID') {
            if (TELEGRAM_CONFIG.debug) {
                console.info('[TelegramTracker] Bot Token or Chat ID not configured. Message not sent:\n', htmlMessage);
            }
            return { success: false, error: 'Bot Token or Chat ID is not configured.' };
        }

        const url = `https://api.telegram.org/bot${token}/sendMessage`;

        try {
            const res = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    chat_id: chatId,
                    text: htmlMessage,
                    parse_mode: 'HTML',
                    disable_web_page_preview: true
                }),
                keepalive: true
            });

            const data = await res.json().catch(() => null);

            if (!res.ok) {
                const desc = (data && data.description) ? data.description : `HTTP error ${res.status}`;
                if (TELEGRAM_CONFIG.debug) {
                    console.warn('[TelegramTracker] Telegram API error:', desc);
                }
                return { success: false, error: desc, status: res.status };
            }

            if (TELEGRAM_CONFIG.debug) {
                console.log('[TelegramTracker] Alert sent successfully.');
            }
            return { success: true, result: data ? data.result : null };
        } catch (err) {
            if (TELEGRAM_CONFIG.debug) {
                console.warn('[TelegramTracker] Failed to send Telegram alert:', err);
            }
            return { success: false, error: err.message || 'Network error' };
        }
    }

    // Main session tracker
    async function trackVisit() {
        const path = window.location.pathname || '/';

        // 1. Ignore admin page and admin users
        if (path.includes('admin.html') || path.includes('/admin')) {
            try { sessionStorage.setItem(ADMIN_FLAG_KEY, 'true'); } catch (e) {}
            return;
        }

        if (TELEGRAM_CONFIG.ignoreAdmin) {
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('notrack') === '1') {
                try {
                    localStorage.setItem(ADMIN_FLAG_KEY, 'true');
                    sessionStorage.setItem(ADMIN_FLAG_KEY, 'true');
                } catch (e) {}
                return;
            }

            try {
                if (sessionStorage.getItem(ADMIN_FLAG_KEY) === 'true' || localStorage.getItem(ADMIN_FLAG_KEY) === 'true') {
                    if (TELEGRAM_CONFIG.debug) console.log('[TelegramTracker] Skipping admin session.');
                    return;
                }
            } catch (e) {}
        }

        // 2. Session cooldown management
        let session = null;
        try {
            const rawSession = sessionStorage.getItem(SESSION_KEY);
            if (rawSession) session = JSON.parse(rawSession);
        } catch (e) {}

        const now = Date.now();
        const cooldownMs = TELEGRAM_CONFIG.sessionCooldownMinutes * 60 * 1000;
        const isNewSession = !session || (now - (session.lastActive || 0) > cooldownMs);

        const pageTitle = document.title || 'Xclusive Tech';
        const pageUrl = window.location.href;
        const trafficSource = getTrafficSource();
        const device = getDeviceInfo();

        // 3. New visitor landing alert
        if (isNewSession && TELEGRAM_CONFIG.notifyOnFirstVisit) {
            const geo = await getGeoLocation();
            const timeStr = getFormattedTime();

            const message = [
                `🔔 <b>New Visitor Landed on Xclusive Tech!</b>`,
                ``,
                `📄 <b>Page:</b> <a href="${escapeHtml(pageUrl)}">${escapeHtml(pageTitle)}</a>`,
                `🌐 <b>Source:</b> ${escapeHtml(trafficSource)}`,
                `🌍 <b>Location:</b> ${escapeHtml(geo.summary)}`,
                `📱 <b>Device:</b> ${escapeHtml(device.summary)} (${device.screenRes})`,
                `🕒 <b>Time:</b> ${escapeHtml(timeStr)}`
            ].join('\n');

            await sendTelegramAlert(message);

            // Save new session state
            try {
                sessionStorage.setItem(SESSION_KEY, JSON.stringify({
                    id: 's_' + Math.random().toString(36).substring(2, 10),
                    startedAt: now,
                    lastActive: now,
                    pagesViewed: 1,
                    initialSource: trafficSource,
                    geoSummary: geo.summary
                }));
            } catch (e) {}

            return;
        }

        // 4. Update ongoing session page view count
        if (session) {
            session.lastActive = now;
            session.pagesViewed = (session.pagesViewed || 1) + 1;
            try { sessionStorage.setItem(SESSION_KEY, JSON.stringify(session)); } catch (e) {}

            // 5. Check if visitor reached a high-intent key page (e.g. /pricing, /contact)
            if (TELEGRAM_CONFIG.notifyOnKeyPages) {
                const isKeyPage = TELEGRAM_CONFIG.keyPages.some(kp => path.toLowerCase().includes(kp));
                if (isKeyPage) {
                    let notifiedKeyPages = [];
                    try {
                        notifiedKeyPages = JSON.parse(sessionStorage.getItem(KEY_PAGES_NOTIFIED_KEY) || '[]');
                    } catch (e) {}

                    // Avoid duplicate alerts for the same key page in the same session
                    if (!notifiedKeyPages.includes(path)) {
                        notifiedKeyPages.push(path);
                        try {
                            sessionStorage.setItem(KEY_PAGES_NOTIFIED_KEY, JSON.stringify(notifiedKeyPages));
                        } catch (e) {}

                        const sessionDurationMinutes = Math.max(1, Math.round((now - (session.startedAt || now)) / 60000));
                        const message = [
                            `👀 <b>High-Intent Visitor on Key Page!</b>`,
                            ``,
                            `📄 <b>Key Page:</b> <a href="${escapeHtml(pageUrl)}">${escapeHtml(pageTitle)}</a>`,
                            `🌍 <b>Location:</b> ${escapeHtml(session.geoSummary || 'Kenya')}`,
                            `📱 <b>Device:</b> ${escapeHtml(device.summary)}`,
                            `⏱️ <b>Engagement:</b> ${session.pagesViewed} pages viewed (${sessionDurationMinutes} min on site)`,
                            `🕒 <b>Time:</b> ${escapeHtml(getFormattedTime())}`
                        ].join('\n');

                        await sendTelegramAlert(message);
                    }
                }
            }
        }
    }

    // Form submission listener
    function attachFormListener() {
        if (!TELEGRAM_CONFIG.notifyOnFormSubmit) return;

        document.addEventListener('submit', function (e) {
            const form = e.target;
            if (!form || form.tagName !== 'FORM') return;

            // Check if this is a contact/lead form
            const isContactForm = form.id === 'contact-form' ||
                form.classList.contains('contact-form') ||
                form.action.includes('contact') ||
                form.querySelector('input[name="name"], input[name="email"], textarea[name="message"]');

            if (!isContactForm) return;

            try {
                const formData = new FormData(form);
                const name = formData.get('name') || formData.get('full_name') || formData.get('fname') || '';
                const email = formData.get('email') || '';
                const phone = formData.get('phone') || formData.get('telephone') || formData.get('tel') || '';
                const service = formData.get('service') || formData.get('package') || formData.get('subject') || '';
                const messageText = formData.get('message') || formData.get('details') || '';

                const alertMessage = [
                    `⚡ <b>NEW LEAD INQUIRY SUBMITTED!</b>`,
                    ``,
                    `👤 <b>Name:</b> ${escapeHtml(name) || 'Not provided'}`,
                    `📧 <b>Email:</b> ${escapeHtml(email) || 'Not provided'}`,
                    `📞 <b>Phone:</b> ${escapeHtml(phone) || 'Not provided'}`,
                    `💼 <b>Service/Budget:</b> ${escapeHtml(service) || 'General inquiry'}`,
                    `💬 <b>Message:</b>\n<i>${escapeHtml(messageText ? messageText.slice(0, 500) : 'No message body')}</i>`,
                    ``,
                    `📄 <b>Page:</b> <a href="${escapeHtml(window.location.href)}">${escapeHtml(document.title)}</a>`,
                    `🕒 <b>Time:</b> ${escapeHtml(getFormattedTime())}`
                ].join('\n');

                sendTelegramAlert(alertMessage);
            } catch (err) {
                if (TELEGRAM_CONFIG.debug) console.warn('[TelegramTracker] Form alert error:', err);
            }
        }, true);
    }

    // Public API for testing and configuration
    window.TelegramTracker = {
        config: TELEGRAM_CONFIG,
        setConfig: function (newConf) {
            Object.assign(TELEGRAM_CONFIG, newConf);
            try {
                if (TELEGRAM_CONFIG.botToken) localStorage.setItem('xt_telegram_bot_token', TELEGRAM_CONFIG.botToken);
                if (TELEGRAM_CONFIG.chatId) localStorage.setItem('xt_telegram_chat_id', TELEGRAM_CONFIG.chatId);
                localStorage.setItem('xt_telegram_enabled', TELEGRAM_CONFIG.enabled ? 'true' : 'false');
                localStorage.setItem('xt_telegram_notify_visit', TELEGRAM_CONFIG.notifyOnFirstVisit ? 'true' : 'false');
                localStorage.setItem('xt_telegram_notify_pages', TELEGRAM_CONFIG.notifyOnKeyPages ? 'true' : 'false');
                localStorage.setItem('xt_telegram_notify_forms', TELEGRAM_CONFIG.notifyOnFormSubmit ? 'true' : 'false');
            } catch (e) {}
            return TELEGRAM_CONFIG;
        },
        sendTest: async function () {
            const timeStr = getFormattedTime();
            const dev = getDeviceInfo();
            const testMsg = [
                `🧪 <b>Xclusive Tech — Telegram Bot Test Alert</b>`,
                ``,
                `✅ <b>Status:</b> Connected & active!`,
                `🕒 <b>Current Time:</b> ${timeStr}`,
                `🌐 <b>Website:</b> ${window.location.origin || 'https://xclusivetech.co.ke'}`,
                `📱 <b>Device:</b> ${escapeHtml(dev.summary)}`,
                ``,
                `You will receive instant alerts whenever someone visits your site or submits an inquiry!`
            ].join('\n');
            return await sendTelegramAlert(testMsg);
        }
    };

    // Auto-restore saved keys from localStorage if present
    try {
        const savedToken = localStorage.getItem('xt_telegram_bot_token');
        const savedChatId = localStorage.getItem('xt_telegram_chat_id');
        const savedEnabled = localStorage.getItem('xt_telegram_enabled');
        const savedNotifyVisit = localStorage.getItem('xt_telegram_notify_visit');
        const savedNotifyPages = localStorage.getItem('xt_telegram_notify_pages');
        const savedNotifyForms = localStorage.getItem('xt_telegram_notify_forms');

        if (savedToken && savedToken !== 'YOUR_TELEGRAM_BOT_TOKEN') TELEGRAM_CONFIG.botToken = savedToken;
        if (savedChatId && savedChatId !== 'YOUR_TELEGRAM_CHAT_ID') TELEGRAM_CONFIG.chatId = savedChatId;
        if (savedEnabled !== null) TELEGRAM_CONFIG.enabled = savedEnabled === 'true';
        if (savedNotifyVisit !== null) TELEGRAM_CONFIG.notifyOnFirstVisit = savedNotifyVisit === 'true';
        if (savedNotifyPages !== null) TELEGRAM_CONFIG.notifyOnKeyPages = savedNotifyPages === 'true';
        if (savedNotifyForms !== null) TELEGRAM_CONFIG.notifyOnFormSubmit = savedNotifyForms === 'true';
    } catch (e) {}

    // Initialize non-blockingly after page load
    function init() {
        attachFormListener();
        // Give 1 second breathing room after page load before sending geo/telegram requests
        setTimeout(trackVisit, 1200);
    }

    if (document.readyState === 'complete') {
        init();
    } else {
        window.addEventListener('load', init);
    }
})();
