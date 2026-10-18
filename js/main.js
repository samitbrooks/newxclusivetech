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
        this.setupTelegramTracker();
        this.setupQuoteEstimator();
    }

    // Dynamic loader for Telegram Visitor Tracker
    static setupTelegramTracker() {
        if (!document.querySelector('script[src*="telegram-tracker.js"]')) {
            const script = document.createElement('script');
            script.src = '/js/telegram-tracker.js';
            script.defer = true;
            document.head.appendChild(script);
        }
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
                            <div class="xt-fast-wa-bar mb-4">
                                <a href="https://wa.me/254722753819?text=Hi%20Samuel,%20I'd%20like%20a%20free%20website%20quote%20for%20my%20business." target="_blank" rel="noopener noreferrer" class="w-full py-3.5 px-4 rounded-xl font-bold text-sm text-white flex items-center justify-center gap-2 text-center shadow-lg transition-all" style="background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important; color: #FFFFFF !important; text-decoration: none !important;">
                                    <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.67-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.076 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421-7.403h-.004c-1.025 0-2.031.313-2.891.893L9.9 4.504C10.742 3.74 11.853 3.3 13.05 3.3c2.969 0 5.387 2.418 5.387 5.387 0 1.197-.46 2.307-1.224 3.15l.531 1.465c.592-.689.956-1.586.956-2.615 0-2.206-1.794-4-4-4zm0 0"/></svg>
                                    <span>⚡ Chat on WhatsApp (+254 722 753 819) — Fastest</span>
                                </a>
                                <div style="display: flex; align-items: center; margin: 12px 0; color: #94A3B8; font-size: 12px; justify-content: center; gap: 8px;">
                                    <span style="height: 1px; background: #E2E8F0; flex: 1;"></span>
                                    <span>or leave your contact for a fast callback</span>
                                    <span style="height: 1px; background: #E2E8F0; flex: 1;"></span>
                                </div>
                            </div>
                            <form id="xt-exit-form" class="xt-exit-form">
                                <div class="xt-form-row xt-form-row-2">
                                    <div class="xt-input-group">
                                        <input type="text" id="xt-exit-name" name="name" required placeholder="Your full name*" class="xt-input">
                                    </div>
                                    <div class="xt-phone-group">
                                        <div class="xt-phone-prefix" title="Kenya (+254)">
                                            <span class="xt-flag">🇰🇪</span>
                                            <span class="xt-caret">▾</span>
                                            <span class="xt-code">+254</span>
                                        </div>
                                        <input type="tel" id="xt-exit-phone" name="phone" required placeholder="Phone / WhatsApp*" class="xt-input xt-input-phone">
                                    </div>
                                </div>

                                <div class="xt-form-row xt-form-row-2">
                                    <div class="xt-input-group">
                                        <input type="email" id="xt-exit-email" name="email" placeholder="Email address (optional)" class="xt-input">
                                    </div>
                                    <div class="xt-select-group">
                                        <select id="xt-exit-service" name="service" class="xt-select">
                                            <option value="" selected>What package do you need?</option>
                                            <option value="Express Sales Landing Page (KES 15K)">Express Sales Landing Page (KES 15K)</option>
                                            <option value="Starter Business Website (KES 25K–45.5K)">Starter Business Website (KES 25K–45.5K)</option>
                                            <option value="Business Growth Web App (KES 49K–62K)">Business Growth Web App (KES 49K–62K)</option>
                                            <option value="M-Pesa E-Commerce Store (KES 72K–85K)">M-Pesa E-Commerce Store (KES 72K–85K)</option>
                                            <option value="Custom Web Platform / SaaS">Custom Web Platform / SaaS</option>
                                            <option value="SEO, GEO & AEO Optimization">SEO, GEO &amp; AEO Optimization</option>
                                        </select>
                                    </div>
                                </div>

                                <div class="xt-form-row">
                                    <textarea id="xt-exit-project" name="project" rows="2" placeholder="Brief note about your business (optional)" class="xt-input xt-textarea"></textarea>
                                </div>

                                <div class="xt-terms-row">
                                    <label class="xt-checkbox-label">
                                        <input type="checkbox" id="xt-exit-terms" name="terms" checked>
                                        <span>I accept the <a href="/terms" target="_blank" rel="noopener">Terms</a> &amp; <a href="/privacy" target="_blank" rel="noopener">Privacy Policy</a>.</span>
                                    </label>
                                </div>

                                <button type="submit" id="xt-exit-submit-btn" class="xt-exit-submit-btn">
                                    <span>REQUEST QUICK CALLBACK &rarr;</span>
                                </button>

                                <p class="xt-exit-security-note">
                                    🛡️ 100% Risk-Free Guarantee &bull; <strong class="xt-secure-highlight">Zero Spam. Direct Engineer Response.</strong>
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

                    if (!nameInput.value.trim() || !phoneInput.value.trim()) {
                        feedbackEl.textContent = 'Please provide your name and WhatsApp/phone number.';
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

    // Setup 1-Minute Interactive Quote Estimator
    static setupQuoteEstimator() {
        const estimator = document.getElementById('quote-estimator');
        if (!estimator) return;

        const pkgCards = estimator.querySelectorAll('.estimator-pkg-card');
        const addonDomain = estimator.querySelector('#addon-domain');
        const addonMaintenance = estimator.querySelector('#addon-maintenance');
        const totalEl = estimator.querySelector('#estimator-total');
        const depositEl = estimator.querySelector('#estimator-deposit');
        const balanceEl = estimator.querySelector('#estimator-balance');
        const pkgNameEl = estimator.querySelector('#estimator-pkg-name');
        const timelineEl = estimator.querySelector('#estimator-timeline');
        const deliverablesListEl = estimator.querySelector('#estimator-deliverables-list');
        const waBtn = estimator.querySelector('#estimator-whatsapp-btn');

        if (!pkgCards.length || !totalEl || !waBtn) return;

        const deliverablesMap = {
            express: [
                '1 High-Converting Long-Form Landing Page (5 Core Sections)',
                'Delivered in 48 Hours (2 Days) with Full Revisions Round',
                'Floating WhatsApp Quick-Chat Widget & Click-to-Call CTAs',
                'Lead Intake Form with Instant Email & Mobile Notifications',
                'Mobile-First Responsive Design Tested on Safaricom 4G/5G',
                '100% Upgrade Credit: Full KES 15,000 credited if upgrading in 6 mos.',
                '100% Source Code & Asset Ownership (Zero builder lock-in fees)'
            ],
            starter: [
                '5 Custom Pages: Home, About Company, Services, Portfolio & Contact',
                'Guaranteed 7-Day Fast Delivery with Milestone Approval Stages',
                'Bespoke Figma UI/UX Design System Tailored to Your Brand Identity',
                'Foundational On-Page SEO (Schema.org markup, meta tags & sitemap)',
                'Interactive Google Maps Location & Google Business Profile Integration',
                '1-Tap WhatsApp Chat & Multi-Field Contact Intake Forms',
                '30 Days Free Post-Launch Technical Support & Automated Cloud Backups',
                '100% Code & Domain Ownership with Direct Server Access'
            ],
            growth: [
                'Up to 15 Bespoke Responsive Pages & High-Performance Templates',
                '10–14 Days Delivery with Dedicated Staging Preview Environment',
                'Lightweight Headless CMS Blog/News Engine for Publishing Articles',
                'Interactive Quote Requests, Service Calculators or Booking Forms',
                'Comprehensive County-by-County Kenya Local SEO & Semantic Schemas',
                'Google Analytics 4 (GA4) & Google Search Console Setup & Verification',
                '90 Days Dedicated Priority Maintenance & Technical Warranty'
            ],
            ecommerce: [
                'Full E-Commerce Storefront with Product Catalog & Categories',
                '14 Days Delivery with End-to-End Real-Time Payment Testing',
                'Automated Safaricom Daraja M-Pesa STK Push Checkout Integration',
                'Credit/Debit Card (Visa/Mastercard) & Bank Payment Gateway Option',
                'Customer Accounts, Order History Dashboard & Automated PDF Invoices',
                'Instant WhatsApp & SMS Notifications to Owner on Every New Order',
                'Inventory Management, Low Stock Alerts & Coupon Promo Code Engine',
                '6 Months Technical Warranty & Merchant Video Training Session'
            ]
        };

        let selectedPrice = 15000;
        let selectedName = 'Express Sales Landing Page';
        let selectedTime = '2 Days (48 Hours)';
        let selectedKey = 'express';

        const updateDeliverables = (key) => {
            if (!deliverablesListEl) return;
            const items = [...(deliverablesMap[key] || deliverablesMap.express)];
            if (addonDomain && addonDomain.checked) {
                items.push('Custom .co.ke Domain Registration & 3 Branded Business Webmail Accounts');
            }
            if (addonMaintenance && addonMaintenance.checked) {
                items.push('Monthly Maintenance Care Plan (Daily Cloud Backups, Security Scans & Updates)');
            }
            deliverablesListEl.innerHTML = items.map(item => `
                <li class="estimator-deliverable-item">
                    <svg fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
                    <span>${item}</span>
                </li>
            `).join('');
        };

        const calculate = () => {
            let total = selectedPrice;
            let addonsList = [];

            if (addonDomain && addonDomain.checked) {
                total += 2500;
                addonsList.push('Domain & Business Emails (+KES 2,500)');
            }
            if (addonMaintenance && addonMaintenance.checked) {
                total += 2000;
                addonsList.push('Monthly Care Plan (+KES 2,000)');
            }

            const deposit = Math.round(total * 0.5);
            const balance = total - deposit;

            totalEl.textContent = `KES ${total.toLocaleString()}`;
            if (depositEl) depositEl.textContent = `KES ${deposit.toLocaleString()}`;
            if (balanceEl) balanceEl.textContent = `KES ${balance.toLocaleString()}`;
            if (pkgNameEl) pkgNameEl.textContent = selectedName;
            if (timelineEl) timelineEl.textContent = selectedTime;

            updateDeliverables(selectedKey);

            // Generate WhatsApp conversion link with pre-filled message
            let waMsg = `Hi Samuel, I used your website price calculator on Xclusive Tech:\n\n• Package: ${selectedName} (KES ${selectedPrice.toLocaleString()})\n• Turnaround: ${selectedTime}`;
            if (addonsList.length > 0) {
                waMsg += `\n• Add-ons: ${addonsList.join(', ')}`;
            }
            waMsg += `\n• Total: KES ${total.toLocaleString()} (50% deposit: KES ${deposit.toLocaleString()})\n• Deliverables: ${selectedKey === 'express' ? 'Landing page in 2 days' : 'Website in 7 days'}, 100% ownership & approval before final balance.\n\nCan you confirm your availability to get started?`;

            waBtn.href = `https://wa.me/254722753819?text=${encodeURIComponent(waMsg)}`;
        };

        pkgCards.forEach(card => {
            card.addEventListener('click', () => {
                pkgCards.forEach(c => c.classList.remove('is-selected'));
                card.classList.add('is-selected');

                const radio = card.querySelector('input[type="radio"]');
                if (radio) radio.checked = true;

                selectedPrice = parseInt(card.getAttribute('data-price') || '15000', 10);
                selectedName = card.getAttribute('data-name') || 'Express Sales Landing Page';
                selectedTime = card.getAttribute('data-time') || '2 Days (48 Hours)';
                selectedKey = card.getAttribute('data-pkg') || 'express';

                calculate();
            });
        });

        if (addonDomain) addonDomain.addEventListener('change', calculate);
        if (addonMaintenance) addonMaintenance.addEventListener('change', calculate);

        // Initial calculation and deliverables render
        calculate();
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
