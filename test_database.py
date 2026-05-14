#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test de la base de données SQLite
Démontre l'utilisation des endpoints de persistance
"""

import json
import requests
from datetime import datetime

# Configuration
BASE_URL = 'http://localhost:5000/api'
USER_ID = 1

def print_section(title):
    """Affiche une section"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health():
    """Tester la santé du serveur"""
    print_section("1. Vérifier l'état du serveur")
    response = requests.get(f'{BASE_URL}/health')
    print(f"✅ Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_save_profile():
    """Créer un profil"""
    print_section("2. Créer un profil de simulation")
    
    profile_data = {
        'user_id': USER_ID,
        'name': 'Profil Prudent',
        'description': 'Configuration pour stratégie prudente',
        'domain': 'Assurance Maladie',
        'default_num_simulations': 5000,
        'sinistres_config': {
            'consultation': {'lambda': 2.0, 'cout_moyen': 5000, 'nom_complet': 'Consultation médicale'},
            'hospitalisation': {'lambda': 0.3, 'cout_moyen': 250000, 'nom_complet': 'Hospitalisation'},
            'chirurgie': {'lambda': 0.1, 'cout_moyen': 1000000, 'nom_complet': 'Chirurgie'},
            'medicaments': {'lambda': 1.5, 'cout_moyen': 30000, 'nom_complet': 'Médicaments'}
        },
        'is_default': True
    }
    
    response = requests.post(f'{BASE_URL}/profiles', json=profile_data)
    print(f"✅ Status: {response.status_code}")
    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result.get('profile_id', 1) if response.status_code == 201 else None

def test_list_profiles():
    """Lister les profils"""
    print_section("3. Lister les profils d'un utilisateur")
    
    response = requests.get(f'{BASE_URL}/profiles', params={'user_id': USER_ID})
    print(f"✅ Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_get_profile(profile_id):
    """Récupérer un profil"""
    if not profile_id:
        print_section("4. Récupérer un profil (SKIP - pas de profil créé)")
        return
    
    print_section("4. Récupérer un profil")
    
    response = requests.get(f'{BASE_URL}/profiles/{profile_id}')
    print(f"✅ Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_simulate_and_save():
    """Simuler et sauvegarder"""
    print_section("5. Lancer une simulation et sauvegarder")
    
    # Lancer simulation
    simulate_data = {
        'num_simulations': 1000,
        'sinistres': {
            'consultation': {'lambda': 2.0, 'cout_moyen': 5000, 'nom_complet': 'Consultation médicale'},
            'hospitalisation': {'lambda': 0.3, 'cout_moyen': 250000, 'nom_complet': 'Hospitalisation'}
        }
    }
    
    print("📊 Lancement simulation (1000 runs)...")
    response = requests.post(f'{BASE_URL}/simulate', json=simulate_data)
    
    if response.status_code != 200:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text)
        return None
    
    sim_results = response.json()
    print(f"✅ Simulation complétée")
    print(f"   Perte Moyenne: {sim_results['statistics']['moyenne']:,.2f} FCFA")
    
    # Sauvegarder dans BD
    print("\n💾 Sauvegarde dans SQLite...")
    save_data = {
        'user_id': USER_ID,
        'num_simulations': simulate_data['num_simulations'],
        'sinistres_config': simulate_data['sinistres'],
        'statistics': sim_results['statistics'],
        'statistics_by_type': sim_results['statistics_by_type'],
        'histogram': sim_results['histogram'],
        'name': f'Simulation {datetime.now().strftime("%Y-%m-%d %H:%M")}',
        'description': 'Test automatisé de la BD'
    }
    
    response = requests.post(f'{BASE_URL}/simulations/save', json=save_data)
    print(f"✅ Status: {response.status_code}")
    result = response.json()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result.get('simulation_id') if response.status_code == 201 else None

def test_list_simulations():
    """Lister les simulations"""
    print_section("6. Lister les simulations d'un utilisateur")
    
    response = requests.get(f'{BASE_URL}/simulations', params={'user_id': USER_ID})
    print(f"✅ Status: {response.status_code}")
    result = response.json()
    print(f"Nombre de simulations: {result.get('count', 0)}")
    if result.get('simulations'):
        for sim in result['simulations']:
            print(f"\n  📌 ID {sim['id']}: {sim.get('name', 'N/A')}")
            print(f"     Pertes: {sim['statistics']['moyenne']:,.2f} FCFA")

def test_get_simulation(sim_id):
    """Récupérer une simulation"""
    if not sim_id:
        print_section("7. Récupérer une simulation (SKIP - pas de simulation créée)")
        return
    
    print_section("7. Récupérer une simulation détaillée")
    
    response = requests.get(f'{BASE_URL}/simulations/{sim_id}')
    print(f"✅ Status: {response.status_code}")
    sim = response.json()
    print(f"📊 Simulation ID {sim['id']}: {sim.get('name', 'N/A')}")
    print(f"   Nombre de runs: {sim['num_simulations']}")
    print(f"   Perte moyenne: {sim['statistics']['moyenne']:,.2f} FCFA")
    print(f"   Date: {sim['created_at']}")
    print(f"\n   Contribution par type:")
    for type_name, stats in sim['statistics_by_type'].items():
        print(f"   - {stats['nom_complet']}: {stats['contribution_pct']:.1f}%")

def test_delete_simulation(sim_id):
    """Supprimer une simulation"""
    if not sim_id:
        print_section("8. Supprimer une simulation (SKIP)")
        return
    
    print_section("8. Supprimer une simulation")
    
    response = requests.delete(f'{BASE_URL}/simulations/{sim_id}')
    print(f"✅ Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  TEST DE LA BASE DE DONNÉES SQLite")
    print("="*60)
    print("Pour que ce script fonctionne, assurez-vous que:")
    print("  1. Le backend Flask est démarré (python backend/app.py)")
    print("  2. L'URL du backend est correcte (BASE_URL)")
    print("\nInstaller les dépendances:")
    print("  pip install requests")
    
    try:
        # Test de connectivité
        test_health()
        
        # Tests CRUD
        profile_id = test_save_profile()
        test_list_profiles()
        test_get_profile(profile_id)
        
        sim_id = test_simulate_and_save()
        test_list_simulations()
        test_get_simulation(sim_id)
        
        # Ne pas supprimer pour conserver l'historique
        # test_delete_simulation(sim_id)
        
        print_section("✅ TESTS COMPLÉTÉS AVEC SUCCÈS")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERREUR: Impossible de se connecter au backend")
        print("   Assurez-vous que Flask est démarré: python backend/app.py")
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
