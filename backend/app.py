"""
Application Flask pour le simulateur de risques financiers
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from simulation import MonteCarlo
import traceback

app = Flask(__name__)
CORS(app)  # Active CORS pour les requêtes cross-origin


@app.route('/api/simulate', methods=['POST'])
def simulate():
    """
    Endpoint pour effectuer une simulation
    
    Données JSON attendues:
    {
        "lambda": float,  # Fréquence des sinistres
        "mu": float,      # Coût moyen
        "num_simulations": int
    }
    """
    try:
        data = request.json
        
        # Validation des données
        if not data:
            return jsonify({'error': 'Données manquantes'}), 400
        
        lambda_param = float(data.get('lambda', 1.0))
        mu_param = float(data.get('mu', 100.0))
        num_simulations = int(data.get('num_simulations', 10000))
        
        # Validation des paramètres
        if lambda_param <= 0 or mu_param <= 0 or num_simulations <= 0:
            return jsonify({'error': 'Les paramètres doivent être positifs'}), 400
        
        if num_simulations > 1000000:
            return jsonify({'error': 'Nombre de simulations trop élevé (max 1 000 000)'}), 400
        
        # Effectuer la simulation
        mc = MonteCarlo(lambda_param, mu_param, num_simulations)
        losses = mc.simulate()
        
        # Calculer les statistiques
        stats = mc.get_statistics()
        
        # Obtenir les données d'histogramme
        bin_centers, frequencies = mc.get_histogram_data(bins=50)
        
        # Calculer la probabilité de dépasser un seuil (exemple: moyenne * 2)
        threshold = stats['mean'] * 1.5
        prob_above = mc.get_probability_above_threshold(threshold)
        
        return jsonify({
            'success': True,
            'statistics': stats,
            'histogram': {
                'bins': bin_centers,
                'frequencies': frequencies
            },
            'threshold': threshold,
            'probability_above_threshold': prob_above,
            'parameters': {
                'lambda': lambda_param,
                'mu': mu_param,
                'num_simulations': num_simulations
            }
        }), 200
    
    except ValueError as ve:
        return jsonify({'error': f'Erreur de valeur: {str(ve)}'}), 400
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint de vérification de santé"""
    return jsonify({'status': 'OK', 'message': 'Serveur fonctionnel'}), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint non trouvé'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Erreur serveur interne'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
