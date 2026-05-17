/**
 * APPLICATION PRINCIPALE - Simulateur de Risques Financiers
 * Gestion du formulaire, API et interface utilisateur
 */

// Configuration (depuis config.js)
const API_BASE_URL = CONFIG.API.BASE_URL;
const CURRENCY = CONFIG.CURRENCY.CODE;

// États de l'application
let appState = {
    isLoading: false,
    results: null,
    chart: null
};

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', async () => {
    // Vérifier l'authentification
    if (!AUTH.requireAuth()) {
        return;
    }
    
    // Afficher l'utilisateur connecté
    const currentUser = AUTH.getCurrentUser();
    const userSection = document.getElementById('userSection');
    const currentUserSpan = document.getElementById('currentUser');
    const logoutBtn = document.getElementById('logoutBtn');
    
    if (userSection && currentUserSpan) {
        userSection.style.display = 'flex';
        userSection.style.alignItems = 'center';
        currentUserSpan.textContent = currentUser;
    }
    
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            if (confirm('Êtes-vous sûr de vouloir vous déconnecter?')) {
                AUTH.logout();
            }
        });
    }
    
    initializeApp();
});

function initializeApp() {
    console.log('Initialisation de l\'application...');
    
    // Verifier la connexion au serveur
    checkServerHealth();
    
    // Initialiser les profils
    PROFILES_MODULE.init();
    PROFILES_MODULE.createProfileSelector('profileContainer');
    
    // Initialiser les sinistres
    SINISTRES_MODULE.init().then(() => {
        SINISTRES_MODULE.createFormFields('sinistreContainer');
    });
    
    // Event listeners
    setupFormListeners();
    setupEventListeners();
}

// ==================== SERVER HEALTH CHECK ====================
async function checkServerHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        const statusElement = document.getElementById('serverStatus');
        if (response.ok) {
            statusElement.innerHTML = `
                <span class="status-dot online"></span>
                <span class="status-text">Serveur actif</span>
            `;
            console.log('Serveur connecte');
        } else {
            throw new Error('Serveur non disponible');
        }
    } catch (error) {
        console.error('❌ Erreur de connexion:', error);
        const statusElement = document.getElementById('serverStatus');
        statusElement.innerHTML = `
            <span class="status-dot"></span>
            <span class="status-text">Serveur indisponible</span>
        `;
    }
}

// ==================== FORM SETUP ====================
function setupFormListeners() {
    const form = document.getElementById('simulationForm');
    const submitBtn = document.getElementById('submitBtn');
    
    console.log('Form found:', form ? 'YES' : 'NO');
    console.log('Button found:', submitBtn ? 'YES' : 'NO');
    
    if (!form) {
        console.error('❌ CRITICAL: Form #simulationForm not found!');
        return;
    }
    
    // Listener on form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Form submitted via form listener!');
        await handleFormSubmit();
    });
    
    // CRITICAL: Also listen to button click directly (fallback)
    if (submitBtn) {
        submitBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            console.log('Form submitted via button click!');
            await handleFormSubmit();
        });
    }
    
    // Validation en temps réel
    const inputs = form.querySelectorAll('.form-input');
    inputs.forEach(input => {
        input.addEventListener('change', validateField);
        input.addEventListener('input', validateField);
    });
    
    console.log('Form listeners setup complete');
}

function validateField(e) {
    const input = e.target;
    const value = parseFloat(input.value);
    
    if (isNaN(value) || value <= 0) {
        input.style.borderColor = '#EF4444';
    } else {
        input.style.borderColor = '#E5E7EB';
    }
}

// ==================== FORM SUBMIT ====================
async function handleFormSubmit() {
    console.log('handleFormSubmit called');
    
    const numSimulations = parseInt(document.getElementById('numSimulations').value);
    
    // Obtenir la configuration des sinistres
    const sinistresConfig = SINISTRES_MODULE.getFormConfig();
    
    console.log('Sinistres config:', sinistresConfig);
    console.log('Num simulations:', numSimulations);
    
    // Validation du nombre de simulations
    if (!numSimulations || numSimulations < 100 || numSimulations > 1000000) {
        showError('Le nombre de simulations doit être entre 100 et 1000000');
        return;
    }
    
    // Validation des sinistres
    let hasError = false;
    for (const [key, config] of Object.entries(sinistresConfig)) {
        if (!config.lambda || config.lambda <= 0 || config.lambda > 1000) {
            showError(`${key}: Lambda doit être entre 0.01 et 1000`);
            hasError = true;
            break;
        }
        if (!config.cout_moyen || config.cout_moyen <= 0 || config.cout_moyen > 1000000) {
            showError(`${key}: Coût moyen doit être entre 0.01 et 1000000`);
            hasError = true;
            break;
        }
    }
    
    if (hasError) {
        console.log('Validation failed');
        return;
    }
    
    console.log('Validation passed');
    
    // Afficher le loader
    showLoading(true);
    
    try {
        // Appel API
        console.log('Calling API with multiple sinistres...');
        const token = AUTH.getToken();
        const response = await fetch(`${API_BASE_URL}/simulate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                num_simulations: numSimulations,
                sinistres: sinistresConfig
            })
        });
        
        console.log('API Response:', response.status, response.ok);
        
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        
        const response_data = await response.json();
        console.log('Response data:', response_data);
        
        // Transformer la réponse de l'API au format attendu
        const data = {
            mean: response_data.statistics?.mean,
            median: response_data.statistics?.median,
            min: response_data.statistics?.min,
            max: response_data.statistics?.max,
            std: response_data.statistics?.std,
            histogram_data: response_data.histogram,
            statistics_by_type: response_data.statistics_by_type || {}
        };
        
        console.log('Transformed data:', data);
        
        // Sauvegarder les résultats
        appState.results = data;
        
        // Afficher les résultats
        console.log('Calling displayResults...');
        displayResults(data);
        
        console.log('Simulation reussie');
        
    } catch (error) {
        console.error('❌ Erreur:', error);
        showError(`Erreur lors de la simulation: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// ==================== VALIDATION ====================
function validate(lambda, mu, numSimulations) {
    const constraints = CONFIG.CONSTRAINTS;
    
    if (isNaN(lambda) || lambda < constraints.LAMBDA.min || lambda > constraints.LAMBDA.max) {
        showError(`λ doit être entre ${constraints.LAMBDA.min} et ${constraints.LAMBDA.max}`);
        return false;
    }
    
    if (isNaN(mu) || mu < constraints.MU.min || mu > constraints.MU.max) {
        showError(`μ doit être entre ${constraints.MU.min} et ${constraints.MU.max}`);
        return false;
    }
    
    if (isNaN(numSimulations) || numSimulations < constraints.NUM_SIMULATIONS.min || numSimulations > constraints.NUM_SIMULATIONS.max) {
        showError(`Nombre de simulations doit être entre ${constraints.NUM_SIMULATIONS.min} et ${constraints.NUM_SIMULATIONS.max}`);
        return false;
    }
    
    return true;
}

// ==================== AFFICHAGE DES RÉSULTATS ====================
function displayResults(data) {
    console.log('displayResults called with:', data);
    
    // Stocker les données pour les utiliser dans displayHistogram
    window.lastSimulationData = data;
    
    // Afficher les statistiques
    displayStats(data);
    
    // Afficher les statistiques par sinistre si disponibles
    if (data.statistics_by_type && Object.keys(data.statistics_by_type).length > 0) {
        displayStatisticsBySinistre(data.statistics_by_type);
    }
    
    // Afficher le graphique
    if (data.histogram || data.histogram_data) {
        console.log('Displaying histogram...');
        const histData = data.histogram || data.histogram_data;
        displayHistogram(histData);
    } else {
        console.warn('⚠️ No histogram data');
    }
    
    // AFFICHER LES BOUTONS D'ACTIONS
    const actionsSection = document.getElementById('actionsSection');
    if (actionsSection) {
        actionsSection.style.display = 'block';
    }
    
    // Attacher les event listeners aux boutons d'actions
    const saveBtn = document.getElementById('saveSimulationBtn');
    if (saveBtn) {
        saveBtn.removeEventListener('click', openModalSave);
        saveBtn.addEventListener('click', openModalSave);
    }
}

function displayStatisticsBySinistre(statsByType) {
    console.log('Affichage des statistiques par sinistre...');
    
    // Créer ou récupérer le conteneur
    let container = document.getElementById('sinisterStatsContainer');
    if (!container) {
        const resultsSection = document.querySelector('.results-section');
        if (resultsSection) {
            container = document.createElement('div');
            container.id = 'sinisterStatsContainer';
            container.className = 'sinister-stats-section';
            resultsSection.insertBefore(container, resultsSection.querySelector('[id="chartSection"]'));
        } else {
            return;
        }
    }
    
    // Créer le tableau des sinistres
    let html = `
        <div class="sinister-stats-container">
            <h3 class="section-title">📊 Analyse par Type de Sinistre</h3>
            <div class="sinister-table-wrapper">
                <table class="sinister-table">
                    <thead>
                        <tr>
                            <th>Type de Sinistre</th>
                            <th>Fréquence (λ)</th>
                            <th>Coût Moyen</th>
                            <th>Perte Moyenne</th>
                            <th>Contribution (%)</th>
                            <th>Min - Max</th>
                        </tr>
                    </thead>
                    <tbody>
    `;
    
    for (const [key, stats] of Object.entries(statsByType)) {
        const contribution = (stats.contribution_pct || 0).toFixed(1);
        const moyenneStr = formatCurrency(stats.moyenne);
        const coutMoyenStr = formatCurrency(stats.cout_moyen);
        const minStr = formatCurrency(stats.min);
        const maxStr = formatCurrency(stats.max);
        
        html += `
            <tr>
                <td><strong>${stats.nom_complet}</strong></td>
                <td>${stats.lambda.toFixed(2)}</td>
                <td>${coutMoyenStr}</td>
                <td><span class="highlight">${moyenneStr}</span></td>
                <td><span class="contribution-badge">${contribution}%</span></td>
                <td>${minStr} → ${maxStr}</td>
            </tr>
        `;
    }
    
    html += `
                    </tbody>
                </table>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}

function displayStats(data) {
    console.log('📊 displayStats called');
    
    const statsContainer = document.getElementById('statsContainer');
    const emptyState = document.getElementById('emptyState');
    
    console.log('DOM Elements:', {
        statsContainer: statsContainer ? 'FOUND' : 'NOT FOUND',
        emptyState: emptyState ? 'FOUND' : 'NOT FOUND',
        statMean: document.getElementById('statMean') ? 'FOUND' : 'NOT FOUND',
        statMedian: document.getElementById('statMedian') ? 'FOUND' : 'NOT FOUND'
    });
    
    // Mettre à jour les valeurs
    const meanElem = document.getElementById('statMean');
    const medianElem = document.getElementById('statMedian');
    const minElem = document.getElementById('statMin');
    const maxElem = document.getElementById('statMax');
    
    if (meanElem) {
        meanElem.textContent = formatCurrency(data.mean);
        console.log('✅ Mean updated:', formatCurrency(data.mean));
    } else {
        console.error('❌ statMean element not found');
    }
    
    if (medianElem) medianElem.textContent = formatCurrency(data.median);
    if (minElem) minElem.textContent = formatCurrency(data.min);
    if (maxElem) maxElem.textContent = formatCurrency(data.max);
    
    // Afficher les stats et masquer l'empty state
    if (statsContainer) {
        statsContainer.style.display = 'grid';
        console.log('✅ Stats container displayed');
    } else {
        console.error('❌ statsContainer not found');
    }
    
    if (emptyState) {
        emptyState.style.display = 'none';
        console.log('✅ Empty state hidden');
    } else {
        console.error('❌ emptyState not found');
    }
}

function displayHistogram(histogramData) {
    const chartSection = document.getElementById('chartSection');
    const histogramDiv = document.getElementById('histogram');
    
    // Vérifier si on a les images matplotlib/seaborn
    if (window.lastSimulationData && window.lastSimulationData.images) {
        // Afficher les images matplotlib/seaborn
        histogramDiv.innerHTML = '';
        
        if (window.lastSimulationData.images.histogram) {
            const img = document.createElement('img');
            img.src = window.lastSimulationData.images.histogram;
            img.style.width = '100%';
            img.style.height = 'auto';
            img.style.borderRadius = '8px';
            img.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
            histogramDiv.appendChild(img);
        }
        
        // Afficher les graphes comparatifs si disponibles
        if (window.lastSimulationData.simulation_mode === 'multiple' && 
            window.lastSimulationData.images.sinistre_comparison) {
            
            const chartsContainer = document.createElement('div');
            chartsContainer.style.marginTop = '30px';
            chartsContainer.style.display = 'grid';
            chartsContainer.style.gridTemplateColumns = '1fr 1fr';
            chartsContainer.style.gap = '20px';
            
            // Graphe de comparaison sinistres
            const img1 = document.createElement('img');
            img1.src = window.lastSimulationData.images.sinistre_comparison;
            img1.style.width = '100%';
            img1.style.height = 'auto';
            img1.style.borderRadius = '8px';
            img1.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
            chartsContainer.appendChild(img1);
            
            // Graphe de distribution
            if (window.lastSimulationData.images.distribution) {
                const img2 = document.createElement('img');
                img2.src = window.lastSimulationData.images.distribution;
                img2.style.width = '100%';
                img2.style.height = 'auto';
                img2.style.borderRadius = '8px';
                img2.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
                chartsContainer.appendChild(img2);
            }
            
            histogramDiv.appendChild(chartsContainer);
        }
    } else {
        // Fallback sur Plotly si pas d'images (compatibilité)
        const trace = {
            x: histogramData.bins,
            type: 'histogram',
            nbinsx: Math.min(50, Math.ceil(Math.sqrt(histogramData.bins.length))),
            marker: {
                color: 'rgba(99, 102, 241, 0.7)',
                line: {
                    color: 'rgba(99, 102, 241, 1)',
                    width: 1.5
                }
            }
        };
        
        const layout = {
            title: {
                text: 'Distribution des Pertes',
                font: { size: 18, color: '#374151' }
            },
            xaxis: {
                title: `Pertes (${CURRENCY})`,
                gridcolor: '#E5E7EB'
            },
            yaxis: {
                title: 'Fréquence',
                gridcolor: '#E5E7EB'
            },
            hovermode: 'closest',
            paper_bgcolor: '#F9FAFB',
            plot_bgcolor: '#FFFFFF',
            margin: { l: 60, r: 40, t: 60, b: 60 }
        };
        
        const config = {
            responsive: true,
            displayModeBar: true,
            displaylogo: false
        };
        
        // Nettoyer le graphique précédent si existe
        Plotly.purge(histogramDiv);
        
        // Créer le graphique
        Plotly.newPlot(histogramDiv, [trace], layout, config);
    }
    
    // Afficher la section
    chartSection.style.display = 'block';
}

// ==================== UTILITAIRES ====================
function formatCurrency(value) {
    if (value === null || value === undefined) {
        return '-';
    }
    
    const formatted = new Intl.NumberFormat(CONFIG.CURRENCY.LOCALE, {
        style: 'decimal',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(value);
    
    return `${formatted} ${CURRENCY}`;
}

function showLoading(show) {
    const loadingState = document.getElementById('loadingState');
    const submitBtn = document.getElementById('submitBtn');
    
    appState.isLoading = show;
    
    if (show) {
        loadingState.style.display = 'flex';
        submitBtn.disabled = true;
    } else {
        loadingState.style.display = 'none';
        submitBtn.disabled = false;
    }
}

function showError(message) {
    alert('⚠️ ' + message);
    console.error(message);
}

// ==================== EVENT LISTENERS ====================
function setupEventListeners() {
    // Les event listeners du formulaire sont déjà setup
}
