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

            // Vérifier le statut HTTP
            if (!response.ok) {
                try {
                    const errorData = await response.json();
                    throw new Error(errorData.error || `Erreur HTTP ${response.status}`);
                } catch (parseError) {
                    throw new Error(`Erreur HTTP ${response.status}`);
                }
            }

            // Récupérer le texte de la réponse
            const text = await response.text();
            
            // Si la réponse est vide, retourner un objet vide
            if (!text) {
                return {};
            }
            
            // Parser le JSON
            try {
                return JSON.parse(text);
            } catch (parseError) {
                log('ERROR', 'Invalid JSON response:', text);
                throw new Error('Réponse serveur invalide');
            }
        } catch (error) {
            clearTimeout(timeoutId);
            log('ERROR', 'API request error:', error.message);
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

    /**
     * Récupère toutes les simulations de l'utilisateur
     * @returns {Promise} Liste des simulations
     */
    async getSimulations() {
        return this.request(CONFIG.API.ENDPOINTS.SIMULATIONS, {
            method: 'GET'
        });
    }

    /**
     * Récupère une simulation spécifique
     * @param {number} simId - ID de la simulation
     * @returns {Promise} Données de la simulation
     */
    async getSimulation(simId) {
        return this.request(`${CONFIG.API.ENDPOINTS.SIMULATIONS}/${simId}`, {
            method: 'GET'
        });
    }

    /**
     * Sauvegarde une simulation
     * @param {object} data - Données de la simulation
     * @returns {Promise} Simulation sauvegardée
     */
    async saveSimulation(data) {
        return this.request('/simulations/save', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    /**
     * Supprime une simulation
     * @param {number} simId - ID de la simulation
     * @returns {Promise} Réponse suppression
     */
    async deleteSimulation(simId) {
        return this.request(`${CONFIG.API.ENDPOINTS.SIMULATIONS}/${simId}`, {
            method: 'DELETE'
        });
    }
}

// Instance globale
const apiClient = new APIClient();

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { APIClient };
}
