"""
Calculs Statistiques

Classe pour calculer les indicateurs de risque
"""
import numpy as np
from ..models import StatisticsResult


class StatisticsCalculator:
    """
    Calculateur de statistiques des résultats de simulation
    
    Fournit les statistiques descriptives et les indicateurs de risque
    """
    
    def __init__(self, losses: np.ndarray):
        """
        Initialise le calculateur
        
        Args:
            losses: Tableau des pertes simulées (résultats de MonteCarlo)
        
        Raises:
            ValueError: Si le tableau est vide
        """
        if losses is None or len(losses) == 0:
            raise ValueError("Les pertes ne peuvent pas être vides")
        
        self.losses = losses
    
    def calculate_mean(self) -> float:
        """Perte moyenne"""
        return float(np.mean(self.losses))
    
    def calculate_median(self) -> float:
        """Perte médiane"""
        return float(np.median(self.losses))
    
    def calculate_std(self) -> float:
        """Écart-type des pertes"""
        return float(np.std(self.losses))
    
    def calculate_min(self) -> float:
        """Perte minimale"""
        return float(np.min(self.losses))
    
    def calculate_max(self) -> float:
        """Perte maximale"""
        return float(np.max(self.losses))
    
    def calculate_var(self, confidence: float = 0.95) -> float:
        """
        Value at Risk (VaR)
        
        Perte maximale probable avec un niveau de confiance
        
        Args:
            confidence: Niveau de confiance (0.95 pour 95%, 0.99 pour 99%)
        
        Returns:
            float: VaR au niveau de confiance donné
        
        Example:
            >>> var_95 = calc.calculate_var(0.95)  # VaR 95%
            >>> var_99 = calc.calculate_var(0.99)  # VaR 99%
        """
        return float(np.percentile(self.losses, confidence * 100))
    
    def calculate_cvar(self, confidence: float = 0.95) -> float:
        """
        Conditional Value at Risk (CVaR) / Expected Shortfall
        
        Perte moyenne en cas de dépassement du VaR
        
        Args:
            confidence: Niveau de confiance (0.95 pour 95%, 0.99 pour 99%)
        
        Returns:
            float: CVaR au niveau de confiance donné
        
        Formule:
            CVaR_α = E[L | L >= VaR_α]
        
        Example:
            >>> cvar_95 = calc.calculate_cvar(0.95)
        """
        var = self.calculate_var(confidence)
        # Pertes supérieures au VaR
        losses_above_var = self.losses[self.losses >= var]
        
        if len(losses_above_var) == 0:
            return var  # Si pas de pertes >= VaR, retourner VaR
        
        return float(np.mean(losses_above_var))
    
    def calculate_probability_above_threshold(self, threshold: float) -> float:
        """
        Probabilité de dépasser un seuil
        
        Args:
            threshold: Seuil de perte
        
        Returns:
            float: Probabilité entre 0 et 1
        
        Example:
            >>> prob = calc.calculate_probability_above_threshold(2000)
        """
        if threshold < 0:
            raise ValueError("Le seuil doit être positif")
        
        return float(np.sum(self.losses > threshold) / len(self.losses))
    
    def calculate_num_zero_loss(self) -> int:
        """
        Nombre de simulations sans perte
        
        Returns:
            int: Nombre de cas où la perte est zéro
        """
        return int(np.sum(self.losses == 0))
    
    def calculate_all(self) -> StatisticsResult:
        """
        Calcule toutes les statistiques
        
        Returns:
            StatisticsResult: Objet contenant toutes les statistiques
        
        Example:
            >>> stats = calc.calculate_all()
            >>> print(stats.mean, stats.var_95, stats.cvar_99)
        """
        return StatisticsResult(
            mean=self.calculate_mean(),
            median=self.calculate_median(),
            std=self.calculate_std(),
            min=self.calculate_min(),
            max=self.calculate_max(),
            var_95=self.calculate_var(0.95),
            var_99=self.calculate_var(0.99),
            cvar_95=self.calculate_cvar(0.95),
            cvar_99=self.calculate_cvar(0.99),
            num_zero_loss=self.calculate_num_zero_loss()
        )
    
    def get_quantiles(self, quantiles: list = [0.05, 0.25, 0.5, 0.75, 0.95]) -> dict:
        """
        Calcule les quantiles
        
        Args:
            quantiles: Liste des quantiles à calculer
        
        Returns:
            dict: Dictionnaire {quantile: valeur}
        """
        return {
            q: float(np.percentile(self.losses, q * 100))
            for q in quantiles
        }
