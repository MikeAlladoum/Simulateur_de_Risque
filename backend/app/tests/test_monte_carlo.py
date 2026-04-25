"""
Tests du Moteur Monte Carlo

Tests unitaires pour la classe MonteCarlo
"""
import pytest
import numpy as np
from app.simulation.monte_carlo import MonteCarlo


class TestMonteCarlo:
    """Tests de la classe MonteCarlo"""
    
    def test_initialization(self):
        """Test l'initialisation"""
        mc = MonteCarlo(lambda_param=5, mu_param=1000, num_simulations=1000)
        assert mc.lambda_param == 5
        assert mc.mu_param == 1000
        assert mc.num_simulations == 1000
    
    def test_invalid_lambda(self):
        """Test avec λ invalide"""
        with pytest.raises(ValueError):
            MonteCarlo(lambda_param=-1, mu_param=1000, num_simulations=1000)
        
        with pytest.raises(ValueError):
            MonteCarlo(lambda_param=0, mu_param=1000, num_simulations=1000)
    
    def test_invalid_mu(self):
        """Test avec μ invalide"""
        with pytest.raises(ValueError):
            MonteCarlo(lambda_param=5, mu_param=-1, num_simulations=1000)
    
    def test_invalid_num_simulations(self):
        """Test avec N invalide"""
        with pytest.raises(ValueError):
            MonteCarlo(lambda_param=5, mu_param=1000, num_simulations=0)
    
    def test_simulate(self):
        """Test la simulation"""
        mc = MonteCarlo(lambda_param=5, mu_param=1000, num_simulations=10000)
        losses = mc.simulate()
        
        assert losses is not None
        assert len(losses) == 10000
        assert np.all(losses >= 0)  # Toutes les pertes >= 0
    
    def test_get_summary(self):
        """Test le résumé"""
        mc = MonteCarlo(lambda_param=5, mu_param=1000, num_simulations=1000)
        mc.simulate()
        summary = mc.get_summary()
        
        assert 'mean' in summary
        assert 'min' in summary
        assert 'max' in summary
        assert 'std' in summary
        assert summary['min'] <= summary['mean'] <= summary['max']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
