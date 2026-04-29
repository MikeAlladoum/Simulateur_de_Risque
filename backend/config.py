"""
Configuration du projet Simulateur de Risques Financiers

Gère les variables d'environnement et les paramètres de configuration
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Flask Configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = FLASK_ENV == 'development'
TESTING = os.getenv('TESTING', False)

# Server
HOST = os.getenv('HOST', '127.0.0.1')
PORT = int(os.getenv('PORT', 5000))
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# CORS
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:*,http://127.0.0.1:*').split(',')

# Simulation Parameters (defaults)
SIMULATION_DEFAULTS = {
    'lambda': 5.0,           # Fréquence des sinistres
    'mu': 1000.0,            # Coût moyen
    'num_simulations': 10000 # Nombre de simulations
}

# Simulation Constraints
SIMULATION_CONSTRAINTS = {
    'lambda': {'min': 0.01, 'max': 1000},
    'mu': {'min': 0.01, 'max': 1000000},
    'num_simulations': {'min': 100, 'max': 1000000}
}

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = BASE_DIR / 'logs' / 'app.log'

# Database (future)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/app.db')

# Version
VERSION = '0.1.0'
