"""
Serverless API Handler pour Vercel
Relaye les appels API vers le backend Flask
"""

import os
import json
import requests
from http.server import BaseHTTPRequestHandler

# URL du backend Flask
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:5000')

class handler(BaseHTTPRequestHandler):
    """
    Handler Vercel pour rediriger les appels API
    """
    
    def do_GET(self):
        self._route_request('GET')
    
    def do_POST(self):
        self._route_request('POST')
    
    def do_PUT(self):
        self._route_request('PUT')
    
    def do_DELETE(self):
        self._route_request('DELETE')
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def _route_request(self, method):
        """
        Route la requête vers le backend Flask
        """
        try:
            # Récupérer l'endpoint
            path = self.path
            if '/api/' in path:
                endpoint = path.split('/api/')[-1]
            else:
                endpoint = path.lstrip('/')
            
            # Construire l'URL du backend
            backend_url = f"{BACKEND_URL}/api/{endpoint}"
            
            # Récupérer les headers
            headers = dict(self.headers)
            headers.pop('Host', None)
            
            # Récupérer le body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            # Faire l'appel au backend
            try:
                if method == 'GET':
                    response = requests.get(backend_url, headers=headers, timeout=30)
                elif method == 'POST':
                    response = requests.post(backend_url, data=body, headers=headers, timeout=30)
                elif method == 'PUT':
                    response = requests.put(backend_url, data=body, headers=headers, timeout=30)
                elif method == 'DELETE':
                    response = requests.delete(backend_url, headers=headers, timeout=30)
                else:
                    raise ValueError(f"Method not supported: {method}")
                
                # Envoyer la réponse du backend
                self.send_response(response.status_code)
                self.send_header('Content-Type', response.headers.get('Content-Type', 'application/json'))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                self.end_headers()
                self.wfile.write(response.content)
            
            except requests.exceptions.Timeout:
                self.send_response(504)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Backend timeout'}).encode())
            
            except requests.exceptions.ConnectionError as e:
                self.send_response(503)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Backend unavailable', 'message': str(e)}).encode())
        
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Internal server error', 'message': str(e)}).encode())
