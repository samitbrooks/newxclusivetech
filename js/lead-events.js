/* Intent, attempts and provider responses remain separate measurements. No PII payloads. */
(() => {
    function init() {
        const config = window.XT_MEASUREMENT_CONFIG || {};
        window.dataLayer = window.dataLayer || [];
        const property = config.ga4MeasurementId;
        if (typeof property === 'string' && /^G-[A-Z0-9]+$/.test(property) && typeof window.gtag !== 'function') {
            window.dataLayer = window.dataLayer || [];
            window.gtag = function () { window.dataLayer.push(arguments); };
            window.gtag('js', new Date());
            window.gtag('config', property);
            const loader = document.createElement('script'); loader.async = true;
            loader.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(property)}`;
            document.head.append(loader);
        }
        const params = new URLSearchParams(location.search);
        const county = (params.get('county') || '').replace(/[^a-zA-Z '\-]/g, '').slice(0, 50);
        if (county && location.pathname.includes('contact')) {
            const subject = document.querySelector('#contact-form [name="_subject"]');
            if (subject) subject.value = `Website design enquiry — ${county} County`;
            const form = document.querySelector('#contact-form');
            if (form && !form.querySelector('[name="county"]')) {
                const input = document.createElement('input'); input.type = 'hidden'; input.name = 'county'; input.value = county; form.append(input);
            }
        }
        function track(name, values = {}) {
            const payload = { event: name, page_path: location.pathname, ...values };
            if (typeof window.gtag === 'function') {
                const { event, ...parameters } = payload; window.gtag('event', event, parameters);
            } else {
                window.dataLayer = window.dataLayer || [];
                if (window.dataLayer.length < 100) window.dataLayer.push(payload);
            }
            document.dispatchEvent(new CustomEvent('xt:conversion-intent', { detail: payload }));
        }
        // An experiment is deliberately inactive until a real reporting property is connected.
        let variant = 'control';
        if (config.ctaExperimentEnabled && (property || typeof window.gtag === 'function')) {
            try {
                variant = sessionStorage.getItem(config.ctaExperimentId);
                if (!['written-quote', 'discuss-project'].includes(variant)) {
                    const bytes = new Uint8Array(1); crypto.getRandomValues(bytes);
                    variant = bytes[0] % 2 ? 'written-quote' : 'discuss-project';
                    sessionStorage.setItem(config.ctaExperimentId, variant);
                }
            } catch { variant = 'written-quote'; }
            document.querySelectorAll('[data-quote-label="county-primary"]').forEach(label => {
                label.textContent = variant === 'written-quote' ? 'Get a written quote on WhatsApp' : 'Discuss my website on WhatsApp';
            });
            if (document.querySelector('[data-quote-label="county-primary"]')) track('quote_cta_exposure', { experiment_id: config.ctaExperimentId, variant });
        }
        document.addEventListener('click', event => {
            const link = event.target.closest('a[href]'); if (!link) return;
            const href = link.getAttribute('href'); let method;
            if (/^https?:\/\/(?:wa\.me|api\.whatsapp\.com)\//.test(href)) method = 'whatsapp';
            else if (href.startsWith('tel:')) method = 'phone';
            else if (href.startsWith('mailto:')) method = 'email';
            if (method) track('contact_click', { contact_method: method, variant, link_location: link.closest('header, nav') ? 'navigation' : link.closest('footer') ? 'footer' : 'content' });
        });
        document.addEventListener('submit', event => {
            const form = event.target;
            if (!form.matches('#contact-form, #xt-exit-form, [data-lead-form]') || !form.checkValidity()) return;
            const state = { form_id: form.id, timestamp: Date.now(), variant };
            try { sessionStorage.setItem('xt_last_quote_attempt', JSON.stringify(state)); } catch {}
            track('quote_form_attempt', { form_id: form.id, variant });
        });
        document.addEventListener('xt:lead-saved', event => {
            track('lead_saved', { form_id: event.detail?.form_id || 'xt-exit-form', variant });
            try { sessionStorage.removeItem('xt_last_quote_attempt'); } catch {}
        });
        if (params.get('success') === 'true' && /^XT-\d{8}-[A-F0-9]{12}$/.test(params.get('reference') || '') && location.pathname.includes('contact')) {
            try {
                const state = JSON.parse(sessionStorage.getItem('xt_last_quote_attempt') || 'null');
                if (state && Date.now() - state.timestamp < 30 * 60 * 1000) {
                    track('lead_saved_return', { form_id: state.form_id, variant: state.variant });
                    sessionStorage.removeItem('xt_last_quote_attempt');
                }
            } catch {}
        }
        // Field metrics are measured values, never a manufactured Lighthouse score.
        if (window.webVitals) {
            const report = metric => track('web_vital', { metric_name: metric.name, metric_value: metric.value, metric_rating: metric.rating, non_interaction: true });
            window.webVitals.onLCP(report); window.webVitals.onCLS(report); window.webVitals.onINP(report);
        }
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true }); else init();
})();
