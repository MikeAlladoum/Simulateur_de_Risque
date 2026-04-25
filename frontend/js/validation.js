/**
 * Validation - Validation des formulaires
 * 
 * Valide les paramètres de simulation
 */

/**
 * Valide un paramètre
 * @param {string} paramName - Nom du paramètre
 * @param {number} value - Valeur
 * @returns {object} {valid: boolean, error: string}
 */
function validateParameter(paramName, value) {
    const constraints = CONFIG.CONSTRAINTS[paramName.toUpperCase()];

    if (!constraints) {
        return { valid: false, error: `Paramètre inconnu: ${paramName}` };
    }

    // Vérifier que c'est un nombre
    const numValue = parseFloat(value);
    if (isNaN(numValue) || !isFinite(numValue)) {
        return { valid: false, error: `${paramName} doit être un nombre` };
    }

    // Vérifier les limites
    if (numValue < constraints.min) {
        return { valid: false, error: `${paramName} doit être >= ${constraints.min}` };
    }

    if (numValue > constraints.max) {
        return { valid: false, error: `${paramName} doit être <= ${constraints.max}` };
    }

    return { valid: true, error: null };
}

/**
 * Valide le formulaire complet
 * @returns {object} {valid: boolean, errors: array}
 */
function validateForm() {
    const errors = [];

    // Récupérer les valeurs
    const lambda = document.getElementById('lambda').value;
    const mu = document.getElementById('mu').value;
    const numSims = document.getElementById('numSimulations').value;

    // Valider λ
    let result = validateParameter('LAMBDA', lambda);
    if (!result.valid) errors.push(result.error);

    // Valider μ
    result = validateParameter('MU', mu);
    if (!result.valid) errors.push(result.error);

    // Valider N
    result = validateParameter('NUM_SIMULATIONS', numSims);
    if (!result.valid) errors.push(result.error);

    return { valid: errors.length === 0, errors };
}

/**
 * Affiche les erreurs de validation
 * @param {array} errors - Liste des erreurs
 */
function displayValidationErrors(errors) {
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');

    if (errors && errors.length > 0) {
        errorMessage.innerHTML = errors.map(e => `• ${e}`).join('<br>');
        errorSection.style.display = 'block';
    }
}

/**
 * Masque les erreurs
 */
function clearErrors() {
    const errorSection = document.getElementById('errorSection');
    errorSection.style.display = 'none';
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { validateForm, validateParameter, displayValidationErrors, clearErrors };
}
