/* ============================================
   LAUNCH OFFER POPUP
   Shows once per browser session, dismissible.
   ============================================ */

(function () {
    var STORAGE_KEY = 'xtOfferPopupShown';

    if (sessionStorage.getItem(STORAGE_KEY)) {
        return;
    }

    function init() {
        var style = document.createElement('style');
        style.textContent = [
            '.xt-offer-backdrop {',
            '  position: fixed; inset: 0; background: rgba(10, 10, 11, 0.72);',
            '  z-index: 9998; display: flex; align-items: center; justify-content: center;',
            '  padding: 1rem; opacity: 0; transition: opacity 0.3s ease;',
            '}',
            '.xt-offer-backdrop.xt-visible { opacity: 1; }',
            '.xt-offer-card {',
            '  position: relative; max-width: 420px; width: 100%;',
            '  background: #14161a; border: 2px solid rgba(16, 185, 129, 0.6);',
            '  border-radius: 1.25rem; padding: 2rem; text-align: center;',
            '  transform: translateY(16px) scale(0.97); transition: transform 0.3s ease;',
            '  box-shadow: 0 24px 80px rgba(0,0,0,0.5);',
            '  font-family: Montserrat, sans-serif; color: #E5EDF8;',
            '}',
            '.xt-offer-backdrop.xt-visible .xt-offer-card { transform: translateY(0) scale(1); }',
            '.xt-offer-badge {',
            '  display: inline-block; background: #34D399; color: #0A0A0B;',
            '  font-weight: 700; font-size: 0.7rem; letter-spacing: 0.08em;',
            '  text-transform: uppercase; padding: 0.35rem 0.9rem; border-radius: 9999px;',
            '  margin-bottom: 1rem;',
            '}',
            '.xt-offer-close {',
            '  position: absolute; top: 0.75rem; right: 0.9rem; background: none; border: none;',
            '  color: rgba(229,237,248,0.6); font-size: 1.4rem; line-height: 1; cursor: pointer;',
            '}',
            '.xt-offer-close:hover { color: #fff; }',
            '.xt-offer-title { font-size: 1.4rem; font-weight: 700; margin: 0 0 0.5rem; }',
            '.xt-offer-price { color: #34D399; }',
            '.xt-offer-desc { font-size: 0.9rem; color: rgba(229,237,248,0.72); margin: 0 0 0.35rem; }',
            '.xt-offer-note { font-size: 0.78rem; color: rgba(229,237,248,0.56); margin: 0 0 1.4rem; }',
            '.xt-offer-cta {',
            '  display: inline-block; background: #34D399; color: #0A0A0B; font-weight: 700;',
            '  padding: 0.85rem 1.75rem; border-radius: 0.6rem; text-decoration: none;',
            '  transition: background 0.2s ease;',
            '}',
            '.xt-offer-cta:hover { background: #6EE7B7; }'
        ].join('\n');
        document.head.appendChild(style);

        var backdrop = document.createElement('div');
        backdrop.className = 'xt-offer-backdrop';
        backdrop.innerHTML =
            '<div class="xt-offer-card" role="dialog" aria-modal="true" aria-label="Limited launch offer">' +
            '  <button type="button" class="xt-offer-close" aria-label="Close">&times;</button>' +
            '  <span class="xt-offer-badge">Limited Launch Offer</span>' +
            '  <h2 class="xt-offer-title">A website for just <span class="xt-offer-price">KES 20,000</span></h2>' +
            '  <p class="xt-offer-desc">A single-page website — mobile-first, WhatsApp contact button, basic SEO, delivered in ~1&ndash;2 weeks.</p>' +
            '  <p class="xt-offer-note">Limited to our first 10 new clients on this offer.</p>' +
            '  <a class="xt-offer-cta" target="_blank" href="https://wa.me/254722753819?text=Hi%20Xclusive%20Tech%2C%20I%27d%20like%20to%20claim%20the%20KES%2020%2C000%20launch%20offer%20for%20a%20single-page%20website.">Claim This Offer on WhatsApp</a>' +
            '</div>';
        document.body.appendChild(backdrop);

        function close() {
            backdrop.classList.remove('xt-visible');
            setTimeout(function () {
                backdrop.remove();
            }, 300);
        }

        backdrop.querySelector('.xt-offer-close').addEventListener('click', close);
        backdrop.addEventListener('click', function (e) {
            if (e.target === backdrop) close();
        });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && document.body.contains(backdrop)) close();
        });
        backdrop.querySelector('.xt-offer-cta').addEventListener('click', close);

        requestAnimationFrame(function () {
            backdrop.classList.add('xt-visible');
        });

        sessionStorage.setItem(STORAGE_KEY, '1');
    }

    setTimeout(function () {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }
    }, 3000);
})();
