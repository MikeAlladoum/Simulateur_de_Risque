/**
 * Main - Point d'entrée de l'application
 * 
 * Initialisation et gestion des événements
 */

// Cacher le loader au chargement complet
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const loader = document.getElementById('loadingIndicator');
        if (loader) {
            loader.classList.add('hidden');
        }
    }, 300);
});

window.addEventListener('load', () => {
    const loader = document.getElementById('loadingIndicator');
    if (loader) {
        loader.classList.add('hidden');
    }
});

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

    // Ajouter les listeners pour le menu
    setupMenuListeners();
}

/**
 * Configure les listeners du menu de navigation
 */
function setupMenuListeners() {
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const section = item.getAttribute('data-section');
            switchSection(section);
        });
    });
}

/**
 * Bascule vers une section
 */
function switchSection(sectionName) {
    log(`[MENU] Passage à la section: ${sectionName}`);

    // Masquer toutes les sections
    document.getElementById('sectionSimulateur').style.display = 'none';
    
    const historique = document.getElementById('sectionHistorique');
    const parametres = document.getElementById('sectionParametres');
    if (historique) historique.style.display = 'none';
    if (parametres) parametres.style.display = 'none';

    // Afficher la section sélectionnée
    if (sectionName === 'simulateur') {
        document.getElementById('sectionSimulateur').style.display = 'block';
    } else if (sectionName === 'historique') {
        if (historique) {
            historique.style.display = 'block';
            loadSimulationHistory();
        }
    } else if (sectionName === 'parametres') {
        if (parametres) {
            parametres.style.display = 'block';
        }
    }

    // Mettre à jour l'état actif du menu
    document.querySelectorAll('.menu-item').forEach(m => {
        m.classList.remove('active');
    });
    document.querySelector(`[data-section="${sectionName}"]`).classList.add('active');
}

/**
 * Charge l'historique des simulations
 */
async function loadSimulationHistory() {
    try {
        log('[HISTORY] Chargement de l\'historique');
        
        const historiqueListe = document.getElementById('historiqueListe');
        historiqueListe.innerHTML = '<p style="text-align: center; padding: 20px;">Chargement...</p>';

        // TODO: Appeler l'API pour récupérer les simulations
        // const simulations = await apiClient.getSimulations();

        // Placeholder
        historiqueListe.innerHTML = '<p style="text-align: center; padding: 20px;">Aucune simulation sauvegardée pour le moment.</p>';

    } catch (error) {
        log('[ERROR] Erreur lors du chargement de l\'historique:', error);
        document.getElementById('historiqueListe').innerHTML = '<p style="color: red;">Erreur lors du chargement</p>';
    }
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

// Exposer les fonctions à window pour les rendre globales
if (typeof window !== 'undefined') {
    window.switchSection = switchSection;
    window.setupMenuListeners = setupMenuListeners;
    window.loadSimulationHistory = loadSimulationHistory;
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { initApp, setupEventListeners, handleFormSubmit, switchSection, setupMenuListeners };
}
