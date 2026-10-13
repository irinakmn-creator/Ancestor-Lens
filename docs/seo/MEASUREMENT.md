# Measurement plan

## Installed infrastructure

Reuse Microsoft Clarity project `vlfb2lz6qi`. Every one of the 55 content pages now loads `analytics.js` once. It creates the existing Clarity queue, schedules one provider script after browser idle (timeout 1.5 seconds), and queues interactions immediately. The four existing redirect aliases do not initialize a new collector.

Inline installations were removed and the previous homepage-only click logger was replaced. There is no GA4 ID, GTM container or install-attribution SDK in the repository; none was invented or installed. Existing dashboard smart-event definitions and consent rules still require account-owner review.

## One custom event per CTA interaction

Names are `<event_type>__<page_key>__<location>`:

- `app_store_click__home__hero`: actual outbound App Store link.
- `google_play_click__home__hero`: actual outbound Google Play link.
- `cta_click__home__navigation`: on-site header download CTA. It scrolls to download choices; it is not an App Store visit.
- `app_store_click__blog-ai-face-ethnicity-test__article_intro`: article intro badge.
- `app_store_click__blog-ai-face-ethnicity-test__article_body`: contextual download link.
- `app_store_click__blog-ai-face-ethnicity-test__article_end`: article end badge.

The page key uses the existing filename without `.html`; `/` and `/index.html` both use `home`. Section IDs provide homepage locations. Article locations use `article_intro`, `article_body` or `article_end`. Primary and middle-button link activations are tracked once; analytics errors never prevent the link's default navigation.

Supporting custom tags: `page_path`, `content_language`, `referrer_type`, `cta_page`, `cta_location`, `cta_label`, `cta_store`. Tags are session context and may be overwritten; immutable page/location in event names is the reliable event-level attribution. Legacy `data-cro-event` names are retained as CTA labels, not emitted as duplicate events. Previous custom event names stop receiving new traffic; update dashboard filters when deploying.

## Organic-search landing measurement

For a Google/Bing/DuckDuckGo/Yahoo referrer without known paid-click markers or paid UTM medium, emit `search_landing_view__<page_key>`. Known paid markers include `gclid`, `dclid`, `gbraid`, `wbraid`, `msclkid`. This is a **search-referrer candidate**, not a definitive attribution model. Referrers can be suppressed, campaigns may be mistagged and private apps can obscure the source. No referrer query, user identity, GPS or country guess is sent in custom tags.

Use Clarity's existing session/page/entry URL/referrer and country filters for inspection. Confirm the project exposes these filters before creating dashboards. Country comes from Clarity's provider-side data; browser language must not be substituted for visitor country.

Search Console is required for Google organic performance. Export Pages + Queries + Countries and compare 28-day periods. Use Search Console clicks for search performance, not as a proxy for sessions, installs or purchases. For acquisition/session attribution by source/medium, connect an approved GA4 property only after its ID and consent setup are supplied; do not add a second provider automatically.

## Recommended dashboard views

1. Search-referrer candidate sessions by landing URL and country.
2. App Store outbound custom events by page key and CTA location.
3. Google Play outbound custom events by page key and CTA location.
4. On-site CTA events separately from outbound store visits.
5. Search Console impressions, clicks, CTR and query/page overlap for the four priority URLs.
6. App Store Connect / Play Console product-page views and first-time downloads by approved campaign/source attribution.

Outbound click totals are intent signals, not verified downloads. Qualified installs and purchases require store-side measurement. Apple campaign tokens (`pt`, `ct`) require the owner's provider token and campaign configuration. Google Play install-referrer campaigns require approved Android attribution support. These values remain unconfigured; no fake campaign token is appended.

## Manual verification after deployment

- Confirm project access, domain coverage, consent/CMP behavior and website privacy disclosure with the owner. App privacy policy alone is not a disclosure of website session analytics.
- Verify one Clarity provider request per page and one custom event per activation. Check existing no-code smart-event definitions to avoid duplicate dashboard goals.
- Filter the immutable event names and verify page/CTA tags in the dashboard. If a consent rule blocks collection, retain that rule and verify queue/consent behavior with the CMP.
- Check organic landing candidates against Search Console and acquisition analytics; do not label all Google referrals as organic.
- Test App Store and Google Play destinations in actual devices/accounts and validate country availability in the store consoles.
- Record a before/after date range after deployment. This repository audit makes no claim of traffic or conversion improvement.

Reference: [Clarity API and custom events](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-api).
