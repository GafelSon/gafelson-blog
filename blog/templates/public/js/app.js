// app.js

/**
 * Main application entry point.
 * This module initializes the core functionality, handles global configurations, 
 * and manages event listeners for the application.
 */

import './_console.js'
import './commands/_btt.js'
import { loading } from "./commands/_loading.js"
import { initThemeManager } from "./commands/_theme.js"
import { initUpdateManager } from "./commands/_update.js"
import { initProgressManager } from "./commands/_progress.js"


const managers = new Map();

function cleanupManagers() {
    if (managers.has('theme') && managers.get('theme')?.cleanup) {
        try {
            managers.get('theme').cleanup();
        } catch (e) {
            console.error('Error cleaning up theme manager:', e);
        }
        managers.delete('theme');
    }
    
    if (managers.has('update') && managers.get('update')?.cleanup) {
        try {
            managers.get('update').cleanup();
        } catch (e) {
            console.error('Error cleaning up update manager:', e);
        }
        managers.delete('update');
    }

    if (managers.has('progress') && managers.get('progress')?.cleanup) {
        try {
            managers.get('progress').cleanup();
        } catch (e) {
            console.error('Error cleaning up progress manager:', e);
        }
        managers.delete('progress');
    }
}

function initializeManagers() {
    cleanupManagers();
    const theme = initThemeManager();
    const update = initUpdateManager();
    const progress = initProgressManager();
    
    if (theme) managers.set('theme', theme);
    if (update) managers.set('update', update);
    if (progress) managers.set('progress', progress);
}

document.addEventListener('htmx:beforeRequest', () => {
    if (managers.has('progress')) {
        managers.get('progress').start();
    }
});

document.addEventListener('htmx:afterRequest', () => {
    if (managers.has('progress')) {
        managers.get('progress').complete();
    }
});

document.addEventListener('htmx:beforeSwap', () => {
    try {
        cleanupManagers();
    } catch (e) {
        console.error('Error during cleanup:', e);
    }
});
document.addEventListener('htmx:afterSettle', initializeManagers);
document.addEventListener('DOMContentLoaded', initializeManagers);
window.onload = () => (
    loading(),
    document.body.style.visibility = 'visible'
);