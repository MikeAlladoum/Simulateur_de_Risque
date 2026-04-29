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
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    console.log('🚀 Initialisation de l\'application...');
    
    // Vérifier la connexion au serveur
    checkServerHealth();
    
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
            console.log('✅ Serveur connecté');
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
    
    console.log('🔍 Form found:', form ? 'YES' : 'NO');
    console.log('🔍 Button found:', submitBtn ? 'YES' : 'NO');
    
    if (!form) {
        console.error('❌ CRITICAL: Form #simulationForm not found!');
        return;
    }
    
    // Listener on form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('📤 Form submitted via form listener!');
        await handleFormSubmit();
    });
    
    // CRITICAL: Also listen to button click directly (fallback)
    if (submitBtn) {
        submitBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            console.log('📤 Form submitted via button click!');
            await handleFormSubmit();
        });
    }
    
    // Validation en temps réel
    const inputs = form.querySelectorAll('.form-input');
    inputs.forEach(input => {
        input.addEventListener('change', validateField);
        input.addEventListener('input', validateField);
    });
    
    console.log('✅ Form listeners setup complete');
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
    console.log('🚀 handleFormSubmit called');
    
    const lambda = parseFloat(document.getElementById('lambda').value);
    const mu = parseFloat(document.getElementById('mu').value);
    const numSimulations = parseInt(document.getElementById('numSimulations').value);
    
    console.log('📝 Form values:', { lambda, mu, numSimulations });
    
    // Validation
    if (!validate(lambda, mu, numSimulations)) {
        console.log('❌ Validation failed');
        return;
    }
    
    console.log('✅ Validation passed');
    
    // Afficher le loader
    showLoading(true);
    
    try {
        // Appel API
        console.log('📡 Calling API...');
        const response = await fetch(`${API_BASE_URL}/simulate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                lambda: lambda,
                mu: mu,
                num_simulations: numSimulations
            })
        });
        
        console.log('📥 API Response:', response.status, response.ok);
        
        if (!response.ok) {
            throw new Error(`Erreur HTTP: ${response.status}`);
        }
        
        const response_data = await response.json();
        console.log('📊 Response data:', response_data);
        
        // Transformer la réponse de l'API au format attendu
        const data = {
            mean: response_data.statistics?.mean,
            median: response_data.statistics?.median,
            min: response_data.statistics?.min,
            max: response_data.statistics?.max,
            std: response_data.statistics?.std,
            histogram_data: response_data.histogram
        };
        
        console.log('🔄 Transformed data:', data);
        
        // Sauvegarder les résultats
        appState.results = data;
        
        // Afficher les résultats
        console.log('🎨 Calling displayResults...');
        displayResults(data);
        
        console.log('✅ Simulation réussie');
        
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
    console.log('📍 displayResults called with:', data);
    
    // Afficher les statistiques
    displayStats(data);
    
    // Afficher le graphique
    if (data.histogram_data) {
        console.log('📈 Displaying histogram...');
        displayHistogram(data.histogram_data);
    } else {
        console.warn('⚠️ No histogram data');
    }
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
    
    // Préparer les données pour Plotly
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
