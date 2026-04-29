"""
Modèles de données

Classes pour structurer les données de requête/réponse
"""
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class SimulationRequest:
    """Requête de simulation"""
    lambda_param: float          # Fréquence des sinistres
    mu_param: float              # Coût moyen
    num_simulations: int         # Nombre de simulations
    scenario_name: Optional[str] = None  # Nom optionnel du scénario


@dataclass
class SimulationResult:
    """Résultat de simulation"""
    success: bool
    statistics: Dict
    histogram: Dict
    parameters: Dict
    chart_image: Optional[str] = None  # Image matplotlib en base64
    error: Optional[str] = None
    
    def to_dict(self):
        """Convertir en dictionnaire pour JSON"""
        return {
            'success': self.success,
            'statistics': self.statistics,
            'histogram': self.histogram,
            'chart_image': self.chart_image,
            'parameters': self.parameters,
            'error': self.error
        }


@dataclass
class StatisticsResult:
    """Résultats statistiques"""
    mean: float
    median: float
    std: float
    min: float
    max: float
    var_95: float
    var_99: float
    cvar_95: float
    cvar_99: float
    num_zero_loss: int
    
    def to_dict(self):
        return {
            'mean': self.mean,
            'median': self.median,
            'std': self.std,
            'min': self.min,
            'max': self.max,
            'var_95': self.var_95,
            'var_99': self.var_99,
            'cvar_95': self.cvar_95,
            'cvar_99': self.cvar_99,
            'num_zero_loss': self.num_zero_loss
        }
