"""
Serverless API Handler pour Vercel
Relaye les appels API vers le backend Flask
"""

import os
import json
import requests
from typing import Callable

# URL du backend Flask
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5000')


def handler(request):
    """
    Fonction handler callable pour Vercel
    """
    try:
        # Récupérer la méthode HTTP
        method = request.method
        
        # Récupérer l'endpoint
        path = request.path
        if '/api/' in path:
            endpoint = path.split('/api/')[-1]
        else:
            endpoint = path.lstrip('/')
        
        # Construire l'URL du backend
        backend_url = f"{BACKEND_URL}/api/{endpoint}"
        
        # Préparer les headers
        headers = {}
        if hasattr(request, 'headers'):
            headers = dict(request.headers)
            headers.pop('Host', None)
            headers.pop('Content-Length', None)
        
        # Récupérer le body
        body = None
        if method in ['POST', 'PUT']:
            if hasattr(request, 'body'):
                body = request.body
            elif hasattr(request, 'data'):
                body = request.data
        
        # Faire l'appel au backend selon la méthode
        try:
            if method == 'GET':
                response = requests.get(backend_url, headers=headers, timeout=30)
            elif method == 'POST':
                response = requests.post(backend_url, data=body, headers=headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(backend_url, data=body, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(backend_url, headers=headers, timeout=30)
            elif method == 'OPTIONS':
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                        'Content-Type': 'text/plain'
                    }
                }
            else:
                return {
                    'statusCode': 405,
                    'body': json.dumps({'error': 'Method not allowed'}),
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    }
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
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        
        except requests.exceptions.ConnectionError as e:
            return {
                'statusCode': 503,
                'body': json.dumps({'error': 'Backend unavailable', 'details': str(e)}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error', 'details': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
