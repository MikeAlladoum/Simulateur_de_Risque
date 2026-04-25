/**
 * API Client - Communication avec le backend
 * 
 * Gère les requêtes HTTP vers l'API
 */

/**
 * Client API
 */
class APIClient {
    constructor(baseURL = CONFIG.API.BASE_URL) {
        this.baseURL = baseURL;
        this.timeout = CONFIG.API.TIMEOUT;
    }

    /**
     * Effectue une requête HTTP
     * @param {string} endpoint - Endpoint API
     * @param {object} options - Options fetch
     * @returns {Promise} Réponse JSON
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);

        try {
            const response = await fetch(url, {
                ...options,
                signal: controller.signal,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Erreur HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            clearTimeout(timeoutId);
            throw error;
        }
    }

    /**
     * Effectue une simulation
     * @param {object} params - Paramètres {lambda, mu, num_simulations}
     * @returns {Promise} Résultats
     */
    async simulate(params) {
        return this.request(CONFIG.API.ENDPOINTS.SIMULATE, {
            method: 'POST',
            body: JSON.stringify(params)
        });
    }

    /**
     * Vérifie la santé du serveur
     * @returns {Promise} Réponse health check
     */
    async healthCheck() {
        return this.request(CONFIG.API.ENDPOINTS.HEALTH, {
            method: 'GET'
        });
    }

    /**
     * Récupère les informations de l'API
     * @returns {Promise} Infos API
     */
    async getInfo() {
        return this.request(CONFIG.API.ENDPOINTS.INFO, {
            method: 'GET'
        });
    }
}

// Instance globale
const apiClient = new APIClient();

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { APIClient };
}
