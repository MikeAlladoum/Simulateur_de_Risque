/**
 * Formatters - Utilitaires de formatage
 * 
 * Formate les nombres pour l'affichage
 */

/**
 * Formate un nombre avec séparateurs
 * @param {number} num - Nombre à formater
 * @param {number} decimals - Nombre de décimales (défaut: 2)
 * @returns {string} Nombre formaté
 */
function formatNumber(num, decimals = 2) {
    if (num === null || num === undefined) {
        return '-';
    }

    if (!isFinite(num)) {
        return '-';
    }

    // Arrondir
    const rounded = Math.round(num * Math.pow(10, decimals)) / Math.pow(10, decimals);

    // Formater avec locales
    return rounded.toLocaleString('fr-FR', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

/**
 * Formate un nombre en devise
 * @param {number} num - Montant
 * @returns {string} Montant formaté
 */
function formatCurrency(num) {
    return formatNumber(num, 2) + ' €';
}

/**
 * Formate un nombre en pourcentage
 * @param {number} num - Valeur (0-1 ou 0-100)
 * @returns {string} Pourcentage formaté
 */
function formatPercentage(num) {
    if (num < 1) {
        num *= 100;
    }
    return formatNumber(num, 2) + '%';
}

// Export pour modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { formatNumber, formatCurrency, formatPercentage };
}
