// commands/_loading.js
/**
 * Handles the page loading process.
 * This module is responsible for initializing and loading the necessary content and resources for the page.
 */

class LoadingPage extends HTMLElement {
    connectedCallback() {
        this.style.position = "fixed";
        this.style.top = "0";
        this.style.left = "0";
        this.style.width = "100%";
        this.style.margin = "auto";
        this.style.height = "100%";
        this.style.backgroundColor = "var(--bg-color)";
        this.style.display = "flex";
        this.style.justifyContent = "center";
        this.style.alignItems = "center";
        this.style.zIndex = "102";
        this.style.fontWeight = "900";
        this.style.fontSize = "2rem";

        const style = document.createElement('style');
        style.textContent = `
            @keyframes gradient {
                0% { background-position: 200% center; }
                100% { background-position: -200% center; }
            }
            .loading-gradient {
                background: linear-gradient(90deg, 
                    var(--text-color) 0%, 
                    var(--main-color) 50%, 
                    var(--text-color) 100%);
                background-size: 200% auto;
                color: transparent;
                -webkit-background-clip: text;
                background-clip: text;
                animation: gradient 2s linear infinite;
            }
        `;
        document.head.appendChild(style);
    }
}
customElements.define("loading-page", LoadingPage);

export function loading() {
    window.requestAnimationFrame(() => {
        const dynamicLoad = document.createElement("loading-page");
        const preLoad = document.createElement("pre");
        preLoad.style.textAlign = "center";

        preLoad.textContent = "گاف."
        preLoad.classList.add("loading-gradient");
        document.body.appendChild(dynamicLoad);
        dynamicLoad.appendChild(preLoad);

        setTimeout(() => {
            document.body.removeChild(dynamicLoad);
        }, 2500);
    });
};