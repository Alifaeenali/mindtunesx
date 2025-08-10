// Contact Modal functionality
const contactModal = document.getElementById('contactModal');
const showContactBtns = document.querySelectorAll('.showContact, #contactPage');
const closeBtn = document.getElementById('closeBtn');

showContactBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        contactModal.classList.add('show');
        document.body.style.overflow = 'hidden';
    });
});

closeBtn.addEventListener('click', () => {
    contactModal.classList.remove('show');
    document.body.style.overflow = 'auto';
});

contactModal.addEventListener('click', (e) => {
    if (e.target === contactModal) {
        contactModal.classList.remove('show');
        document.body.style.overflow = 'auto';
    }
});

// Contact form submission
const contactForm = document.getElementById('contactForm');
contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Thank you for your interest! We will get back to you within 24 hours to discuss your project.');
    contactModal.classList.remove('show');
    document.body.style.overflow = 'auto';
    contactForm.reset();
});