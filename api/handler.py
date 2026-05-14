"""
Serverless API Handler pour Vercel
Relaye les appels API vers le backend Flask
"""

import os
import json
import requests
from urllib.parse import urlencode

# URL du backend Flask
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5000')

def handler(request):
    """
    Fonction handler Vercel pour rediriger les appels API
    """
    
    # Récupérer l'endpoint demandé
    path = request.path
    
    # Enlever le prefix /api
    if path.startswith('/api/'):
        endpoint = path[5:]  # Enlever '/api/'
    else:
        endpoint = path
    
    # Construire l'URL du backend
    backend_url = f"{BACKEND_URL}/api/{endpoint}"
    
    # Ajouter les query parameters
    if request.query_string:
        backend_url += f"?{request.query_string}"
    
    try:
        # Préparer les headers
        headers = dict(request.headers)
        headers.pop('Host', None)  # Enlever l'header Host
        
        # Faire l'appel au backend
        if request.method == 'GET':
            response = requests.get(backend_url, headers=headers, timeout=30)
        elif request.method == 'POST':
            response = requests.post(
                backend_url,
                json=request.json if request.is_json else None,
                data=request.data if not request.is_json else None,
                headers=headers,
                timeout=30
            )
        elif request.method == 'PUT':
            response = requests.put(
                backend_url,
                json=request.json if request.is_json else None,
                headers=headers,
                timeout=30
            )
        elif request.method == 'DELETE':
            response = requests.delete(backend_url, headers=headers, timeout=30)
        else:
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method not allowed'})
            }
        
        # Retourner la réponse du backend
        return {
            'statusCode': response.status_code,
            'body': response.text,
            'headers': {
                'Content-Type': response.headers.get('Content-Type', 'application/json'),
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            }
        }
    
    except requests.exceptions.Timeout:
        return {
            'statusCode': 504,
            'body': json.dumps({'error': 'Backend timeout'}),
            'headers': {'Content-Type': 'application/json'}
        }
    except requests.exceptions.ConnectionError:
        return {
            'statusCode': 503,
            'body': json.dumps({'error': 'Backend unavailable'}),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {'Content-Type': 'application/json'}
        }
