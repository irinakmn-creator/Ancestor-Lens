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
const currentLangSpan = langBtn.querySelector('.current-lang');

// Toggle dropdown
langBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    langDropdown.classList.toggle('active');
});

// Close dropdown when clicking outside
document.addEventListener('click', () => {
    langDropdown.classList.remove('active');
});

// Initialize language
document.addEventListener('DOMContentLoaded', () => {
    const savedLang = localStorage.getItem('ancestor-lens-lang') || 'en';
    changeLanguage(savedLang);
});

function changeLanguage(lang) {
    if (!translations[lang]) return;

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
    currentLangSpan.textContent = lang.toUpperCase();

    // Persist choice
    localStorage.setItem('ancestor-lens-lang', lang);

    // Update document lang attribute
    document.documentElement.lang = lang;

    // Reset intersection observer entries if needed (optional)
    // Some translations might change element height, affecting scroll animations
}

// Make changeLanguage global for the onclick handlers
window.changeLanguage = changeLanguage;
