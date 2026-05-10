/* ============================================
   XCLUSIVETECH MAIN SCRIPT
   Global functionality and utilities
   ============================================ */

// Global utility functions
class XclusiveTech {
    // Initialize app
    static init() {
        this.setupEventListeners();
        this.setupFormHandling();
        this.optimizePerformance();
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
