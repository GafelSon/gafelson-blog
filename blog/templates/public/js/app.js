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
}

function initializeManagers() {
    cleanupManagers();
    const theme = initThemeManager();
    const update = initUpdateManager();
    
    if (theme) managers.set('theme', theme);
    if (update) managers.set('update', update);
}

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