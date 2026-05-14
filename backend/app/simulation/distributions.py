"""
Distributions Statistiques

Générateurs de nombres aléatoires pour Poisson et Exponentielle
"""
import numpy as np
from abc import ABC, abstractmethod


class Distribution(ABC):
    """Classe abstraite pour les distributions"""
    
    @abstractmethod
    def generate(self, size: int = 1):
        """Générer des échantillons aléatoires"""
        pass


class PoissonDistribution(Distribution):
    """
    Loi de Poisson
    
    Utilisée pour modéliser le nombre de sinistres
    
    Paramètre: λ (lambda)
    - λ = nombre moyen de sinistres
    """
    
    def __init__(self, lambda_param: float):
        """
        Initialise la distribution de Poisson
        
        Args:
            lambda_param: Paramètre λ > 0
        
        Raises:
            ValueError: Si λ <= 0
        """
        if lambda_param <= 0:
            raise ValueError("λ doit être strictement positif")
        
        self.lambda_param = lambda_param
    
    def generate(self, size: int = 1) -> np.ndarray | int:
        """
        Génère des échantillons selon Poisson(λ)
        
        Args:
            size: Nombre d'échantillons à générer (défaut: 1)
        
        Returns:
            np.ndarray | int: Valeur(s) aléatoire(s)
        
        Example:
            >>> dist = PoissonDistribution(lambda_param=5)
            >>> n = dist.generate()  # Un entier ~ Poisson(5)
            >>> ns = dist.generate(size=1000)  # 1000 valeurs
        """
        result = np.random.poisson(lam=self.lambda_param, size=size)
        
        # Retourner un entier si size=1
        if size == 1 and isinstance(result, np.ndarray):
            return int(result[0])
        
        return int(result) if size == 1 else result


class ExponentialDistribution(Distribution):
    """
    Loi Exponentielle
    
    Utilisée pour modéliser les coûts des sinistres
    
    Paramètre: μ (mu) = coût moyen
    
    La loi exponentielle est définie par :
    f(x) = (1/μ) * exp(-x/μ)
    """
    
    def __init__(self, mu_param: float):
        """
        Initialise la distribution exponentielle
        
        Args:
            mu_param: Paramètre μ > 0 (coût moyen)
        
        Raises:
            ValueError: Si μ <= 0
        """
        if mu_param <= 0:
            raise ValueError("μ doit être strictement positif")
        
        self.mu_param = mu_param
    
    def generate(self, size: int = 1) -> np.ndarray | float:
        """
        Génère des échantillons selon Exp(μ)
        
        Args:
            size: Nombre d'échantillons à générer (défaut: 1)
        
        Returns:
            np.ndarray | float: Valeur(s) aléatoire(s)
        
        Example:
            >>> dist = ExponentialDistribution(mu_param=1000)
            >>> cost = dist.generate()  # Un coût ~ Exp(1000)
            >>> costs = dist.generate(size=100)  # 100 coûts
        """
        result = np.random.exponential(scale=self.mu_param, size=size)
        
        # Retourner un float si size=1
        if size == 1 and isinstance(result, np.ndarray):
            return float(result[0])
        
        return float(result) if size == 1 else result


# Distribution Factory (optionnel, pour extension future)
class DistributionFactory:
    """Factory pour créer les distributions"""
    
    @staticmethod
    def create_poisson(lambda_param: float) -> PoissonDistribution:
        return PoissonDistribution(lambda_param)
    
    @staticmethod
    def create_exponential(mu_param: float) -> ExponentialDistribution:
        return ExponentialDistribution(mu_param)
