"""
Optimisations et améliorations de performance pour les simulations

Module créé par Gad105 pour améliorer l'efficacité des calculs
et ajouter du caching pour les simulations répétitives.
"""
import hashlib
import json
from functools import lru_cache
import numpy as np


class SimulationCache:
    """
    Cache pour stocker les résultats des simulations
    
    Évite de recalculer pour les mêmes paramètres
    """
    
    def __init__(self, max_cache_size=100):
        """
        Initialiser le cache
        
        Args:
            max_cache_size: Nombre maximum d'entrées en cache
        """
        self.cache = {}
        self.max_size = max_cache_size
        self.hits = 0
        self.misses = 0
    
    @staticmethod
    def generate_key(lambda_param, mu_param, num_simulations):
        """
        Générer une clé unique pour une simulation
        
        Args:
            lambda_param: Paramètre lambda
            mu_param: Paramètre mu
            num_simulations: Nombre de simulations
            
        Returns:
            str: Clé de hash unique
        """
        params_str = f"{lambda_param}_{mu_param}_{num_simulations}"
        return hashlib.sha256(params_str.encode()).hexdigest()
    
    def get(self, lambda_param, mu_param, num_simulations):
        """Récupérer les résultats du cache si disponibles"""
        key = self.generate_key(lambda_param, mu_param, num_simulations)
        
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        
        self.misses += 1
        return None
    
    def set(self, lambda_param, mu_param, num_simulations, results):
        """Stocker les résultats en cache"""
        if len(self.cache) >= self.max_size:
            # Supprimer l'entrée la plus ancienne (FIFO)
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
        
        key = self.generate_key(lambda_param, mu_param, num_simulations)
        self.cache[key] = results
    
    def get_stats(self):
        """Obtenir les statistiques du cache"""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        
        return {
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'cached_entries': len(self.cache)
        }
    
    def clear(self):
        """Vider le cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0


class PerformanceMonitor:
    """
    Moniteur de performance pour les simulations
    
    Suit le temps d'exécution et les ressources utilisées
    """
    
    def __init__(self):
        """Initialiser le moniteur"""
        self.metrics = []
    
    def record(self, duration, num_simulations, lambda_param, mu_param):
        """
        Enregistrer une métrique de performance
        
        Args:
            duration: Temps d'exécution en secondes
            num_simulations: Nombre de simulations
            lambda_param: Paramètre lambda
            mu_param: Paramètre mu
        """
        sims_per_second = num_simulations / duration if duration > 0 else 0
        
        self.metrics.append({
            'duration': duration,
            'num_simulations': num_simulations,
            'lambda': lambda_param,
            'mu': mu_param,
            'sims_per_second': sims_per_second
        })
    
    def get_average_performance(self):
        """Obtenir la performance moyenne"""
        if not self.metrics:
            return None
        
        avg_duration = np.mean([m['duration'] for m in self.metrics])
        avg_sims_per_sec = np.mean([m['sims_per_second'] for m in self.metrics])
        
        return {
            'average_duration': avg_duration,
            'average_sims_per_second': avg_sims_per_sec,
            'total_runs': len(self.metrics)
        }
    
    def get_slowest_simulation(self):
        """Obtenir la simulation la plus lente"""
        if not self.metrics:
            return None
        return max(self.metrics, key=lambda x: x['duration'])
    
    def get_fastest_simulation(self):
        """Obtenir la simulation la plus rapide"""
        if not self.metrics:
            return None
        return min(self.metrics, key=lambda x: x['duration'])
    
    def clear(self):
        """Effacer les métriques"""
        self.metrics.clear()


# Instance globale du cache
simulation_cache = SimulationCache()

# Instance globale du moniteur de performance
performance_monitor = PerformanceMonitor()
