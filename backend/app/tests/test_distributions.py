"""
Tests des Distributions

Tests unitaires pour les distributions Poisson et Exponentielle
"""
import pytest
import numpy as np
from app.simulation.distributions import PoissonDistribution, ExponentialDistribution


class TestPoissonDistribution:
    """Tests de la distribution de Poisson"""
    
    def test_initialization(self):
        """Test l'initialisation"""
        dist = PoissonDistribution(lambda_param=5)
        assert dist.lambda_param == 5
    
    def test_invalid_lambda(self):
        """Test avec λ invalide"""
        with pytest.raises(ValueError):
            PoissonDistribution(lambda_param=-1)
        
        with pytest.raises(ValueError):
            PoissonDistribution(lambda_param=0)
    
    def test_generate_single(self):
        """Test génération d'une valeur"""
        dist = PoissonDistribution(lambda_param=5)
        value = dist.generate()
        assert isinstance(value, int)
        assert value >= 0
    
    def test_generate_multiple(self):
        """Test génération de plusieurs valeurs"""
        dist = PoissonDistribution(lambda_param=5)
        values = dist.generate(size=1000)
        assert len(values) == 1000
        assert np.all(values >= 0)


class TestExponentialDistribution:
    """Tests de la distribution exponentielle"""
    
    def test_initialization(self):
        """Test l'initialisation"""
        dist = ExponentialDistribution(mu_param=1000)
        assert dist.mu_param == 1000
    
    def test_invalid_mu(self):
        """Test avec μ invalide"""
        with pytest.raises(ValueError):
            ExponentialDistribution(mu_param=-100)
    
    def test_generate_single(self):
        """Test génération d'une valeur"""
        dist = ExponentialDistribution(mu_param=1000)
        value = dist.generate()
        assert isinstance(value, float)
        assert value >= 0
    
    def test_generate_multiple(self):
        """Test génération de plusieurs valeurs"""
        dist = ExponentialDistribution(mu_param=1000)
        values = dist.generate(size=1000)
        assert len(values) == 1000
        assert np.all(values >= 0)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
