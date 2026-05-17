#!/usr/bin/env python3
"""
WSGI entry point for Railway deployment
"""

from app import app

if __name__ == '__main__':
    import os
    import logging
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    port = int(os.environ.get('PORT', 8000))
    logger.info(f"Starting server on port {port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
