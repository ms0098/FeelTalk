/* Configuration & Constants */

const CONFIG = {
    API_URL: 'http://127.0.0.1:8000',
    MODES: {
        'angry roast': {
            color: '#E63946',
            emoji: '🔥',
            name: 'Angry Roast',
            description: 'Get roasted mercilessly'
        },
        'soft roast': {
            color: '#F77F88',
            emoji: '😏',
            name: 'Soft Roast',
            description: 'Gentle teasing vibes'
        },
        'general motivation': {
            color: '#06D6A0',
            emoji: '💪',
            name: 'Motivation',
            description: 'Get inspired and motivated'
        },
        'religious motivation': {
            color: '#F4A261',
            emoji: '🙏',
            name: 'Religious',
            description: 'Spiritual guidance and faith'
        },
        'seductive roast': {
            color: '#E76F51',
            emoji: '😘',
            name: 'Seductive',
            description: 'Flirty roasting vibes'
        },
        'seductive motivation': {
            color: '#F4A460',
            emoji: '✨',
            name: 'Charm',
            description: 'Charming encouragement'
        },
        'flirty': {
            color: '#FF6B9D',
            emoji: '💋',
            name: 'Flirty',
            description: 'Playful banter and fun'
        },
        'dumb friend': {
            color: '#FFD60A',
            emoji: '🤪',
            name: 'Dumb Friend',
            description: 'Silly and absurd humor'
        }
    },
    STORAGE_KEYS: {
        AUTH_TOKEN: 'feel_talk_auth_token',
        USERNAME: 'feel_talk_username',
        SELECTED_MODE: 'feel_talk_selected_mode'
    }
};
