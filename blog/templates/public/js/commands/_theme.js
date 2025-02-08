// commands/_theme.js

/**
 * Manages theme settings and appearance customization.
 * This module is responsible for handling light/dark mode, applying user preferences, 
 * and dynamically updating the UI based on theme changes.
 */

// Theme Constants & Config
const THEME_STORAGE_KEY = 'selected_theme';
const DEFAULT_THEME = 'material';

// Theme Color
const THEMES = {
    "material": {
        "bgColor": "#263238",
        "mainColor": "#80cbc4",
        "caretColor": "#80cbc4",
        "subColor": "#4c6772",
        "subAltColor": "#2e3c43",
        "textColor": "#e6edf3",
        "errorColor": "#fb4934",
        "errorExtraColor": "#cc241d",
        "colorfulErrorColor": "#fb4934",
        "colorfulErrorExtraColor": "#cc241d"
    },
    "matrix": {
        "bgColor": "#000000",
        "mainColor": "#15ff00",
        "caretColor": "#15ff00",
        "subColor": "#006500",
        "subAltColor": "#032000",
        "textColor": "#d1ffcd",
        "errorColor": "#da3333",
        "errorExtraColor": "#791717",
        "colorfulErrorColor": "#da3333",
        "colorfulErrorExtraColor": "#791717"
    },
    "modern_ink": {
        "bgColor": "#ffffff",
        "mainColor": "#ff360d",
        "caretColor": "#ff0000",
        "subColor": "#b7b7b7",
        "subAltColor": "#ececec",
        "textColor": "#000000",
        "errorColor": "#d70000",
        "errorExtraColor": "#b00000",
        "colorfulErrorColor": "#000000",
        "colorfulErrorExtraColor": "#000000"
    },
    "serika": {
        "bgColor": "#e1e1e3",
        "mainColor": "#e2b714",
        "caretColor": "#e2b714",
        "subColor": "#aaaeb3",
        "subAltColor": "#d1d3d8",
        "textColor": "#323437",
        "errorColor": "#da3333",
        "errorExtraColor": "#791717",
        "colorfulErrorColor": "#da3333",
        "colorfulErrorExtraColor": "#791717"
    },
    "soaring_skies": {
        "bgColor": "#fff9f2",
        "mainColor": "#55c6f0",
        "caretColor": "#1e107a",
        "subColor": "#1e107a",
        "subAltColor": "#e5ddd4",
        "textColor": "#1d1e1e",
        "errorColor": "#fb5745",
        "errorExtraColor": "#b03c30",
        "colorfulErrorColor": "#fb5745",
        "colorfulErrorExtraColor": "#b03c30"
    },
    "miami_nights": {
        "bgColor": "#18181a",
        "mainColor": "#e4609b",
        "caretColor": "#e4609b",
        "subColor": "#47bac0",
        "subAltColor": "#0f0f10",
        "textColor": "#fff",
        "errorColor": "#fff591",
        "errorExtraColor": "#b6af68",
        "colorfulErrorColor": "#fff591",
        "colorfulErrorExtraColor": "#b6af68"
    },
    "matcha_moccha": {
        "bgColor": "#523525",
        "mainColor": "#7ec160",
        "caretColor": "#7ec160",
        "subColor": "#9e6749",
        "subAltColor": "#422b1e",
        "textColor": "#ecddcc",
        "errorColor": "#fb4934",
        "errorExtraColor": "#cc241d",
        "colorfulErrorColor": "#fb4934",
        "colorfulErrorExtraColor": "#cc241d"
    },
    "iceberg_light": {
        "bgColor": "#e8e9ec",
        "mainColor": "#2d539e",
        "caretColor": "#262a3f",
        "subColor": "#adb1c4",
        "subAltColor": "#ccceda",
        "textColor": "#33374c",
        "errorColor": "#cc517a",
        "errorExtraColor": "#cc3768",
        "colorfulErrorColor": "#cc517a",
        "colorfulErrorExtraColor": "#cc3768"
    },
    "horizon": {
        "bgColor": "#1c1e26",
        "mainColor": "#c4a88a",
        "caretColor": "#bbbbbb",
        "subColor": "#db886f",
        "subAltColor": "#17181f",
        "textColor": "#bbbbbb",
        "errorColor": "#d55170",
        "errorExtraColor": "#ff3d3d",
        "colorfulErrorColor": "#d55170",
        "colorfulErrorExtraColor": "#d55170"
    },
    "aether": {
        "bgColor": "#101820",
        "mainColor": "#eedaea",
        "caretColor": "#eedaea",
        "subColor": "#cf6bdd",
        "subAltColor": "#292136",
        "textColor": "#eedaea",
        "errorColor": "#ff5253",
        "errorExtraColor": "#e3002b",
        "colorfulErrorColor": "#ff5253",
        "colorfulErrorExtraColor": "#e3002b"
    },
    "blueberry_light": {
        "bgColor": "#dae0f5",
        "mainColor": "#506477",
        "caretColor": "#df4576",
        "subColor": "#92a4be",
        "subAltColor": "#c1c7df",
        "textColor": "#678198",
        "errorColor": "#df4576",
        "errorExtraColor": "#d996ac",
        "colorfulErrorColor": "#df4576",
        "colorfulErrorExtraColor": "#d996ac"
    },
    "cyberspace": {
        "bgColor": "#181c18",
        "mainColor": "#00ce7c",
        "caretColor": "#00ce7c",
        "subColor": "#9578d3",
        "subAltColor": "#131613",
        "textColor": "#c2fbe1",
        "errorColor": "#ff5f5f",
        "errorExtraColor": "#d22a2a",
        "colorfulErrorColor": "#ff5f5f",
        "colorfulErrorExtraColor": "#d22a2a"
    },
    "incognito": {
        "bgColor": "#0e0e0e",
        "mainColor": "#ff9900",
        "caretColor": "#ff9900",
        "subColor": "#555555",
        "subAltColor": "#151515",
        "textColor": "#c6c6c6",
        "errorColor": "#e44545",
        "errorExtraColor": "#e44545",
        "colorfulErrorColor": "#b13535",
        "colorfulErrorExtraColor": "#b13535"
    },
}


let themeManagerInstance = null;

class ThemeManager {
    constructor() {

        if (themeManagerInstance) {
            themeManagerInstance.cleanup();
        }
        
        this.paletteButton = document.getElementById('pallette');
        this.activeModal = null;
        this.modalOverlay = null;
        this.currentTheme = localStorage.getItem(THEME_STORAGE_KEY) || DEFAULT_THEME;
        this.faviconElement = document.querySelector('link[rel="icon"]');
        this.boundHandleClick = null;
        
        themeManagerInstance = this;
        this.init();
        return this;
    }

    cleanup() {
        if (this.activeModal) {
            this.toggleModal();
        }
        if (this.boundHandleClick && this.paletteButton) {
            this.paletteButton.removeEventListener('click', this.boundHandleClick);
        }
        this.boundHandleClick = null;
        themeManagerInstance = null;
    }
    setupEventListeners() {
        if (this.paletteButton) {
            if (this.boundHandleClick) {
                this.paletteButton.removeEventListener('click', this.boundHandleClick);
            }
            this.boundHandleClick = this.handlePaletteClick.bind(this);
            this.paletteButton.addEventListener('click', this.boundHandleClick);
        }
    }

    
    handlePaletteClick(e) {
        e.preventDefault();
        e.stopPropagation();
        this.toggleModal();
    }
    init() {
        this.loadTheme(this.currentTheme);
        this.setupEventListeners();
    }
    setupEventListeners() {
        this.paletteButton?.addEventListener('click', this.handlePaletteClick.bind(this));
    }
    setupEventListeners() {
        if (this.boundHandleClick) {
            this.paletteButton?.removeEventListener('click', this.boundHandleClick);
        }
        this.boundHandleClick = this.handlePaletteClick.bind(this);
        this.paletteButton?.addEventListener('click', this.boundHandleClick);
    }
    loadTheme(themeName) {
        const theme = THEMES[themeName];
        if (!theme) return;

        const root = document.documentElement;
        localStorage.setItem(THEME_STORAGE_KEY, themeName);
        
        Object.entries(theme).forEach(([key, value]) => {
            const cssVar = `--${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`;
            root.style.setProperty(cssVar, value);
        });
        this.updateFaviconColors(theme.bgColor, theme.mainColor);
    }
    updateFaviconColors(bgColor, mainColor) {
        if (!this.faviconElement) return;
        const updatedSvg = `<?xml version="1.0" encoding="utf-8"?><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 32 32" style="enable-background:new 0 0 32 32;"><style type="text/css">.st0{fill:${bgColor};}.st1{fill:${mainColor};}</style><rect x="0" class="st0" width="32" height="32"/><path class="st1" d="M18.1,5.2l-7.2,2.6c-0.1,0-0.2,0.1-0.2,0.3V10c0,0.2,0.2,0.3,0.4,0.3l7.8-2.8c0.1-0.1,0.2-0.2,0.2-0.3l-0.6-1.7C18.4,5.3,18.3,5.2,18.1,5.2z"/><path class="st1" d="M21.2,21.2c0.2,0.9,0,1.8-0.4,2.7c-0.4,0.9-1,1.6-1.7,2.1c-0.8,0.5-1.7,0.8-2.7,0.8H2.2c-0.1,0-0.3-0.1-0.3-0.3v-3.8c0-0.1,0.1-0.3,0.3-0.3h13.9c0.2,0,0.4-0.1,0.5-0.2c0.1-0.1,0.2-0.3,0.2-0.5s-0.1-0.4-0.2-0.5l-5.8-6.1c0,0-0.1-0.1-0.1-0.2v-3.8c0-0.1,0.1-0.2,0.2-0.2l9.1-3.5c0.1-0.1,0.3,0,0.3,0.2l1.2,3.3c0.1,0.1,0,0.3-0.1,0.3l-6.1,2.3c-0.2,0.1-0.2,0.3-0.1,0.4l4.5,4.7C20.6,19.4,21,20.2,21.2,21.2z"/><path class="st1" d="M1.6,22.7v3.8c0,0.2-0.1,0.3-0.3,0.3H0v-4.4h1.3C1.4,22.4,1.6,22.5,1.6,22.7z"/></svg>`;
        const encodedSvg = encodeURIComponent(updatedSvg);
        this.faviconElement.href = `data:image/svg+xml;charset=utf-8,${encodedSvg}`;
    }
    toggleModal() {
        if (this.activeModal) {
            this.activeModal.remove();
            this.modalOverlay.remove();
            this.activeModal = null;
            this.modalOverlay = null;
            return;
        }
        
        this.createModal();
        this.setupModalCloseListener();
    }
    createModal() {
        this.modalOverlay = this.createOverlay();
        this.activeModal = this.createModalContent();
        
        document.body.appendChild(this.modalOverlay);
        document.body.appendChild(this.activeModal);
    }
    createOverlay() {
        const overlay = document.createElement('div');
        Object.assign(overlay.style, {
            position: 'fixed',
            top: '0',
            left: '0',
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(0, 0, 0, 0.5)',
            zIndex: '999',
            pointerEvents: 'auto'
        });
        return overlay;
    }
    createModalContent() {
        const modal = document.createElement('div');
        Object.assign(modal.style, {
            position: 'fixed',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: '80%',
            maxWidth: '500px',
            maxHeight: '70vh',
            background: 'var(--bg-color)',
            borderRadius: '0.75rem',
            border: '4px solid var(--sub-alt-color)',
            overflow: 'auto',
            zIndex: '1000',
            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
        });

        const searchBox = document.createElement('input');
        searchBox.placeholder = 'جستوجو کنید...';
        Object.assign(searchBox.style, {
            width: '100%',
            padding: '0.75rem 2.5rem 0.75rem 0.75rem',
            borderRadius: '0.75rem',
            marginBottom: '1rem',
            background: 'var(--bg-color)',
            color: 'var(--text-color)',
            border: 'none',
            outline: 'none'
        });
        const searchIcon = document.createElement('div');
        searchIcon.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" 
                 fill="none" stroke="var(--text-color)" stroke-width="2" 
                 stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
        `;
        Object.assign(searchIcon.style, {
            position: 'absolute',
            right: '0.75rem',
            top: '50%',
            transform: 'translateY(70%)',
            pointerEvents: 'none',
            opacity: '0.5'
        });

        const searchContainer = document.createElement('div');        
        Object.assign(searchContainer.style, {
            position: 'relative',
            width: '100%',
            display: 'flex',
            alignItems: 'center'
        });

        searchContainer.appendChild(searchIcon);
        searchContainer.appendChild(searchBox);
        modal.appendChild(searchContainer);
        
        const themeGrid = document.createElement('div');
        themeGrid.style.display = 'grid';
        const themeButtons = Object.keys(THEMES).map(theme => 
            this.generateThemeButton(theme)
        );

        searchBox.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            themeButtons.forEach(button => {
                const matches = button.dataset.themeName.includes(query);
                button.style.display = matches ? 'block' : 'none';
            });
        });

        modal.appendChild(searchBox);
        modal.appendChild(themeGrid);
        themeGrid.append(...themeButtons);

        return modal;
    }

    generateThemeButton(themeName) {
        const theme = THEMES[themeName];
        const isActive = themeName === this.currentTheme;
        const button = document.createElement('button');
        
        button.className = 'theme-option';
        button.dataset.themeName = themeName.toLowerCase();
        Object.assign(button.style, {
            display: 'block',
            width: '100%',
            padding: '0.25rem 0',
            border: 'none',
            background: 'transparent',
            cursor: 'pointer',
            color: 'var(--text-color)'
        });

        button.innerHTML = `
            <div class="flex justify-between items-center px-2 w-full">
                <ul class="flex gap-2 justify-between items-center p-1 rounded-full" style="background: ${theme.bgColor}">
                    <li class="w-3 h-3 rounded-full" style="background: ${theme.mainColor}"></li>
                    <li class="w-3 h-3 rounded-full" style="background: ${theme.textColor}"></li>
                    <li class="w-3 h-3 rounded-full" style="background: ${theme.subColor}"></li>
                </ul>
                <div class="flex gap-2 items-center p-1 temp-container">
                    <p class="temp font-light ${isActive ? '' : 'pl-[24px]'}">${this.formatThemeName(themeName)}</p>
                    ${isActive ? `
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" 
                             fill="none" stroke="var(--main-color)" stroke-width="2" 
                             stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                    ` : ''}
                </div>
            </div>
        `;

        button.addEventListener('click', () => {
            this.currentTheme = themeName;
            this.loadTheme(themeName);
            const allButtons = this.activeModal.querySelectorAll('.theme-option');
            allButtons.forEach(btn => {
                const isActive = btn.dataset.themeName === themeName;
                const nameElement = btn.querySelector('p');
                const checkmarkContainer = btn.querySelector('.temp-container');
                
                if (isActive) {
                    nameElement.classList.remove('pl-[24px]');
                    if (!checkmarkContainer.querySelector('svg')) {
                        checkmarkContainer.innerHTML += `
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" 
                                 fill="none" stroke="var(--main-color)" stroke-width="2" 
                                 stroke-linecap="round" stroke-linejoin="round">
                                <polyline points="20 6 9 17 4 12"></polyline>
                            </svg>
                        `;
                    }
                } else {
                    nameElement.classList.add('pl-[24px]');
                    const svg = checkmarkContainer.querySelector('svg');
                    if (svg) svg.remove();
                }
            });
        });

        return button;
    }
    setupModalCloseListener() {
        const clickHandler = (e) => {
            if (!this.activeModal?.contains(e.target) && e.target !== this.paletteButton) {
                this.toggleModal();
                document.removeEventListener('click', clickHandler);
            }
        };
        document.addEventListener('click', clickHandler);
    }
    formatThemeName(name) {
        return name.split('_')
            .map(word => word[0].toUpperCase() + word.slice(1))
            .join(' ');
    }
    handlePaletteClick(e) {
        e.preventDefault();
        this.toggleModal();
    }
}
export function initThemeManager() {
    const manager = new ThemeManager();
    manager.loadTheme(localStorage.getItem(THEME_STORAGE_KEY) || DEFAULT_THEME);
}