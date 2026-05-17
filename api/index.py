"""
Serverless API Handler pour Vercel
Relaye les appels API vers le backend Flask
"""

import os
import json
import requests

# URL du backend Flask
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5000')

def handler(request):
    """
    Fonction handler Vercel pour rediriger les appels API
    """
    try:
        # Récupérer l'endpoint demandé
        path = request.path if hasattr(request, 'path') else request.url
        
        # Extraire l'endpoint
        if '/api/' in path:
            endpoint = path.split('/api/')[-1]
        else:
            endpoint = path.lstrip('/')
        
        # Construire l'URL du backend
        backend_url = f"{BACKEND_URL}/api/{endpoint}"
        
        # Ajouter les query parameters
        if hasattr(request, 'query_string') and request.query_string:
            backend_url += f"?{request.query_string.decode() if isinstance(request.query_string, bytes) else request.query_string}"
        
        # Préparer les headers
        headers = {}
        if hasattr(request, 'headers'):
            headers = dict(request.headers)
            headers.pop('Host', None)
            headers.pop('Connection', None)
        
        # Récupérer la méthode HTTP
        method = getattr(request, 'method', 'GET')
        
        # Récupérer le body
        body = None
        if hasattr(request, 'body'):
            body = request.body
        elif hasattr(request, 'get_json'):
            try:
                body = json.dumps(request.get_json())
            except:
                body = None
        
        # Faire l'appel au backend selon la méthode
        if method == 'GET':
            response = requests.get(backend_url, headers=headers, timeout=30)
        elif method == 'POST':
            content_type = headers.get('Content-Type', 'application/json')
            if body:
                if 'application/json' in content_type:
                    response = requests.post(backend_url, json=json.loads(body) if isinstance(body, str) else body, headers=headers, timeout=30)
                else:
                    response = requests.post(backend_url, data=body, headers=headers, timeout=30)
            else:
                response = requests.post(backend_url, headers=headers, timeout=30)
        elif method == 'PUT':
            if body:
                response = requests.put(backend_url, json=json.loads(body) if isinstance(body, str) else body, headers=headers, timeout=30)
            else:
                response = requests.put(backend_url, headers=headers, timeout=30)
        elif method == 'DELETE':
            response = requests.delete(backend_url, headers=headers, timeout=30)
        elif method == 'OPTIONS':
            return {
                'statusCode': 200,
                'body': '',
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization'
                }
            }
        else:
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method not allowed'}),
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
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
            'body': json.dumps({'error': 'Backend timeout', 'backend_url': BACKEND_URL}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }
    except requests.exceptions.ConnectionError as e:
        return {
            'statusCode': 503,
            'body': json.dumps({'error': 'Backend unavailable', 'message': str(e), 'backend_url': BACKEND_URL}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error', 'message': str(e)}),
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        }
