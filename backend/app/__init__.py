"""
Initialisation de l'application Flask

Crée et configure l'application
"""
from flask import Flask
from flask_cors import CORS
import config


def create_app():
    """
    Application Factory Pattern
    
    Crée et configure l'application Flask
    
    Returns:
        Flask: Application Flask configurée
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['DEBUG'] = config.DEBUG
    app.config['TESTING'] = config.TESTING
    app.config['SECRET_KEY'] = config.SECRET_KEY
    
    # CORS
    CORS(app, origins=config.CORS_ORIGINS)
    
    # Enregistrer les blueprints
    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Routes de base
    @app.route('/')
    def index():
        return {
            'app': 'Simulateur de Risques Financiers',
            'version': config.VERSION,
            'status': 'running'
        }, 200
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Endpoint non trouvé'}, 404
    
    @app.errorhandler(500)
    def server_error(error):
        return {'error': 'Erreur serveur interne'}, 500
    
    return app
