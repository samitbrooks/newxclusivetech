/* First-party enquiry submission. Acknowledgement means durable storage, not inbox delivery. */
(() => {
    const attempts = new Map();
    window.XTLeadAPI = {
        async submit(values, formId) {
            const payload = { ...values, form_id: formId, page_path: location.pathname };
            const signature = JSON.stringify(payload);
            if (!attempts.has(signature)) attempts.set(signature, crypto.randomUUID());
            payload.client_request_id = attempts.get(signature);
            const controller = new AbortController();
            const timer = setTimeout(() => controller.abort(), 20000);
            try {
                const response = await fetch('/api/leads', { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(payload), signal: controller.signal });
                const result = await response.json();
                if (!response.ok || result.success !== true || result.status !== 'saved' || !/^XT-\d{8}-[A-F0-9]{12}$/.test(result.reference || '')) throw new Error(result.error || 'Please retry or use WhatsApp.');
                document.dispatchEvent(new CustomEvent('xt:lead-saved', { detail: { form_id: formId } }));
                return result;
            } finally { clearTimeout(timer); }
        }
    };
    document.addEventListener('submit', async event => {
        const form = event.target;
        if (!form.matches('form[action="/api/leads"]') || !form.checkValidity()) return;
        event.preventDefault();
        if (form.dataset.sending === 'true') return;
        form.dataset.sending = 'true';
        const button = form.querySelector('[type="submit"]');
        const label = button?.textContent;
        if (button) { button.disabled = true; button.textContent = 'Saving enquiry…'; }
        let feedback = form.querySelector('[data-lead-feedback]');
        if (!feedback) { feedback = document.createElement('p'); feedback.dataset.leadFeedback = ''; feedback.setAttribute('role','status'); feedback.style.cssText = 'padding:1rem;margin-top:1rem;white-space:normal'; form.append(feedback); }
        feedback.textContent = '';
        try {
            const result = await window.XTLeadAPI.submit(Object.fromEntries(new FormData(form)), form.id || 'website-enquiry');
            feedback.textContent = `Thank you. Your enquiry is saved. Reference: ${result.reference}. For immediate help, call +254 722 753 819 or use WhatsApp.`;
            feedback.style.color = '#065f46';
            form.reset();
            if (button) button.textContent = 'Enquiry saved';
        } catch {
            feedback.textContent = 'We could not confirm your enquiry was saved. Your details are still here. Please retry, call +254 722 753 819, or use WhatsApp.';
            feedback.style.color = '#991b1b';
            if (button) { button.disabled = false; button.textContent = label || 'Retry enquiry'; }
        } finally { form.dataset.sending = 'false'; }
    });
})();
