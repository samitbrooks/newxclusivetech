/* ============================================
   XCLUSIVETECH NAVIGATION SCRIPT
   Mobile menu toggle and sticky nav
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const navbar = document.getElementById('navbar');
    
    // Animate the mobile drawer while keeping its state accessible.
    let menuAnimation;
    function setMenu(open) {
        if (!mobileMenu) return;
        menuAnimation?.cancel();
        mobileMenuBtn?.setAttribute('aria-expanded', String(open));
        mobileMenu.inert = !open;
        const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (open) mobileMenu.classList.remove('hidden');
        if (!reduced && mobileMenu.animate) {
            menuAnimation = mobileMenu.animate(
                open ? { opacity: [0, 1], translate: ['0 -8px', '0 0'] } : { opacity: [1, 0], translate: ['0 0', '0 -8px'] },
                { duration: 180, easing: 'ease-out' }
            );
            menuAnimation.onfinish = () => { mobileMenu.classList.toggle('hidden', !open); menuAnimation = null; };
        } else mobileMenu.classList.toggle('hidden', !open);
    }
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.setAttribute('aria-expanded', String(!mobileMenu.classList.contains('hidden')));
        mobileMenu.inert = mobileMenu.classList.contains('hidden');
        mobileMenuBtn.addEventListener('click', () => setMenu(mobileMenuBtn.getAttribute('aria-expanded') !== 'true'));
        mobileMenu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false)));
        document.addEventListener('keydown', event => {
            if (event.key === 'Escape' && mobileMenuBtn.getAttribute('aria-expanded') === 'true') {
                setMenu(false); mobileMenuBtn.focus();
            }
        });
    }

    // Sticky Navigation - Add shadow on scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar?.classList.add('shadow-md');
        } else {
            navbar?.classList.remove('shadow-md');
        }
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (!href || href === '#') return;
            let target;
            try { target = document.getElementById(decodeURIComponent(href.slice(1))); } catch { return; }
            if (!target) return;
            e.preventDefault();
            if (target) {
                target.scrollIntoView({
                    behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
                    block: 'start'
                });
            }
        });
    });
});
