"""
Input Validation Module

Validates simulation parameters before processing.
"""

from typing import List
import logging

logger = logging.getLogger(__name__)


def validate_simulation_params(lambda_param: float, mu_param: float, num_simulations: int) -> List[str]:
    """
    Validate simulation parameters.
    
    Args:
        lambda_param (float): Parameter λ for Poisson distribution
        mu_param (float): Parameter μ for Exponential distribution
        num_simulations (int): Number of simulations
    
    Returns:
        List[str]: List of error messages (empty if valid)
    """
    
    errors = []
    
    # Validate lambda
    if not isinstance(lambda_param, (int, float)):
        errors.append("λ (lambda) must be a number")
    elif lambda_param <= 0:
        errors.append("λ (lambda) must be positive")
    elif lambda_param > 1000:
        errors.append("λ (lambda) must be <= 1000")
    
    # Validate mu
    if not isinstance(mu_param, (int, float)):
        errors.append("μ (mu) must be a number")
    elif mu_param <= 0:
        errors.append("μ (mu) must be positive")
    elif mu_param > 1000000:
        errors.append("μ (mu) must be <= 1,000,000")
    
    # Validate num_simulations
    try:
        num_simulations = int(num_simulations)
    except:
        errors.append("Number of simulations must be an integer")
        return errors
    
    if num_simulations < 100:
        errors.append("Number of simulations must be >= 100")
    elif num_simulations > 1000000:
        errors.append("Number of simulations must be <= 1,000,000")
    
    return errors

