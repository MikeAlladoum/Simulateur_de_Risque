"""
Statistics Calculator

Computes statistical measures from simulation results.
"""

import numpy as np
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class StatisticsCalculator:
    """Calculate statistics from Monte Carlo simulation results."""
    
    def __init__(self, losses: np.ndarray):
        """
        Initialize with simulation results.
        
        Args:
            losses (np.ndarray): Array of simulated losses
        """
        self.losses = losses
        self.stats = {}
        
    def calculate_all(self) -> 'StatisticsCalculator':
        """
        Calculate all statistics.
        
        Returns:
            StatisticsCalculator: self (for chaining)
        """
        
        self.stats = {
            'mean': float(np.mean(self.losses)),
            'median': float(np.median(self.losses)),
            'std': float(np.std(self.losses)),
            'min': float(np.min(self.losses)),
            'max': float(np.max(self.losses)),
            'var_95': float(np.percentile(self.losses, 95)),
            'var_99': float(np.percentile(self.losses, 99)),
            'cvar_95': float(np.mean(self.losses[self.losses >= np.percentile(self.losses, 95)])),
            'cvar_99': float(np.mean(self.losses[self.losses >= np.percentile(self.losses, 99)])),
            'num_zero_loss': int(np.sum(self.losses == 0))
        }
        
        return self
    
    def get_statistics(self) -> Dict:
        """Get calculated statistics."""
        if not self.stats:
            self.calculate_all()
        return self.stats
    
    def to_dict(self) -> Dict:
        """Get statistics as dictionary (API compatibility)."""
        if not self.stats:
            self.calculate_all()
        return self.stats
    
    def get_histogram_data(self) -> Dict:
        """
        Generate histogram data for visualization.
        
        Returns:
            Dict: Histogram bins and frequencies
        """
        # Create 50 bins
        num_bins = 50
        hist, bin_edges = np.histogram(self.losses, bins=num_bins)
        
        # Calculate bin centers
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        return {
            'bins': bin_centers.tolist(),
            'frequencies': hist.tolist(),
            'edges': bin_edges.tolist()
        }

