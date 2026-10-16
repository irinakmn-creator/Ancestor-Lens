/* Reuse the site's Clarity project. Do not install a second analytics collector. */
(() => {
    if (window.ancestorLensAnalyticsInitialized) return;
    window.ancestorLensAnalyticsInitialized = true;

    const project = 'vlfb2lz6qi';
    const canonicalPath = path => path === '/index.html' ? '/' : path;
    const pagePath = canonicalPath(location.pathname);
    const pageKey = pagePath === '/' ? 'home' : pagePath.replace(/^\//, '').replace(/\.html$/, '').replace(/[^a-z0-9_-]/gi, '_');
    const existingLoader = document.querySelector('script[src*="clarity.ms/tag/"]');
    if (typeof window.clarity !== 'function') {
        window.clarity = function () {
            (window.clarity.q = window.clarity.q || []).push(arguments);
        };
    }
    const send = (...args) => {
        try { window.clarity(...args); } catch (_) { /* Analytics must not block navigation. */ }
    };

    let referrerHost = '';
    try { referrerHost = new URL(document.referrer).hostname; } catch (_) { /* Direct visit. */ }
    const query = new URLSearchParams(location.search);
    const paid = ['gclid', 'dclid', 'gbraid', 'wbraid', 'msclkid'].some(key => query.has(key)) ||
        /^(cpc|ppc|paid|paidsearch|paid_search|display|paid_social)$/i.test(query.get('utm_medium') || '');
    const searchHost = /(^|\.)(google\.[a-z.]+|bing\.com|duckduckgo\.com|search\.yahoo\.com)$/.test(referrerHost);
    send('set', 'page_path', pagePath);
    send('set', 'content_language', document.documentElement.lang || 'en');
    send('set', 'referrer_type', paid ? 'campaign_paid' : searchHost ? 'search_candidate' : referrerHost ? 'referral' : 'direct_or_unknown');
    if (searchHost && !paid) send('event', `search_landing_view__${pageKey}`);

    // Existing inline installations are detected; events can queue before Clarity loads.
    if (!existingLoader) {
        const load = () => {
            if (document.querySelector('script[src*="clarity.ms/tag/"]')) return;
            const tag = document.createElement('script');
            tag.async = true;
            tag.src = `https://www.clarity.ms/tag/${project}`;
            document.head.appendChild(tag);
        };
        if ('requestIdleCallback' in window) window.requestIdleCallback(load, { timeout: 1500 });
        else window.setTimeout(load, 0);
    }

    const track = event => {
        if (event.type === 'auxclick' && event.button !== 1) return;
        const element = event.target.closest('a,button');
        if (!element) return;
        let url;
        try { url = new URL(element.getAttribute('href') || '', location.href); } catch (_) { return; }
        const apple = url.hostname === 'apps.apple.com' && url.pathname.includes('/id6755190587') && !url.hash;
        const google = url.hostname === 'play.google.com' && url.pathname === '/store/apps/details' && url.searchParams.get('id') === 'com.deepqeeb.ancestorlens';
        const cta = element.matches('[data-cro-event], .btn, .store-btn, .store-badge-btn, .internal-blog-link');
        if (!apple && !google && !cta) return;
        const locationName = element.closest('section[id]')?.id ||
            (element.closest('header .nav') ? 'navigation' : element.closest('.try-it-block') ? 'article_intro' : element.closest('.cta-box, .article-cta') ? 'article_end' : 'article_body');
        const label = element.getAttribute('data-cro-event') || element.getAttribute('aria-label') || element.textContent.trim().replace(/\s+/g, ' ').slice(0, 80) || element.querySelector('img')?.alt || 'download';
        send('set', 'cta_page', pagePath);
        send('set', 'cta_location', locationName);
        send('set', 'cta_label', label);
        send('set', 'cta_store', apple ? 'app_store' : google ? 'google_play' : 'on_site');
        // Exactly one custom event per interaction, including legacy homepage CTAs.
        const type = apple ? 'app_store_click' : google ? 'google_play_click' : 'cta_click';
        if (apple || google) {
            // Persistent session flags simplify deduplicated conversion reports.
            // Keep store flags separate so a second store click cannot erase the first.
            send('set', 'download_clicked', 'yes');
            send('set', apple ? 'download_app_store' : 'download_google_play', 'yes');
        }
        // Clarity tags are session context; embed page/location in the event itself
        // so a later page or CTA cannot overwrite its attribution.
        send('event', `${type}__${pageKey}__${locationName}`);
    };
    document.addEventListener('click', track);
    document.addEventListener('auxclick', track);
})();
