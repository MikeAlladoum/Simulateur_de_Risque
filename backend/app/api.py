"""
API REST - Endpoints Flask

Routes pour les requêtes de simulation et gestion
"""
from flask import Blueprint, request, jsonify
import traceback
from .models import SimulationRequest, SimulationResult
from .simulation.monte_carlo import MonteCarlo
from .simulation.validators import validate_simulation_params
from .simulation.statistics import StatisticsCalculator
from .simulation.chart_generator import InteractiveChartGenerator
import config

# Blueprint API
api_bp = Blueprint('api', __name__)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Vérification de santé du serveur
    
    Returns:
        JSON: {status: 'OK', message: '...'}
    """
    return jsonify({
        'status': 'OK',
        'app': 'Simulateur de Risques Financiers',
        'version': config.VERSION
    }), 200


@api_bp.route('/simulate', methods=['POST'])
def simulate():
    """
    Endpoint principal de simulation Monte Carlo
    
    JSON Input:
    {
        "lambda": float,           # Fréquence des sinistres (Poisson)
        "mu": float,              # Coût moyen (Exponentielle)
        "num_simulations": int,   # Nombre de simulations
        "scenario_name": str      # (optionnel)
    }
    
    JSON Output:
    {
        "success": bool,
        "statistics": {...},
        "histogram": {...},
        "parameters": {...}
    }
    """
    try:
        # Récupérer les données JSON
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Données JSON manquantes'}), 400
        
        # Extraire les paramètres
        lambda_param = float(data.get('lambda', config.SIMULATION_DEFAULTS['lambda']))
        mu_param = float(data.get('mu', config.SIMULATION_DEFAULTS['mu']))
        num_simulations = int(data.get('num_simulations', config.SIMULATION_DEFAULTS['num_simulations']))
        scenario_name = data.get('scenario_name', 'Default')
        
        # Validation
        errors = validate_simulation_params(
            lambda_param,
            mu_param,
            num_simulations
        )
        
        if errors:
            return jsonify({
                'success': False,
                'errors': errors
            }), 400
        
        # Créer la requête
        sim_request = SimulationRequest(
            lambda_param=lambda_param,
            mu_param=mu_param,
            num_simulations=num_simulations,
            scenario_name=scenario_name
        )
        
        # Effectuer la simulation
        monte_carlo = MonteCarlo(
            lambda_param=sim_request.lambda_param,
            mu_param=sim_request.mu_param,
            num_simulations=sim_request.num_simulations
        )
        
        # Générer les résultats
        losses = monte_carlo.simulate()
        
        # Calculer les statistiques
        stats_calc = StatisticsCalculator(losses)
        stats = stats_calc.calculate_all()
        
        # Préparer les données d'histogramme
        histogram = monte_carlo.get_histogram_data(bins=50)
        
        # Générer le graphique interactif avec Plotly
        chart_generator = InteractiveChartGenerator()
        chart_html = chart_generator.generate_histogram(
            losses,
            stats.to_dict(),
            bins=50
        )
        
        # Créer la réponse
        result = SimulationResult(
            success=True,
            statistics=stats.to_dict(),
            histogram=histogram,
            chart_image=chart_html,  # HTML du graphique Plotly interactif
            parameters={
                'lambda': lambda_param,
                'mu': mu_param,
                'num_simulations': num_simulations,
                'scenario_name': scenario_name
            }
        )
        
        return jsonify(result.to_dict()), 200
    
    except ValueError as ve:
        return jsonify({
            'success': False,
            'error': f'Erreur de valeur: {str(ve)}'
        }), 400
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erreur serveur: {str(e)}'
        }), 500


@api_bp.route('/info', methods=['GET'])
def info():
    """
    Informations sur l'API
    
    Returns:
        JSON: Informations sur les endpoints disponibles
    """
    return jsonify({
        'app': 'Simulateur de Risques Financiers',
        'version': config.VERSION,
        'endpoints': {
            'GET /api/health': 'Vérification de santé',
            'POST /api/simulate': 'Effectuer une simulation',
            'GET /api/info': 'Informations sur l\'API'
        },
        'defaults': config.SIMULATION_DEFAULTS,
        'constraints': config.SIMULATION_CONSTRAINTS
    }), 200
