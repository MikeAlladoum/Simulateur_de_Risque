/**
 * UI - Gestion de l'interface utilisateur
 * 
 * Affichage des résultats et gestion de l'état
 */

/**
 * Formate un nombre comme devise (FCFA)
 * @param {number} num - Nombre à formater
 * @param {string} currency - Devise (défaut: FCFA)
 * @returns {string} Nombre formaté avec devise
 */
function formatCurrency(num, currency = 'FCFA') {
    if (num === null || num === undefined) return '-';
    
    const formatted = Math.round(num).toLocaleString('fr-FR');
    return `${formatted} ${currency}`;
}

/**
 * Formate un nombre simple
 * @param {number} num - Nombre à formater
 * @returns {string} Nombre formaté
 */
function formatNumber(num) {
    if (num === null || num === undefined) return '-';
    return Math.round(num).toLocaleString('fr-FR');
}

/**
 * Affiche les résultats
 * @param {object} data - Résultats de la simulation
 */
function displayResults(data) {
    const stats = data.statistics;

    // Afficher les statistiques avec devise FCFA
    document.getElementById('statMean').textContent = formatCurrency(stats.mean);
    document.getElementById('statMedian').textContent = formatCurrency(stats.median);
    document.getElementById('statStd').textContent = formatCurrency(stats.std);
    document.getElementById('statMin').textContent = formatCurrency(stats.min);
    document.getElementById('statMax').textContent = formatCurrency(stats.max);
    document.getElementById('statZeroLoss').textContent = formatNumber(stats.num_zero_loss);

    // Afficher les indicateurs de risque avec devise
    document.getElementById('statVar95').textContent = formatCurrency(stats.var_95);
    document.getElementById('statVar99').textContent = formatCurrency(stats.var_99);
    document.getElementById('statCvar95').textContent = formatCurrency(stats.cvar_95);
    document.getElementById('statCvar99').textContent = formatCurrency(stats.cvar_99);

    // Afficher l'histogramme
    displayHistogram(data.histogram);

    // Afficher la section des résultats
    document.getElementById('resultsSection').style.display = 'block';
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Affiche un message de chargement
 * @param {boolean} show - Afficher ou masquer
 */
function showLoading(show = true) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
    document.getElementById('simulateBtn').disabled = show;
}

/**
 * Affiche une erreur
 * @param {string} message - Message d'erreur
 */
function showError(message) {
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');

    errorMessage.textContent = message;
    errorSection.style.display = 'block';
    errorSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Masque l'erreur
 */
function hideError() {
    document.getElementById('errorSection').style.display = 'none';
}

/**
 * Masque les résultats
 */
function hideResults() {
    document.getElementById('resultsSection').style.display = 'none';
    destroyHistogram();
}

/**
 * Réinitialise l'interface
 */
function resetUI() {
    hideError();
    hideResults();
    showLoading(false);
    document.getElementById('simulationForm').reset();

    // Remettre les valeurs par défaut
    document.getElementById('lambda').value = CONFIG.DEFAULTS.LAMBDA;
    document.getElementById('mu').value = CONFIG.DEFAULTS.MU;
    document.getElementById('numSimulations').value = CONFIG.DEFAULTS.NUM_SIMULATIONS;
}

/**
 * Mets à jour le statut du serveur
 * @param {boolean} online - Serveur en ligne?
 */
function updateServerStatus(online) {
    const statusElement = document.getElementById('serverStatus');
    if (online) {
        statusElement.textContent = '🟢 Serveur en ligne';
        statusElement.style.color = '#27ae60';
    } else {
        statusElement.textContent = '🔴 Serveur hors ligne';
        statusElement.style.color = '#e74c3c';
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        displayResults,
        showLoading,
        showError,
        hideError,
        hideResults,
        resetUI,
        updateServerStatus
    };
}
