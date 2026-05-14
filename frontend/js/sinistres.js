/**
 * Module de Gestion des Sinistres
 * Gère les différents types de risques et leurs configurations
 */

const SINISTRES_MODULE = {
    // État actuel des sinistres
    sinistres: {},
    mode: 'default', // 'default' ou 'custom'
    
    /**
     * Initialise les sinistres par défaut
     */
    async init() {
        try {
            const response = await fetch(`${CONFIG.API.BASE_URL.replace('/api', '')}/api/sinistres/default`);
            const data = await response.json();
            
            if (data.success) {
                this.sinistres = data.sinistres;
                console.log('Sinistres charges:', Object.keys(this.sinistres).length);
                return true;
            }
        } catch (error) {
            console.error('Erreur chargement sinistres:', error);
        }
        
        // Fallback
        this.sinistres = {
            "consultation": {"lambda": 2.0, "cout_moyen": 5000, "nom_complet": "Consultation médicale"},
            "hospitalisation": {"lambda": 0.3, "cout_moyen": 250000, "nom_complet": "Hospitalisation"},
            "chirurgie": {"lambda": 0.1, "cout_moyen": 1000000, "nom_complet": "Chirurgie"},
            "medicaments": {"lambda": 1.5, "cout_moyen": 30000, "nom_complet": "Médicaments"}
        };
        return false;
    },
    
    /**
     * Obtient la configuration actuelle des sinistres
     */
    getConfig() {
        return this.sinistres;
    },
    
    /**
     * Obtient les sinistres au format formulaire
     */
    getFormConfig() {
        const config = {};
        
        for (const [key, value] of Object.entries(this.sinistres)) {
            const lambdaInput = document.getElementById(`lambda_${key}`);
            const coutInput = document.getElementById(`cout_${key}`);
            
            if (lambdaInput && coutInput) {
                config[key] = {
                    lambda: parseFloat(lambdaInput.value),
                    cout_moyen: parseFloat(coutInput.value),
                    nom_complet: value.nom_complet || key
                };
            }
        }
        
        return config;
    },
    
    /**
     * Crée les champs de formulaire pour les sinistres
     */
    createFormFields(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        container.innerHTML = '';
        
        for (const [key, config] of Object.entries(this.sinistres)) {
            const sinisterCard = document.createElement('div');
            sinisterCard.className = 'sinister-card';
            sinisterCard.innerHTML = `
                <div class="sinister-header">
                    <h4 class="sinister-title">${config.nom_complet}</h4>
                    <p class="sinister-description">${config.nom_complet}</p>
                </div>
                
                <div class="sinister-form-group">
                    <div class="form-column">
                        <label class="form-label">
                            <span>Frequence (λ)</span>
                            <span class="label-hint">Nombre moyen par periode</span>
                        </label>
                        <input 
                            type="number" 
                            id="lambda_${key}"
                            class="form-input"
                            step="0.1" 
                            min="0.01"
                            max="1000"
                            value="${config.lambda}"
                            required
                        >
                    </div>
                    
                    <div class="form-column">
                        <label class="form-label">
                            <span>Cout moyen (FCFA)</span>
                            <span class="label-hint">Cout par sinistre</span>
                        </label>
                        <input 
                            type="number" 
                            id="cout_${key}"
                            class="form-input"
                            step="1000" 
                            min="0.01"
                            max="1000000"
                            value="${config.cout_moyen}"
                            required
                        >
                    </div>
                </div>
            `;
            
            container.appendChild(sinisterCard);
        }
    }
};

// Export
window.SINISTRES_MODULE = SINISTRES_MODULE;
