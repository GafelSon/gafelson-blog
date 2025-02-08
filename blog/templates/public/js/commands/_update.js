// commands/_update.js

/**
 * Manages update notifications and version history display.
 * This module is responsible for showing new features, bug fixes,
 * and other important updates to users through a modal interface.
 */

const UPDATE_STORAGE_KEY = 'last_update_viewed';
let CURRENT_VERSION = '1.0.0';
let updateManagerInstance = null;

function compareVersions(versionA, versionB) {
  const aParts = versionA.split('.').map(Number);
  const bParts = versionB.split('.').map(Number);

  for (let i = 0; i < Math.max(aParts.length, bParts.length); i++) {
    const a = aParts[i] || 0;
    const b = bParts[i] || 0;

    if (a > b) return 1;
    if (a < b) return -1;
  }

  return 0;
}

class UpdateManager {
  constructor() {
    if (updateManagerInstance) {
      updateManagerInstance.cleanup();
      updateManagerInstance = null;
    }
    
    this.updateButton = document.getElementById('update-info');
    this.activeModal = null;
    this.modalOverlay = null;
    this.lastViewedVersion = localStorage.getItem(UPDATE_STORAGE_KEY) || '0.0.0';
    this.updateHistory = [];
    this.boundHandleClick = this.handleUpdateClick.bind(this);
    if (this.updateButton && !this.updateButton.dataset.listenerAttached) {
      this.updateButton.addEventListener('click', this.boundHandleClick);
      this.updateButton.dataset.listenerAttached = "true";
    }
    
    updateManagerInstance = this;
    this.init();
  }

  cleanup() {
    if (this.activeModal) {
      this.toggleModal();
    }
    if (this.updateButton && this.boundHandleClick && this.updateButton.dataset.listenerAttached) {
      this.updateButton.removeEventListener('click', this.boundHandleClick);
      delete this.updateButton.dataset.listenerAttached;
    }
    updateManagerInstance = null;
  }

  async init() {
    await this.fetchUpdateHistory();
    this.checkForNewUpdates();
  }

  checkForNewUpdates() {
    if (compareVersions(CURRENT_VERSION, this.lastViewedVersion) > 0) {
      console.log('* New update detected!');
      if (this.updateButton) {
        this.updateButton.classList.add('has-updates');
      }
    } else {
      console.log('* No new updates.');
    }
  }

  async fetchUpdateHistory() {
    try {
      const response = await fetch('/api/update-history/');
      if (!response.ok) {
        throw new Error('Failed to fetch update history');
      }
      const data = await response.json();
      this.updateHistory = data.map(update => ({
        version: update.version,
        date: update.date,
        features: this.parseQuerySet(update.features),
        bugFixes: this.parseQuerySet(update.bug_fixes)
      }));
      
      if (this.updateHistory.length > 0) {
        CURRENT_VERSION = this.updateHistory[0].version;
      }
    } catch (error) {
      console.error('Error fetching update history:', error);
      this.updateHistory = [];
    }
  }
  
  parseQuerySet(querySetString) {
    if (!querySetString) return [];
    
    try {
      const matches = querySetString.match(/\[(.*)\]/);
      if (!matches || !matches[1]) return [];
  
      return matches[1]
        .split('), (')
        .map(item => {
          const match = item.match(/'([^']+)'/);
          if (!match) return '';
          return match[1].replace(/\\u([0-9a-fA-F]{4})/g, (_, code) =>
            String.fromCharCode(parseInt(code, 16))
          );
        })
        .filter(Boolean);
    } catch (error) {
      console.error('Error parsing QuerySet:', error);
      return [];
    }
  }

  handleUpdateClick(e) {
    e.preventDefault();
    e.stopPropagation();
    this.toggleModal();
  }

  toggleModal() {
    if (this.activeModal) {
      if (document.body.contains(this.activeModal)) {
        document.body.removeChild(this.activeModal);
      }
      if (document.body.contains(this.modalOverlay)) {
        document.body.removeChild(this.modalOverlay);
      }
      this.activeModal = null;
      this.modalOverlay = null;
      return;
    }
    this.createModal();
    this.setupModalCloseListener();
    localStorage.setItem(UPDATE_STORAGE_KEY, CURRENT_VERSION);
    this.updateButton?.classList.remove('has-updates');
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
    overlay.addEventListener('click', () => this.toggleModal());
    return overlay;
  }

  createModalContent() {
    const modal = document.createElement('div');
    Object.assign(modal.style, {
      position: 'fixed',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      width: '90%',
      maxWidth: '600px',
      maxHeight: '80vh',
      background: 'var(--bg-color)',
      borderRadius: '0.75rem',
      border: '4px solid var(--sub-alt-color)',
      overflow: 'hidden',
      zIndex: '1000',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      padding: '1.5rem',
      display: 'flex',
      flexDirection: 'column'
    });
  
    modal.addEventListener('click', (e) => {
      e.stopPropagation();
    });
    
    const title = document.createElement('h2');
    title.textContent = 'به‌روزرسانی‌ها';
    Object.assign(title.style, {
      color: 'var(--main-color)',
      marginBottom: '1.5rem',
      fontSize: '1.5rem',
      fontWeight: 'bold',
      textAlign: 'right'
    });
  
    const updateList = document.createElement('div');
    updateList.className = 'update-list';
    Object.assign(updateList.style, {
      display: 'flex',
      flexDirection: 'column',
      gap: '2rem',
      flex: '1 1 auto',
      overflowY: 'auto',
      marginBottom: '1rem',
      paddingLeft: '10px'
    });
  
    this.updateHistory.forEach(update => {
      const updateEntry = this.createUpdateEntry(update);
      updateList.appendChild(updateEntry);
    });
  
    const buttonContainer = document.createElement('div');
    Object.assign(buttonContainer.style, {
      display: 'flex',
      justifyContent: 'flex-end',
      marginTop: 'auto',
      paddingTop: '1rem'
    });
  
    const closeButton = document.createElement('button');
    closeButton.textContent = 'متوجه شدم';
    Object.assign(closeButton.style, {
      position: 'relative',
      background: 'var(--main-color)',
      color: 'var(--bg-color)',
      border: 'none',
      padding: '0.75rem 1.5rem',
      borderRadius: '0.5rem',
      cursor: 'pointer',
      fontSize: '1rem',
      fontWeight: 'bold'
    });
    closeButton.addEventListener('click', () => this.toggleModal());
  
    buttonContainer.appendChild(closeButton);
    modal.appendChild(title);
    modal.appendChild(updateList);
    modal.appendChild(buttonContainer);
  
    return modal;
  }

  createUpdateEntry(update) {
    const entry = document.createElement('div');
    Object.assign(entry.style, {
      borderBottom: '1px solid var(--sub-alt-color)',
      paddingBottom: '1.5rem'
    });
  
    const header = document.createElement('div');
    Object.assign(header.style, {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: '1rem',
      direction: 'rtl'
    });
  
    const version = document.createElement('h3');
    version.textContent = `نسخه ${update.version}`;
    Object.assign(version.style, {
      color: 'var(--main-color)',
      fontSize: '1.1rem',
      fontWeight: 'bold'
    });
  
    const date = document.createElement('span');
    date.textContent = update.date;
    Object.assign(date.style, {
      color: 'var(--sub-color)',
      fontSize: '0.9rem'
    });
  
    header.appendChild(version);
    header.appendChild(date);
  
    const content = document.createElement('div');
    Object.assign(content.style, {
      display: 'flex',
      flexDirection: 'column',
      gap: '1rem',
      direction: 'rtl'
    });
  
    if (update.features && Array.isArray(update.features) && update.features.length > 0) {
      content.appendChild(this.createUpdateSection('ویژگی‌های جدید', update.features));
    }
  
    if (update.bugFixes && Array.isArray(update.bugFixes) && update.bugFixes.length > 0) {
      content.appendChild(this.createUpdateSection('رفع اشکالات', update.bugFixes));
    }
  
    entry.appendChild(header);
    entry.appendChild(content);
  
    return entry;
  }
  
  createUpdateSection(title, items) {
    const section = document.createElement('div');
    Object.assign(section.style, {
      display: 'flex',
      flexDirection: 'column',
      gap: '0.5rem'
    });
  
    const sectionTitle = document.createElement('h4');
    sectionTitle.textContent = title;
    Object.assign(sectionTitle.style, {
      color: 'var(--text-color)',
      fontSize: '1rem',
      fontWeight: 'bold',
      marginBottom: '0.5rem'
    });
  
    const list = document.createElement('ul');
    Object.assign(list.style, {
      listStyle: 'none',
      padding: 0,
      margin: 0
    });
  
    (Array.isArray(items) ? items : []).forEach(item => {
      const listItem = document.createElement('li');
      listItem.textContent = item;
      Object.assign(listItem.style, {
        color: 'var(--text-color)',
        padding: '0.25rem 0',
        display: 'flex',
        alignItems: 'center',
        gap: '0.5rem'
      });
  
      const bullet = document.createElement('span');
      bullet.textContent = '•';
      bullet.style.color = 'var(--main-color)';
      
      listItem.insertBefore(bullet, listItem.firstChild);
      list.appendChild(listItem);
    });
  
    section.appendChild(sectionTitle);
    section.appendChild(list);
  
    return section;
  }
  
  setupModalCloseListener() {
    const clickHandler = (e) => {
      if (this.activeModal && !this.activeModal.contains(e.target) && e.target !== this.updateButton) {
        this.toggleModal();
      }
    };
    document.addEventListener('click', clickHandler);
    const modalCloseObserver = new MutationObserver((mutations) => {
      mutations.forEach(() => {
        if (!document.body.contains(this.activeModal)) {
          document.removeEventListener('click', clickHandler);
          modalCloseObserver.disconnect();
        }
      });
    });
    
    modalCloseObserver.observe(document.body, { childList: true, subtree: true });
  }

}

export function initUpdateManager() {
    if (updateManagerInstance) {
      updateManagerInstance.cleanup();
    }
    const manager = new UpdateManager();
    return manager;
}
