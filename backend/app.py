#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend API - Simulateur de Risques Financiers
API Flask pour les simulations Monte Carlo
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# ==================== ROUTES HEALTH ====================
@app.route('/api/health', methods=['GET'])
def health():
    """Vérification du statut du serveur"""
    return jsonify({
        'status': 'ok',
        'server': 'Simulateur de Risques API',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200

# ==================== ROUTES SIMULATION ====================
@app.route('/api/simulate', methods=['POST'])
def simulate():
    """Effectue une simulation Monte Carlo"""
    try:
        data = request.json
        num_simulations = int(data.get('num_simulations', 10000))
        
        # Validation
        if num_simulations <= 0:
            return jsonify({'error': 'Nombre de simulations invalide'}), 400
        
        if num_simulations > 100000:
            num_simulations = 100000
        
        # Vérifier le format des données
        sinistres = data.get('sinistres', {})
        
        if sinistres and isinstance(sinistres, dict):
            # Nouveau format avec sinistres multiples
            results = perform_monte_carlo_sinistres(sinistres, num_simulations)
        else:
            # Ancien format simple
            lambda_param = float(data.get('lambda', 5))
            mu = float(data.get('mu', 1000))
            distribution = data.get('distribution', 'normal')
            
            if lambda_param <= 0 or mu <= 0:
                return jsonify({'error': 'Paramètres invalides'}), 400
            
            results = perform_monte_carlo(lambda_param, mu, num_simulations, distribution)
        
        # Construire la réponse sans les données brutes de simulations
        response_data = {
            'success': True,
            'statistics': results.get('statistics', {}),
            'histogram': results.get('histogram', {}),
            'statistics_by_type': results.get('statistics_by_type', {}),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ROUTES INFO ====================
@app.route('/api/info', methods=['GET'])
def info():
    """Informations sur l'API"""
    return jsonify({
        'name': 'Simulateur de Risques Financiers',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'simulate': '/api/simulate',
            'info': '/api/info'
        }
    }), 200

# ==================== FONCTIONS UTILITAIRES ====================
def perform_monte_carlo_sinistres(sinistres_config, num_simulations):
    """
    Effectue une simulation Monte Carlo pour plusieurs sinistres (optimisée pour la RAM)
    
    Args:
        sinistres_config: Dict avec configuration des sinistres
        num_simulations: Nombre de simulations
    
    Returns:
        Dictionnaire avec résultats pour chaque sinistre
    """
    
    try:
        total_pertes = np.zeros(num_simulations)
        statistics_by_type = {}
        
        # Simuler pour chaque type de sinistre
        for sinistre_key, sinistre_config in sinistres_config.items():
            lambda_param = float(sinistre_config.get('lambda', 1))
            cout_moyen = float(sinistre_config.get('cout_moyen', 1000))
            nom_complet = sinistre_config.get('nom_complet', sinistre_key)
            
            # Générer le nombre de sinistres (distribution de Poisson)
            num_sinistres = np.random.poisson(lambda_param, num_simulations)
            
            # Générer les coûts directement sans boucle (vectorisé pour performance)
            pertes_sinistre = np.zeros(num_simulations)
            
            # Traiter par chunks pour économiser la RAM
            chunk_size = 1000
            for i in range(0, num_simulations, chunk_size):
                end_i = min(i + chunk_size, num_simulations)
                for j in range(i, end_i):
                    if num_sinistres[j] > 0:
                        couts_individuels = np.random.lognormal(
                            np.log(cout_moyen), 
                            0.5, 
                            num_sinistres[j]
                        )
                        pertes_sinistre[j] = np.sum(couts_individuels)
            
            # Ajouter aux pertes totales
            total_pertes += pertes_sinistre
            
            # Calculer les statistiques pour ce sinistre
            statistics_by_type[sinistre_key] = {
                'nom_complet': nom_complet,
                'lambda': lambda_param,
                'cout_moyen': cout_moyen,
                'moyenne': float(np.mean(pertes_sinistre)),
                'min': float(np.min(pertes_sinistre)),
                'max': float(np.max(pertes_sinistre)),
                'std': float(np.std(pertes_sinistre)),
                'median': float(np.median(pertes_sinistre)),
                'q25': float(np.percentile(pertes_sinistre, 25)),
                'q75': float(np.percentile(pertes_sinistre, 75)),
                'contribution_pct': 0.0  # Sera calculé après
            }
            
            # Libérer la mémoire
            del num_sinistres, pertes_sinistre
        
        # Calculer les contributions
        total_moyenne = np.mean(total_pertes)
        for sinistre_key in statistics_by_type:
            contribution = (statistics_by_type[sinistre_key]['moyenne'] / total_moyenne * 100) if total_moyenne > 0 else 0
            statistics_by_type[sinistre_key]['contribution_pct'] = float(contribution)
        
        # Statistiques globales
        results = {
            'statistics': {
                'mean': float(np.mean(total_pertes)),
                'std': float(np.std(total_pertes)),
                'min': float(np.min(total_pertes)),
                'max': float(np.max(total_pertes)),
                'median': float(np.median(total_pertes)),
                'q25': float(np.percentile(total_pertes, 25)),
                'q75': float(np.percentile(total_pertes, 75)),
                'var': float(np.percentile(total_pertes, 5)),  # VaR 95%
                'cvar': float(np.percentile(total_pertes, 1))   # CVaR 99%
            },
            'histogram': {
                'values': np.histogram(total_pertes, bins=40)[0].tolist(),
                'bins': np.histogram(total_pertes, bins=40)[1].tolist()
            },
            'statistics_by_type': statistics_by_type
        }
        
        # Libérer la mémoire des pertes totales
        del total_pertes
        
        return results
        
    except Exception as e:
        raise Exception(f"Erreur simulation sinistres: {str(e)}")

def perform_monte_carlo(lambda_param, mu, num_simulations, distribution='normal'):
    """
    Effectue une simulation Monte Carlo (optimisée RAM)
    
    Args:
        lambda_param: Paramètre lambda (fréquence)
        mu: Paramètre mu (moyenne)
        num_simulations: Nombre de simulations
        distribution: Type de distribution
    
    Returns:
        Dictionnaire avec résultats statistiques
    """
    
    try:
        # Générer les nombres aléatoires selon la distribution
        if distribution == 'normal':
            simulations = np.random.normal(mu, lambda_param, num_simulations)
        elif distribution == 'lognormal':
            simulations = np.random.lognormal(np.log(mu), lambda_param, num_simulations)
        elif distribution == 'uniform':
            simulations = np.random.uniform(mu - lambda_param, mu + lambda_param, num_simulations)
        else:
            simulations = np.random.normal(mu, lambda_param, num_simulations)
        
        # Calculs statistiques directement (sans stockage des simulations brutes)
        results = {
            'statistics': {
                'mean': float(np.mean(simulations)),
                'std': float(np.std(simulations)),
                'min': float(np.min(simulations)),
                'max': float(np.max(simulations)),
                'median': float(np.median(simulations)),
                'q25': float(np.percentile(simulations, 25)),
                'q75': float(np.percentile(simulations, 75)),
                'var': float(np.percentile(simulations, 5)),  # VaR 95%
                'cvar': float(np.percentile(simulations, 1))   # CVaR 99%
            },
            'histogram': {
                'values': np.histogram(simulations, bins=40)[0].tolist(),
                'bins': np.histogram(simulations, bins=40)[1].tolist()
            }
        }
        
        # Libérer la mémoire
        del simulations
        
        return results
        
    except Exception as e:
        raise Exception(f"Erreur simulation: {str(e)}")

# ==================== ROUTES AUTH (MOCK) ====================
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authentification utilisateur (mock)"""
    try:
        data = request.json
        username = data.get('username', '')
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Credentials required'}), 400
        
        # Mock authentication
        return jsonify({
            'success': True,
            'user': {
                'id': 1,
                'username': username,
                'email': f'{username}@example.com',
                'role': 'user'
            },
            'token': f'token_{username}_{datetime.now().timestamp()}'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Déconnexion utilisateur"""
    return jsonify({'success': True, 'message': 'Logged out'}), 200

# ==================== ROUTES PROFILES ====================
@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    """Récupère les profils utilisateur"""
    return jsonify({
        'profiles': [
            {'id': 1, 'name': 'Prudent', 'risk_level': 'low', 'lambda': 2, 'mu': 800},
            {'id': 2, 'name': 'Modéré', 'risk_level': 'medium', 'lambda': 5, 'mu': 1000},
            {'id': 3, 'name': 'Agressif', 'risk_level': 'high', 'lambda': 10, 'mu': 1500}
        ]
    }), 200

@app.route('/api/profiles', methods=['POST'])
def create_profile():
    """Crée un nouveau profil"""
    data = request.json
    return jsonify({
        'success': True,
        'profile': data,
        'id': 4
    }), 201

# ==================== ROUTES SINISTRES ====================
@app.route('/api/sinistres/default', methods=['GET'])
def get_default_sinistres():
    """Récupère les sinistres par défaut"""
    return jsonify({
        'success': True,
        'sinistres': {
            'consultation': {
                'lambda': 2.0,
                'cout_moyen': 5000,
                'nom_complet': 'Consultation médicale'
            },
            'hospitalisation': {
                'lambda': 0.3,
                'cout_moyen': 250000,
                'nom_complet': 'Hospitalisation'
            },
            'chirurgie': {
                'lambda': 0.1,
                'cout_moyen': 1000000,
                'nom_complet': 'Chirurgie'
            },
            'medicaments': {
                'lambda': 1.5,
                'cout_moyen': 30000,
                'nom_complet': 'Médicaments'
            }
        }
    }), 200

@app.route('/api/sinistres', methods=['GET'])
def get_sinistres():
    """Récupère les sinistres"""
    return jsonify({
        'sinistres': [
            {'id': 1, 'amount': 50000, 'date': '2024-01-15', 'category': 'Vol'},
            {'id': 2, 'amount': 75000, 'date': '2024-02-20', 'category': 'Dégât'},
            {'id': 3, 'amount': 120000, 'date': '2024-03-10', 'category': 'Responsabilité'}
        ]
    }), 200

@app.route('/api/sinistres', methods=['POST'])
def create_sinistre():
    """Crée un nouveau sinistre"""
    data = request.json
    return jsonify({
        'success': True,
        'sinistre': data,
        'id': 4
    }), 201

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

# ==================== MAIN ====================
if __name__ == '__main__':
    import sys
    
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    debug = '--debug' in sys.argv or '-d' in sys.argv
    
    print(f"🚀 Serveur démarrant sur http://localhost:{port}")
    print(f"Mode debug: {debug}")
    print(f"📚 Documentation API: http://localhost:{port}/api/info")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
