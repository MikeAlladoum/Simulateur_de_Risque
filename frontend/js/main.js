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

        // Récupérer les simulations de l'API
        const data = await apiClient.getSimulations();
        const simulations = data.simulations || [];

        if (!simulations || simulations.length === 0) {
            historiqueListe.innerHTML = '<p style="text-align: center; padding: 20px; color: #999;">Aucune simulation sauvegardée pour le moment.</p>';
            return;
        }

        // Construire le HTML pour afficher les simulations
        let html = '<div style="padding: 20px;">';
        html += '<table style="width: 100%; border-collapse: collapse; background: white; border-radius: 8px;">';
        html += '<thead style="background: #f0f0f0; border-bottom: 2px solid #ddd;">';
        html += '<tr>';
        html += '<th style="padding: 12px; text-align: left; font-weight: bold;">Date</th>';
        html += '<th style="padding: 12px; text-align: left; font-weight: bold;">Nombre Simulations</th>';
        html += '<th style="padding: 12px; text-align: left; font-weight: bold;">Perte Moyenne</th>';
        html += '<th style="padding: 12px; text-align: center; font-weight: bold;">Actions</th>';
        html += '</tr>';
        html += '</thead>';
        html += '<tbody>';

        simulations.forEach((sim, idx) => {
            const stats = sim.statistics || {};
            const createdAt = new Date(sim.created_at).toLocaleDateString('fr-FR', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });

            html += '<tr style="border-bottom: 1px solid #eee; hover: { background: #f9f9f9; }">';
            html += `<td style="padding: 12px;">${createdAt}</td>`;
            html += `<td style="padding: 12px;">${sim.num_simulations.toLocaleString('fr-FR')}</td>`;
            html += `<td style="padding: 12px;">${(stats.mean || 0).toLocaleString('fr-FR', { maximumFractionDigits: 2 })} FCFA</td>`;
            html += `<td style="padding: 12px; text-align: center;">`;
            html += `<button onclick="loadSimulationById(${sim.id})" style="padding: 6px 12px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; margin-right: 6px;">📂 Charger</button>`;
            html += `<button onclick="deleteSimulationById(${sim.id})" style="padding: 6px 12px; background: #e74c3c; color: white; border: none; border-radius: 4px; cursor: pointer;">🗑️ Supprimer</button>`;
            html += `</td>`;
            html += '</tr>';
        });

        html += '</tbody>';
        html += '</table>';
        html += '</div>';

        historiqueListe.innerHTML = html;

    } catch (error) {
        log('[ERROR] Erreur lors du chargement de l\'historique:', error);
        document.getElementById('historiqueListe').innerHTML = '<p style="color: red; padding: 20px;">Erreur: ' + error.message + '</p>';
    }
}

/**
 * Charge une simulation par ID et l'affiche dans le simulateur
 */
async function loadSimulationById(simId) {
    try {
        log(`[HISTORY] Chargement de la simulation ${simId}`);
        
        const sim = await apiClient.getSimulation(simId);
        
        // Afficher les résultats
        document.getElementById('sectionSimulateur').style.display = 'block';
        document.getElementById('sectionHistorique').style.display = 'none';
        
        // Mettre à jour le menu
        document.querySelectorAll('.menu-item').forEach(m => m.classList.remove('active'));
        document.querySelector('[data-section="simulateur"]').classList.add('active');
        
        // Afficher les stats sauvegardées
        if (sim.statistics) {
            displayStats(sim.statistics);
        }
        
        log('[HISTORY] Simulation chargée avec succès');
        
    } catch (error) {
        log('[ERROR] Erreur lors du chargement:', error);
        alert('Erreur: ' + error.message);
    }
}

/**
 * Supprime une simulation
 */
async function deleteSimulationById(simId) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette simulation?')) {
        return;
    }
    
    try {
        log(`[HISTORY] Suppression de la simulation ${simId}`);
        
        await apiClient.deleteSimulation(simId);
        
        log('[HISTORY] Simulation supprimée');
        
        // Recharger la liste
        loadSimulationHistory();
        
    } catch (error) {
        log('[ERROR] Erreur lors de la suppression:', error);
        alert('Erreur: ' + error.message);
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

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { initApp, setupEventListeners, handleFormSubmit };
}
