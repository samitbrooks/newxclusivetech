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
        this.setupScrollQuotePopup();
    }

    // Setup Theme Toggle (Light / Dark mode)
    static setupThemeToggle() {
        const THEME_KEY = 'xclusive_theme';
        const getPreferredTheme = () => {
            try {
                const stored = window.localStorage.getItem(THEME_KEY);
                if (stored === 'dark') return 'dark';
                if (stored === 'light') return 'light';
            } catch (e) {}
            return 'light'; // Always default to light mode
        };

        const updateToggleButtons = (theme) => {
            const isDark = theme === 'dark';
            const label = isDark ? 'Switch to light mode' : 'Switch to dark mode';
            document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
                btn.setAttribute('aria-label', label);
                btn.setAttribute('title', label);
                btn.setAttribute('aria-pressed', isDark ? 'true' : 'false');
            });
        };

        const applyTheme = (theme, persist = false) => {
            document.documentElement.setAttribute('data-theme', theme);
            if (persist) {
                try {
                    window.localStorage.setItem(THEME_KEY, theme);
                } catch (e) {}
            }
            updateToggleButtons(theme);
            try {
                window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
            } catch (e) {}
        };

        // Initialize state on buttons
        const currentTheme = document.documentElement.getAttribute('data-theme') || getPreferredTheme();
        applyTheme(currentTheme, false);

        // Click handlers on all theme toggle buttons
        document.querySelectorAll('.theme-toggle-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const active = document.documentElement.getAttribute('data-theme') || getPreferredTheme();
                const nextTheme = active === 'dark' ? 'light' : 'dark';
                applyTheme(nextTheme, true);
            });
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

    // Scroll-triggered floating quote popup
    static setupScrollQuotePopup() {
        try {
            if (window.sessionStorage && window.sessionStorage.getItem('xt_quote_popup_closed') === 'true') {
                return;
            }
        } catch (e) {
            // sessionStorage unavailable or restricted
        }

        let scrollTimer = null;
        let hasTriggered = false;

        const triggerPopup = () => {
            if (hasTriggered) return;
            hasTriggered = true;
            window.removeEventListener('scroll', handleScroll);

            if (document.getElementById('xt-scroll-quote-popup')) return;

            const popup = document.createElement('aside');
            popup.id = 'xt-scroll-quote-popup';
            popup.className = 'xt-quote-popup';
            popup.setAttribute('role', 'dialog');
            popup.setAttribute('aria-labelledby', 'xt-popup-title');
            popup.setAttribute('aria-modal', 'false');
            popup.innerHTML = `
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
                    <div style="display: inline-flex; align-items: center; background: #ECFDF5; border: 1px solid #A7F3D0; padding: 2px 8px; border-radius: 9999px;">
                        <span class="xt-pulse-dot" style="display: inline-block; width: 6px; height: 6px; border-radius: 9999px; background-color: #10B981; margin-right: 6px;"></span>
                        <span style="font-size: 0.72rem; font-weight: 600; color: #047857; text-transform: uppercase; letter-spacing: 0.04em;">Online &middot; Instant Quote</span>
                    </div>
                    <button type="button" id="xt-popup-close-x" class="xt-popup-close-btn" aria-label="Close quote offer" style="background: none; border: none; font-size: 1.25rem; line-height: 1; color: #94A3B8; cursor: pointer; padding: 2px 6px; border-radius: 6px; display: inline-flex; align-items: center; justify-content: center; transition: all 0.2s;">&times;</button>
                </div>
                <h3 id="xt-popup-title" style="margin: 0.25rem 0 0.35rem; font-size: 1.05rem; font-weight: 700; color: #0F172A; line-height: 1.35;">Need a Quick Website Quote?</h3>
                <p style="margin: 0 0 0.85rem; font-size: 0.84rem; color: #64748B; line-height: 1.45;">Chat directly with our lead developers in Nairobi on WhatsApp. Transparent packages from <strong style="color: #0F172A;">KES 31,500</strong> with free domain &amp; hosting.</p>
                <a href="https://wa.me/254722753819?text=Hello%20XclusiveTech%2C%20I%20would%20like%20a%20free%20quote%20for%20my%20website%20project." target="_blank" rel="noopener noreferrer" class="xt-popup-cta-btn" id="xt-popup-whatsapp-link" style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; width: 100%; background-color: #2563EB; color: #FFFFFF !important; font-weight: 600; font-size: 0.875rem; padding: 0.65rem 1rem; border-radius: 0.75rem; text-decoration: none; transition: all 0.2s; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                        <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217l.332.006c.106.005.249-.04.39.298.144.347.491 1.2.534 1.287.043.087.072.188.014.304-.058.116-.087.188-.173.289l-.26.304c-.087.086-.177.18-.076.354.101.174.449.741.964 1.201.662.591 1.221.774 1.394.861.174.086.275.073.376-.044.101-.116.433-.506.549-.68.116-.173.231-.145.39-.086s1.011.477 1.184.564.289.13.332.202c.045.072.045.419-.099.824zm-3.392-12.416c-5.514 0-10 4.486-10 10 0 1.942.554 3.756 1.517 5.292l-1.556 5.688 5.864-1.538c1.474.88 3.204 1.378 5.175 1.378 5.514 0 10-4.486 10-10s-4.486-10-10-10z"/>
                    </svg>
                    <span>Get a Free WhatsApp Quote</span>
                </a>
                <button type="button" id="xt-popup-dismiss-btn" class="xt-popup-dismiss-text" style="display: block; width: 100%; text-align: center; background: none; border: none; margin-top: 0.5rem; font-size: 0.78rem; color: #94A3B8; cursor: pointer; padding: 4px; transition: color 0.2s;">Maybe later</button>
            `;

            document.body.appendChild(popup);

            // Trigger animation in next animation frame
            requestAnimationFrame(() => {
                popup.classList.add('xt-popup-visible');
            });

            const closePopup = () => {
                try {
                    if (window.sessionStorage) {
                        window.sessionStorage.setItem('xt_quote_popup_closed', 'true');
                    }
                } catch (e) {}

                popup.classList.remove('xt-popup-visible');
                popup.classList.add('xt-popup-closing');
                setTimeout(() => {
                    if (popup.parentNode) {
                        popup.parentNode.removeChild(popup);
                    }
                }, 350);
            };

            const closeX = document.getElementById('xt-popup-close-x');
            const dismissBtn = document.getElementById('xt-popup-dismiss-btn');
            const waLink = document.getElementById('xt-popup-whatsapp-link');

            if (closeX) closeX.addEventListener('click', closePopup);
            if (dismissBtn) dismissBtn.addEventListener('click', closePopup);
            if (waLink) {
                waLink.addEventListener('click', () => {
                    try {
                        if (window.sessionStorage) {
                            window.sessionStorage.setItem('xt_quote_popup_closed', 'true');
                        }
                    } catch (e) {}
                    closePopup();
                });
            }

            // Also allow Escape key to dismiss
            const handleEsc = (e) => {
                if (e.key === 'Escape' && document.getElementById('xt-scroll-quote-popup')) {
                    closePopup();
                    document.removeEventListener('keydown', handleEsc);
                }
            };
            document.addEventListener('keydown', handleEsc);
        };

        const handleScroll = () => {
            if (hasTriggered) return;
            // When user scrolls past 200px
            if (window.scrollY >= 200) {
                if (!scrollTimer) {
                    // Wait 5 seconds of browsing after scrolling has started
                    scrollTimer = setTimeout(() => {
                        triggerPopup();
                    }, 5000);
                }
            }
        };

        window.addEventListener('scroll', handleScroll, { passive: true });
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
