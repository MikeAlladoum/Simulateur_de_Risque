#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Backend API - Simulateur de Risques Financiers
API Flask pour les simulations Monte Carlo
"""

import sys
import logging

# Configure logging FIRST
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    import numpy as np
    from datetime import datetime
    import json
    import os
    from models import db, User, Simulation, Profile
    
    logger.info("✅ All imports successful")
except Exception as e:
    logger.error(f"❌ Import failed: {str(e)}", exc_info=True)
    sys.exit(1)

app = Flask(__name__)

# Configuration SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///simulateur.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

logger.info(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

# Initialiser la base de données
db.init_app(app)

# Configuration CORS
CORS(app)

# ==================== INITIALISATION BASE DE DONNÉES ====================
try:
    with app.app_context():
        logger.info("Creating database tables...")
        db.create_all()
        logger.info("✅ Database tables created/verified")
        
        # Créer un utilisateur par défaut si la table est vide
        if User.query.first() is None:
            logger.info("Creating default user...")
            default_user = User(
                username='demo',
                email='demo@example.com',
                role='user'
            )
            db.session.add(default_user)
            db.session.commit()
            logger.info("✅ Default user created")
        else:
            logger.info("✅ Default user already exists")
except Exception as e:
    logger.error(f"❌ Database initialization failed: {str(e)}", exc_info=True)
    # Don't exit - Flask can still serve health checks

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

# ==================== ROUTES SIMULATIONS ====================
@app.route('/api/simulations/save', methods=['POST'])
def save_simulation():
    """Sauvegarder une simulation"""
    try:
        data = request.json
        user_id = data.get('user_id', 1)  # Default user
        
        simulation = Simulation(
            user_id=user_id,
            num_simulations=data.get('num_simulations'),
            sinistres_config=data.get('sinistres_config', {}),
            statistics=data.get('statistics', {}),
            statistics_by_type=data.get('statistics_by_type', {}),
            histogram=data.get('histogram', {}),
            name=data.get('name'),
            description=data.get('description')
        )
        
        db.session.add(simulation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'simulation_id': simulation.id,
            'message': 'Simulation sauvegardée'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/simulations/<int:sim_id>', methods=['GET'])
def get_simulation(sim_id):
    """Récupérer une simulation"""
    try:
        simulation = Simulation.query.get(sim_id)
        if not simulation:
            return jsonify({'error': 'Simulation non trouvée'}), 404
        
        return jsonify(simulation.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/simulations', methods=['GET'])
def list_simulations():
    """Lister les simulations d'un utilisateur"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        simulations = Simulation.query.filter_by(user_id=user_id).order_by(Simulation.created_at.desc()).all()
        
        return jsonify({
            'success': True,
            'count': len(simulations),
            'simulations': [sim.to_dict() for sim in simulations]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/simulations/<int:sim_id>', methods=['DELETE'])
def delete_simulation(sim_id):
    """Supprimer une simulation"""
    try:
        simulation = Simulation.query.get(sim_id)
        if not simulation:
            return jsonify({'error': 'Simulation non trouvée'}), 404
        
        db.session.delete(simulation)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Simulation supprimée'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== ROUTES PROFILES ====================
@app.route('/api/profiles', methods=['POST'])
def create_profile():
    """Créer un profil de simulation"""
    try:
        data = request.json
        user_id = data.get('user_id', 1)
        
        profile = Profile(
            user_id=user_id,
            name=data.get('name'),
            description=data.get('description'),
            domain=data.get('domain'),
            default_num_simulations=data.get('default_num_simulations', 10000),
            sinistres_config=data.get('sinistres_config', {}),
            is_default=data.get('is_default', False)
        )
        
        db.session.add(profile)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'profile_id': profile.id,
            'message': 'Profil créé'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/profiles/<int:profile_id>', methods=['GET'])
def get_profile(profile_id):
    """Récupérer un profil"""
    try:
        profile = Profile.query.get(profile_id)
        if not profile:
            return jsonify({'error': 'Profil non trouvé'}), 404
        
        return jsonify(profile.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/profiles', methods=['GET'])
def list_profiles():
    """Lister les profils d'un utilisateur"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        profiles = Profile.query.filter_by(user_id=user_id).all()
        
        return jsonify({
            'success': True,
            'count': len(profiles),
            'profiles': [p.to_dict() for p in profiles]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/profiles/<int:profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    """Supprimer un profil"""
    try:
        profile = Profile.query.get(profile_id)
        if not profile:
            return jsonify({'error': 'Profil non trouvé'}), 404
        
        db.session.delete(profile)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Profil supprimé'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

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
    
    # Récupérer le port depuis l'environnement (Railway/Render) ou l'argument CLI
    port = int(os.environ.get('PORT', sys.argv[1] if len(sys.argv) > 1 else 5000))
    debug = '--debug' in sys.argv or '-d' in sys.argv
    
    print(f"🚀 Serveur démarrant sur http://0.0.0.0:{port}")
    print(f"Mode debug: {debug}")
    print(f"📚 Documentation API: http://localhost:{port}/api/info")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
