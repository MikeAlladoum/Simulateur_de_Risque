/**
 * Chart Configuration
 * 
 * Configuration pour Chart.js
 */

/**
 * Options par défaut pour les graphiques
 */
const chartDefaults = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            display: true,
            position: 'top',
            labels: {
                font: {
                    size: 12,
                    family: CONFIG.CHART_COLORS.PRIMARY
                },
                padding: 15,
                usePointStyle: true
            }
        },
        tooltip: {
            callbacks: {
                label: function(context) {
                    let label = context.dataset.label || '';
                    if (label) {
                        label += ': ';
                    }
                    label += formatNumber(context.parsed.y);
                    return label;
                }
            }
        }
    },
    scales: {
        x: {
            title: {
                display: true,
                text: 'Perte (unités monétaires)',
                font: {
                    size: 12,
                    weight: 'bold'
                }
            },
            ticks: {
                maxTicksLimit: 10,
                callback: function(value) {
                    return formatNumber(value, 0);
                }
            }
        },
        y: {
            title: {
                display: true,
                text: 'Fréquence',
                font: {
                    size: 12,
                    weight: 'bold'
                }
            },
            beginAtZero: true,
            ticks: {
                maxTicksLimit: 10
            }
        }
    }
};

/**
 * Création d'un graphique histogramme
 * @param {CanvasRenderingContext2D} ctx - Canvas context
 * @param {array} bins - Valeurs des bins
 * @param {array} frequencies - Fréquences
 * @returns {Chart} Instance Chart.js
 */
function createHistogram(ctx, bins, frequencies) {
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: bins.map(b => formatNumber(b, 0)),
            datasets: [{
                label: 'Distribution des Pertes',
                data: frequencies,
                backgroundColor: CONFIG.CHART_COLORS.PRIMARY,
                borderColor: '#2980b9',
                borderWidth: 1,
                borderRadius: 4,
                hoverBackgroundColor: '#2980b9'
            }]
        },
        options: chartDefaults
    });
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { createHistogram };
}
