document.addEventListener('DOMContentLoaded', () => {
    const mobileNav = document.querySelector('.mobile-nav');
    const openNavIcon = document.querySelector('.openNav');
    const closeNavIcon = document.querySelector('.closeNav');
    const navbar = document.getElementById('navbar');

    let lastScrollY = window.scrollY;

    // Burger Menu Toggle Logic
    openNavIcon.addEventListener('click', () => {
        mobileNav.classList.add('active');
        openNavIcon.style.display = 'none';
        closeNavIcon.style.display = 'flex';
    });

    closeNavIcon.addEventListener('click', () => {
        mobileNav.classList.remove('active');
        closeNavIcon.style.display = 'none';
        openNavIcon.style.display = 'flex';
    });

    // Navbar Scroll Behavior Logic
    window.addEventListener('scroll', () => {
        if (lastScrollY < window.scrollY) {
            // Scrolling Down
            navbar.classList.add('hidden');
        } else {
            // Scrolling Up
            navbar.classList.remove('hidden');
        }
        lastScrollY = window.scrollY;
    });
});