/* Authentication Module */

class AuthManager {
    constructor() {
        this.token = localStorage.getItem(CONFIG.STORAGE_KEYS.AUTH_TOKEN);
        this.username = localStorage.getItem(CONFIG.STORAGE_KEYS.USERNAME);
    }

    async signup(userData) {
        try {
            const response = await fetch(`${CONFIG.API_URL}/auth/signup`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Signup failed');
            }

            const data = await response.json();
            this.setAuth(data.token, data.username);
            return data;
        } catch (error) {
            console.error('Signup error:', error);
            throw error;
        }
    }

    setAuth(token, username) {
        this.token = token;
        this.username = username;
        localStorage.setItem(CONFIG.STORAGE_KEYS.AUTH_TOKEN, token);
        localStorage.setItem(CONFIG.STORAGE_KEYS.USERNAME, username);
    }

    getAuth() {
        return {
            token: this.token,
            username: this.username,
            isAuthenticated: !!this.token
        };
    }

    logout() {
        this.token = null;
        this.username = null;
        localStorage.removeItem(CONFIG.STORAGE_KEYS.AUTH_TOKEN);
        localStorage.removeItem(CONFIG.STORAGE_KEYS.USERNAME);
    }

    getHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (this.token) {
            headers['X-Auth-Token'] = this.token;
        }
        return headers;
    }
}

const authManager = new AuthManager();

function showSignupModal() {
    const modal = document.getElementById('auth-modal');
    const modalBody = document.getElementById('modal-body');

    const regions = [
        'Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata',
        'Hyderabad', 'Pune', 'Gurgaon', 'Noida', 'Indore',
        'Jaipur', 'Lucknow', 'Ahmedabad', 'Surat', 'Chandigarh',
        'Amritsar', 'Goa', 'Kochi', 'USA', 'UK', 'Australia'
    ];

    modalBody.innerHTML = `
        <h2>Create Account</h2>
        <form id="signup-form">
            <div class="form-group">
                <label>Username (3-50 characters)</label>
                <input type="text" id="signup-username" required placeholder="Enter username" minlength="3" maxlength="50">
            </div>
            <div class="form-group">
                <label>Gender</label>
                <select id="signup-gender" required>
                    <option value="">Select gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                </select>
            </div>
            <div class="form-group">
                <label>Profession (2-100 characters)</label>
                <input type="text" id="signup-profession" required placeholder="Your profession" minlength="2" maxlength="100">
            </div>
            <div class="form-group">
                <label>About Yourself (minimum 10 characters)</label>
                <input type="text" id="signup-description" required placeholder="Tell us about yourself (at least 10 chars)" minlength="10" maxlength="500">
            </div>
            <div class="form-group">
                <label>Region</label>
                <select id="signup-region">
                    ${regions.map(region => `<option value="${region}">${region}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <button type="submit">Create Account</button>
            </div>
        </form>
    `;

    const form = modalBody.querySelector('#signup-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('signup-username').value.trim();
        const gender = document.getElementById('signup-gender').value.trim();
        const profession = document.getElementById('signup-profession').value.trim();
        const description = document.getElementById('signup-description').value.trim();
        const region = document.getElementById('signup-region').value || 'Delhi';

        // Validation
        if (!username || username.length < 3) {
            showNotification('Username must be at least 3 characters', 'error');
            return;
        }
        if (!gender) {
            showNotification('Please select a gender', 'error');
            return;
        }
        if (!profession || profession.length < 2) {
            showNotification('Profession must be at least 2 characters', 'error');
            return;
        }
        if (!description || description.length < 10) {
            showNotification('Description must be at least 10 characters', 'error');
            return;
        }

        const userData = {
            username,
            gender,
            profession,
            description,
            region
        };

        try {
            await authManager.signup(userData);
            modal.style.display = 'none';
            updateAuthUI();
            showNotification('Account created successfully!');
        } catch (error) {
            showNotification('Signup failed: ' + error.message, 'error');
        }
    });

    modal.style.display = 'flex';
}

function updateAuthUI() {
    const auth = authManager.getAuth();
    const loginBtn = document.getElementById('login-btn');
    const userInfo = document.getElementById('user-info');
    const usernameDisplay = document.getElementById('username-display');

    if (auth.isAuthenticated) {
        loginBtn.style.display = 'none';
        userInfo.style.display = 'flex';
        usernameDisplay.textContent = `Welcome, ${auth.username}!`;
    } else {
        loginBtn.style.display = 'block';
        userInfo.style.display = 'none';
    }
}

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        background-color: ${type === 'error' ? '#E63946' : '#06D6A0'};
        color: white;
        border-radius: 8px;
        z-index: 2000;
        animation: slideIn 0.3s ease;
        font-size: 14px;
        font-weight: 500;
    `;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}
