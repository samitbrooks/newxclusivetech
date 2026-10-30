/* Budget arithmetic progressively enhances the static project guide. */
(() => {
    function init() {
        document.querySelectorAll('.ownership-calculator').forEach(form => {
            const output = form.querySelector('output');
            function update() {
                const value = name => Math.max(0, Number(form.elements[name].value) || 0);
                const total = value('build') + value('domain') + value('hosting') + 12 * value('care');
                const missingHosting = form.elements.hosting.value === '';
                output.textContent = `First-year estimate: KES ${total.toLocaleString('en-KE')}${missingHosting ? ' plus hosting (not entered)' : ''}. Other unlisted costs are excluded.`;
            }
            form.addEventListener('input', update);
            form.addEventListener('submit', event => { event.preventDefault(); update(); });
            update();
        });
    }
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true }); else init();
})();
