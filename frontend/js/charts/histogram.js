/**
 * Histogram Chart
 * 
 * Gestion du graphique histogramme
 */

let histogramChart = null;

/**
 * Affiche l'histogramme
 * @param {object} histogramData - Données {bins, frequencies}
 */
function displayHistogram(histogramData) {
    const canvas = document.getElementById('histogram');
    if (!canvas) return;

    // Détruire le graphique existant
    if (histogramChart) {
        histogramChart.destroy();
    }

    const ctx = canvas.getContext('2d');
    histogramChart = createHistogram(ctx, histogramData.bins, histogramData.frequencies);
}

/**
 * Détruit le graphique
 */
function destroyHistogram() {
    if (histogramChart) {
        histogramChart.destroy();
        histogramChart = null;
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { displayHistogram, destroyHistogram };
}
