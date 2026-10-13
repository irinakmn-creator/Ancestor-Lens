# Implemented SEO improvements — October 13, 2026

## Outcome

Implemented in the existing local repository. All 59 HTML file URLs and their canonical targets are preserved. All 55 content pages remain present; the four pre-existing alias/redirect pages are untouched. No article was deleted, merged, newly redirected or substantially rewritten. Existing hero, grids, brand colors, typography, buttons, animations, navigation and responsive layouts were retained.

The pre-edit findings and reasons for deferred content work are in [the audit report](AUDIT-2026-10-13.md). Full URL inventories are in [baseline.csv](baseline.csv) and [current.csv](current.csv). These changes have not been deployed in this request; the live audit describes the pre-edit site.

## Changes by file

| Files | Implemented changes |
|---|---|
| `index.html` | Exact requested SEO title, H1 and description; aligned Open Graph/Twitter text. Homepage links to all four priority URLs. Existing three-card preview reused; accuracy guide linked contextually. Unsupported aggregate rating and unsourced “verified” testimonials removed; existing cards now explain published app features. Corrected repeated marquee claims, purchase terms, processing-time promises and iOS minimum. Privacy statements attributed to the developer policy. Marketing montage and example scores labelled illustrative. SoftwareApplication describes visual entertainment, both platform destinations and a verified free US Apple download with in-app purchases; no invented rich-result rating. |
| `blog-what-nationality-look-like.html` | Differentiated metadata and H1; helpful country-label/map interpretation section with sourced app screenshot; contextual links to the other three guides; visible update/byline; BlogPosting and breadcrumbs aligned. Existing country-perception content retained for the separately flagged editorial review. |
| `blog-what-ethnicity-i-look-like.html` | Differentiated metadata and H1; screenshot annotations explaining labels, scores and the distinction from DNA; contextual links; byline/update and schema alignment. Existing regional-feature sections retained pending evidence-led review rather than silently removed. |
| `blog-ai-face-ethnicity-test.html` | App workflow and sourced Roots Match screenshot annotations; clear explanation that the score is not shared DNA or a relationship probability; current-purchase check and direct store choices; contextual links, metadata, byline and schema updates. |
| `blog-how-accurate-ai-ethnicity-test.html` | Accuracy-focused metadata/H1; visible evidence limits; practical consistency-check protocol that does not invent an accuracy benchmark; sourced Historical Twin screenshot and interpretation notes. Narrow correction of the unverified facial-landmark implementation claim. Broken image, author and logo schema references repaired. |
| `blog.html` | Added cards for the three previously absent articles; all 53 articles now appear once. Accessible H2 above card collection; four priority card headings synchronized. No duplicate cards existed in this baseline. |
| All 55 content HTML pages | Actual image dimensions, asynchronous decoding and appropriate below-fold lazy loading; compressed image references; one deferred analytics loader; external new-tab links use `noopener`; Apple links normalized to the verified app ID. Legacy article download buttons now have a native `index.html#download` fallback before JavaScript runs. Canonicals and article paths unchanged. Six invalid schema author/logo paths repaired. Three generic missing image paths repaired. |
| `blog-historical-twin-ai-app.html` | Corrected malformed Google Play destination `/store/objects/details` to `/store/apps/details`. |
| `styles.css` | Small screenshot/annotation layout scoped to existing article columns; responsive stacking; matching intro-CTA H2 style; accessible visually hidden heading utility. No site redesign. |
| `script.js` | One delegated analytics implementation replaces the old homepage click logger. Handle unavailable localStorage. Keep `html lang="en"` when only interface labels translate; preserve the existing language selector. |
| `translations.js` | EN/DE/ES privacy-notice labels now point readers to published policy information instead of asserting instant analysis/deletion or never-sharing. Full content localization remains a planned follow-up. |
| `analytics.js` (new) | Reuses Clarity project with a guarded idle loader, queued events and one interaction event. Immutable event names identify page and CTA location; real outbound clicks are separate from on-site CTAs. Search-referrer candidates exclude known paid markers. No GA4/GTM ID invented. |
| `sitemap.xml` | Validated 55 unique canonical content URLs; updated lastmod for actual homepage/index/priority/image-repair changes only. `robots.txt` already allows crawling and points to the correct sitemap, so no robots edit was needed. |
| `run_generator.py` | Fix nonexistent author and logo references in the template. Existing generator/redirect scripts inspected but not executed. |
| New WebP assets and `images/app-store-*.webp` | Compressed existing editorial imagery without cropping/replacing it, plus responsive 600/900px hero versions. Original assets retained. Three official Apple promotional screenshots converted to WebP without content alteration. Sources recorded in [screenshot-sources.json](screenshot-sources.json). |
| `tools/seo_audit.py`, `docs/seo/*` | Reproducible static audit, before/after inventories, live URL/storefront checks, claim-review register, change manifest, measurement plan and verification evidence. |

The exhaustive file list is [change-manifest.json](change-manifest.json). Sitewide HTML changes are mechanical resource/measurement/accessibility edits outside the four priority articles; no claims of substantive editorial review for every legacy page.

## Verification

- Static audit: 59 HTML files; 55 content pages; 55 unique sitemap URLs; 53 unique article cards. No local missing assets, links or schema resources; no duplicate titles/descriptions/cards/IDs; no missing sitemap content URL; no image without dimensions.
- All canonical targets are byte-for-byte the same URLs as before. All original files remain available.
- XML sitemap parses. Robots permits content crawling and names the correct sitemap. All live pre-edit site pages/crawl files were HTTP 200; nonexistent `/about.html` was 404 and is no longer referenced in schemas.
- JSON-LD parses. Priority headlines, dates, images and schema page URLs match the updated pages. Descriptive SoftwareApplication is retained without claiming Google software-app rich-result eligibility.
- JavaScript syntax checks pass for `script.js`, `translations.js` and `analytics.js`.
- [Sitewide browser check](sitewide-browser-check.json): all 55 content pages at 390px and 1440px (110 page/viewport combinations), with external fonts/analytics blocked for the broad structural sweep. One H1, canonical, one analytics reference, no horizontal overflow and no page errors.
- [Focused browser checks](browser-verification.json): homepage/blog at 320, 390, 768 and 1440px; four priority articles at 390 and 1440px, with real font loading and stubbed analytics. Images load; no horizontal overflow/page errors; mobile menu, Escape, FAQ and language controls pass. Exactly one Clarity provider request per page and one event per tested CTA.
- [Final interaction checks](interaction-verification.json): revised homepage at 320/390/1440px; all four priority links visible in no-JavaScript HTML; disabled-storage mode produces no errors; one middle-click outbound event; Google referrer candidate recorded, paid `gclid`/CPC visits excluded, unrelated referral excluded.
- Visual inspection of desktop/mobile homepage and screenshot annotations confirms the original site components, fonts and colors remain in use.

## Performance evidence and limits

The original hero PNG is 2,021,498 bytes. The full WebP is 193,864 bytes (90.4% smaller); 600px and 900px variants are 49,846 and 111,656 bytes. At 390px the browser selects the 600px variant; at 1440px it selects 900px. The same image aspect ratio and transparent composition are retained.

Across 31 converted existing PNG assets, original files total 21,043,181 bytes and WebP copies total 4,096,174 bytes (80.5% smaller). This is an asset-byte comparison, not a measured traffic, ranking or Core Web Vitals uplift. Browser diagnostic LCP/CLS samples are included in the evidence JSON; they are localhost samples with test interactions and are not field CWV. Real mobile INP/LCP/CLS still require CrUX/Search Console or an approved real-user performance setup.

## Deferred/manual items

See [audit manual-verification items](AUDIT-2026-10-13.md) and [measurement plan](MEASUREMENT.md). In particular: active purchases and platform parity, country/device eligibility, third-party photo handling and retention, current screenshots, rating/review provenance, legacy claims/overlap, full DE/ES content, web analytics consent/disclosure, Search Console indexing/query overlap, and store-side download attribution.

[claim-review.csv](claim-review.csv) contains automated excerpt candidates for product/privacy/timing/technical-method verification. Matches can be comparative, attributed or already qualified; they are not all confirmed false claims. Do not blindly rewrite the matched articles. Get product/source evidence and query/page data before a substantial editorial change.

No rankings, traffic, search volumes, downloads or conversion results are invented. No promised “best ranking” or guaranteed rich result is claimed.
