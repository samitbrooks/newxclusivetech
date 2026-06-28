/* ============================================
   XCLUSIVETECH ANIMATIONS SCRIPT
   Scroll animations and intersection observer
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    // Intersection Observer for Scroll Animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                
                // Add stagger delay for multiple elements
                const siblings = entry.target.parentElement?.children;
                if (siblings) {
                    Array.from(siblings).forEach((sibling, index) => {
                        if (sibling.classList.contains('animate-fade-in-up') ||
                            sibling.classList.contains('animate-fade-in')) {
                            sibling.style.animationDelay = `${index * 0.1}s`;
                        }
                    });
                }
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe all animated elements
    document.querySelectorAll('.animate-fade-in, .animate-fade-in-up, .animate-scale, .animate-slide-in-left, .animate-slide-in-right').forEach(element => {
        observer.observe(element);
    });
    
    // Counter Animation for Statistics
    const counterElements = document.querySelectorAll('.counter');
    const animateCounter = (element) => {
        const target = parseInt(element.getAttribute('data-target'));
        const duration = 2000; // 2 seconds
        const increment = target / (duration / 16); // 60fps
        let current = 0;
        
        const counter = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target;
                clearInterval(counter);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 16);
    };
    
    // Observe counters
    const counterObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    // Respect prefers-reduced-motion: show final values immediately instead of animating
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    counterElements.forEach(element => {
        if (prefersReducedMotion) {
            element.textContent = element.getAttribute('data-target');
        } else {
            counterObserver.observe(element);
        }
    });
    
    // Parallax Effect on Hero Section
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    if (parallaxElements.length > 0) {
        window.addEventListener('scroll', () => {
            const scrollY = window.scrollY;
            parallaxElements.forEach(element => {
                const speed = element.getAttribute('data-parallax');
                element.style.transform = `translateY(${scrollY * speed}px)`;
            });
        });
    }
    
    // Hover effects on service cards
    const serviceCards = document.querySelectorAll('.hover-scale');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05) translateY(-5px)';
            this.style.boxShadow = '0 20px 40px rgba(0, 217, 255, 0.3)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) translateY(0)';
            this.style.boxShadow = '0 10px 30px rgba(0, 217, 255, 0.1)';
        });
    });
});

// Performance: Debounce scroll events
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Lazy loading for images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img.lazy').forEach(img => imageObserver.observe(img));
}
