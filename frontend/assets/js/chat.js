/* Chat Module */

class ChatManager {
    constructor() {
        this.currentMode = localStorage.getItem(CONFIG.STORAGE_KEYS.SELECTED_MODE) || 'angry roast';
        this.messages = [];
        this.isLoading = false;
    }

    setMode(mode) {
        this.currentMode = mode;
        localStorage.setItem(CONFIG.STORAGE_KEYS.SELECTED_MODE, mode);
        this.updateModeUI();
    }

    updateModeUI() {
        const modeConfig = CONFIG.MODES[this.currentMode];
        
        const emojiDisplay = document.getElementById('emoji-display');
        if (emojiDisplay) {
            emojiDisplay.textContent = modeConfig.emoji;
        }

        const modeDescription = document.getElementById('mode-description');
        if (modeDescription) {
            modeDescription.innerHTML = `You're in <strong>${modeConfig.name}</strong> mode. ${modeConfig.description}. Start chatting!`;
        }

        document.querySelectorAll('.mode-btn').forEach((btn) => {
            btn.classList.toggle('active', btn.dataset.mode === this.currentMode);
        });

        const root = document.documentElement;
        root.style.setProperty('--color-primary', modeConfig.color);
        root.style.setProperty('--color-accent', modeConfig.color);
    }

    async sendMessage(userMessage) {
        if (this.isLoading || !userMessage.trim()) return;

        this.isLoading = true;
        
        this.addMessage({
            role: 'user',
            content: userMessage
        });

        this.showLoading();

        try {
            const requestBody = {
                message: userMessage,
                mode: this.currentMode
            };

            const response = await fetch(`${CONFIG.API_URL}/chat/`, {
                method: 'POST',
                headers: authManager.getHeaders(),
                body: JSON.stringify(requestBody)
            });

            if (!response.ok) {
                throw new Error('Chat request failed');
            }

            const data = await response.json();

            this.removeLoading();

            this.addMessage({
                role: 'ai',
                content: data.reply,
                metadata: {
                    language: data.detected_language,
                    style: data.detected_style
                }
            });

        } catch (error) {
            console.error('Chat error:', error);
            this.removeLoading();
            this.addMessage({
                role: 'ai',
                content: 'Oops! Something went wrong. Please try again.',
                isError: true
            });
        } finally {
            this.isLoading = false;
        }
    }

    addMessage(message) {
        this.messages.push(message);
        this.renderMessage(message);
        this.scrollToBottom();
    }

    renderMessage(message) {
        const chatMessages = document.getElementById('chat-messages');
        const welcomeSection = document.getElementById('welcome-section');

        if (this.messages.length === 1) {
            welcomeSection.style.display = 'none';
            chatMessages.style.display = 'flex';
        }

        const messageEl = document.createElement('div');
        messageEl.className = `message ${message.role}`;

        const contentEl = document.createElement('div');
        contentEl.className = 'message-content';
        contentEl.textContent = message.content;

        messageEl.appendChild(contentEl);
        chatMessages.appendChild(messageEl);
    }

    showLoading() {
        const chatMessages = document.getElementById('chat-messages');
        const loadingEl = document.createElement('div');
        loadingEl.className = 'message ai';
        loadingEl.id = 'loading-message';
        
        const contentEl = document.createElement('div');
        contentEl.className = 'message-content loading';
        contentEl.innerHTML = '<span class="loading-dot"></span><span class="loading-dot"></span><span class="loading-dot"></span>';
        
        loadingEl.appendChild(contentEl);
        chatMessages.appendChild(loadingEl);
        this.scrollToBottom();
    }

    removeLoading() {
        const loadingEl = document.getElementById('loading-message');
        if (loadingEl) {
            loadingEl.remove();
        }
    }

    scrollToBottom() {
        const chatMessages = document.getElementById('chat-messages');
        setTimeout(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 0);
    }

    clearMessages() {
        this.messages = [];
        const chatMessages = document.getElementById('chat-messages');
        const welcomeSection = document.getElementById('welcome-section');
        chatMessages.innerHTML = '';
        welcomeSection.style.display = 'flex';
        chatMessages.style.display = 'none';
    }
}

const chatManager = new ChatManager();
