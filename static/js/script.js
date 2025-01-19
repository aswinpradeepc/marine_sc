// Countdown Timer
function updateCountdown() {
    const conferenceDate = new Date('March 26, 2025 00:00:00').getTime();
    const now = new Date().getTime();
    const distance = conferenceDate - now;

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById('countdown').innerHTML = `
        <div>
            <span>${days}</span>
            <span>Days</span>
        </div>
        <div>
            <span>${hours}</span>
            <span>Hours</span>
        </div>
        <div>
            <span>${minutes}</span>
            <span>Minutes</span>
        </div>
        <div>
            <span>${seconds}</span>
            <span>Seconds</span>
        </div>
    `;
}


/*visible effect

document.addEventListener("DOMContentLoaded", () => {
    const sections = document.querySelectorAll("section"); // Target all sections

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("section-visible");
                observer.unobserve(entry.target); // Stop observing once it's visible
            }
        });
    }, { threshold: 0.5 }); // Trigger when 10% of the section is visible

    sections.forEach((section) => {
        section.classList.add("section-hidden"); // Start with hidden state
        observer.observe(section); // Observe each section
    });
});

*/


const cursor = document.createElement("div");
cursor.className = "custom-cursor";
document.body.appendChild(cursor);

document.addEventListener("mousemove", (e) => {
    cursor.style.left = `${e.pageX}px`;
    cursor.style.top = `${e.pageY}px`;
});

document.addEventListener("mousedown", () => {
    cursor.style.transform = "scale(1.5)";
    cursor.style.background = "#79d2e6";
});

document.addEventListener("mouseup", () => {
    cursor.style.transform = "scale(1)";
    cursor.style.background = "#0056b3";
});




// Update countdown every second
setInterval(updateCountdown, 1000);

// Contact Form Handling
document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form values
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        subject: document.getElementById('subject').value,
        message: document.getElementById('message').value
    };

    // Add animation to button
    const submitBtn = this.querySelector('.submit-btn');
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    
    // Simulate form submission (replace with actual form submission logic)
    setTimeout(() => {
        // Reset form
        this.reset();
        
        // Show success message
        submitBtn.innerHTML = '<i class="fas fa-check"></i> Sent Successfully';
        submitBtn.style.background = '#28a745';
        
        // Reset button after 3 seconds
        setTimeout(() => {
            submitBtn.innerHTML = '<span>Send Message</span><i class="fas fa-paper-plane"></i>';
            submitBtn.style.background = '';
        }, 3000);
    }, 2000);
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Scroll Animation Observer
const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.visibility = 'visible';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe elements with animation classes
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.fade-in, .slide-in-left, .slide-in-right');
    animatedElements.forEach(el => {
        el.style.visibility = 'hidden';
        observer.observe(el);
    });
    updateCountdown();
});

// Initialize the countdown on page load
document.addEventListener('DOMContentLoaded', updateCountdown);

// Mobile Menu Toggle
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const navLinks = document.querySelector('.nav-links');

mobileMenuBtn.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    document.body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
});

// Close mobile menu when clicking a link
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        document.body.style.overflow = '';
    });
});

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if (!navLinks.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
        navLinks.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// Theme Section Interaction
document.querySelectorAll('.theme-card').forEach(card => {
    card.addEventListener('click', function () {
        // If the clicked card is already active, collapse it
        if (this.classList.contains('active')) {
            this.classList.remove('active');
        } else {
            // Collapse all other cards
            document.querySelectorAll('.theme-card').forEach(c => c.classList.remove('active'));
            // Expand the clicked card
            this.classList.add('active');
        }
    });
});
