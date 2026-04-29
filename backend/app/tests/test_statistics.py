"""
Tests des Calculs Statistiques

Tests unitaires pour le calculateur de statistiques
"""
import pytest
import numpy as np
from app.simulation.statistics import StatisticsCalculator


class TestStatisticsCalculator:
    """Tests de la classe StatisticsCalculator"""
    
    def setup_method(self):
        """Préparation avant chaque test"""
        # Créer des données de test
        np.random.seed(42)
        self.losses = np.array([0, 100, 500, 1000, 2000, 3000, 5000])
        self.calc = StatisticsCalculator(self.losses)
    
    def test_initialization(self):
        """Test l'initialisation"""
        assert self.calc.losses is not None
        assert len(self.calc.losses) == 7
    
    def test_calculate_mean(self):
        """Test le calcul de la moyenne"""
        mean = self.calc.calculate_mean()
        expected = np.mean(self.losses)
        assert mean == expected
    
    def test_calculate_median(self):
        """Test le calcul de la médiane"""
        median = self.calc.calculate_median()
        expected = np.median(self.losses)
        assert median == expected
    
    def test_calculate_std(self):
        """Test le calcul de l'écart-type"""
        std = self.calc.calculate_std()
        expected = np.std(self.losses)
        assert std == expected
    
    def test_calculate_min(self):
        """Test le calcul du minimum"""
        min_loss = self.calc.calculate_min()
        assert min_loss == 0
    
    def test_calculate_max(self):
        """Test le calcul du maximum"""
        max_loss = self.calc.calculate_max()
        assert max_loss == 5000
    
    def test_calculate_var(self):
        """Test le calcul du VaR"""
        var_95 = self.calc.calculate_var(0.95)
        var_99 = self.calc.calculate_var(0.99)
        assert var_95 <= var_99
        assert var_95 > 0
    
    def test_calculate_cvar(self):
        """Test le calcul du CVaR"""
        cvar_95 = self.calc.calculate_cvar(0.95)
        var_95 = self.calc.calculate_var(0.95)
        assert cvar_95 >= var_95
    
    def test_calculate_all(self):
        """Test le calcul de toutes les statistiques"""
        stats = self.calc.calculate_all()
        assert stats.mean > 0
        assert stats.std >= 0
        assert stats.var_95 <= stats.var_99
        assert stats.num_zero_loss >= 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
