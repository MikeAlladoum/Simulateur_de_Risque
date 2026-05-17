/**
 * Gestion de la modale de sauvegarde de simulation
 * Functions for saving simulations modal
 */

/**
 * Ouvre la modale de sauvegarde
 */
function openModalSave() {
    const modal = document.getElementById('saveModal');
    if (modal) {
        modal.classList.add('show');
        modal.style.display = 'flex';
        document.getElementById('simName').focus();
    }
}

/**
 * Ferme la modale de sauvegarde
 */
function closeModalSave() {
    const modal = document.getElementById('saveModal');
    if (modal) {
        modal.classList.remove('show');
        modal.style.display = 'none';
        // Réinitialiser le formulaire
        document.getElementById('saveForm').reset();
    }
}

/**
 * Soumet le formulaire de sauvegarde
 */
async function submitSaveForm(event) {
    event.preventDefault();
    
    const simName = document.getElementById('simName').value.trim();
    const simDescription = document.getElementById('simDescription').value.trim();
    
    if (!simName) {
        alert('Le nom de la simulation est requis');
        return;
    }
    
    try {
        // Récupérer les données de la simulation actuelle
        const sinistresConfig = SINISTRES_MODULE.getFormConfig();
        const numSimulations = parseInt(document.getElementById('numSimulations').value);
        const stats = appState.results;
        
        // Préparer les données à envoyer
        const saveData = {
            name: simName,
            description: simDescription,
            num_simulations: numSimulations,
            sinistres_config: sinistresConfig,
            statistics: stats
        };
        
        console.log('Saving simulation:', saveData);
        
        // Appeler l'API
        const response = await apiClient.saveSimulation(saveData);
        
        console.log('Save response:', response);
        
        if (response.success) {
            alert(`✅ Simulation enregistrée avec succès (ID: ${response.simulation_id})`);
            closeModalSave();
        } else {
            alert('❌ Erreur lors de la sauvegarde: ' + response.error);
        }
        
    } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error);
        alert('❌ Erreur: ' + error.message);
    }
}

// Fermer la modale au clic sur le fond
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('saveModal');
    if (modal) {
        const overlay = modal.querySelector('.modal-overlay');
        if (overlay) {
            overlay.addEventListener('click', closeModalSave);
        }
        
        // Fermer aussi avec Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('show')) {
                closeModalSave();
            }
        });
    }
});
