// commands/_progress.js

/**
 * Handles the loading progress bar functionality.
 * This module manages a progress bar that appears during HTMX requests
 * and provides visual feedback about loading states.
 */

class LoadingProgress {
    constructor() {
        this.progressBar = document.createElement('div');
        this.setupProgressBar();
        this.progress = 0;
        this.progressInterval = null;
    }

    setupProgressBar() {
        this.progressBar.className = 'loading-progress-bar';
        Object.assign(this.progressBar.style, {
            position: 'fixed',
            top: '0',
            left: '0',
            width: '0%',
            height: '3px',
            backgroundColor: 'var(--main-color)',
            transition: 'width 0.2s ease-in-out',
            zIndex: '9999',
            opacity: '0',
            transform: 'translateZ(0)',
            willChange: 'width, opacity'
        });

        document.body.appendChild(this.progressBar);
    }

    start() {
        this.progress = 0;
        this.progressBar.style.opacity = '1';
        this.progressBar.style.width = '0%';

        // Simulate progress
        this.progressInterval = setInterval(() => {
            if (this.progress < 90) {
                this.progress += (90 - this.progress) * 0.05;
                this.progressBar.style.width = `${this.progress}%`;
            }
        }, 100);
    }

    complete() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }

        this.progress = 100;
        this.progressBar.style.width = '100%';

        setTimeout(() => {
            this.progressBar.style.opacity = '0';
            setTimeout(() => {
                this.progress = 0;
                this.progressBar.style.width = '0%';
            }, 200);
        }, 200);
    }

    cleanup() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
        if (document.body.contains(this.progressBar)) {
            document.body.removeChild(this.progressBar);
        }
    }
}

let progressInstance = null;

export function initProgressManager() {
    if (progressInstance) {
        progressInstance.cleanup();
    }
    progressInstance = new LoadingProgress();
    return progressInstance;
}