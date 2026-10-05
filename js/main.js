/* ============================================
   XCLUSIVETECH MAIN SCRIPT
   Global functionality and utilities
   ============================================ */

// Global utility functions
class XclusiveTech {
    // Initialize app
    static init() {
        this.setupThemeToggle();
        this.setupEventListeners();
        this.setupFormHandling();
        this.checkQueryParams();
        this.optimizePerformance();
        this.setupSmartExitIntent();
        this.setupTypewriter();
    }

    // Theme enforcement (Strict Light Mode)
    static setupThemeToggle() {
        try {
            window.localStorage.removeItem('xclusive_theme');
            document.documentElement.removeAttribute('data-theme');
            document.documentElement.classList.remove('dark');
        } catch (e) {}
        document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
            btn.style.display = 'none';
        });
    }
    
    // Setup event listeners
    static setupEventListeners() {
        // Button ripple effect
        document.querySelectorAll('button, a.btn').forEach(button => {
            button.addEventListener('click', (e) => {
                this.createRipple(e);
            });
        });
        
        // Link navigation tracking (for analytics)
        document.querySelectorAll('a[href^="http"]').forEach(link => {
            link.addEventListener('click', () => {
                this.trackEvent('outbound-link', link.href);
            });
        });
    }
    
    // Setup form handling
    static setupFormHandling() {
        const contactForm = document.getElementById('contact-form');
        if (contactForm) {
            contactForm.addEventListener('submit', (e) => {
                const shouldUseNativeSubmit = contactForm.action && contactForm.method.toLowerCase() === 'post';
                const formData = new FormData(contactForm);
                const data = {
                    name: formData.get('name'),
                    email: formData.get('email'),
                    subject: formData.get('subject'),
                    message: formData.get('message'),
                    service: formData.get('service')
                };

                if (!this.validateForm(data)) {
                    e.preventDefault();
                    alert('Please fill in all required fields');
                    return;
                }

                if (shouldUseNativeSubmit) {
                    return;
                }

                e.preventDefault();
                this.handleFormSubmit(contactForm);
            });
        }
    }
    
    // Handle form submission
    static handleFormSubmit(form) {
        const formData = new FormData(form);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            subject: formData.get('subject'),
            message: formData.get('message'),
            service: formData.get('service')
        };
        
        // Validate form
        if (!this.validateForm(data)) {
            alert('Please fill in all required fields');
            return;
        }
        
        // Show success message (in production, send to backend)
        this.showSuccessMessage(form);
        form.reset();
        
        // Log for demonstration
        console.log('Form submitted:', data);
        
        // In production, you would send this to a backend API:
        // fetch('/api/contact', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify(data)
        // })
    }
    
    // Validate form
    static validateForm(data) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return data.name && data.email && emailRegex.test(data.email) && data.message;
    }
    
    // Show success message
    static showSuccessMessage(form) {
        const successMsg = form.querySelector('#success-message');
        if (successMsg) {
            successMsg.classList.remove('hidden');
            setTimeout(() => {
                successMsg.classList.add('hidden');
            }, 5000);
        }
    }
    
    // Create ripple effect on button click
    static createRipple(e) {
        const button = e.target.closest('button, a.btn');
        if (!button) return;
        
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        button.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    }
    
    // Track events (for analytics integration)
    static trackEvent(eventName, eventValue) {
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, { value: eventValue });
        }
        console.log(`Event tracked: ${eventName} - ${eventValue}`);
    }
    
    // Performance optimization
    static optimizePerformance() {
        // Lazy load images
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                        }
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
        
        // Defer non-critical resources
        this.deferNonCriticalResources();
    }
    
    // Defer non-critical resources
    static deferNonCriticalResources() {
        // Load web fonts asynchronously
        if (document.fonts) {
            document.fonts.ready.then(() => {
                document.documentElement.classList.add('fonts-loaded');
            });
        }
    }
    
    // Utility: Get element position
    static getElementPosition(element) {
        const rect = element.getBoundingClientRect();
        return {
            top: rect.top + window.scrollY,
            left: rect.left + window.scrollX,
            width: rect.width,
            height: rect.height
        };
    }
    
    // Utility: Check if element is in viewport
    static isElementInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }
    
    // Utility: Get query parameters
    static getQueryParams() {
        const params = {};
        new URLSearchParams(window.location.search).forEach((value, key) => {
            params[key] = value;
        });
        return params;
    }

    // Show success message if redirected after native submit
    static checkQueryParams() {
        const params = this.getQueryParams();
        if (params.success === 'true') {
            const contactForm = document.getElementById('contact-form');
            if (contactForm) {
                this.showSuccessMessage(contactForm);
                contactForm.reset();
            }
        }
    }

    // Smart Exit-Intent Form Modal (Patterned after davidesabwa design)
    static setupSmartExitIntent() {
        let isArmed = false;
        let hasTriggered = false;

        // Check if already submitted or dismissed cooldown
        const isCooldownActive = () => {
            try {
                if (window.localStorage && window.localStorage.getItem('xt_exit_intent_submitted') === 'true') {
                    return true;
                }
                if (window.sessionStorage && window.sessionStorage.getItem('xt_exit_intent_dismissed') === 'true') {
                    return true;
                }
                const closedTimestamp = window.localStorage && window.localStorage.getItem('xt_exit_intent_closed_time');
                if (closedTimestamp && Date.now() - parseInt(closedTimestamp, 10) < 24 * 60 * 60 * 1000) {
                    return true; // Suppress for 24h after explicit dismissal
                }
            } catch (e) {}
            return false;
        };

        // Delay arming exit-intent for 5 seconds to prevent premature annoyance
        setTimeout(() => {
            isArmed = true;
        }, 5000);

        const openModal = (force = false) => {
            if (!force && (hasTriggered || isCooldownActive())) return;
            hasTriggered = true;

            // Remove trigger listeners
            document.documentElement.removeEventListener('mouseleave', handleMouseLeave);
            document.documentElement.removeEventListener('mousemove', handleMouseMove);
            window.removeEventListener('scroll', handleMobileScroll);

            let existingOverlay = document.getElementById('xt-exit-modal-overlay');
            if (existingOverlay) {
                existingOverlay.classList.add('xt-exit-visible');
                document.body.style.overflow = 'hidden';
                return;
            }

            const modalOverlay = document.createElement('div');
            modalOverlay.id = 'xt-exit-modal-overlay';
            modalOverlay.className = 'xt-exit-overlay';
            modalOverlay.setAttribute('role', 'dialog');
            modalOverlay.setAttribute('aria-modal', 'true');
            modalOverlay.setAttribute('aria-labelledby', 'xt-exit-title');

            modalOverlay.innerHTML = `
                <div class="xt-exit-modal-card">
                    <button type="button" class="xt-exit-close-btn" id="xt-exit-close-btn" aria-label="Close dialog">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="18" y1="6" x2="6" y2="18"></line>
                            <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                    </button>

                    <div class="xt-exit-grid">
                        <!-- Left Column: Value Prop & Badges -->
                        <div class="xt-exit-left">
                            <h2 id="xt-exit-title" class="xt-exit-headline">
                                Tell us what you're building<br>
                                <span class="xt-exit-headline-accent">We'll make it smarter.</span>
                            </h2>

                            <ul class="xt-exit-checklist">
                                <li>
                                    <span class="xt-check-icon">✓</span>
                                    <span>Shape your vision into something smart, secure &amp; scalable.</span>
                                </li>
                                <li>
                                    <span class="xt-check-icon">✓</span>
                                    <span>Talk directly with our founder about your goals.</span>
                                </li>
                                <li>
                                    <span class="xt-check-icon">✓</span>
                                    <span>Define milestones and success metrics together.</span>
                                </li>
                                <li>
                                    <span class="xt-check-icon">✓</span>
                                    <span>We help you pick the best stack for your project.</span>
                                </li>
                                <li>
                                    <span class="xt-check-icon">✓</span>
                                    <span>A custom plan with timeline, budget &amp; solutions — free.</span>
                                </li>
                            </ul>

                            <div class="xt-exit-badges-grid">
                                <!-- Badge 1: WordPress & Woo -->
                                <div class="xt-exit-badge-pill">
                                    <div class="xt-badge-icons-duo">
                                        <svg class="xt-badge-svg" viewBox="0 0 24 24" width="16" height="16" fill="#21759B" aria-label="WordPress">
                                            <path d="M12 2C6.48 2 2 6.48 2 12c0 4.42 2.87 8.17 6.84 9.49L3.74 7.51A9.97 9.97 0 0 1 12 4c2.08 0 4.02.64 5.61 1.73L12 2zm8.26 5.74A9.96 9.96 0 0 1 22 12c0 2.22-.72 4.28-1.95 5.94l-4.53-13.11a9.98 9.98 0 0 1 4.74 2.91zM12 22a9.95 9.95 0 0 1-5.07-1.38l5.07-14.74 5.23 14.8A9.94 9.94 0 0 1 12 22zm-7.66-9.5c0-.85.31-1.45.57-1.92.35-.61.69-1.2.69-1.85 0-.73-.55-1.4-1.33-1.4-.06 0-.13.01-.19.02A9.95 9.95 0 0 0 2.06 12c0 1.26.23 2.46.66 3.58l1.62-3.08zm9.5 4.79l-3.33-9.66c.31-.02.6-.05.89-.05.38 0 1.23-.05 1.23-.05.38 0 .43-.57.04-.57 0 0-.85.05-1.49.05-.6 0-1.49-.05-1.49-.05-.38 0-.34.57.04.57 0 0 .81.05 1.19.05l1.77 5.28-2.5 7.5a9.95 9.95 0 0 0 3.65-.07z"/>
                                        </svg>
                                        <svg class="xt-badge-svg" viewBox="0 0 24 24" width="18" height="13" fill="#96588A" aria-label="WooCommerce">
                                            <path d="M2.5 5.5C1.67 5.5 1 6.17 1 7v7c0 .83.67 1.5 1.5 1.5h1.2v2.8c0 .4.46.63.78.38l3.42-3.18H18c.83 0 1.5-.67 1.5-1.5V7c0-.83-.67-1.5-1.5-1.5H2.5zm3.2 6.8c-.8 0-1.4-.7-1.4-1.6s.6-1.6 1.4-1.6c.8 0 1.4.7 1.4 1.6s-.6 1.6-1.4 1.6zm4.8 0c-.8 0-1.4-.7-1.4-1.6s.6-1.6 1.4-1.6c.8 0 1.4.7 1.4 1.6s-.6 1.6-1.4 1.6zm4.8 0c-.8 0-1.4-.7-1.4-1.6s.6-1.6 1.4-1.6c.8 0 1.4.7 1.4 1.6s-.6 1.6-1.4 1.6zm5.2-6.8h1.8c.83 0 1.5.67 1.5 1.5v7c0 .83-.67 1.5-1.5 1.5h-.8v2.4c0 .35-.4.55-.68.33l-2.62-2.43-.2-.3h2.5V7h-1.5V5.5z"/>
                                        </svg>
                                    </div>
                                    <span class="xt-badge-title">WordPress &amp; Woo</span>
                                </div>

                                <!-- Badge 2: M-PESA -->
                                <div class="xt-exit-badge-pill xt-badge-mpesa">
                                    <span class="xt-mpesa-tag">M-PESA</span>
                                    <span class="xt-badge-sub">Daraja 2.0 API</span>
                                </div>

                                <!-- Badge 3: 95+ PageSpeed -->
                                <div class="xt-exit-badge-pill xt-badge-speed">
                                    <span class="xt-speed-score">95+</span>
                                    <span class="xt-badge-sub">PageSpeed</span>
                                </div>

                                <!-- Badge 4: Digitally Fit '26 -->
                                <div class="xt-exit-badge-pill xt-badge-award">
                                    <span class="xt-badge-trophy">🏆</span>
                                    <span class="xt-badge-sub font-semibold">Digitally Fit '26</span>
                                </div>
                            </div>

                            <div class="xt-exit-reviews-grid">
                                <div class="xt-exit-review-card">
                                    <div class="xt-review-stars">★★★★★</div>
                                    <div class="xt-review-text"><strong>5.0</strong> Based on 202+ reviews</div>
                                </div>
                                <div class="xt-exit-award-card">
                                    <div class="xt-award-badge-tag">AWARD WINNER</div>
                                    <div class="xt-award-text">Digitally Fit Awards 2026</div>
                                </div>
                            </div>
                        </div>

                        <!-- Right Column: Form -->
                        <div class="xt-exit-right">
                            <form id="xt-exit-form" class="xt-exit-form">
                                <div class="xt-form-row xt-form-row-2">
                                    <div class="xt-input-group">
                                        <input type="text" id="xt-exit-name" name="name" required placeholder="Full name*" class="xt-input">
                                    </div>
                                    <div class="xt-input-group">
                                        <input type="email" id="xt-exit-email" name="email" required placeholder="Email*" class="xt-input">
                                    </div>
                                </div>

                                <div class="xt-form-row xt-form-row-2">
                                    <div class="xt-phone-group">
                                        <div class="xt-phone-prefix" title="Kenya (+254)">
                                            <span class="xt-flag">🇰🇪</span>
                                            <span class="xt-caret">▾</span>
                                            <span class="xt-code">+254</span>
                                        </div>
                                        <input type="tel" id="xt-exit-phone" name="phone" required placeholder="Phone*" class="xt-input xt-input-phone">
                                    </div>
                                    <div class="xt-input-group">
                                        <input type="text" id="xt-exit-company" name="company" placeholder="Company" class="xt-input">
                                    </div>
                                </div>

                                <div class="xt-form-row xt-form-row-2">
                                    <div class="xt-select-group">
                                        <select id="xt-exit-service" name="service" class="xt-select">
                                            <option value="" selected>Service interested in (option...</option>
                                            <option value="Express Sales Landing Page (KES 15K)">Express Sales Landing Page (KES 15K)</option>
                                            <option value="Starter Business Website (KES 25K–45.5K)">Starter Business Website (KES 25K–45.5K)</option>
                                            <option value="Business Growth Web App (KES 49K–62K)">Business Growth Web App (KES 49K–62K)</option>
                                            <option value="M-Pesa E-Commerce Store (KES 72K–85K)">M-Pesa E-Commerce Store (KES 72K–85K)</option>
                                            <option value="Custom Web Platform / SaaS">Custom Web Platform / SaaS</option>
                                            <option value="SEO, GEO & AEO Optimization">SEO, GEO &amp; AEO Optimization</option>
                                        </select>
                                    </div>
                                    <div class="xt-select-group">
                                        <select id="xt-exit-budget" name="budget" class="xt-select">
                                            <option value="" selected>Budget range (optional)</option>
                                            <option value="KES 15,000 – KES 25,000">KES 15,000 – KES 25,000</option>
                                            <option value="KES 25,000 – KES 50,000">KES 25,000 – KES 50,000</option>
                                            <option value="KES 50,000 – KES 100,000">KES 50,000 – KES 100,000</option>
                                            <option value="KES 100,000+">KES 100,000+</option>
                                            <option value="Flexible / Need Consultation">Flexible / Need Consultation</option>
                                        </select>
                                    </div>
                                </div>

                                <div class="xt-form-row">
                                    <textarea id="xt-exit-project" name="project" required rows="3" placeholder="Tell us about your project*" class="xt-input xt-textarea"></textarea>
                                </div>

                                <div class="xt-terms-row">
                                    <label class="xt-checkbox-label">
                                        <input type="checkbox" id="xt-exit-terms" name="terms" required checked>
                                        <span>I accept the <a href="/terms" target="_blank" rel="noopener">Terms &amp; Conditions</a> and <a href="/privacy" target="_blank" rel="noopener">Privacy Policy</a>.</span>
                                    </label>
                                </div>

                                <button type="submit" id="xt-exit-submit-btn" class="xt-exit-submit-btn">
                                    <span>SUBMIT &rarr;</span>
                                </button>

                                <p class="xt-exit-security-note">
                                    All our projects are secured by NDA. <strong class="xt-secure-highlight">100% Secure. Zero Spam.</strong>
                                </p>

                                <div id="xt-exit-feedback" class="xt-exit-feedback" style="display: none;"></div>
                            </form>

                            <!-- Success State -->
                            <div id="xt-exit-success" class="xt-exit-success" style="display: none;">
                                <div class="xt-success-icon">✓</div>
                                <h3 class="xt-success-title">Inquiry Received!</h3>
                                <p class="xt-success-desc">Thank you. Samuel Kidemi and our Nairobi engineering team will review your project details and respond with a custom roadmap within 2 hours.</p>
                                <a href="https://wa.me/254722753819?text=Hi%20Samuel%2C%20I%20just%20submitted%20my%20project%20details%20on%20Xclusive%20Tech." target="_blank" rel="noopener noreferrer" class="xt-success-whatsapp-btn">
                                    <span>Chat Directly on WhatsApp</span>
                                    <span>&rarr;</span>
                                </a>
                                <button type="button" class="xt-success-done-btn" id="xt-exit-done-btn">Close Window</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            document.body.appendChild(modalOverlay);

            requestAnimationFrame(() => {
                modalOverlay.classList.add('xt-exit-visible');
            });

            // Prevent background scrolling while modal is open
            document.body.style.overflow = 'hidden';

            const closeModal = () => {
                modalOverlay.classList.remove('xt-exit-visible');
                document.body.style.overflow = '';
                try {
                    if (window.sessionStorage) {
                        window.sessionStorage.setItem('xt_exit_intent_dismissed', 'true');
                    }
                    if (window.localStorage) {
                        window.localStorage.setItem('xt_exit_intent_closed_time', Date.now().toString());
                    }
                } catch (e) {}

                setTimeout(() => {
                    if (modalOverlay.parentNode) {
                        modalOverlay.parentNode.removeChild(modalOverlay);
                    }
                }, 300);
            };

            // Event Listeners for Closing
            const closeBtn = modalOverlay.querySelector('#xt-exit-close-btn');
            const doneBtn = modalOverlay.querySelector('#xt-exit-done-btn');
            if (closeBtn) closeBtn.addEventListener('click', closeModal);
            if (doneBtn) doneBtn.addEventListener('click', closeModal);

            modalOverlay.addEventListener('click', (e) => {
                if (e.target === modalOverlay) closeModal();
            });

            const handleEsc = (e) => {
                if (e.key === 'Escape') {
                    closeModal();
                    document.removeEventListener('keydown', handleEsc);
                }
            };
            document.addEventListener('keydown', handleEsc);

            // Form Submit Handling
            const exitForm = modalOverlay.querySelector('#xt-exit-form');
            const feedbackEl = modalOverlay.querySelector('#xt-exit-feedback');
            const submitBtn = modalOverlay.querySelector('#xt-exit-submit-btn');
            const successEl = modalOverlay.querySelector('#xt-exit-success');

            if (exitForm) {
                exitForm.addEventListener('submit', async (e) => {
                    e.preventDefault();

                    const nameInput = modalOverlay.querySelector('#xt-exit-name');
                    const emailInput = modalOverlay.querySelector('#xt-exit-email');
                    const phoneInput = modalOverlay.querySelector('#xt-exit-phone');
                    const companyInput = modalOverlay.querySelector('#xt-exit-company');
                    const serviceSelect = modalOverlay.querySelector('#xt-exit-service');
                    const budgetSelect = modalOverlay.querySelector('#xt-exit-budget');
                    const projectInput = modalOverlay.querySelector('#xt-exit-project');
                    const termsInput = modalOverlay.querySelector('#xt-exit-terms');

                    if (!nameInput.value.trim() || !emailInput.value.trim() || !phoneInput.value.trim() || !projectInput.value.trim()) {
                        feedbackEl.textContent = 'Please fill in all required fields marked with *.';
                        feedbackEl.className = 'xt-exit-feedback error';
                        feedbackEl.style.display = 'block';
                        return;
                    }

                    if (!termsInput.checked) {
                        feedbackEl.textContent = 'Please accept the Terms & Conditions and Privacy Policy.';
                        feedbackEl.className = 'xt-exit-feedback error';
                        feedbackEl.style.display = 'block';
                        return;
                    }

                    // Format phone number
                    let cleanPhone = phoneInput.value.replace(/\s+/g, '');
                    if (cleanPhone.startsWith('0')) {
                        cleanPhone = '+254' + cleanPhone.substring(1);
                    } else if (!cleanPhone.startsWith('+')) {
                        cleanPhone = '+254' + cleanPhone;
                    }

                    submitBtn.disabled = true;
                    submitBtn.innerHTML = `<span>SUBMITTING...</span>`;
                    feedbackEl.style.display = 'none';

                    const payload = {
                        name: nameInput.value.trim(),
                        email: emailInput.value.trim(),
                        phone: cleanPhone,
                        company: companyInput.value.trim() || 'N/A',
                        service: serviceSelect.value || 'Not specified',
                        budget: budgetSelect.value || 'Not specified',
                        project_details: projectInput.value.trim(),
                        _subject: `⚡ Smart Exit-Intent Lead: ${nameInput.value.trim()} (${cleanPhone})`,
                        _captcha: 'false'
                    };

                    try {
                        await fetch('https://formsubmit.co/ajax/hello@xclusivetech.co.ke', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Accept': 'application/json'
                            },
                            body: JSON.stringify(payload)
                        });

                        try {
                            if (window.localStorage) {
                                window.localStorage.setItem('xt_exit_intent_submitted', 'true');
                            }
                        } catch (err) {}

                        // Switch to Success State
                        exitForm.style.display = 'none';
                        successEl.style.display = 'flex';

                        // Pre-populate WhatsApp button link
                        const waBtn = successEl.querySelector('.xt-success-whatsapp-btn');
                        if (waBtn) {
                            const waText = encodeURIComponent(`Hi Samuel, I just submitted an inquiry on Xclusive Tech for ${payload.name} (${payload.phone}). Service: ${payload.service}.`);
                            waBtn.href = `https://wa.me/254722753819?text=${waText}`;
                        }
                    } catch (err) {
                        try {
                            if (window.localStorage) {
                                window.localStorage.setItem('xt_exit_intent_submitted', 'true');
                            }
                        } catch (e) {}

                        exitForm.style.display = 'none';
                        successEl.style.display = 'flex';
                    }
                });
            }
        };

        // Expose global methods for testing or direct button invocation
        window.openSmartExitIntent = () => openModal(true);
        window.openExitIntentModal = () => openModal(true);
        window.resetExitIntent = () => {
            try {
                if (window.localStorage) {
                    window.localStorage.removeItem('xt_exit_intent_submitted');
                    window.localStorage.removeItem('xt_exit_intent_closed_time');
                }
                if (window.sessionStorage) {
                    window.sessionStorage.removeItem('xt_exit_intent_dismissed');
                }
                console.log('Xclusive Tech Exit-Intent Reset: Cooldown cleared.');
            } catch (e) {}
        };

        // Check URL parameters for immediate preview / testing (?exit_intent=1 or ?quote=1)
        try {
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('exit_intent') === '1' || urlParams.get('quote') === '1' || urlParams.get('smart_form') === '1' || urlParams.get('preview_form') === '1') {
                setTimeout(() => openModal(true), 400);
            }
        } catch (e) {}

        // Listen for clicks on any quote/inquiry buttons configured for the modal
        document.addEventListener('click', (e) => {
            const trigger = e.target.closest('[data-open-exit-modal], .js-smart-exit-trigger, [href="#smart-quote"], [href="#exit-modal"]');
            if (trigger) {
                e.preventDefault();
                openModal(true);
            }
        });

        // Desktop: Mouse leaves viewport towards the top
        const handleMouseLeave = (e) => {
            if (!isArmed || hasTriggered) return;
            // Check if cursor moved out of top window boundary
            if (e.clientY <= 25) {
                openModal();
            }
        };

        // Desktop: Fast upward mouse movement towards top boundary
        const handleMouseMove = (e) => {
            if (!isArmed || hasTriggered) return;
            if (e.clientY <= 45 && e.movementY < -10) {
                openModal();
            }
        };

        // Mobile: Scroll down past 30%, then rapid scroll up
        let lastScrollY = window.scrollY;
        let maxScrollY = 0;

        const handleMobileScroll = () => {
            if (!isArmed || hasTriggered) return;

            const currentScrollY = window.scrollY;
            if (currentScrollY > maxScrollY) {
                maxScrollY = currentScrollY;
            }

            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            if (docHeight > 0) {
                const scrolledPercent = (maxScrollY / docHeight) * 100;
                // If user scrolled down past 30% and rapidly scrolls up > 80px
                if (scrolledPercent >= 30 && (lastScrollY - currentScrollY > 80)) {
                    openModal();
                }
            }

            lastScrollY = currentScrollY;
        };

        // Mobile / Inactive Dwell fallback: If user is on page for 45s and scrolled
        setTimeout(() => {
            if (isArmed && !hasTriggered) {
                if (window.scrollY > 250) {
                    openModal();
                }
            }
        }, 45000);

        document.documentElement.addEventListener('mouseleave', handleMouseLeave);
        document.documentElement.addEventListener('mousemove', handleMouseMove, { passive: true });
        window.addEventListener('scroll', handleMobileScroll, { passive: true });
    }

    // Setup Rotating Typewriter Effect
    static setupTypewriter() {
        const target = document.querySelector('.hero-typewriter-target');
        if (!target) return;

        // Respect reduced motion preference
        if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            return;
        }

        const textSpan = target.querySelector('.typewriter-text');
        if (!textSpan) return;

        let words = [];
        try {
            const raw = target.getAttribute('data-words');
            if (raw) words = JSON.parse(raw);
        } catch (e) {
            console.warn('Typewriter data-words parsing error:', e);
        }

        if (!words || words.length <= 1) return;

        let wordIndex = 0;
        let charIndex = words[0].length;
        let isDeleting = false;
        const typingSpeed = 65; // ms per char when typing
        const deletingSpeed = 35; // ms per char when backspacing
        const holdDelay = 2800; // ms pause with full word
        const nextWordDelay = 400; // ms pause before typing next word

        const tick = () => {
            const currentWord = words[wordIndex];

            if (isDeleting) {
                charIndex--;
                textSpan.textContent = currentWord.substring(0, charIndex);
            } else {
                charIndex++;
                textSpan.textContent = currentWord.substring(0, charIndex);
            }

            let delay = isDeleting ? deletingSpeed : typingSpeed;

            if (!isDeleting && charIndex === currentWord.length) {
                delay = holdDelay;
                isDeleting = true;
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                wordIndex = (wordIndex + 1) % words.length;
                delay = nextWordDelay;
            }

            setTimeout(tick, delay);
        };

        // Pause initially so visitor reads the primary SEO phrase first
        setTimeout(() => {
            isDeleting = true;
            tick();
        }, holdDelay);
    }

    // Utility: Store in localStorage
    static localStorage(action, key, value = null) {
        try {
            if (action === 'set') {
                window.localStorage.setItem(key, JSON.stringify(value));
            } else if (action === 'get') {
                return JSON.parse(window.localStorage.getItem(key));
            } else if (action === 'remove') {
                window.localStorage.removeItem(key);
            }
        } catch (e) {
            console.warn('localStorage error:', e);
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    XclusiveTech.init();
});

// Performance monitoring
if ('PerformanceObserver' in window) {
    try {
        const perfObserver = new PerformanceObserver((entryList) => {
            for (const entry of entryList.getEntries()) {
                console.log(`Performance - ${entry.name}: ${entry.duration.toFixed(2)}ms`);
            }
        });
        perfObserver.observe({ entryTypes: ['navigation', 'resource'] });
    } catch (e) {
        console.warn('Performance observer error:', e);
    }
}

// Service Worker Registration (for PWA)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(err => {
            console.warn('Service Worker registration failed:', err);
        });
    });
}
