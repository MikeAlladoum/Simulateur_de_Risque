/**
 * Configuration Frontend
 * 
 * Variables globales pour le frontend
 */

// Configuration de l'API
const CONFIG = {
    // API Backend
    API: {
        BASE_URL: 'http://localhost:5000/api',
        ENDPOINTS: {
            HEALTH: '/health',
            SIMULATE: '/simulate',
            INFO: '/info'
        },
        TIMEOUT: 30000  // 30 secondes
    },

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
