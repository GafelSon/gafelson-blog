// commands/_btt.js

/**
 * Handles the "Back to Top" button functionality.
 * This module manages the visibility, behavior, and smooth scrolling effect of the button, 
 * allowing users to quickly navigate to the top of the page.
 */

document.addEventListener('DOMContentLoaded', () => {
    const backToTopButton = document.getElementById('article-back-to-top');
    const mainScroll = document.getElementById('main-scroll')

    
    if (backToTopButton) {
        mainScroll.addEventListener('scroll', () => {
            if (window.scrollY < 20) {
                backToTopButton.style.opacity = '1';
            } else {
                backToTopButton.style.opacity = '.5';
            }
        });
        backToTopButton.addEventListener('click', () => {
            mainScroll.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
        backToTopButton.style.opacity = '.5';
        backToTopButton.style.transition = 'opacity 0.3s ease-in-out';
    }
});