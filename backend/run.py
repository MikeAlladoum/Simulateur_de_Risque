"""
Point d'entrée principal du backend

Démarre le serveur Flask
"""
import sys
from pathlib import Path

# Ajouter le répertoire backend au path Python
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app import create_app
import config

if __name__ == '__main__':
    app = create_app()
    
    print(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║   Simulateur de Risques Financiers - Backend         ║
    ║   Version {config.VERSION}                               
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    print(f"🚀 Démarrage du serveur...")
    print(f"📍 URL : http://{config.HOST}:{config.PORT}")
    print(f"🔧 Mode : {config.FLASK_ENV}")
    print(f"🐛 Debug : {config.DEBUG}")
    print(f"\n💡 API Documentation : http://{config.HOST}:{config.PORT}/docs (optionnel)")
    print(f"🏥 Health Check : http://{config.HOST}:{config.PORT}/api/health")
    print(f"\n⚠️  Appuyez sur CTRL+C pour arrêter le serveur\n")
    
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
