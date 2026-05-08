/* ============================================
   XCLUSIVETECH NAVIGATION SCRIPT
   Mobile menu toggle and sticky nav
   ============================================ */

document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const navbar = document.getElementById('navbar');
    
    // Mobile Menu Toggle
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Close mobile menu when a link is clicked
    const mobileMenuLinks = mobileMenu?.querySelectorAll('a');
    if (mobileMenuLinks) {
        mobileMenuLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenu.classList.add('hidden');
            });
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
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});
