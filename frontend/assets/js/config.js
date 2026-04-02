/* Configuration & Constants */

const CONFIG = {
    API_URL: 'http://127.0.0.1:8000',
    MODES: {
        'angry roast': {
            color: '#E63946',
            emoji: '🤬',
            name: 'Angry Roast',
            shortDesc: 'Get roasted mercilessly',
            fullDesc: 'Receive brutal, toxic, and savage roasts with maximum profanity and harsh disrespect. This mode will destroy you verbally with extreme aggression and make you feel harshly tortured.'
        },
        'soft roast': {
            color: '#F77F88',
            emoji: '😏',
            name: 'Soft Roast',
            shortDesc: 'Gentle teasing vibes',
            fullDesc: 'Get gently mocked with clever wit and sarcasm. Light-hearted roasts that make you smile without being mean-spirited. Perfect for playful teasing.'
        },
        'general motivation': {
            color: '#06D6A0',
            emoji: '💪',
            name: 'Motivation',
            shortDesc: 'Get inspired and motivated',
            fullDesc: 'Receive genuine, encouraging messages that inspire action and positive change. Get powerful motivation to believe in yourself and achieve your goals.'
        },
        'religious motivation': {
            color: '#F4A261',
            emoji: '🙏',
            name: 'Religious',
            shortDesc: 'Spiritual guidance and faith',
            fullDesc: 'Receive faith-based inspiration and spiritual guidance rooted in wisdom and divine principles. Find inner peace through spiritually grounded encouragement.'
        },
        'seductive roast': {
            color: '#E76F51',
            emoji: '😘',
            name: 'Seductive',
            shortDesc: 'Flirty roasting vibes',
            fullDesc: 'Get roasted with charm and flirtation mixed with witty mockery. Playfully suggestive jabs that are fun and engaging without crossing boundaries.'
        },
        'seductive motivation': {
            color: '#F4A460',
            emoji: '✨',
            name: 'Charm',
            shortDesc: 'Charming encouragement',
            fullDesc: 'Receive charming and flirty motivation that uplifts you with genuine support. Mix of flattery and powerful belief in your abilities.'
        },
        'flirty': {
            color: '#FF6B9D',
            emoji: '💋',
            name: 'Flirty',
            shortDesc: 'Playful banter and fun',
            fullDesc: 'Enjoy playful and charming banter with witty compliments and teasing. Light, fun engagement that keeps things entertaining and engaging.'
        },
        'dumb friend': {
            color: '#FFD60A',
            emoji: '🤪',
            name: 'Dumb Friend',
            shortDesc: 'Silly and absurd humor',
            fullDesc: 'Get hilariously silly responses with absurd logic and ridiculous humor. Goofy best friend energy that makes you laugh with dumb jokes.'
        }
    },
    STORAGE_KEYS: {
        AUTH_TOKEN: 'feel_talk_auth_token',
        USERNAME: 'feel_talk_username',
        SELECTED_MODE: 'feel_talk_selected_mode'
    }
};
