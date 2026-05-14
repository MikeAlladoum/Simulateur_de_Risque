#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de démarrage du serveur Flask
"""

import sys
import os

# Ajouter le dossier backend au path
sys.path.insert(0, os.path.dirname(__file__))

from app import app

if __name__ == '__main__':
    port = 5000
    debug = True
    
    print("=" * 60)
    print("🚀 SIMULATEUR DE RISQUES - BACKEND")
    print("=" * 60)
    print(f"📡 Serveur: http://localhost:{port}")
    print(f"🔧 Mode debug: {debug}")
    print(f"📚 API: http://localhost:{port}/api/info")
    print(f"💚 Health: http://localhost:{port}/api/health")
    print("=" * 60)
    print("\nAppuyer sur Ctrl+C pour arrêter\n")
    
    app.run(host='127.0.0.1', port=port, debug=debug)
