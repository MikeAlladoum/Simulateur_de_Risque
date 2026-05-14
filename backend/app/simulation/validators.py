"""
Validation des Paramètres

Valide les paramètres de simulation
"""
import config
from typing import List


def validate_simulation_params(
    lambda_param: float,
    mu_param: float,
    num_simulations: int
) -> List[str]:
    """
    Valide les paramètres de simulation
    
    Args:
        lambda_param: Fréquence des sinistres
        mu_param: Coût moyen
        num_simulations: Nombre de simulations
    
    Returns:
        List[str]: Liste des erreurs (vide si valide)
    
    Example:
        >>> errors = validate_simulation_params(5, 1000, 10000)
        >>> if errors:
        ...     print("Erreurs:", errors)
    """
    errors = []
    
    # Validation λ
    if not isinstance(lambda_param, (int, float)):
        errors.append("λ doit être un nombre")
    else:
        constraints = config.SIMULATION_CONSTRAINTS['lambda']
        if lambda_param < constraints['min']:
            errors.append(f"λ doit être >= {constraints['min']}")
        elif lambda_param > constraints['max']:
            errors.append(f"λ doit être <= {constraints['max']}")
    
    # Validation μ
    if not isinstance(mu_param, (int, float)):
        errors.append("μ doit être un nombre")
    else:
        constraints = config.SIMULATION_CONSTRAINTS['mu']
        if mu_param < constraints['min']:
            errors.append(f"μ doit être >= {constraints['min']}")
        elif mu_param > constraints['max']:
            errors.append(f"μ doit être <= {constraints['max']}")
    
    # Validation N
    if not isinstance(num_simulations, int):
        errors.append("N doit être un entier")
    else:
        constraints = config.SIMULATION_CONSTRAINTS['num_simulations']
        if num_simulations < constraints['min']:
            errors.append(f"N doit être >= {constraints['min']}")
        elif num_simulations > constraints['max']:
            errors.append(f"N doit être <= {constraints['max']}")
    
    return errors


def validate_lambda(lambda_param: float) -> bool:
    """Valide λ seul"""
    return lambda_param > 0


def validate_mu(mu_param: float) -> bool:
    """Valide μ seul"""
    return mu_param > 0


def validate_num_simulations(num_simulations: int) -> bool:
    """Valide N seul"""
    return num_simulations > 0 and isinstance(num_simulations, int)
