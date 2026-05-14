/**
 * Configuration Frontend
 * 
 * Variables globales pour le frontend
 */

// Configuration de l'API
const CONFIG = {
    // Détection environnement
    ENVIRONMENT: (() => {
        const hostname = window.location.hostname;
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'development';
        }
        return 'production';
    })(),

    // API Backend
    API: (() => {
        const env = CONFIG.ENVIRONMENT;
        const isDev = env === 'development';
        
        return {
            BASE_URL: isDev 
                ? 'http://localhost:5000/api'
                : (window.location.origin + '/api'), // Sur Vercel, utiliser proxy
            ENDPOINTS: {
                HEALTH: '/health',
                SIMULATE: '/simulate',
                INFO: '/info',
                SINISTRES_DEFAULT: '/sinistres/default',
                AUTH_LOGIN: '/auth/login'
            },
            TIMEOUT: 30000  // 30 secondes
        };
    })(),

    // Valeurs par défaut
    DEFAULTS: {
        LAMBDA: 5,
        MU: 1000,
        NUM_SIMULATIONS: 10000
    },

    // Limites
    CONSTRAINTS: {
        LAMBDA: { min: 0.01, max: 1000 },
        MU: { min: 0.01, max: 1000000 },
        NUM_SIMULATIONS: { min: 100, max: 1000000 }
    },

    // Devise
    CURRENCY: {
        CODE: 'FCFA',
        SYMBOL: 'FCFA',
        LOCALE: 'fr-FR'
    },

    // UI
    CHART_COLORS: {
        PRIMARY: '#3498db',
        SUCCESS: '#27ae60',
        WARNING: '#f39c12',
        DANGER: '#e74c3c',
        LIGHT: '#ecf0f1',
        DARK: '#2c3e50'
    },

    ANIMATION: {
        DURATION: 300  // ms
    }
};

// Debug mode
const DEBUG = false;

function log(...args) {
    if (DEBUG) {
        console.log('[DEBUG]', ...args);
    }
}
