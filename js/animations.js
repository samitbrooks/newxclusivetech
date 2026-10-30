/* Shared progressive motion: content stays visible without JavaScript. */
(() => {
    function init() {
        const media = matchMedia('(prefers-reduced-motion: reduce)');
        const root = document.documentElement;
        const cleanups = new Set();
        let observer;
        const motion = () => !media.matches;
        // Animate only below-fold content; never delay the first screen.
        const candidates = new Set(document.querySelectorAll('section > div > h2, .tj-sec-heading, .animate-fade-in-up, .animate-fade-in, main article > h2'));
        document.querySelectorAll('.grid, .services-grid, .pricing-grid, .blog-grid, .portfolio-grid').forEach(grid => {
            [...grid.children].forEach((card, index) => {
                if (card.matches('a, article, .service-card, .pricing-card, .group')) {
                    card.style.setProperty('--xt-stagger', `${Math.min(index % 3, 2) * 75}ms`);
                    candidates.add(card);
                }
            });
        });
        function revealAll() {
            observer?.disconnect();
            document.querySelectorAll('.xt-reveal').forEach(el => el.classList.remove('xt-reveal'));
        }
        if (motion() && 'IntersectionObserver' in window) {
            observer = new IntersectionObserver(entries => entries.forEach(entry => {
                if (!entry.isIntersecting) return;
                entry.target.classList.add('xt-revealed');
                observer.unobserve(entry.target);
            }), { threshold: 0, rootMargin: '0px 0px -24px 0px' });
            candidates.forEach(el => {
                if (el.getBoundingClientRect().top < innerHeight || el.closest('.xt-reveal')) return;
                el.classList.add('xt-reveal'); observer.observe(el);
            });
        }
        // Identify shared controls without changing their labels or destinations.
        document.querySelectorAll('.nav-link, .footer-nav-link, .footer-location-link, .footer-bottom-link, main p a, article p a').forEach(el => el.classList.add('xt-link'));
        document.querySelectorAll('a[class*="btn"], button[class*="btn"], a[class*="rounded-full"][class*="px-"], button[type="submit"]').forEach(el => {
            el.classList.add('xt-button');
            el.querySelectorAll('svg, [aria-hidden="true"]').forEach(icon => icon.classList.add('xt-icon'));
        });
        document.querySelectorAll('.service-card svg, .services-card svg, .footer-contact-icon').forEach(el => el.classList.add('xt-service-icon'));
        document.querySelectorAll('img[src*="/portfolio/"], img[src*="/blog/"]').forEach(el => {
            const frame = el.closest('.overflow-hidden');
            if (frame) { frame.classList.add('xt-image-frame'); el.classList.add('xt-preview'); }
        });
        document.querySelectorAll('.hero-section, .cta-section, section[id="hero"], section[class*="bg-gradient"], header[class*="bg-gradient"]').forEach(el => {
            el.classList.add('xt-ambient');
            const layer = document.createElement('div');
            layer.className = 'xt-ambient-layer'; layer.setAttribute('aria-hidden', 'true'); el.prepend(layer);
        });
        // Turn existing FAQ articles into keyboard-accessible accordions.
        document.querySelectorAll('.faq-item').forEach((item, index) => {
            const question = item.querySelector('.faq-question');
            const answer = item.querySelector('.faq-answer');
            if (!question || !answer || question.querySelector('button')) return;
            const button = document.createElement('button'); button.type = 'button';
            button.className = 'xt-faq-toggle';
            while (question.firstChild) button.append(question.firstChild);
            const plus = document.createElement('span'); plus.className = 'xt-faq-plus'; plus.textContent = '+'; plus.setAttribute('aria-hidden', 'true'); button.append(plus); question.append(button);
            const panel = document.createElement('div'); panel.className = 'xt-faq-panel'; panel.id = `xt-faq-${index}`;
            const inner = document.createElement('div'); inner.className = 'xt-faq-inner';
            answer.before(panel); panel.append(inner); inner.append(answer);
            button.setAttribute('aria-controls', panel.id); button.setAttribute('aria-expanded', 'false');
            panel.inert = true; panel.setAttribute('aria-hidden', 'true');
            button.addEventListener('click', () => {
                const open = button.getAttribute('aria-expanded') !== 'true';
                button.setAttribute('aria-expanded', String(open)); panel.inert = !open;
                panel.setAttribute('aria-hidden', String(!open)); panel.classList.toggle('xt-open', open);
            });
        });
        // Native details retain their built-in keyboard and accessibility behavior.
        document.querySelectorAll('details').forEach(details => {
            const summary = details.querySelector(':scope > summary'); if (!summary) return;
            let animation, desired = details.open;
            const settle = () => {
                animation?.cancel(); animation = null; details.open = desired;
                details.style.height = ''; details.style.overflow = '';
            };
            cleanups.add(settle);
            summary.addEventListener('click', event => {
                if (!motion() || !details.animate) return;
                event.preventDefault();
                const start = details.getBoundingClientRect().height;
                desired = !desired; animation?.cancel(); details.open = true;
                details.style.height = ''; details.style.overflow = 'hidden';
                const end = desired ? details.getBoundingClientRect().height : summary.getBoundingClientRect().height + parseFloat(getComputedStyle(details).paddingTop) + parseFloat(getComputedStyle(details).paddingBottom);
                animation = details.animate({ height: [`${start}px`, `${end}px`] }, { duration: 240, easing: 'ease-out' });
                animation.onfinish = settle;
            });
            details.addEventListener('toggle', () => { if (!animation) desired = details.open; });
        });
        // One passive scroll listener drives header and reading progress.
        const navbar = document.querySelector('.site-header, #navbar');
        const isPost = location.pathname.includes('/blog/') && !/\/blog\/(?:index\.html)?$/.test(location.pathname);
        const article = isPost ? document.querySelector('main article, article, main') : null;
        let progress;
        if (article) {
            progress = document.createElement('div'); progress.className = 'xt-reading-progress';
            progress.setAttribute('aria-hidden', 'true'); document.body.append(progress);
        }
        let scheduled = false;
        function updateScroll() {
            scheduled = false;
            navbar?.classList.toggle('xt-scrolled', scrollY > 50);
            if (progress) {
                const start = article.getBoundingClientRect().top + scrollY;
                const distance = Math.max(article.offsetHeight - innerHeight, 1);
                const value = Math.min(1, Math.max(0, (scrollY - start) / distance));
                progress.style.transform = `scaleX(${value})`;
            }
        }
        function scheduleScroll() { if (!scheduled) { scheduled = true; requestAnimationFrame(updateScroll); } }
        addEventListener('scroll', scheduleScroll, { passive: true }); addEventListener('resize', scheduleScroll); updateScroll();
        // Counters finish immediately when motion is disabled, including mid-animation.
        const counterObserver = 'IntersectionObserver' in window ? new IntersectionObserver(entries => entries.forEach(({ target, isIntersecting }) => {
            if (!isIntersecting) return;
            counterObserver.unobserve(target); const value = Number(target.dataset.target); const start = performance.now();
            function tick(now) {
                const fraction = motion() ? Math.min((now - start) / 1200, 1) : 1;
                target.textContent = String(Math.round(value * (1 - (1 - fraction) ** 3)));
                if (fraction < 1) requestAnimationFrame(tick);
            }
            requestAnimationFrame(tick);
        }), { threshold: 0.25 }) : null;
        document.querySelectorAll('.counter[data-target]').forEach(el => {
            if (motion() && counterObserver) counterObserver.observe(el); else el.textContent = el.dataset.target;
        });
        document.querySelectorAll('img.lazy[data-src]').forEach(img => { img.loading = 'lazy'; img.src = img.dataset.src; img.classList.remove('lazy'); });
        const preferenceChanged = () => {
            if (media.matches) {
                revealAll(); cleanups.forEach(fn => fn()); counterObserver?.disconnect();
                document.querySelectorAll('.counter[data-target]').forEach(el => el.textContent = el.dataset.target);
            }
        };
        media.addEventListener('change', preferenceChanged);
        document.addEventListener('focusin', event => event.target.closest('.xt-reveal')?.classList.add('xt-revealed'));
        document.addEventListener('visibilitychange', () => root.classList.toggle('xt-motion-paused', document.hidden));
        addEventListener('pageshow', event => { if (event.persisted) revealAll(); });
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true }); else init();
})();
