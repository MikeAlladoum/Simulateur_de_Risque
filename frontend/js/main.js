/**
 * Main - Point d'entrée de l'application
 * 
 * Initialisation et gestion des événements
 */

/**
 * Initialise l'application
 */
async function initApp() {
    log('[INIT] Initialisation de l\'application');

    // Vérifier la santé du serveur
    checkServerHealth();

    // Ajouter les event listeners
    setupEventListeners();

    log('[INIT] Application initialisée');
}

/**
 * Vérifie la santé du serveur
 */
async function checkServerHealth() {
    try {
        await apiClient.healthCheck();
        updateServerStatus(true);
    } catch (error) {
        log('[ERROR] Serveur non accessible:', error);
        updateServerStatus(false);
    }
}

/**
 * Configure les event listeners
 */
function setupEventListeners() {
    const form = document.getElementById('simulationForm');
    const resetBtn = document.getElementById('resetBtn');

    // Soumettre le formulaire
    form.addEventListener('submit', handleFormSubmit);

    // Réinitialiser
    resetBtn.addEventListener('click', (e) => {
        e.preventDefault();
        resetUI();
    });
}

/**
 * Gère la soumission du formulaire
 */
async function handleFormSubmit(e) {
    e.preventDefault();

    log('[SUBMIT] Soumission du formulaire');

    // Masquer les erreurs précédentes
    hideError();
    hideResults();

    // Valider
    const validation = validateForm();
    if (!validation.valid) {
        displayValidationErrors(validation.errors);
        return;
    }

    // Afficher le chargement
    showLoading(true);

    try {
        // Récupérer les paramètres
        const params = {
            lambda: parseFloat(document.getElementById('lambda').value),
            mu: parseFloat(document.getElementById('mu').value),
            num_simulations: parseInt(document.getElementById('numSimulations').value)
        };

        log('[API] Appel de la simulation avec:', params);

        // Appeler l'API
        const result = await apiClient.simulate(params);

        if (!result.success) {
            throw new Error(result.error || 'Erreur lors de la simulation');
        }

        log('[SUCCESS] Simulation réussie');

        // Afficher les résultats
        displayResults(result);

    } catch (error) {
        log('[ERROR] Erreur:', error.message);
        showError(`❌ ${error.message}`);

    } finally {
        showLoading(false);
    }
}

/**
 * Point d'entrée quand le DOM est chargé
 */
document.addEventListener('DOMContentLoaded', initApp);

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { initApp, setupEventListeners, handleFormSubmit };
}
