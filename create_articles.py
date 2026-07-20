import os
import markdown
from datetime import datetime

# Common HTML parts
header_nav = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta_title}</title>
    <meta name="description" content="{meta_description}">
    <link rel="canonical" href="https://ancestorlens.app/{url}">

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://ancestorlens.app/{url}">
    <meta property="og:title" content="{meta_title}">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:image" content="https://ancestorlens.app/{image}">

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://ancestorlens.app/{url}">
    <meta property="twitter:title" content="{meta_title}">
    <meta property="twitter:description" content="{meta_description}">
    <meta property="twitter:image" content="https://ancestorlens.app/{image}">

    <!-- JSON-LD Article Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "headline": "{meta_title}",
      "description": "{meta_description}",
      "image": "https://ancestorlens.app/{image}",
      "author": {
        "@type": "Organization",
        "name": "Ancestor Lens Editorial Team"
      },
      "publisher": {
        "@type": "Organization",
        "name": "Ancestor Lens",
        "logo": {
          "@type": "ImageObject",
          "url": "https://ancestorlens.app/logo.jpg"
        }
      },
      "datePublished": "2026-07-10",
      "dateModified": "2026-07-10",
      "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "https://ancestorlens.app/{url}"
      },
      "keywords": "{keywords}"
    }
    </script>
    
    <!-- JSON-LD Breadcrumb Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [{
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://ancestorlens.app/index.html"
      },{
        "@type": "ListItem",
        "position": 2,
        "name": "Blog",
        "item": "https://ancestorlens.app/blog.html"
      },{
        "@type": "ListItem",
        "position": 3,
        "name": "{meta_title}"
      }]
    }
    </script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
    <style>
        .post-page { padding-top: 120px; padding-bottom: 80px; }
        .post-header { max-width: 800px; margin: 0 auto 60px; text-align: center; }
        .post-tag { color: var(--color-gold); font-weight: 600; text-transform: uppercase; letter-spacing: 2px; font-size: 0.875rem; margin-bottom: 1rem; display: block; }
        .post-meta { font-size: 0.9rem; color: #666; margin-top: 16px; margin-bottom: 24px; }
        .breadcrumb { display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 0.9rem; margin-bottom: 24px; color: #555; }
        .breadcrumb a { color: var(--color-dark-green); text-decoration: none; }
        .breadcrumb a:hover { text-decoration: underline; }
        .post-title { font-family: var(--font-serif); font-size: 2.5rem !important; line-height: 1.2; color: var(--color-dark-green); margin-bottom: 24px; }
        .post-visual { width: 100%; aspect-ratio: 21/9; background: #F4F1EA; border-radius: 24px; margin-bottom: 60px; overflow: hidden; }
        .post-content { max-width: 700px; margin: 0 auto; font-size: 1.125rem; line-height: 1.8; color: #333; }
        .post-content p { margin-bottom: 24px; }
        .post-content h2 { font-family: var(--font-serif); font-size: 2.25rem; color: var(--color-dark-green); margin: 48px 0 24px; }
        .post-content h3 { font-family: var(--font-serif); font-size: 1.5rem; color: var(--color-dark-green); margin: 32px 0 16px; }
        .post-content ul { margin: 0 0 24px 24px; }
        .post-content ul li { margin-bottom: 8px; }
        .cta-box { background: var(--color-dark-green); color: white; padding: 40px; border-radius: 24px; text-align: center; margin-top: 60px; }
        .cta-box h3 { font-family: var(--font-serif); font-size: 1.75rem; margin-bottom: 16px; color: white; }
        .cta-box p { opacity: 0.9; margin-bottom: 24px; }
        .back-link { display: inline-flex; align-items: center; gap: 8px; text-decoration: none; color: var(--color-text-secondary); margin-bottom: 32px; font-weight: 500; transition: color 0.2s; }
        .back-link:hover { color: var(--color-dark-green); }
        .internal-blog-link { display: block; background: #FAFAFA; padding: 24px; border-radius: 16px; border-left: 4px solid var(--color-gold); margin: 40px 0; text-decoration: none; color: inherit; transition: all 0.2s ease; }
        .internal-blog-link:hover { transform: translateX(4px); background: #F4F1EA; }
        .disclaimer-box { background: #F4F1EA; border-radius: 16px; padding: 24px 28px; margin: 40px 0; font-size: 0.95rem; color: #555; border-left: 4px solid var(--color-gold); font-style: italic; }
        .author-box { margin-bottom: 32px; font-size: 0.95rem; color: #555; font-style: italic; text-align: center; }
    </style>
    <!-- Clarity Tracking -->
    <script type="text/javascript">
        (function (c, l, a, r, i, t, y) {
            c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments) };
            t = l.createElement(r); t.async = 1; t.src = "https://www.clarity.ms/tag/" + i;
            y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
        })(window, document, "clarity", "script", "vlfb2lz6qi");
    </script>
</head>
<body>
    <header>
        <nav class="nav">
            <div class="container">
                <div class="nav-content">
                    <a href="index.html" class="logo">Ancestor Lens</a>
                    <div class="nav-links">
                        <a href="index.html#features" data-i18n="nav-features">Features</a>
                        <a href="index.html#faq" data-i18n="nav-faq">FAQ</a>
                        <a href="blog.html" data-i18n="nav-blog">Blog</a>
                    </div>
                    <div class="nav-actions">
                        <div class="lang-switcher">
                            <button class="lang-btn" id="langBtn">
                                <span class="current-lang">EN</span>
                                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <polyline points="6 9 12 15 18 9"></polyline>
                                </svg>
                            </button>
                            <div class="lang-dropdown" id="langDropdown">
                                <button onclick="changeLanguage('en')">EN</button>
                                <button onclick="changeLanguage('de')">DE</button>
                                <button onclick="changeLanguage('es')">ES</button>
                            </div>
                        </div>
                        <div class="nav-actions-btns">
                            <a href="index.html#download" class="btn btn-primary btn-sm btn-dynamic-link" target="_blank" data-i18n="nav-download">Download App</a>
                        </div>
                        <button class="burger-menu" id="burgerMenu" aria-label="Toggle Menu">
                            <span class="bar"></span>
                            <span class="bar"></span>
                            <span class="bar"></span>
                        </button>
                    </div>
                </div>
            </div>
            <!-- Mobile Menu Dropdown -->
            <div class="mobile-menu-overlay" id="mobileMenuOverlay">
                <div class="mobile-menu-content">
                    <a href="index.html#features" data-i18n="nav-features">Features</a>
                    <a href="index.html#faq" data-i18n="nav-faq">FAQ</a>
                    <a href="blog.html" data-i18n="nav-blog">Blog</a>
                </div>
            </div>
        </nav>
    </header>
    <main>
        <article class="post-page">
            <div class="container">
                <a href="blog.html" class="back-link">
                    <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                        <path d="M13 15L8 10L13 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                    </svg>
                    Back to all articles
                </a>
                
                <header class="post-header">
                    <div class="breadcrumb">
                        <a href="index.html">Home</a> &gt; <a href="blog.html">Blog</a> &gt; <span>{meta_title}</span>
                    </div>
                    <span class="post-tag">{category}</span>
                    <h1 class="post-title">{meta_title}</h1>
                    <p class="subtitle">{meta_description}</p>
                    <div class="post-meta">
                        Published: 2026-07-10 | Updated: 2026-07-10<br>
                    </div>
                    <div class="author-box">
                        <p>Written by the Ancestor Lens Editorial Team. We provide carefully researched insights into AI visual analysis, genealogy, and family history.</p>
                    </div>

                    <div class="try-it-block">
                        <h3>Try It Yourself</h3>
                        <p>Upload your selfie and discover which countries your face visually resembles.</p>
                        <div class="cta-store-buttons">
                            <a href="https://apps.apple.com/us/app/ancestor-lens-ancestry-dna/id6755190587" class="store-btn apple-store" target="_blank">
                                <img src="app-store-badge.png" alt="Download Ancestor Lens on App Store">
                            </a>
                            <a href="https://play.google.com/store/apps/details?id=com.deepqeeb.ancestorlens" class="store-btn google-play" target="_blank">
                                <img src="google-play-badge.png" alt="Get Ancestor Lens on Google Play">
                            </a>
                        </div>
                    </div>
                </header>

                <div class="post-visual">
                    <img src="{image}" alt="{alt_text}" style="width: 100%; height: 100%; object-fit: cover;">
                </div>

                <div class="post-content">
"""

footer = """
                    <div class="cta-box">
                        <h3>Discover Your Face Heritage with Ancestor Lens</h3>
                        <p>Ready to see what country your facial features may resemble? Try Ancestor Lens and discover your face heritage instantly. No DNA required.</p>
                        <div class="cta-store-buttons" style="display: flex; justify-content: center; gap: 40px; margin-top: 24px;">
                            <a href="https://apps.apple.com/us/app/ancestor-lens-ancestry-dna/id6755190587" class="store-btn apple-store btn-large" target="_blank" aria-label="Download on App Store">
                                <img src="app-store-badge.png" alt="Download Ancestor Lens on App Store" style="height: 48px;">
                            </a>
                            <a href="https://play.google.com/store/apps/details?id=com.deepqeeb.ancestorlens" class="store-btn google-play btn-large" target="_blank" aria-label="Get it on Google Play">
                                <img src="google-play-badge.png" alt="Get Ancestor Lens on Google Play" style="height: 48px;">
                            </a>
                        </div>
                    </div>

                    <div class="disclaimer-box">
                        <strong>Please note:</strong> Ancestor Lens is designed for fun, curiosity, and entertainment. AI face analysis cannot prove your real ethnicity, nationality, or DNA ancestry. Results are based on visual similarity and should not be treated as scientific or official identity information.
                    </div>
                </div>
            </div>
        </article>
    </main>

    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-left">Ancestor Lens © 2026. All rights reserved.</div>
                <div class="footer-right">
                    <span class="social-label">Follow Us</span>
                    <div class="social-links">
                        <a href="https://www.tiktok.com/@ancestorlens" target="_blank">TikTok</a>
                        <a href="https://x.com/AncestorLensApp" target="_blank">X</a>
                        <a href="https://www.youtube.com/channel/UCjsBum77RkPcAt3qVzpQ8ZA" target="_blank">YouTube</a>
                    </div>
                </div>
            </div>
        </div>
    </footer>

    <script src="translations.js"></script>
    <script src="script.js"></script>
</body>
</html>
"""

def make_html(url, meta_title, meta_desc, image, alt_text, category, keywords, content_html):
    return header_nav.format(
        url=url, meta_title=meta_title, meta_description=meta_desc, 
        image=image, alt_text=alt_text, category=category, keywords=keywords
    ) + content_html + footer

def save_article(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    pass
