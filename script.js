// Navigation scroll effect
const nav = document.querySelector('.nav');
window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
        nav.classList.add('scrolled');
    } else {
        nav.classList.remove('scrolled');
    }
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Animate elements on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe cards and sections
document.querySelectorAll('.value-card, .step, .faq-item, .ethnicity-card, .twin-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(el);
});

// Animate ethnicity bars when visible
const barObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const fills = entry.target.querySelectorAll('.ethnicity-fill');
            fills.forEach(fill => {
                const width = fill.style.width;
                fill.style.width = '0%';
                setTimeout(() => {
                    fill.style.width = width;
                }, 100);
            });
            barObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const ethnicityCard = document.querySelector('.ethnicity-card');
if (ethnicityCard) {
    barObserver.observe(ethnicityCard);
}

// FAQ accordion functionality
document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', function () {
        const item = this.closest('.faq-item');
        const isActive = item.classList.contains('active');

        // Close all other FAQs
        document.querySelectorAll('.faq-item').forEach(el => {
            el.classList.remove('active');
        });

        // Toggle current FAQ
        if (!isActive) {
            item.classList.add('active');
        }
    });
});

// Parallax effect removed per user request

// Hover effects for cards
document.querySelectorAll('.value-card').forEach(card => {
    card.addEventListener('mouseenter', function () {
        this.style.transform = 'translateY(-8px)';
        this.style.boxShadow = '0 12px 32px rgba(0, 0, 0, 0.12)';
    });

    card.addEventListener('mouseleave', function () {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = 'none';
    });
});

// --- Language Switcher Logic ---

const langBtn = document.getElementById('langBtn');
const langDropdown = document.getElementById('langDropdown');
const currentLangSpan = langBtn ? langBtn.querySelector('.current-lang') : null;

// Toggle dropdown
if (langBtn && langDropdown) {
    langBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        langDropdown.classList.toggle('active');
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', () => {
        langDropdown.classList.remove('active');
    });
}

// Initialize language
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('ancestor-lens-lang') || 'en';
    changeLanguage(savedLang);
});

function changeLanguage(lang) {
    if (typeof translations === 'undefined' || !translations[lang]) return;

    // Update all elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const translation = translations[lang][key];

        if (translation) {
            // Use innerHTML for titles/text that might contain spans/break tags
            if (key.includes('title') || key.includes('h2') || key.includes('badge') || key.includes('emo-h2')) {
                el.innerHTML = translation;
            } else {
                el.textContent = translation;
            }
        }
    });

    // Update current lang display
    if (currentLangSpan) {
        currentLangSpan.textContent = lang.toUpperCase();
    }

    // Persist choice
    localStorage.setItem('ancestor-lens-lang', lang);

    // Update document lang attribute
    document.documentElement.lang = lang;
}

// Make changeLanguage global for the onclick handlers
window.changeLanguage = changeLanguage;

// --- Blog Carousel Logic ---
const blogGrid = document.getElementById('blogGrid');
const blogWrapper = document.querySelector('.blog-grid-wrapper');
const blogDotsContainer = document.querySelector('.blog-dots');
const dots = document.querySelectorAll('.blog-dots .dot');
const prevBtn = document.getElementById('blogPrev');
const nextBtn = document.getElementById('blogNext');

if (blogGrid && dots.length > 0) {
    let currentIndex = 0;
    const totalItems = blogGrid.querySelectorAll('.blog-card').length;
    const visibleCardsDesktop = 3;
    const isMobile = () => window.innerWidth <= 968;

    const updateDotsVisibility = () => {
        if (isMobile()) {
            dots.forEach(dot => dot.style.display = 'block');
        } else {
            // On desktop, we only need dots for indices 0 to (total - visible)
            dots.forEach((dot, i) => {
                dot.style.display = i <= (totalItems - visibleCardsDesktop) ? 'block' : 'none';
            });
        }
    };

    const updateCarousel = () => {
        if (isMobile()) {
            // Mobile uses native scroll, dots updated via scroll event
            return;
        }

        const cardWidth = blogGrid.querySelector('.blog-card').offsetWidth;
        const gap = parseInt(window.getComputedStyle(blogGrid).gap) || 32;
        
        // Ensure index is within bounds
        const maxIndex = totalItems - visibleCardsDesktop;
        if (currentIndex > maxIndex) currentIndex = maxIndex;
        if (currentIndex < 0) currentIndex = 0;

        const offset = currentIndex * (cardWidth + gap);
        blogGrid.style.transform = `translateX(-${offset}px)`;
        
        // Update dots
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentIndex);
        });

        // Update nav buttons
        if (prevBtn && nextBtn) {
            prevBtn.disabled = currentIndex === 0;
            nextBtn.disabled = currentIndex >= maxIndex;
        }
    };

    // Mobile scroll handling
    blogWrapper.addEventListener('scroll', () => {
        if (!isMobile()) return;
        const index = Math.round(blogWrapper.scrollLeft / blogWrapper.offsetWidth);
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === index);
        });
        currentIndex = index;
    });

    // Desktop Nav handling
    if (prevBtn && nextBtn) {
        prevBtn.addEventListener('click', () => {
            if (currentIndex > 0) {
                currentIndex--;
                updateCarousel();
            }
        });

        nextBtn.addEventListener('click', () => {
            if (currentIndex < totalItems - visibleCardsDesktop) {
                currentIndex++;
                updateCarousel();
            }
        });
    }

    // Click on dots
    dots.forEach((dot) => {
        dot.addEventListener('click', () => {
            const index = parseInt(dot.getAttribute('data-index'));
            
            if (isMobile()) {
                currentIndex = index;
                blogWrapper.scrollTo({
                    left: index * blogWrapper.offsetWidth,
                    behavior: 'smooth'
                });
            } else {
                const maxIndex = totalItems - visibleCardsDesktop;
                currentIndex = Math.min(index, maxIndex);
                updateCarousel();
            }
        });
    });

    // Initialize & Listeners
    window.addEventListener('resize', () => {
        updateDotsVisibility();
        updateCarousel();
    });

    updateDotsVisibility();
    updateCarousel();
}
// --- Mobile Menu Logic ---
const burgerMenu = document.getElementById('burgerMenu');
const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
const mobileLinks = document.querySelectorAll('.mobile-menu-content a');

if (burgerMenu && mobileMenuOverlay) {
    burgerMenu.addEventListener('click', () => {
        burgerMenu.classList.toggle('active');
        mobileMenuOverlay.classList.toggle('active');
        document.body.style.overflow = mobileMenuOverlay.classList.contains('active') ? 'hidden' : '';
    });

    mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
            burgerMenu.classList.remove('active');
            mobileMenuOverlay.classList.remove('active');
            document.body.style.overflow = '';
        });
    });
}

// --- Dynamic Header Download Button Logic ---
function setDynamicDownloadLink() {
    const downloadBtns = document.querySelectorAll('.btn-dynamic-link');
    if (downloadBtns.length === 0) return;

    let targetUrl;
    let openInNewTab = true;

    // All platforms → anchor to download section

    // Check if we're on the main page or a blog page
    const isMainPage = window.location.pathname.endsWith('index.html') || 
                       window.location.pathname.endsWith('/') ||
                       window.location.pathname === '' ||
                       window.location.pathname.split('/').pop() === 'index.html';
    
    targetUrl = isMainPage ? "#download" : "index.html#download";
    openInNewTab = false;


    downloadBtns.forEach(btn => {
        btn.href = targetUrl;
        if (openInNewTab) {
            btn.setAttribute('target', '_blank');
        } else {
            btn.removeAttribute('target');
        }
    });
}

// Ensure dynamic link is set on load
document.addEventListener('DOMContentLoaded', () => {
    setDynamicDownloadLink();
});
