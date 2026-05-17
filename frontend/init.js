/**
 * Initialisation rapide - doit être le PREMIER script
 * Pas de dépendances circulaires
 */

// Détection simple de l'environnement
const _hostname = window.location.hostname;
const _isDev = (_hostname === 'localhost' || _hostname === '127.0.0.1');

// URL du backend Railway
const _RAILWAY_BACKEND_URL = 'https://simulateur-backend-production-6239.up.railway.app';

// Variables globales SANS dépendances
window.DEBUG = false;
window.CONFIG = {
    ENVIRONMENT: _isDev ? 'development' : 'production',
    API: {
        BASE_URL: _isDev ? 'http://localhost:5000/api' : (_RAILWAY_BACKEND_URL + '/api'),
        ENDPOINTS: {
            HEALTH: '/health',
            SIMULATE: '/simulate',
            INFO: '/info',
            SINISTRES_DEFAULT: '/sinistres/default',
            AUTH_LOGIN: '/auth/login',
            PROFILES: '/profiles',
            SIMULATIONS: '/simulations'
        },
        TIMEOUT: 30000
    },
    DEFAULTS: {
        LAMBDA: 5,
        MU: 1000,
        NUM_SIMULATIONS: 10000
    },
    CONSTRAINTS: {
        LAMBDA: { min: 0.01, max: 1000 },
        MU: { min: 0.01, max: 1000000 },
        NUM_SIMULATIONS: { min: 100, max: 1000000 }
    },
    CURRENCY: {
        CODE: 'FCFA',
        SYMBOL: 'FCFA',
        LOCALE: 'fr-FR'
    },
    CHART_COLORS: {
        PRIMARY: '#3498db',
        SUCCESS: '#27ae60',
        WARNING: '#f39c12',
        DANGER: '#e74c3c',
        LIGHT: '#ecf0f1',
        DARK: '#2c3e50'
    },
    ANIMATION: {
        DURATION: 300
    }
};

// Logger
window.log = function(...args) {
    if (window.DEBUG) {
        console.log('[SimRisque]', ...args);
    }
};
