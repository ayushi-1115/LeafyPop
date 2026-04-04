// LeafyPop Store Logic Refinements

document.addEventListener('DOMContentLoaded', () => {
    console.log("LeafyPop Store script loaded.");

    // 1. Scroll Progress Bar logic
    const scrollProgress = document.getElementById('scrollProgress');
    if (scrollProgress) {
        window.onscroll = () => {
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            scrollProgress.style.width = scrolled + "%";
        };
    }

    // 2. Mobile Menu Logic (Moved from index.html)
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.onclick = () => {
            mobileMenu.classList.toggle('hidden');
            // Add a subtle slide animation or opacity shift if needed
            if (!mobileMenu.classList.contains('hidden')) {
                mobileMenu.classList.add('animate-fade-in');
            }
        };
    }

    // 3. Navbar background shift on scroll
    const navbar = document.querySelector('nav');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('shadow-lg', 'py-1');
                navbar.classList.remove('shadow-sm', 'py-0');
            } else {
                navbar.classList.remove('shadow-lg', 'py-1');
                navbar.classList.add('shadow-sm', 'py-0');
            }
        });
    }
});
