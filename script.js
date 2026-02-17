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
        const svg = this.querySelector('svg');
        const isOpen = svg.style.transform === 'rotate(180deg)';

        // Close all other FAQs
        document.querySelectorAll('.faq-question svg').forEach(s => {
            s.style.transform = 'rotate(0deg)';
        });

        // Toggle current FAQ
        if (!isOpen) {
            svg.style.transform = 'rotate(180deg)';
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
