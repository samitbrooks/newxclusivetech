/* Conversion intent hooks. No analytics requests are sent without a configured provider. */
(() => {
    function init() {
        const params = new URLSearchParams(location.search);
        const county = (params.get('county') || '').replace(/[^a-zA-Z '\-]/g, '').slice(0, 50);
        if (county && location.pathname.includes('contact')) {
            const subject = document.querySelector('#contact-form [name="_subject"]');
            if (subject) {
                subject.value = `Website design enquiry — ${county} County`;
                const form = document.querySelector('#contact-form');
                if (form && !form.querySelector('[name="county"]')) {
                    const input = document.createElement('input'); input.type = 'hidden'; input.name = 'county'; input.value = county; form.append(input);
                }
            }
        }
        function track(name, values) {
            const payload = { event: name, page_path: location.pathname, ...values };
            if (typeof window.gtag === 'function') {
                const { event, ...parameters } = payload; window.gtag('event', event, parameters);
            } else {
                window.dataLayer = window.dataLayer || []; window.dataLayer.push(payload);
            }
            document.dispatchEvent(new CustomEvent('xt:conversion-intent', { detail: payload }));
        }
        document.addEventListener('click', event => {
            const link = event.target.closest('a[href]'); if (!link) return;
            const href = link.getAttribute('href');
            let method;
            if (/^https?:\/\/(?:wa\.me|api\.whatsapp\.com)\//.test(href)) method = 'whatsapp';
            else if (href.startsWith('tel:')) method = 'phone';
            else if (href.startsWith('mailto:')) method = 'email';
            if (method) track('contact_click', { contact_method: method, link_location: link.closest('header, nav') ? 'navigation' : link.closest('footer') ? 'footer' : 'content' });
        });
        document.addEventListener('submit', event => {
            if (!event.target.matches('#contact-form, #xt-exit-form')) return;
            if (event.target.checkValidity()) track('quote_form_attempt', { form_id: event.target.id });
        });
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true }); else init();
})();
