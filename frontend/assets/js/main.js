/* Main App Controller */

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    setupEventListeners();
    updateAuthUI();
    const defaultMode = sessionStorage.getItem(CONFIG.STORAGE_KEYS.SELECTED_MODE) || 'general motivation';
    chatManager.setMode(defaultMode);
}

function setupEventListeners() {
    // Mode buttons
    document.querySelectorAll('.mode-btn').forEach((btn) => {
        btn.addEventListener('click', () => {
            const mode = btn.dataset.mode || 'general motivation';
            const is18Plus = btn.dataset['18plus'] === 'true';

            // Check if 18+ mode and show warning
            if (is18Plus) {
                showAgeVerification(mode, btn);
            } else {
                // Safe mode, switch directly
                document.querySelectorAll('.mode-btn').forEach((b) => b.classList.remove('active'));
                btn.classList.add('active');
                chatManager.setMode(mode);
            }
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

    // Close modals on outside click
    const authModal = document.getElementById('auth-modal');
    if (authModal) {
        authModal.addEventListener('click', (e) => {
            if (e.target.id === 'auth-modal') {
                authModal.style.display = 'none';
            }
        });
    }

    const ageModal = document.getElementById('age-modal');
    if (ageModal) {
        ageModal.addEventListener('click', (e) => {
            if (e.target.id === 'age-modal') {
                ageModal.style.display = 'none';
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

    // Set active mode button on load (Motivation is default)
    const selectedMode = sessionStorage.getItem(CONFIG.STORAGE_KEYS.SELECTED_MODE) || 'general motivation';
    const modeBtn = document.querySelector(`[data-mode="${selectedMode}"]`);
    if (modeBtn) {
        modeBtn.classList.add('active');
    }
}

function showAgeVerification(mode, btn) {
    const modal = document.getElementById('age-modal');
    const modalBody = document.getElementById('age-modal-body');
    
    const modeConfig = CONFIG.MODES[mode];

    modalBody.innerHTML = `
        <div style="margin-bottom: 20px;">
            <div style="font-size: 48px; margin-bottom: 16px;">⚠️</div>
            <h2 style="color: var(--color-primary); margin-bottom: 12px;">18+ Content Warning</h2>
            <p style="color: var(--color-text-secondary); line-height: 1.6; margin-bottom: 16px;">
                The <strong>${modeConfig.name}</strong> mode contains adult-oriented content with profanity and explicit themes.
            </p>
            <p style="color: var(--color-text-secondary); line-height: 1.6; margin-bottom: 24px;">
                <strong>Please confirm you are 18 years or older before proceeding.</strong>
            </p>
        </div>
        <div style="display: flex; gap: 12px; justify-content: center;">
            <button id="age-cancel-btn" class="btn-age-cancel">No, I'm Under 18</button>
            <button id="age-confirm-btn" class="btn-age-confirm">Yes, I'm 18+</button>
        </div>
    `;

    // Add styles for buttons
    const style = document.createElement('style');
    style.textContent = `
        .btn-age-confirm, .btn-age-cancel {
            padding: 10px 24px;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 14px;
        }
        .btn-age-confirm {
            background-color: var(--color-primary);
            color: white;
        }
        .btn-age-confirm:hover {
            opacity: 0.9;
        }
        .btn-age-cancel {
            background-color: var(--color-border);
            color: var(--color-text-primary);
        }
        .btn-age-cancel:hover {
            background-color: var(--color-border);
            opacity: 0.8;
        }
    `;
    if (!document.querySelector('style[data-age-buttons]')) {
        style.setAttribute('data-age-buttons', 'true');
        document.head.appendChild(style);
    }

    const confirmBtn = modalBody.querySelector('#age-confirm-btn');
    const cancelBtn = modalBody.querySelector('#age-cancel-btn');

    confirmBtn.addEventListener('click', () => {
        modal.style.display = 'none';
        document.querySelectorAll('.mode-btn').forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        chatManager.setMode(mode);
    });

    cancelBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    modal.style.display = 'flex';
}

// Global debug object
window.DEBUG = {
    chatManager,
    authManager,
    CONFIG
};
