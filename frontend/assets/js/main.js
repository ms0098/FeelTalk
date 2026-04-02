/* Main App Controller */

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    setupEventListeners();
    updateAuthUI();
    chatManager.setMode(localStorage.getItem(CONFIG.STORAGE_KEYS.SELECTED_MODE) || 'angry roast');
}

function setupEventListeners() {
    // Mode buttons
    document.querySelectorAll('.mode-btn').forEach((btn) => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.mode-btn').forEach((b) => b.classList.remove('active'));
            btn.classList.add('active');
            const mode = btn.dataset.mode || 'angry roast';
            chatManager.setMode(mode);
        });
    });

    // Chat form
    const chatForm = document.getElementById('chat-form');
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const input = document.getElementById('message-input');
        const message = input.value.trim();
        
        if (message) {
            chatManager.sendMessage(message);
            input.value = '';
            input.focus();
        }
    });

    // Auth buttons
    const loginBtn = document.getElementById('login-btn');
    if (loginBtn) {
        loginBtn.addEventListener('click', showSignupModal);
    }

    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            authManager.logout();
            updateAuthUI();
            chatManager.clearMessages();
            showNotification('Logged out successfully');
        });
    }

    // Modal close
    const modalClose = document.querySelector('.modal-close');
    if (modalClose) {
        modalClose.addEventListener('click', () => {
            const modal = document.getElementById('auth-modal');
            modal.style.display = 'none';
        });
    }

    // Close modal on outside click
    const modal = document.getElementById('auth-modal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target.id === 'auth-modal') {
                modal.style.display = 'none';
            }
        });
    }

    // Enter key in message input
    const messageInput = document.getElementById('message-input');
    if (messageInput) {
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                chatForm.dispatchEvent(new Event('submit'));
            }
        });
    }

    // Set active mode button on load
    const selectedMode = localStorage.getItem(CONFIG.STORAGE_KEYS.SELECTED_MODE) || 'angry roast';
    const modeBtn = document.querySelector(`[data-mode="${selectedMode}"]`);
    if (modeBtn) {
        modeBtn.classList.add('active');
    }
}

// Global debug object
window.DEBUG = {
    chatManager,
    authManager,
    CONFIG
};
