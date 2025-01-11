// Main JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Theme handling
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    const html = document.documentElement;

    function setTheme(isDark) {
        html.classList.toggle('dark-theme', isDark);
    }

    // Set initial theme
    setTheme(prefersDark.matches);

    // Listen for system theme changes
    prefersDark.addListener((e) => setTheme(e.matches));

    // Navigation handling
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navMenu = document.querySelector('.nav-menu');

    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});
