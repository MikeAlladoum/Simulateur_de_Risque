"""
Moteur Monte Carlo

Classe principale pour effectuer les simulations
"""
import numpy as np
from typing import Tuple, List
from .distributions import PoissonDistribution, ExponentialDistribution


class MonteCarlo:
    """
    Moteur de simulation Monte Carlo
    
    Simule les pertes financières basées sur:
    - Nombre de sinistres (loi de Poisson)
    - Coûts individuels (loi exponentielle)
    """
    
    def __init__(self, lambda_param: float, mu_param: float, num_simulations: int):
        """
        Initialise le simulateur Monte Carlo
        
        Args:
            lambda_param: Paramètre λ de la loi de Poisson (fréquence)
            mu_param: Paramètre μ de la loi exponentielle (coût moyen)
            num_simulations: Nombre de simulations à effectuer
        
        Raises:
            ValueError: Si les paramètres sont invalides
        """
        if lambda_param <= 0:
            raise ValueError("λ doit être positif")
        if mu_param <= 0:
            raise ValueError("μ doit être positif")
        if num_simulations <= 0:
            raise ValueError("Le nombre de simulations doit être positif")
        
        self.lambda_param = lambda_param
        self.mu_param = mu_param
        self.num_simulations = num_simulations
        self.results = None
        
        # Générateurs de distributions
        self.poisson_dist = PoissonDistribution(lambda_param)
        self.exponential_dist = ExponentialDistribution(mu_param)
    
    def simulate(self) -> np.ndarray:
        """
        Effectue la simulation Monte Carlo
        
        Algorithme:
        Pour chaque simulation (i = 1 à N):
            1. Générer N_i ~ Poisson(λ)  [nombre de sinistres]
            2. Générer X_i1, X_i2, ..., X_iN_i ~ Exp(μ)  [coûts]
            3. Calculer L_i = Σ X_ij  [perte totale]
        
        Returns:
            np.ndarray: Tableau des pertes (shape: (num_simulations,))
        
        Example:
            >>> mc = MonteCarlo(lambda_param=5, mu_param=1000, num_simulations=10000)
            >>> losses = mc.simulate()
            >>> losses.shape
            (10000,)
        """
        losses = np.zeros(self.num_simulations)
        
        for i in range(self.num_simulations):
            # Générer le nombre de sinistres
            num_claims = self.poisson_dist.generate()
            
            # Générer les coûts et calculer la perte totale
            if num_claims > 0:
                costs = self.exponential_dist.generate(num_claims)
                losses[i] = np.sum(costs)
            else:
                losses[i] = 0.0
        
        self.results = losses
        return losses
    
    def get_histogram_data(self, bins: int = 50) -> dict:
        """
        Prépare les données pour créer un histogramme
        
        Args:
            bins: Nombre de classes pour l'histogramme
        
        Returns:
            dict: {'bins': [...], 'frequencies': [...]}
        
        Raises:
            ValueError: Si aucune simulation n'a été effectuée
        """
        if self.results is None:
            raise ValueError("Effectuez une simulation d'abord (simulate())")
        
        frequencies, bin_edges = np.histogram(self.results, bins=bins)
        
        # Centres des bins
        bin_centers = [
            (bin_edges[i] + bin_edges[i+1]) / 2 
            for i in range(len(bin_edges) - 1)
        ]
        
        return {
            'bins': [float(b) for b in bin_centers],
            'frequencies': frequencies.tolist()
        }
    
    def get_results(self) -> np.ndarray:
        """
        Retourne les résultats de simulation
        
        Returns:
            np.ndarray: Tableau des pertes
        
        Raises:
            ValueError: Si aucune simulation n'a été effectuée
        """
        if self.results is None:
            raise ValueError("Effectuez une simulation d'abord (simulate())")
        
        return self.results
    
    def get_summary(self) -> dict:
        """
        Résumé rapide des résultats
        
        Returns:
            dict: Statistiques basiques
        """
        if self.results is None:
            raise ValueError("Effectuez une simulation d'abord (simulate())")
        
        return {
            'mean': float(np.mean(self.results)),
            'min': float(np.min(self.results)),
            'max': float(np.max(self.results)),
            'std': float(np.std(self.results))
        }
