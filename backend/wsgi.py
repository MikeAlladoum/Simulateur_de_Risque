#!/usr/bin/env python3
"""
WSGI entry point for Railway deployment
Handles startup and error logging
"""

import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

try:
    logger.info("Starting application...")
    from app import app
    logger.info("✅ Application initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize application: {str(e)}", exc_info=True)
    sys.exit(1)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"🚀 Starting server on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
