// commands/_search.js

/**
 * Handles search functionality within the application.
 * This module is responsible for processing search queries, filtering results, 
 * and updating the UI dynamically based on user input.
 */

class SpotlightSearch {
    constructor() {
        this.searchButton = document.getElementById('search');
        this.searchBox = document.createElement('input');
        this.backdrop = document.createElement('div');
        this.setupBackdrop();
        this.setupSearchBox();
        this.setupEventListeners();
        this.searchValue = '';
    }

    setupBackdrop() {
        this.backdrop.className = 'spotlight-backdrop';
        this.backdrop.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            opacity: 0;
            transition: opacity 0.2s ease-in-out;
            z-index: 998;
            display: none;
        `;
        document.body.appendChild(this.backdrop);
    }

    setupSearchBox() {
        const searchContainer = document.createElement('div');
        searchContainer.style.cssText = `
            position: relative;
            width: 90%;
            max-width: 600px;
            margin: 0 auto;
        `;

        this.searchBox.type = 'text';
        this.searchBox.placeholder = 'جستجو...';
        this.searchBox.className = 'spotlight-search';
        this.searchBox.style.cssText = `
            width: 100%;
            background: var(--bg-color);
            border: 1px solid var(--main-color);
            border-radius: 1rem;
            padding: 16px 48px 16px 16px;
            font-size: 1.1rem;
            color: var(--text-color);
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.2);
            outline: none;
            direction: rtl;
        `;

        this.searchIcon = document.createElement('div');
        this.searchIcon.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
        `;
        this.searchIcon.style.cssText = `
            position: absolute;
            right: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-color);
            opacity: 0.7;
            pointer-events: none;
        `;

        searchContainer.appendChild(this.searchBox);
        searchContainer.appendChild(this.searchIcon);

        const containerWrapper = document.createElement('div');
        containerWrapper.style.cssText = `
            position: fixed;
            top: 10%;
            left: 50%;
            transform: translateX(-50%) scale(0.95);
            width: 100%;
            z-index: 999;
            opacity: 0;
            transition: all 0.2s ease-in-out;
            display: none;
        `;
        containerWrapper.appendChild(searchContainer);
        document.body.appendChild(containerWrapper);
        this.searchContainer = containerWrapper;
    }


    setupEventListeners() {
        this.searchButton.addEventListener('click', () => this.toggleSearch());
        document.addEventListener('keydown', (e) => {
            if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                e.preventDefault();
                this.toggleSearch();
            }
            if (e.key === 'Escape' && this.isOpen()) {
                e.preventDefault();
                this.closeSearch();
            }
        });

        this.backdrop.addEventListener('click', () => this.closeSearch());
        this.searchBox.addEventListener('input', (e) => {
            this.searchValue = e.target.value;
        });
    }

    isOpen() {
        return this.backdrop.style.display === 'block';
    }

    toggleSearch() {
        if (this.isOpen()) {
            this.closeSearch();
        } else {
            this.openSearch();
        }
    }

    openSearch() {
        this.backdrop.style.display = 'block';
        this.searchContainer.style.display = 'block';
        this.backdrop.offsetHeight;
        this.searchContainer.offsetHeight;
        
        this.backdrop.style.opacity = '1';
        this.searchContainer.style.opacity = '1';
        this.searchContainer.style.transform = 'translateX(-50%) scale(1)';
        this.searchBox.value = this.searchValue;
        this.searchBox.focus();
    }

    closeSearch() {
        this.searchValue = this.searchBox.value;
        this.backdrop.style.opacity = '0';
        this.searchContainer.style.opacity = '0';
        this.searchContainer.style.transform = 'translateX(-50%) scale(0.95)';
        
        setTimeout(() => {
            this.backdrop.style.display = 'none';
            this.searchContainer.style.display = 'none';
        }, 200);
    }
}
document.addEventListener('DOMContentLoaded', () => {
    new SpotlightSearch();
});