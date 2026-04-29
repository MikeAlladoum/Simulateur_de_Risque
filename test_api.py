#!/usr/bin/env python3
"""
Test l'API de simulation directement
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

try:
    # Tester health
    print("🔍 Test health...")
    resp = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"✅ Health: {resp.status_code}")
    print(json.dumps(resp.json(), indent=2))
    
    # Tester simulate
    print("\n🔍 Test simulate...")
    data = {
        "lambda": 5,
        "mu": 100,
        "num_simulations": 1000
    }
    resp = requests.post(f"{BASE_URL}/simulate", json=data, timeout=30)
    print(f"✅ Simulate: {resp.status_code}")
    result = resp.json()
    
    # Afficher la structure
    print("\n📊 Structure de la réponse:")
    print(f"Keys: {list(result.keys())}")
    
    if 'statistics' in result:
        print(f"Statistics keys: {list(result['statistics'].keys())}")
        print(f"  - mean: {result['statistics'].get('mean')}")
        print(f"  - median: {result['statistics'].get('median')}")
        print(f"  - min: {result['statistics'].get('min')}")
        print(f"  - max: {result['statistics'].get('max')}")
    
    if 'histogram' in result:
        print(f"Histogram: {len(result['histogram'].get('bins', []))} bins")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
