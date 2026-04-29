"""
Monte Carlo Simulation Engine

Implements Monte Carlo simulation for financial risk analysis.
Uses Poisson process for frequency and Exponential distribution for severity.
"""

import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class MonteCarlo:
    """Monte Carlo simulation for financial loss analysis."""
    
    def __init__(self, lambda_param: float, mu_param: float, num_simulations: int):
        """
        Initialize Monte Carlo simulator.
        
        Args:
            lambda_param (float): Parameter λ for Poisson distribution (frequency)
            mu_param (float): Parameter μ for Exponential distribution (severity)
            num_simulations (int): Number of simulations to run
        """
        self.lambda_param = lambda_param
        self.mu_param = mu_param
        self.num_simulations = num_simulations
        self.losses = None
        
    def simulate(self) -> np.ndarray:
        """
        Execute Monte Carlo simulation.
        
        Returns:
            np.ndarray: Array of simulated total losses for each simulation
        """
        logger.info(f"Running {self.num_simulations} simulations with λ={self.lambda_param}, μ={self.mu_param}")
        
        # Initialize losses array
        self.losses = np.zeros(self.num_simulations)
        
        # Run simulations
        for i in range(self.num_simulations):
            # Generate number of events (Poisson)
            num_events = np.random.poisson(self.lambda_param)
            
            # If events occur, generate severity from Exponential distribution
            if num_events > 0:
                severities = np.random.exponential(self.mu_param, num_events)
                self.losses[i] = np.sum(severities)
            else:
                self.losses[i] = 0.0
        
        logger.info(f"Simulation complete. Mean loss: {np.mean(self.losses):.2f}")
        return self.losses
    
    def run(self) -> np.ndarray:
        """Alias for simulate() for backwards compatibility."""
        return self.simulate()
    
    def get_losses(self) -> np.ndarray:
        """Get simulated losses."""
        if self.losses is None:
            raise ValueError("Simulation not run yet. Call simulate() first.")
        return self.losses
    
    def get_histogram_data(self, bins: int = 50) -> Dict:
        """
        Generate histogram data for visualization.
        
        Args:
            bins (int): Number of histogram bins
        
        Returns:
            Dict: Histogram bins and frequencies
        """
        if self.losses is None:
            raise ValueError("Simulation not run yet. Call simulate() first.")
        
        # Create histogram
        hist, bin_edges = np.histogram(self.losses, bins=bins)
        
        # Calculate bin centers
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        return {
            'bins': bin_centers.tolist(),
            'frequencies': hist.tolist(),
            'edges': bin_edges.tolist()
        }

